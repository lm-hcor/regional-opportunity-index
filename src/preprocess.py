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

    layers = gpd.list_layers(file_path)

    logger.info(
        "Available layers: %s",
        list(layers.name),
    )

    for layer in layers.name:

        sample = gpd.read_file(
            file_path,
            layer=layer,
            rows=1,
        )

        if sample.geometry.iloc[0].geom_type in (
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

    layer = find_municipal_layer(
        file_path,
    )

    gdf = gpd.read_file(
        file_path,
        layer=layer,
    )

    logger.info(
        "Municipalities loaded: %s",
        len(gdf),
    )

    return gdf


def clean_column_names(
    gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:

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

    return gdf.rename(
        columns=rename_map,
    )


def remove_invalid_records(
    gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:

    logger.info(
        "Cleaning municipality codes."
    )

    before = len(gdf)

    gdf = gdf[
        gdf["municipality_code"].notna()
    ]


    logger.info(
        "Removed invalid municipalities: %s",
        before - len(gdf),
    )

    return gdf


def remove_non_municipal_entities(
    gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:

    logger.info(
        "Removing non-municipal entities."
    )

    invalid_entities = [
        "COMUNIDAD DE BASCUÑANA Y VILORIA DE RIOJA",
        "LEDANÍA DE HACINAS, SALAS DE LOS INFANTES Y VILLANUEVA DE CARAZO",
        "VALLE DE LAS VENADAS",
        "COMUNIDAD DE TARDAJOS Y RABÉ DE LAS CALZADAS",
        "COMUNIDAD DE VILVIESTRE DEL PINAR Y PALACIOS DE LA SIERRA",
        "PEÑÓN DE ALHUCEMAS",
        "ISLA DEL PEREJIL",
        "PEÑÓN DE VÉLEZ DE LA GOMERA",
        "ISLAS CHAFARINAS",
        "ISLAS ALHUCEMAS",
        "PARZONERÍA GENERAL DE GUIPÚZCOA Y ÁLAVA",
        "NO PERTENECE",
    ]

    before = len(gdf)

    gdf = gdf[
        ~gdf["municipality_name"]
        .str.upper()
        .isin(invalid_entities)
    ]

    logger.info(
        "Removed non-municipal entities: %s",
        before - len(gdf),
    )

    return gdf


def remove_duplicate_municipalities(
    gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:

    """
    Remove duplicated IGN municipality codes.

    IGN may contain bilingual names for the same municipality.
    """

    logger.info(
        "Removing duplicate municipalities."
    )

    before = len(gdf)

    gdf = (
        gdf
        .drop_duplicates(
            subset=["municipality_code"],
            keep="first",
        )
    )


    logger.info(
        "Removed duplicate municipalities: %s",
        before - len(gdf),
    )

    return gdf


def validate_geometries(
    gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:

    invalid = (
        (~gdf.geometry.is_valid)
        .sum()
    )

    logger.info(
        "Invalid geometries: %s",
        invalid,
    )

    if invalid:

        gdf.geometry = (
            gdf.geometry
            .buffer(0)
        )

    return gdf


def add_spatial_features(
    gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:

    projected = gdf.to_crs(
        "EPSG:25830",
    )

    gdf["area_km2"] = (
        projected.geometry.area
        /
        1_000_000
    )

    centroids = (
        projected.geometry
        .centroid
        .to_crs("EPSG:4326")
    )

    gdf["longitude"] = centroids.x
    gdf["latitude"] = centroids.y

    return gdf


def save_dataset(
    gdf: gpd.GeoDataFrame,
) -> None:

    logger.info(
        "Saving processed municipalities."
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    gdf.to_parquet(
        OUTPUT_FILE,
    )


def main():

    logger.info(
        "Starting boundary preprocessing."
    )

    gdf = load_boundaries(
        BOUNDARIES_FILE,
    )

    gdf = clean_column_names(
        gdf,
    )

    gdf = remove_invalid_records(
        gdf,
    )

    gdf = remove_non_municipal_entities(
        gdf,
    )

    gdf = remove_duplicate_municipalities(
        gdf,
    )

    gdf = validate_geometries(
        gdf,
    )

    gdf = add_spatial_features(
        gdf,
    )


    logger.info(
        "Final municipalities: %s",
        len(gdf),
    )

    logger.info(
        "Unique municipality codes: %s",
        gdf["municipality_code"].nunique(),
    )


    save_dataset(
        gdf,
    )


    logger.info(
        "Preprocessing completed."
    )


if __name__ == "__main__":
    main()
