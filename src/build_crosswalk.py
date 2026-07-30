"""
Build municipality crosswalk between IGN and INE codes.
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd


INPUT = Path("data/processed/municipalities.parquet")

OUTPUT = Path("data/external/municipality_crosswalk.csv")


def build_crosswalk():

    print("Loading municipalities")

    municipalities = gpd.read_parquet(INPUT)

    crosswalk = municipalities[
        [
            "municipality_code",
            "municipality_name",
            "nuts3_code",
        ]
    ].copy()

    print("Creating INE codes")

    # Ensure IGN code is string
    crosswalk["municipality_code"] = (
        crosswalk["municipality_code"].astype(str).str.strip()
    )

    # Extract province and municipality codes
    crosswalk["province_code"] = crosswalk["municipality_code"].str[2:4]

    crosswalk["municipality_local_code"] = crosswalk["municipality_code"].str[6:]

    # Build INE municipality code
    crosswalk["ine_code"] = (
        crosswalk["province_code"] + crosswalk["municipality_local_code"]
    )

    # Keep leading zeros
    crosswalk["ine_code"] = crosswalk["ine_code"].astype(str).str.zfill(7)

    # Remove auxiliary columns
    crosswalk = crosswalk[
        [
            "municipality_code",
            "ine_code",
            "municipality_name",
            "nuts3_code",
        ]
    ]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    crosswalk.to_csv(OUTPUT, index=False, encoding="utf-8")

    print(f"Saved: {OUTPUT}")

    print(f"Municipalities: {len(crosswalk)}")

    print(crosswalk.head())


def main():

    build_crosswalk()


if __name__ == "__main__":
    main()
