"""
Merge education indicators with IGN municipality dataset.

Creates one unique education record per IGN municipality.
"""

from pathlib import Path

import pandas as pd


EDUCATION_FILE = Path("data/raw/education/education.csv")

CROSSWALK_FILE = Path("data/external/municipality_crosswalk.csv")

OUTPUT = Path("data/processed/education_indicators.csv")


def main():

    print("Loading education dataset")

    education = pd.read_csv(EDUCATION_FILE, dtype={"municipality_ine_code": str})

    print("Loading municipality crosswalk")

    crosswalk = pd.read_csv(
        CROSSWALK_FILE, dtype={"municipality_code": str, "ine_code": str}
    )

    # Remove duplicated IGN-INE mappings
    crosswalk = crosswalk.drop_duplicates(subset=["municipality_code"], keep="first")

    print("Filtering total population")

    education = education[education["gender"] == "total"].copy()

    education = education[education["year"] == 2024].copy()

    print("Removing duplicate INE municipalities")

    education = education.drop_duplicates(
        subset=["municipality_ine_code"], keep="first"
    )

    print("Education municipalities:", education["municipality_ine_code"].nunique())

    print(
        "Education duplicates:", education["municipality_ine_code"].duplicated().sum()
    )

    print("Matching INE and IGN codes")

    merged = crosswalk.merge(
        education[
            [
                "municipality_ine_code",
                "population_15_plus",
                "higher_education",
                "higher_education_rate",
            ]
        ],
        left_on="ine_code",
        right_on="municipality_ine_code",
        how="left",
        indicator=True,
    )

    print("\nMatching results:")
    print(merged["_merge"].value_counts())

    merged["education_available"] = merged["population_15_plus"].notna().astype(int)

    output = merged[
        [
            "municipality_code",
            "population_15_plus",
            "higher_education",
            "higher_education_rate",
            "education_available",
        ]
    ]

    # Final safety check:
    # one row per municipality
    output = output.drop_duplicates(subset=["municipality_code"], keep="first")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    output.to_csv(OUTPUT, index=False, encoding="utf-8")

    print(f"\nSaved: {OUTPUT}")

    print(f"Rows: {len(output)}")

    print(output.head())


if __name__ == "__main__":
    main()
