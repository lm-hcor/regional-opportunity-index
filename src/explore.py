"""
Dataset exploration utility.

Displays basic information about processed datasets.
"""

from pathlib import Path

import pandas as pd

from src.logger import get_logger


logger = get_logger(__name__)


DATASET = (
    Path("data/processed")
    / "territorial_dataset.parquet"
)


def explore_dataset():

    logger.info(
        "Loading dataset: %s",
        DATASET,
    )

    df = pd.read_parquet(
        DATASET,
    )

    logger.info(
        "Number of rows: %s",
        len(df),
    )

    logger.info(
        "Columns available: %s",
        list(df.columns),
    )

    print("\nColumn types:")
    print(
        df.dtypes,
    )

    print(
    df["municipality_code"].head(20)
    )

    df["code_length"] = df["municipality_code"].str.len()
    
    print(
    df["code_length"].value_counts()
    )

    print("\nFirst rows:")
    print(
        df.head(),
    )

    print("\nMissing values:")
    print(
        df.isna()
        .sum()
        .sort_values(
            ascending=False,
        ),
    )


def main():

    explore_dataset()


if __name__ == "__main__":
    main()