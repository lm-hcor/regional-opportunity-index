"""
Preprocess raw geographic datasets.

Transforms official municipal boundary data into a clean
spatial dataset for territorial analysis.
"""

from pathlib import Path

import geopandas as gpd

from src.config import PROCESSED, RAW
from src.logger import get_logger


logger = get_logger(__name__)


BOUNDARIES_FILE = (
    RAW
    / "boundaries"
    / "municipalities.gpkg"
)

OUTPUT_FILE = (
    PROCESSED
    / "municipalities.parquet"
)


def find_municipal_layer(
    file_path: Path,
) -> str:
    """
    Find the municipality polygon layer.

    Args:
        file_path:
            GeoPackage path.

    Returns:
        Layer name.
    """

    layers = gpd.list_layers(
        file_path,
    )

    logger.info(
        "Available layers: %s",
        list(layers.name),
    )

    for layer in layers.name:

        gdf = gpd.read_file(
            file_path,
            layer=layer,
            rows=1,
        )

        geometry_type = (
            gdf.geometry.iloc[0]
            .geom_type
        )

        if geometry_type in (
            "Polygon",
            "MultiPolygon",
        ):
            logger.info(
                "Selected polygon layer: %s",
                layer,
            )

            return layer

    raise ValueError(
        "No polygon municipality layer found."
    )


def load_boundaries(
    file_path: Path,
) -> gpd.GeoDataFrame:
    """
    Load municipality polygons.

    Args:
        file_path:
            GeoPackage path.

    Returns:
        Municipal polygons.
    """

    layer = find_municipal_layer(
        file_path,
    )

    gdf = gpd.read_file(
        file_path,
        layer=layer,
    )

    return gdf


def clean_column_names(
    gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """
    Standardize geographic variable names.

    Args:
        gdf:
            Input GeoDataFrame.

    Returns:
        Clean GeoDataFrame.
    """

    gdf.columns = (
        gdf.columns
        .str.lower()
        .str.strip()
    )

    rename_map = {
        "inspireid": "municipality_id",
        "nameunit": "municipality_name",
        "codnut1": "nuts1_code",
        "codnut2": "nuts2_code",
        "codnut3": "nuts3_code",
        "natcode": "municipality_code",
    }

    gdf = gdf.rename(
        columns=rename_map,
    )

    return gdf


def validate_geometries(
    gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """
    Validate geometries.
    """

    invalid = (
        (~gdf.geometry.is_valid)
        .sum()
    )

    logger.info(
        "Invalid geometries: %s",
        invalid,
    )

    if invalid > 0:
        gdf.geometry = (
            gdf.geometry
            .buffer(0)
        )

    return gdf

def add_spatial_features(
    gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """
    Add spatial analytical features.

    Args:
        gdf:
            Municipal polygons.

    Returns:
        Enhanced GeoDataFrame.
    """

    projected = gdf.to_crs(
        "EPSG:25830",
    )

    gdf["area_km2"] = (
        projected
        .geometry
        .area
        / 1_000_000
    )

    centroids = (
        projected
        .geometry
        .centroid
        .to_crs("EPSG:4326")
    )

    gdf["longitude"] = (
        centroids.x
    )

    gdf["latitude"] = (
        centroids.y
    )

    return gdf

def save_dataset(
    gdf: gpd.GeoDataFrame,
) -> None:
    """
    Save processed dataset.
    """

    logger.info(
        "Saving processed municipalities."
    )

    gdf.to_parquet(
        OUTPUT_FILE,
    )


def main() -> None:
    """
    Execute preprocessing pipeline.
    """

    logger.info(
        "Starting boundary preprocessing."
    )

    gdf = load_boundaries(
        BOUNDARIES_FILE,
    )

    gdf = clean_column_names(
        gdf,
    )

    gdf = validate_geometries(
        gdf,
    )

    gdf = add_spatial_features(
    gdf,
    )

    save_dataset(
        gdf,
    )

    logger.info(
        "Preprocessing completed."
    )


if __name__ == "__main__":
    main()