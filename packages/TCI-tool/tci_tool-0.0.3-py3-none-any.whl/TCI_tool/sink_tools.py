from tqdm.auto import tqdm
import geopandas as gpd
import pandas as pd
import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio.features import shapes, rasterize
from shapely.geometry import shape, box
from tqdm import tqdm
from rasterio.mask import geometry_mask
from scipy.ndimage import label
from definitions import FN
import logging


logger = logging.getLogger(__name__)

def create_sink_gdf(fp_diff, fp_area_of_interest, min_area=1000):
    """
    Create a GeoDataFrame of sink polygons from a difference raster.

    Steps:
    1. Identify connected depressions using scipy.ndimage.label on positive pixel values.
    2. Filter out depressions smaller than min_area.
    3. Polygonize the remaining depressions and return them as a GeoDataFrame.

    Args:
        fp_diff (str or pathlib.Path): File path to the difference raster.
        min_area (float, optional): Minimum area threshold for depressions, in map units².

    Returns:
        gpd.GeoDataFrame: GeoDataFrame of sink polygons with 'poly_idx' as an identifier.
    """
    # Load AOI polygon
    if fp_area_of_interest.suffix == ".parquet":
        aoi_gdf = gpd.read_parquet(fp_area_of_interest)
    else:
        aoi_gdf = gpd.read_file(fp_area_of_interest)

    if aoi_gdf.crs is None:
        raise ValueError("AOI polygon does not have a defined CRS.")

    with rasterio.open(fp_diff) as diff_raster:
        diff_data_full = diff_raster.read(1)
        transform = diff_raster.transform
        crs = diff_raster.crs
        pixel_area = abs(transform.a * transform.e)
        no_data = diff_raster.nodata
        width = diff_raster.width
        height = diff_raster.height

        # Ensure AOI is in the same CRS as the raster
        if aoi_gdf.crs != crs:
            aoi_gdf = aoi_gdf.to_crs(crs)

        # Rasterize the AOI polygon to create a mask
        aoi_mask = rasterize(
            [(geom, 1) for geom in aoi_gdf.geometry],
            out_shape=(height, width),
            transform=transform,
            fill=0,
            dtype='uint8'
        )

    # Identify depressions: positive values represent depressions
    depression_mask = (diff_data_full != 0) & (diff_data_full != no_data) & (aoi_mask == 1)

    # Label connected components (8-connectivity)
    structure = np.ones((3,3), dtype=bool)
    labeled_array, num_features = label(depression_mask, structure=structure)

    # Compute areas of each labeled region
    unique_labels, counts = np.unique(labeled_array, return_counts=True)
    label_areas = {lbl: cnt * pixel_area for lbl, cnt in zip(unique_labels, counts) if lbl != 0}

    # Keep only labels that meet the min_area
    valid_labels = {lbl for lbl, area in label_areas.items() if area >= min_area}
    final_mask = np.isin(labeled_array, list(valid_labels))

    # Polygonize only the valid depressions
    polygons_list = []
    for geom, val in tqdm(shapes(labeled_array, mask=final_mask, transform=transform, connectivity=8),
                          total=len(valid_labels), desc="Creating polygons"):
        polygons_list.append(shape(geom))

    # Create GeoDataFrame
    polygons = gpd.GeoDataFrame(geometry=polygons_list, crs=crs)
    polygons = polygons.reset_index(drop=True)
    polygons["poly_idx"] = range(len(polygons))
    print(f"Created {len(polygons)} sink polygons.")
    fp_out = fp_diff.parent / "sink_polygons.gpkg"
    polygons.to_file(fp_out, driver="GPKG")
    return polygons


def calculate_volume_by_tiles_no_overlap(fp_diff, polygons, n_rows=4, n_cols=4, water_level=0.3):
    """
    Calculate water volumes for sink polygons by partitioning the raster into a grid
    of non-overlapping tiles, but instead of using overlap or reading the entire tile's raster data,
    only read the raster subset defined by the polygons' bounding boxes.

    Once polygons are processed in a tile, they are removed from the set to avoid reprocessing.
    """

    # Build spatial index for polygons
    gdf_sinks = polygons.copy()
    sindex = polygons.sindex
    fp_out = fp_diff.parent / "sink_polygons.gpkg"

    with rasterio.open(fp_diff) as diff_raster:
        height, width = diff_raster.shape
        transform = diff_raster.transform
        pixel_area = abs(transform.a * transform.e)

    tile_height = height // n_rows
    tile_width = width // n_cols

    volume_results = []

    # Iterate over the tile grid (no overlap this time)
    for row_idx in range(n_rows):
        for col_idx in range(n_cols):
            # Define tile boundaries in pixel coordinates
            row_start = tile_height * row_idx
            row_end = tile_height * (row_idx + 1) if row_idx < n_rows - 1 else height
            col_start = tile_width * col_idx
            col_end = tile_width * (col_idx + 1) if col_idx < n_cols - 1 else width

            # Compute tile bounds in map coordinates
            x_min, y_min = transform * (col_start, row_start)
            x_max, y_max = transform * (col_end, row_end)
            tile_bounds = box(x_min, y_min, x_max, y_max)

            # Select polygons intersecting this tile
            candidate_idxs = list(sindex.intersection(tile_bounds.bounds))
            if not candidate_idxs:
                print(f"No polygons in tile [{row_idx}, {col_idx}]")
                continue

            tile_polygons = polygons.iloc[candidate_idxs]
            tile_polygons = tile_polygons[tile_polygons.intersects(tile_bounds)]

            if tile_polygons.empty:
                print(f"No polygons intersecting tile [{row_idx}, {col_idx}]")
                continue

            print(f"\nProcessing tile [{row_idx}, {col_idx}] with {len(tile_polygons)} polygons")

            # Compute combined bounding box of all selected polygons
            # This ensures we only read the necessary raster data
            combined_bounds = tile_polygons.total_bounds  # (minx, miny, maxx, maxy)
            minx, miny, maxx, maxy = combined_bounds
            extension = 100 * ((maxx-minx) * (maxy-miny) / ((x_max - x_min) * (y_max - y_min)) - 1)
            print(f"extended tile [{row_idx}, {col_idx}] by {extension:.2f} %")

            with rasterio.open(fp_diff) as diff_raster:
                # Convert map coordinates back to row/col window
                row_start_w, col_start_w = diff_raster.index(minx, maxy)  # Note maxy for row start
                row_end_w, col_end_w = diff_raster.index(maxx, miny)

                # Ensure indices are within raster bounds
                row_start_w = max(row_start_w, 0)
                col_start_w = max(col_start_w, 0)
                row_end_w = min(row_end_w, height - 1)
                col_end_w = min(col_end_w, width - 1)

                # Create window from slices
                window = Window.from_slices((row_start_w, row_end_w + 1), (col_start_w, col_end_w + 1))
                diff_data = diff_raster.read(1, window=window)
                sub_transform = diff_raster.window_transform(window)

            # Process polygons
            for _, poly in tqdm(tile_polygons.iterrows(), total=tile_polygons.shape[0]):
                geom = poly.geometry
                poly_idx = poly.poly_idx

                # Create mask for polygon in the windowed raster data
                mask = geometry_mask(
                    [geom],
                    transform=sub_transform,
                    invert=True,
                    out_shape=diff_data.shape
                )

                masked_diff = np.where(mask, diff_data, np.nan)

                # Compute max depth and threshold
                max_depth = np.nanmax(masked_diff)
                if np.isnan(max_depth) or max_depth <= 0:
                    # Polygon may not have positive values in this subset
                    continue

                threshold = max_depth - water_level
                clipped_raster = np.where(masked_diff >= threshold, masked_diff - threshold, 0)
                water_volume = np.nansum(clipped_raster) * geom.area

                if water_volume > 0:
                    volume_results.append({"poly_idx": poly_idx,
                                           "water_vol_m3": water_volume,
                                           "h_max": max_depth,
                                           "h_avg": water_volume / geom.area})

            # Remove processed polygons from the main dataframe to avoid reprocessing
            # In practice, you might want to mark them as processed instead,
            # but here we drop them.
            polygons = polygons.drop(tile_polygons.index)

            # Rebuild spatial index after removal if necessary (could be done less frequently)
            polygons = polygons.reset_index(drop=True)
            # polygons["poly_idx"] = range(len(polygons))
            sindex = polygons.sindex

    # Aggregate results by polygon
    # Note: We need to consider that poly_idx changed after dropping polygons.
    # To handle this properly, you can store a unique ID before dropping polygons.
    # For simplicity, assume poly_idx is stable or you have a unique ID column.
    if volume_results:
        print(f"Saving output to {fp_out}")
        df = pd.DataFrame(volume_results).set_index("poly_idx")
        gdf = gpd.GeoDataFrame(pd.concat([gdf_sinks.set_index("poly_idx"), df], axis=1), geometry="geometry")
        gdf["area"] = gdf.geometry.area
        gdf.to_file(fp_out, driver="GPKG")
        print("Done!")
    else:
        # No volumes found
        gdf = polygons.copy()
        print("No volumes found!")
        gdf["water_vol_m3"] = 0
    return gdf

def extract_sinks(fp_difference, fp_area_of_interest, min_area=500, min_level=0.1, n_rows=4, n_cols=4, water_level=0.3, fp_out=None):
    if fp_out is None:
        fp_out = fp_difference.parent / FN.SINK_POLYGONS

    gdf_sinks = create_sink_gdf(fp_difference, fp_area_of_interest, min_area=min_area)
    gdf_sinks = calculate_volume_by_tiles_no_overlap(fp_difference, gdf_sinks, n_rows, n_cols, water_level)
    gdf_sinks = gdf_sinks.loc[gdf_sinks["h_max"] >= min_level]
    gdf_sinks.to_file(fp_out, driver="GPKG")
    return fp_out
