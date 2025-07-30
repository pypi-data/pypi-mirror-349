import numpy as np
import rasterio
import geopandas as gpd
from rasterio.features import rasterize
import logging
from definitions import FN


logger = logging.getLogger(__name__)

def calculate_raster_difference(fp_raster1, fp_raster2, fp_out):
    """Calculate the difference between two single-band raster files.

    This function reads two raster files, computes the pixel-wise difference
    (fp_raster1 - fp_raster2), and writes the resulting difference raster to
    a new file named "difference.tif" in the same directory as fp_raster1.

    Args:
        fp_raster1 (pathlib.Path): Path to the first raster file.
        fp_raster2 (pathlib.Path): Path to the second raster file.

    Returns:
        pathlib.Path: The file path to the newly created difference raster.
    """
    # Output raster path
    fp_raster_out = fp_out

    # Open the first raster
    with rasterio.open(fp_raster1) as src1:
        # Read the first raster band into a NumPy array
        band1 = src1.read(1)  # Adjust if you have multiple bands and need a specific one
        profile = src1.profile  # Store the profile for later use

    # Open the second raster
    with rasterio.open(fp_raster2) as src2:
        # Read the second raster band
        band2 = src2.read(1)

    # Compute the difference
    difference_array = band1 - band2

    # Update the profile if necessary (e.g., data type if values are different)
    # Here we assume the difference can fit into the same data type.
    # If not, you might do: profile.update(dtype='float32') or suitable dtype
    profile.update(dtype=difference_array.dtype)

    # Write the difference array to a new raster file
    with rasterio.open(fp_raster_out, 'w', **profile) as dst:
        dst.write(difference_array, 1)
    return fp_raster_out

def create_mask_from_polygon_gdf(fp_features, fp_dem, fp_out=None):
    """
    Create a raster mask from polygons, aligned to a given DEM.

    Pixels where polygons are present will be set to 1,
    and pixels without polygons will be set to 0.

    Args:
        fp_features (str or pathlib.Path): Path to the GeoPackage or Shapefile with polygons.
        fp_dem (str or pathlib.Path): Path to the DEM raster to match spatial extent and resolution.
        fp_out: output raster filename.
    """
    if fp_out is None:
        fp_out_mask = fp_features.parent / FN.SINK_MASK
    else:
        fp_out_mask = fp_out

    # Read the sink polygons
    sinks_gdf = gpd.read_file(fp_features)

    with rasterio.open(fp_dem) as dem_src:
        # Copy the DEM's profile for spatial reference
        out_profile = dem_src.profile.copy()
        # We only need a single band mask
        out_profile.update(count=1, dtype='uint8', nodata=0)

        # Prepare shapes (polygons) with their associated values
        # Each sink polygon will be assigned the value 1
        shapes = ((geom, 1) for geom in sinks_gdf.geometry)

        # Rasterize polygons onto an array matching DEM dimensions
        mask_data = rasterize(
            shapes=shapes,
            out_shape=(dem_src.height, dem_src.width),
            transform=dem_src.transform,
            fill=0,  # Value for pixels not covered by any polygon
            dtype='uint8'  # 8-bit unsigned integer
        )

    # Write the mask to disk
    with rasterio.open(fp_out_mask, 'w', **out_profile) as mask_dst:
        mask_dst.write(mask_data, 1)

    return fp_out_mask

def replace_values_with_mask(fp_dem_og, fp_dem_filled, fp_mask, fp_out=None):
    if fp_out is None:
        output_path = fp_dem_og.parent / FN.DEM_PARTIAL
    else:
        output_path = fp_out

    # Open DEM1, DEM2, and mask raster files
    with rasterio.open(fp_dem_og) as dem1_src, rasterio.open(fp_dem_filled) as dem2_src, rasterio.open(fp_mask) as mask_src:
        dem1 = dem1_src.read(1).astype(np.float64)  # Read DEM1
        dem2 = dem2_src.read(1).astype(np.float64)  # Read DEM2
        mask = mask_src.read(1)  # Read mask

        # Ensure the rasters align in dimensions
        if not (dem1.shape == dem2.shape == mask.shape):
            raise ValueError("DEM1, DEM2, and mask must have the same dimensions.")

        # Handle NoData values
        dem1_nodata = dem1_src.nodata
        dem2_nodata = dem2_src.nodata
        mask_nodata = mask_src.nodata

        # Initialize the output array with DEM1 values
        result = np.copy(dem2)

        # Replace values in DEM1 with those from DEM2 where mask == 1
        replacement_condition = (mask == 1)
        result[replacement_condition] = dem1[replacement_condition]

        # Propagate NoData values where applicable
        if dem1_nodata is not None:
            result[dem1 == dem1_nodata] = dem1_nodata
        if dem2_nodata is not None:
            result[dem2 == dem2_nodata] = dem2_nodata

        # Update metadata for the output raster
        output_meta = dem1_src.meta
        output_meta.update(dtype=rasterio.float64, nodata=dem1_nodata)

        # Write the result to the output raster
        with rasterio.open(output_path, 'w', **output_meta) as output_src:
            output_src.write(result, 1)
        return output_path