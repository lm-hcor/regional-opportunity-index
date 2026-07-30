"""
Merge spatial and demographic datasets.
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd

from src.logger import get_logger


logger = get_logger(__name__)


MUNICIPAL_FILE = Path(
    "data/processed/municipal_indicators.parquet"
)

POPULATION_FILE = Path(
    "data/raw/demographics/population.csv"
)

OUTPUT_FILE = Path(
    "data/processed/territorial_dataset.parquet"
)


def load_data():

    logger.info("Loading municipal indicators.")

    municipalities = gpd.read_parquet(
        MUNICIPAL_FILE
    )

    logger.info("Loading population data.")

    population = pd.read_csv(
        POPULATION_FILE,
        dtype={
            "municipality_code": str
        }
    )

    return municipalities, population


def merge_population(
    municipalities,
    population
):

    logger.info("Merging population.")

    gdf = municipalities.merge(
        population,
        on="municipality_code",
        how="left"
    )

    return gdf


def create_density(gdf):

    logger.info("Creating population density.")

    gdf["population_density"] = (
        gdf["population"]
        /
        gdf["area_km2"]
    )

    return gdf


def save_dataset(gdf):

    logger.info("Saving territorial dataset.")

    gdf.to_parquet(
        OUTPUT_FILE,
        engine="pyarrow",
        compression="snappy"
    )


def main():

    municipalities, population = load_data()

    gdf = merge_population(
        municipalities,
        population
    )

    gdf = create_density(
        gdf
    )

    save_dataset(
        gdf
    )

    logger.info(
        "Territorial dataset created successfully."
    )


if __name__ == "__main__":
    main()