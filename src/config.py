"""
Project configuration.

Defines project directories and external data sources.
"""

from pathlib import Path


# =============================================================================
# PROJECT ROOT
# =============================================================================

ROOT = Path(__file__).resolve().parents[1]


# =============================================================================
# DATA DIRECTORIES
# =============================================================================

DATA = ROOT / "data"

RAW = DATA / "raw"
PROCESSED = DATA / "processed"

BOUNDARIES = RAW / "boundaries"
DEMOGRAPHICS = RAW / "demographics"
HEALTH = RAW / "health"
TRANSPORT = RAW / "transport"
EDUCATION = RAW / "education"


# =============================================================================
# OUTPUT DIRECTORIES
# =============================================================================

ASSETS = ROOT / "assets"


# =============================================================================
# DATA SOURCES
# =============================================================================

BOUNDARIES_URL = (
    "https://centrodedescargas.cnig.es/"
    "CentroDescargas/documentos/atom/"
    "unidades-administrativas/"
    "unidades-administrativas.gpkg"
)


# =============================================================================
# CREATE DIRECTORIES
# =============================================================================

DIRECTORIES = (
    DATA,
    RAW,
    PROCESSED,
    BOUNDARIES,
    DEMOGRAPHICS,
    HEALTH,
    TRANSPORT,
    EDUCATION,
    ASSETS,
)


for directory in DIRECTORIES:
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )
