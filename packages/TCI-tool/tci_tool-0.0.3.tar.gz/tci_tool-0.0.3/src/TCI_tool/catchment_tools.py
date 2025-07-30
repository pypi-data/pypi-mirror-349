import os
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import rasterize
from rasterio.windows import Window
from shapely.geometry import box, Point
from pathlib import Path
from tqdm.auto import tqdm
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from whitebox import WhiteboxTools
from definitions import FN
import logging


logger = logging.getLogger(__name__)

def calculate_shortest_path_distances(mask, pour_point):
    """
    Calculates the shortest path distances from a pour point to all cells within a polygon mask.
    - mask: 2D NumPy array (binary mask), where 1 represents valid cells and 0 represents invalid cells.
    - pour_point: Tuple of (row, col) indicating the location of the pour point within the mask.
    Returns:
        A 2D NumPy array of distances, where distances are defined only for valid cells in the mask.
    """
    # Get rows and columns of valid cells in the mask
    rows, cols = np.where(mask == 1)
    valid_cells = list(zip(rows, cols))
    num_cells = len(valid_cells)

    # Create a mapping from 2D coordinates to 1D indices
    coord_to_index = {coord: i for i, coord in enumerate(valid_cells)}

    # Construct the adjacency matrix for valid cells
    adj_matrix = []
    adj_row = []
    adj_col = []
    for i, (row, col) in enumerate(valid_cells):
        # Check neighbors (8-connectivity)
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            neighbor = (row + dr, col + dc)
            if neighbor in coord_to_index:  # Neighbor must also be in the mask
                adj_row.append(i)
                adj_col.append(coord_to_index[neighbor])
                adj_matrix.append(1)  # Uniform edge weight for neighbors

    # Create a sparse adjacency matrix
    graph = csr_matrix((adj_matrix, (adj_row, adj_col)), shape=(num_cells, num_cells))

    # Find the 1D index of the pour point
    pour_point_index = coord_to_index[pour_point]

    # Compute shortest path distances using Dijkstra
    distances = dijkstra(csgraph=graph, directed=False, indices=pour_point_index)

    # Map distances back to a 2D array
    distance_matrix = np.full_like(mask, np.inf, dtype=float)
    for (row, col), dist in zip(valid_cells, distances):
        distance_matrix[row, col] = dist
    return distance_matrix


def modify_dem_for_pour_points_tiled(fp_dem, fp_polygons, depression_range, fp_dem_out=None, fp_pp_out=None, n_rows=4, n_cols=4):
    """
    Modifies the DEM tile-wise to create artificial pour points for each polygon.
    Writes the modified DEM to "dem_mod.tif" and pour points to "pour_points.gpkg".
    - fp_dem: File path to the input DEM (GeoTIFF).
    - fp_polygons: File path to the polygon GeoDataFrame (e.g., GeoPackage or Shapefile).
    - depression_range: User-defined range for scaling pour points.
    - output_dem: File path to write the modified DEM.
    - n_rows: Number of tiles in the vertical direction.
    - n_cols: Number of tiles in the horizontal direction.
    """
    window_list = []

    # Read the polygons
    gdf_polygons = gpd.read_file(fp_polygons)
    sindex = gdf_polygons.sindex

    if fp_dem_out is None:
        fp_dem_mod = fp_dem.parent / FN.DEM_MOD
    if fp_pp_out is None:
        fp_pp_out = fp_dem.parent / FN.POUR_POINTS

    # --- ganz oben: Kopie anlegen ---
    with rasterio.open(fp_dem) as src:
        profile = src.profile
        with rasterio.open(fp_dem_mod, 'w', **profile) as dst:
            dst.write(src.read(1), 1)  # komplette Kopie

    # Open the DEM
    with rasterio.open(fp_dem_mod, "r+") as dst:
        height, width = dst.height, dst.width
        transform = dst.transform
        crs = dst.crs

        # Initialize GeoDataFrame for pour points
        pour_points_list = []

        # Tile dimensions
        tile_height = height // n_rows
        tile_width = width // n_cols

        # Iterate over tiles
        for row_idx in range(n_rows):
            for col_idx in range(n_cols):
                # Define tile boundaries
                row_start = tile_height * row_idx
                row_end = tile_height * (row_idx + 1) if row_idx < n_rows - 1 else height
                col_start = tile_width * col_idx
                col_end = tile_width * (col_idx + 1) if col_idx < n_cols - 1 else width

                # Compute tile bounds in map coordinates
                x_min, y_min = transform * (col_start, row_start)
                x_max, y_max = transform * (col_end, row_end)
                tile_bounds = box(x_min, y_min, x_max, y_max)

                # Select polygons intersecting the tile
                candidate_idxs = list(sindex.intersection(tile_bounds.bounds))
                if not candidate_idxs:
                    print(f"No polygons in tile [{row_idx}, {col_idx}]")
                    continue

                tile_polygons = gdf_polygons.iloc[candidate_idxs]
                tile_polygons = tile_polygons[tile_polygons.intersects(tile_bounds)]

                if tile_polygons.empty:
                    print(f"No polygons intersecting tile [{row_idx}, {col_idx}]")
                    continue

                print(f"\nProcessing tile [{row_idx}, {col_idx}] with {len(tile_polygons)} polygons")

                # Compute combined bounding box of all selected polygons
                # This ensures we only read the necessary raster data
                combined_bounds = tile_polygons.total_bounds  # (minx, miny, maxx, maxy)
                minx, miny, maxx, maxy = combined_bounds
                extension = 100 * ((maxx-minx) * (maxy-miny) / ((x_max - x_min) * (y_max - y_min)))
                print(f"extended tile [{row_idx}, {col_idx}] by {extension:.2f} %")

                # Convert map coordinates back to row/col window
                row_start_w, col_start_w = dst.index(minx, maxy)  # Note maxy for row start
                row_end_w, col_end_w = dst.index(maxx, miny)

                # Ensure indices are within raster bounds
                row_start_w = max(row_start_w, 0)
                col_start_w = max(col_start_w, 0)
                row_end_w = min(row_end_w, height - 1)
                col_end_w = min(col_end_w, width - 1)

                # Create window from slices
                window = Window.from_slices((row_start_w, row_end_w + 1), (col_start_w, col_end_w + 1))
                dem_tile = dst.read(1, window=window)
                tile_bounds = box(minx, miny, maxx, maxy)
                window_list.append({
                    "row_idx": row_idx,
                    "col_idx": col_idx,
                    "geometry": tile_bounds
                })

                # Process each polygon in the tile
                for idx, polygon in tqdm(tile_polygons.iterrows(), total=tile_polygons.shape[0]):
                    # Rasterize the polygon to create a mask
                    polygon_mask = rasterize(
                        [(polygon.geometry, 1)],
                        out_shape=dem_tile.shape,
                        transform=rasterio.windows.transform(window, transform),
                        fill=0,
                        dtype="uint8",
                    )

                    # Get rows and columns of valid cells in the mask
                    rows, cols = np.where(polygon_mask == 1)
                    if len(rows) == 0 or len(cols) == 0:
                        continue

                    # Compute the center of the raster mask
                    center_row = int(rows.mean())
                    center_col = int(cols.mean())

                    # Ensure the chosen point is inside the polygon
                    if polygon_mask[center_row, center_col] != 1:
                        valid_coords = np.column_stack((rows, cols))
                        nearest_idx = np.argmin(np.linalg.norm(valid_coords - [center_row, center_col], axis=1))
                        center_row, center_col = valid_coords[nearest_idx]

                    # Global pour point coordinates
                    global_row = row_start_w + center_row
                    global_col = col_start_w + center_col
                    x, y = rasterio.transform.xy(transform, global_row, global_col)
                    pour_points_list.append({"poly_idx": polygon["poly_idx"],
                                             "geometry": Point(x, y),
                                             "water_vol_m3": polygon["water_vol_m3"],
                                             "h_avg": polygon["h_avg"],
                                             "h_max": polygon["h_max"],
                                             "area": polygon["area"]
                                             })

                    # Calculate shortest path distances
                    distances = calculate_shortest_path_distances(polygon_mask, (center_row, center_col))
                    # Exclude inf values when calculating max_distance
                    valid_distances = distances[polygon_mask == 1]
                    valid_distances = valid_distances[np.isfinite(valid_distances)]
                    min_elev = np.nanmin(dem_tile)

                    if valid_distances.size > 0:  # Ensure there are valid distances
                        max_distance = np.max(valid_distances)
                    else:
                        max_distance = 0  # Fallback if no valid distances are present

                    if max_distance > 0:
                        try:
                            dem_tile[polygon_mask == 1] = (
                                min_elev - depression_range * (1 - distances[polygon_mask == 1] / max_distance)
                            )
                        except:
                            print(f"RuntimeWarning encountered:")
                            print(f"Polygon index: {idx}")
                            print(f"Max distance: {max_distance}")
                            print(f"Distances: {distances[polygon_mask == 1]}")
                            # print(f"DEM tile: {dem_tile}")
                            raise  # Re-raise the exception after debugging if needed

                dst.write(dem_tile.astype("float64"), 1, window=window)
                gdf_polygons = gdf_polygons.drop(tile_polygons.index)
                gdf_polygons = gdf_polygons.reset_index(drop=True)
                sindex = gdf_polygons.sindex

    # Create a GeoDataFrame for pour points and save it
    gdf_pour_points = gpd.GeoDataFrame(pour_points_list, crs=crs).set_index("poly_idx")

    print(f"Modified DEM written to: {fp_dem_mod}")
    gdf_pour_points.to_file(fp_pp_out, driver="GPKG")
    print(f"Pourpoints written to: {fp_pp_out}")

    gdf_windows = gpd.GeoDataFrame(window_list, crs=crs)
    fp_windows = fp_dem_mod.parent / FN.TILE_WINDOWS
    gdf_windows.to_parquet(fp_windows)  # benötigt geopandas ≥ 0.12 und pyarrow

    print(f"Tile windows written to: {fp_windows}")
    return fp_dem_mod, fp_pp_out


