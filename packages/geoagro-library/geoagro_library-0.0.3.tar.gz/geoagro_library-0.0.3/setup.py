#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GeoAgro – Manejo de series de tiempo NDVI/EVI a partir de imágenes satelitales.
Para instalar en modo editable:
    $ pip install -e .
Notas importantes (ver README):
1.  conda create -n geoagro python=3.11.11 && conda activate geoagro
2.  pip install -r requirements.txt        # instala dependencias “puros wheels”
3.  conda install -c conda-forge gdal      # GDAL binarios listos para tu sistema
"""
import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

# --------------------------------------------------------------------------- #
# METADATOS BÁSICOS
# --------------------------------------------------------------------------- #
PACKAGE_NAME   = "geoagro-library"                       # minúsculas + guion bajo
VERSION        = "0.0.3"                         # actualiza con cada release
AUTHOR         = "Team Agrosavia"
AUTHOR_EMAIL   = "crey@agrosavia.co"
URL            = "https://github.com/CristianR8/geoagro"
LICENSE        = "MIT"
DESCRIPTION    = (
    "Librería para el manejo de series de tiempo NDVI/EVI a partir de "
    "imágenes satelitales."
)
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding="utf-8")
LONG_DESC_TYPE   = "text/markdown"

# --------------------------------------------------------------------------- #
# DEPENDENCIAS
# --------------------------------------------------------------------------- #
INSTALL_REQUIRES = [
    "rasterio",
    "opencv-python",
    "ipympl",
    "tslearn",
    "scipy",
    "scikit-learn",
    "geopandas",
    # GDAL se instala aparte (ver nota en cabecera)
    "numpy>=2.1,<3.0",
    "matplotlib",
    "shapely",
    "fiona",
    "pyproj",
    "statsmodels",
    "tifffile",
    "Pillow",
    "scikit-image",
    "requests",
    "plotly",
    "futures; python_version<'3.10'",  # sólo para versiones antiguas
]

EXTRAS_REQUIRE = {
    "dev": [               # pip install geoagro[dev]
        "black",
        "pytest",
        "pre-commit",
        "build",
        "twine",
    ],
}

# --------------------------------------------------------------------------- #
# CONFIGURACIÓN DEL SETUP
# --------------------------------------------------------------------------- #
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    python_requires=">=3.9",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=find_packages(exclude=("tests", "docs")),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Bug Tracker": f"{URL}/issues",
        "Documentation": f"{URL}#readme",
    },
)
