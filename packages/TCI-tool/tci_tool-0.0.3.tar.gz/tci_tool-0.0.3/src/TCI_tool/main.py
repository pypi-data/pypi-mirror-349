from pathlib import Path
import numpy as np
import logging
import geopandas as gpd
from rasterstats import zonal_stats
from raster_tools import calculate_raster_difference
from dem_tools import get_slope, calc_filled_dem, partially_fill_dem
from sink_tools import extract_sinks
from definitions import FN
from catchment_tools import modify_dem_for_pour_points_tiled, delineate_and_map_watersheds
import logging_config


logger = logging.getLogger(__name__)

def full_workflow(fp_dem_original, fp_area_of_interest):
    logging_config.configure_logging()

    work_dir = fp_dem_original.parent

    logger.info(f"01/10 CALCULATING FILLED DEM")
    fp_dem_filled = work_dir / (fp_dem_original.stem + FN.FILLED)
    fp_dem_filled = calc_filled_dem(fp_dem_original, fp_out=fp_dem_filled)

    logger.info(f"02/10 CALCULATING DIFFERENCE RASTER")
    fp_difference = work_dir / "difference.tif"
    fp_difference = calculate_raster_difference(fp_dem_filled, fp_dem_original, fp_out=fp_difference)

    logger.info(f"03/10 EXTRACT AND FILTER SINKS FROM DIFFERENCE RASTER")
    fp_sinks = work_dir / FN.SINK_POLYGONS
    fp_sinks = extract_sinks(fp_difference, fp_area_of_interest, min_area=500, min_level=0.1, fp_out=fp_sinks)

    logger.info(f"04/10 PARTIALLY FILL DEM")
    fp_dem_partial = work_dir / FN.DEM_PARTIAL
    fp_dem_partial = partially_fill_dem(fp_dem_original, fp_dem_filled, fp_sinks, fp_out=fp_dem_partial)

    logger.info("05/10 CALCULATE SLOPE")
    fp_slope = work_dir / FN.SLOPE
    fp_slope = get_slope(fp_dem_filled, fp_out=fp_slope)

    logger.info("06/10 DELINEATE CATCHMENT AREAS")

    logger.info("07/10 MODIFY DEM FOR ARTIFICAL POUR POINTS")
    fp_pourpoints = work_dir / FN.POUR_POINTS
    fp_dem_mod = work_dir / FN.DEM_MOD
    fp_dem_mod, fp_pourpoints = modify_dem_for_pour_points_tiled(fp_dem_partial, fp_sinks, depression_range=10,
                                                                 fp_dem_out=fp_dem_mod, fp_pp_out=fp_pourpoints)

    logger.info("08/10 CALCULATE WATERSHEDS FROM POUR POINTS")
    fp_watersheds = work_dir / FN.WATERSHEDS_GPKG
    fp_watersheds = delineate_and_map_watersheds(fp_dem_mod, fp_pourpoints, fp_out=fp_watersheds)
    gdf_watersheds = gpd.read_parquet(fp_watersheds)

    logger.info("09/10 CALCULATING AVERAGE SLOPE IN CATCHMENTS")
    stats = zonal_stats(gdf_watersheds, fp_slope, stats=['mean'])
    # Add the means back to your GeoDataFrame
    gdf_watersheds['slope'] = [item['mean'] for item in stats]

    # geometry.area instead of facc, as facc would only be max of facc values within cathcment which would be area of catchment
    logger.info("10/10 CALCULATE TCI")
    gdf_watersheds["tci"] = np.log(gdf_watersheds.geometry.area * gdf_watersheds["slope"]**0.5 /  gdf_watersheds["water_vol_m3"])

    gdf_watersheds.to_file(fp_watersheds.parent / "tci.gpkg", driver="GPKG")
    logger.info(f"PROCESS FINISHED. FILE WRITTEN TO {fp_watersheds}")
    # gdf_watersheds.to_file(fp_watersheds.with_suffix(".gpkg"), driver="GPKG")
    return


def main():
    pass


if __name__ == "__main__":
    dem_feldkirch = Path(r"C:\Users\albert\Documents\Perisponge\Feldkirch\tci_automated\DGM_watershed_EPSG32155.tif")
    aoi_feldkirch = Path(r"C:\Users\albert\Documents\Perisponge\Feldkirch\tci_automated\aoi_feldkirch.gpkg")
    dem_wels = Path(r"C:\Users\albert\Documents\Perisponge\Wels\tci_automated\dgm_empty.tif")
    aoi_wels = Path(r"C:\Users\albert\Documents\Perisponge\Wels\tci_automated\wels_aoi.gpkg")
    dem_feldbach = Path(r"W:\Fließweganalyse\Erweitertes_Einzugsgebiet\Feldbach\DGM_WATERSHED\DGM_Watershed_EPSG_32633_1x1m.tif")
    aoi_feldbach = Path(r"C:\Users\albert\Documents\Perisponge\Feldbach\admin_feldbach.parquet")
    fp_dem_original = dem_feldbach#dem_wels#dem_feldkirch
    fp_area_of_interest = aoi_feldbach#aoi_wels#aoi_feldkirch
    full_workflow(fp_dem_original, fp_area_of_interest)
    pass
