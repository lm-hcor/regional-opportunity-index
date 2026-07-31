"""
Merge territorial indicators with demographic and education data.
"""

from pathlib import Path

import pandas as pd
import numpy as np
import logging


# -------------------------
# Paths
# -------------------------

INDICATORS = Path("data/processed/municipal_indicators.parquet")

POPULATION = Path("data/raw/demographics/population.csv")

EDUCATION = Path("data/processed/education_indicators.csv")

OUTPUT = Path("data/processed/territorial_dataset.parquet")


# -------------------------
# Logging
# -------------------------

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)


# -------------------------
# Main pipeline
# -------------------------


def main():

    logging.info("Loading municipal indicators.")

    df = pd.read_parquet(INDICATORS)

    logging.info(f"Municipal indicators loaded: {len(df)}")

    # -------------------------
    # Population
    # -------------------------

    logging.info("Loading population data.")

    population = pd.read_csv(POPULATION, dtype={"municipality_code": str})

    population["municipality_code"] = population["municipality_code"].str.zfill(11)

    logging.info("Merging population.")

    df = df.merge(
        population[["municipality_code", "population"]],
        on="municipality_code",
        how="left",
    )

    # -------------------------
    # Education
    # -------------------------

    logging.info("Loading education indicators.")

    education = pd.read_csv(EDUCATION, dtype={"municipality_code": str})

    education["municipality_code"] = education["municipality_code"].str.zfill(11)

    logging.info("Merging education.")

    df = df.merge(education, on="municipality_code", how="left")

    # -------------------------
    # Derived indicators
    # -------------------------

    logging.info("Creating population density.")

    df["population_density"] = df["population"] / df["area_km2"]

    df["log_population"] = np.log1p(df["population"])

    # -------------------------
    # Save
    # -------------------------

    logging.info("Saving territorial dataset.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(OUTPUT, index=False)

    logging.info("Territorial dataset created successfully.")

    logging.info(f"Rows: {len(df)}")

    logging.info(f"Columns: {len(df.columns)}")


if __name__ == "__main__":
    main()
