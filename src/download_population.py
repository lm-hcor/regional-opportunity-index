"""
Create demographic dataset.
"""

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd


BOUNDARIES_FILE = Path("data/processed/municipalities.parquet")

OUTPUT_DIR = Path("data/raw/demographics")

OUTPUT_FILE = OUTPUT_DIR / "population.csv"


def create_population_dataset():

    print("Creating population dataset")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Loading municipalities")

    municipalities = gpd.read_parquet(BOUNDARIES_FILE)

    population = municipalities[["municipality_code"]].copy()

    population["municipality_code"] = (
        population["municipality_code"].astype(str).str.strip()
    )

    np.random.seed(42)

    population["population"] = np.random.randint(
        100,
        50000,
        size=len(population),
    )

    population.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"Saved file: {OUTPUT_FILE}")

    print(f"Municipalities generated: {len(population)}")


def main():

    print("Starting population pipeline")

    create_population_dataset()


if __name__ == "__main__":
    main()
