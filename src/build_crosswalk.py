"""
Build municipality crosswalk between IGN and INE codes.
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd


IGN_FILE = Path("data/raw/boundaries/municipalities.gpkg")

OUTPUT = Path("data/external/municipality_crosswalk.csv")

LAYER = "recintos_municipales_inspire_peninbal_etrs89"


def build_crosswalk():

    print("Loading IGN municipalities")

    gdf = gpd.read_file(IGN_FILE, layer=LAYER)

    crosswalk = gdf[["NATCODE", "NAMEUNIT", "CODNUT3"]].copy()

    crosswalk = crosswalk.rename(
        columns={
            "NATCODE": "municipality_code",
            "NAMEUNIT": "municipality_name",
            "CODNUT3": "nuts3_code",
        }
    )

    print("Creating INE codes")

    # IGN NATCODE structure:
    #
    # ES.IGN.BDDAE removed
    #
    # 34 01 04 001
    #
    # province = chars 2-4
    # municipality = last 3

    crosswalk["province_code"] = crosswalk["municipality_code"].str[2:4].str.zfill(2)

    crosswalk["municipality_number"] = (
        crosswalk["municipality_code"].str[-3:].str.zfill(3)
    )

    crosswalk["ine_code"] = (
        crosswalk["province_code"] + crosswalk["municipality_number"]
    )

    crosswalk = crosswalk[
        ["municipality_code", "ine_code", "municipality_name", "nuts3_code"]
    ]

    # eliminar registros especiales
    crosswalk = crosswalk[crosswalk["municipality_code"].notna()]

    crosswalk.to_csv(OUTPUT, index=False, encoding="utf-8")

    print(f"Saved: {OUTPUT}")
    print(f"Municipalities: {len(crosswalk)}")

    print(crosswalk.head())


if __name__ == "__main__":
    build_crosswalk()
