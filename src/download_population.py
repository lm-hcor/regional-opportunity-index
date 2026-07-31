"""
Download and create real population dataset from INE.
"""

from pathlib import Path

import pandas as pd


INE_FILE = Path("data/external/pobmun25.xlsx")

CROSSWALK_FILE = Path(
    "data/external/municipality_crosswalk.csv"
)

OUTPUT_DIR = Path(
    "data/raw/demographics"
)

OUTPUT_FILE = OUTPUT_DIR / "population.csv"


def load_ine_population():

    print("Loading INE population data")

    df = pd.read_excel(
        INE_FILE,
        skiprows=1,
        dtype={
            "CPRO": str,
            "CMUN": str
        }
    )

    print(
        f"INE municipalities loaded: {len(df)}"
    )

    return df


def prepare_ine_codes(df):

    print("Creating INE municipality codes")

    df = df.copy()

    df["CPRO"] = (
        df["CPRO"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.zfill(2)
    )

    df["CMUN"] = (
        df["CMUN"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.zfill(3)
    )

    df["ine_code"] = (
        df["CPRO"]
        +
        df["CMUN"]
    )

    df = df[
        [
            "ine_code",
            "POB25"
        ]
    ]

    df = df.rename(
        columns={
            "POB25": "population"
        }
    )

    print(
        "INE duplicate codes:",
        df["ine_code"].duplicated().sum()
    )

    df = (
        df
        .drop_duplicates(
            subset=["ine_code"],
            keep="first"
        )
    )

    return df


def load_crosswalk():

    print("Loading municipality crosswalk")

    crosswalk = pd.read_csv(
        CROSSWALK_FILE,
        dtype={
            "municipality_code": str,
            "ine_code": str
        }
    )

    print(
        f"Crosswalk municipalities: {len(crosswalk)}"
    )

    print(
        "Crosswalk duplicate municipality codes:",
        crosswalk["municipality_code"].duplicated().sum()
    )

    crosswalk = (
        crosswalk
        .drop_duplicates(
            subset=["municipality_code"],
            keep="first"
        )
    )

    return crosswalk


def merge_population(crosswalk, population):

    print("Matching INE and IGN municipalities")

    df = crosswalk.merge(
        population,
        on="ine_code",
        how="left",
        indicator=True
    )

    print("\nMatching results:")
    print(
        df["_merge"].value_counts()
    )


    df = df[
        df["_merge"] == "both"
    ]


    df = df[
        [
            "municipality_code",
            "population"
        ]
    ]


    print(
        "Duplicate municipality codes after merge:",
        df["municipality_code"].duplicated().sum()
    )


    df = (
        df
        .drop_duplicates(
            subset=["municipality_code"],
            keep="first"
        )
    )


    return df


def save_population(df):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )


    print(
        f"\nSaved file: {OUTPUT_FILE}"
    )

    print(
        f"Rows generated: {len(df)}"
    )

    print(
        "\nMissing population values:"
    )

    print(
        df["population"].isna().sum()
    )

    print(
        "Unique municipalities:",
        df["municipality_code"].nunique()
    )


def main():

    print(
        "Starting population pipeline"
    )

    ine = load_ine_population()

    ine = prepare_ine_codes(
        ine
    )

    crosswalk = load_crosswalk()

    population = merge_population(
        crosswalk,
        ine
    )

    save_population(
        population
    )


if __name__ == "__main__":
    main()
