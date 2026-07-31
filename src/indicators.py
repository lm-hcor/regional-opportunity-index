"""
Create territorial indicators.

This module generates analytical variables
from municipal spatial datasets.
"""

import geopandas as gpd

from src.config import PROCESSED
from src.logger import get_logger


logger = get_logger(__name__)


INPUT_FILE = PROCESSED / "municipalities.parquet"


OUTPUT_FILE = PROCESSED / "municipal_indicators.parquet"


def load_municipalities() -> gpd.GeoDataFrame:
    """
    Load processed municipal dataset.
    """

    logger.info("Loading municipalities dataset.")

    gdf = gpd.read_parquet(
        INPUT_FILE,
    )

    logger.info(
        "Municipalities loaded: %s",
        len(gdf),
    )

    return gdf


def remove_duplicate_municipalities(
    gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """
    Clean municipality identifiers and remove invalid records.
    """

    logger.info("Cleaning municipality codes.")

    gdf["municipality_code"] = gdf["municipality_code"].astype("string").str.strip()

    before = len(gdf)

    # Remove non-municipality records
    gdf = gdf[gdf["municipality_code"].notna() & (gdf["municipality_code"] != "")]

    logger.info(
        "Removed invalid municipalities: %s",
        before - len(gdf),
    )

    before_duplicates = len(gdf)

    gdf = gdf.drop_duplicates(
        subset=["municipality_code"],
        keep="first",
    )

    logger.info(
        "Removed duplicate municipalities: %s",
        before_duplicates - len(gdf),
    )

    return gdf


def create_spatial_indicators(
    gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """
    Generate territorial indicators.
    """

    logger.info("Creating spatial indicators.")

    gdf["log_area_km2"] = gdf["area_km2"].apply(lambda x: 0 if x <= 0 else x)

    gdf["territorial_fragmentation"] = 1 / gdf["area_km2"]

    return gdf


def save_indicators(
    gdf: gpd.GeoDataFrame,
) -> None:
    """
    Save indicator dataset.
    """

    logger.info("Saving indicators dataset.")

    gdf.to_parquet(
        OUTPUT_FILE,
    )


def main() -> None:
    """
    Execute indicator pipeline.
    """

    gdf = load_municipalities()

    gdf = remove_duplicate_municipalities(
        gdf,
    )

    gdf = create_spatial_indicators(
        gdf,
    )

    save_indicators(
        gdf,
    )

    logger.info("Indicator generation completed.")


if __name__ == "__main__":
    main()
