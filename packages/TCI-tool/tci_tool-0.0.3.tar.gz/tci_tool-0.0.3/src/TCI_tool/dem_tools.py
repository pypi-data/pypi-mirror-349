import logging
from pathlib import Path
from raster_tools import create_mask_from_polygon_gdf, replace_values_with_mask
from definitions import FN
import geopandas as gpd
from whitebox import WhiteboxTools


logger = logging.getLogger(__name__)

def calc_filled_dem(fp_dem_original, fp_out=None):
    """
    Main function to process the DEM for depressions and depression values.

    Parameters:
        fp_dem_original (str): Path to the input DEM.

    Returns:
        None
    """
    fp_dem_original = Path(fp_dem_original)
    if not fp_dem_original.is_file():
        raise FileNotFoundError(f"DEM file not found at: {fp_dem_original}")

    if fp_out is None:
        fp_out = fp_dem_original.parent / (fp_dem_original.stem + FN.FILLED)

    # Step 2: Fill depressions using the Wang and Liu algorithm
    fill_depressions_wang_liu(input_raster=fp_dem_original, output_raster=fp_out)
    return fp_out


def fill_depressions_wang_liu(input_raster, output_raster):
    """
    Fills depressions in a DEM using the Wang and Liu algorithm with WhiteboxTools.

    Parameters:
        input_raster (str): Path to the input DEM.
        output_raster (str): Path to the output filled DEM.

    Returns:
        None
    """
    wbt = WhiteboxTools()
    wbt.set_working_dir(str(Path(input_raster).parent))
    wbt.fill_depressions_wang_and_liu(
        dem=str(input_raster),
        output=str(output_raster),
        fix_flats=True
    )
    print(f"Depressions filled. Output saved at: {output_raster}")
    return

def get_flowacc(input_raster, fp_out=None):
    if fp_out is None:
        fp_out = input_raster.parent/"flowacc.tif"
    wbt = WhiteboxTools()
    wbt.set_working_dir(str(Path(input_raster).parent))
    wbt.d8_flow_accumulation(str(input_raster), str(fp_out), "catchment area")
    print(f"Flow Accumulation calculated at: {fp_out}")
    return fp_out

def get_slope(input_raster, fp_out=None):
    if fp_out is None:
        fp_out = input_raster.parent/ FN.SLOPE
    wbt = WhiteboxTools()
    wbt.set_working_dir(str(Path(input_raster).parent))
    wbt.slope(str(input_raster), str(fp_out))
    print(f"Average Flowpath Slope calculated at: {fp_out}")
    return fp_out

def delineate_watersheds(fp_dem, fp_pourpoints, polygons=True):
    wbt = WhiteboxTools()
    wbt.set_working_dir(str(Path(fp_dem).parent))
    fp_d8pointer = fp_dem.parent / FN.D8POINTER
    wbt.d8_pointer(fp_dem, fp_d8pointer)

    if fp_pourpoints.suffix != ".shp":
        gpd.read_file(fp_pourpoints).to_file(fp_pourpoints.with_suffix('.shp'), driver='ESRI Shapefile')
        fp_pourpoints = fp_pourpoints.with_suffix('.shp')

    fp_watersheds_raster = fp_dem.parent / FN.WATERSHEDS_TIF
    wbt.watershed(str(fp_d8pointer), str(fp_pourpoints.with_suffix(".shp")), str(fp_watersheds_raster))
    if polygons:
        fp_watersheds_vector = fp_dem.parent / FN.WATERSHEDS_SHP
        wbt.raster_to_vector_polygons(str(fp_watersheds_raster), str(fp_watersheds_vector))
        return fp_watersheds_vector
    else:
        return fp_watersheds_raster

def partially_fill_dem(fp_dem_original, fp_dem_filled, fp_sinks_gdf, fp_out=None):
    print("creating mask from sinks")
    fp_mask = create_mask_from_polygon_gdf(fp_sinks_gdf, fp_dem_original)
    print("replacing masked sinks in filled dem")
    fp_dem_partial = replace_values_with_mask(fp_dem_original, fp_dem_filled, fp_mask, fp_out=fp_out)
    return fp_dem_partial