def load_polygon_layer(polygon_layer):
    """
    Lädt den Polygon-Layer (GeoPackage, Shapefile oder GeoDataFrame).
    """
    if isinstance(polygon_layer, str) or isinstance(polygon_layer, Path):
        return gpd.read_file(polygon_layer)
    elif isinstance(polygon_layer, gpd.GeoDataFrame):
        return polygon_layer
    else:
        raise ValueError("Polygon-Layer muss ein Pfad zu einer Datei oder ein GeoDataFrame sein.")


def delineate_and_map_watersheds(fp_dem, fp_pourpoints, fp_out=None):
    """
    Delineates watersheds using a DEM and pour points, maps the pour points to watersheds,
    and saves the result as a GeoPackage.

    Parameters:
        fp_dem (Path): File path to the input DEM raster.
        fp_pourpoints (Path): File path to the pour points (must be a point shapefile).
        fp_out (Path): File path for the output GeoPackage (.gpkg).

    Returns:
        None
    """
    if fp_out is None:
        fp_out = fp_dem.parent / FN.WATERSHEDS_PARQUET

    # Initialize WhiteboxTools
    wbt = WhiteboxTools()
    temp_dir = fp_dem.parent / "temp_watersheds"
    os.makedirs(temp_dir, exist_ok=True)

    # Temporary file paths
    temp_d8_flow = temp_dir / "d8_flow.tif"
    temp_watersheds_raster = temp_dir / "watersheds.tif"
    temp_watersheds_vector = temp_dir / "watersheds.shp"

    try:
        # Create pour points shp-file copy
        if fp_pourpoints.suffix == "shp":
            fp_pourpoints_temp = fp_pourpoints
        else:
            fp_pourpoints_temp = temp_dir / "pourpoints.shp"
            gpd.read_file(fp_pourpoints).to_file(fp_pourpoints_temp)

        # Step 1: Generate D8 flow directions
        wbt.d8_pointer(dem=str(fp_dem), output=str(temp_d8_flow))

        # Step 2: Delineate watersheds
        wbt.watershed(d8_pntr=str(temp_d8_flow), pour_pts=str(fp_pourpoints_temp), output=str(temp_watersheds_raster))

        # Step 3: Convert raster to vector polygons
        wbt.raster_to_vector_polygons(i=temp_watersheds_raster, output=temp_watersheds_vector)

        # Step 3: Load the watershed polygons and pour points into GeoPandas
        watersheds_gdf = gpd.read_file(temp_watersheds_vector)
        # watersheds_gdf = gpd.GeoDataFrame(watersheds_gdf.make_valid())
        # watersheds_gdf = watersheds_gdf.set_geometry(0)

        pourpoints_gdf = gpd.read_file(fp_pourpoints)

        # Step 4: Spatial join to map pour points to watersheds
        pourpoints_gdf = pourpoints_gdf.to_crs(watersheds_gdf.crs)

        gdf_join = gpd.sjoin(watersheds_gdf, pourpoints_gdf, how="left", predicate="contains_properly")
        gdf_join = gdf_join.set_index("poly_idx")
        gdf_join = gdf_join[['geometry', 'index_right', 'water_vol_m3', 'h_avg', 'h_max', 'area']]

        # Step 5: Save the output as a GeoPackage
        gdf_join.to_parquet(fp_out)

        print(f"Output saved to {fp_out}")

    finally:
        print("Cleaning up temporary files")
        # Cleanup temporary files
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)

    return fp_out
