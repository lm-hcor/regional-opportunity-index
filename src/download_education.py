"""
Extract education indicators from INE municipal education dataset.
"""

from pathlib import Path
import re

import pandas as pd


INPUT_FILE = Path("data/external/education.xlsx")

OUTPUT_DIR = Path("data/raw/education")

OUTPUT_FILE = OUTPUT_DIR / "education.csv"


# 2024 columns
# Column 0 contains row labels
# Data starts at column 1

TOTAL_COL = 1
HIGHER_EDUCATION_COL = 17


def clean_number(value):

    if pd.isna(value):
        return 0

    if isinstance(value, str):
        value = value.replace(".", "").replace(",", ".").strip()

    try:
        return float(value)

    except ValueError:
        return 0


def extract_education():

    print("Loading education dataset")

    df = pd.read_excel(INPUT_FILE, header=None)

    records = []

    current_municipality = None
    current_gender = None

    for _, row in df.iterrows():
        first = str(row[0]).strip()

        # Detect municipality code
        match = re.match(r"^(\d{5})\s+", first)

        if match:
            current_municipality = match.group(1)
            current_gender = None

            continue

        # Detect gender blocks

        if first == "Total":
            current_gender = "total"

        elif first == "Hombres":
            current_gender = "men"

        elif first == "Mujeres":
            current_gender = "women"

        # Extract 15+ population

        if first == "15 y más años" and current_municipality and current_gender:
            population = clean_number(row[TOTAL_COL])

            higher = clean_number(row[HIGHER_EDUCATION_COL])

            rate = higher / population if population > 0 else 0

            records.append(
                {
                    "municipality_ine_code": current_municipality,
                    "year": 2024,
                    "gender": current_gender,
                    "population_15_plus": int(population),
                    "higher_education": int(higher),
                    "higher_education_rate": rate,
                }
            )

    education = pd.DataFrame(records)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    education.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"Saved: {OUTPUT_FILE}")

    print(f"Rows generated: {len(education)}")

    print(education.head(10))

    print("\nGender distribution:")

    print(education["gender"].value_counts())


def main():

    print("Starting education pipeline")

    extract_education()


if __name__ == "__main__":
    main()
