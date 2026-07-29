# Regional Opportunity Index (ROI)

## Overview

**Regional Opportunity Index (ROI)** is an open-source geospatial analytics project that measures territorial opportunities across Spanish municipalities using publicly available data and Python.

The project integrates demographic, accessibility and socioeconomic indicators into a multidimensional index designed to support evidence-based public policy analysis.

Rather than focusing on a single dimension of inequality, the framework provides a holistic perspective on territorial disparities by combining spatial accessibility, demographic structure and regional characteristics.

---

## Objectives

* Develop a multidimensional territorial opportunity index.
* Explore regional inequalities using open geospatial data.
* Build an interactive dashboard for policy analysis.
* Demonstrate a reproducible GIS workflow in Python.
* Showcase how spatial analytics can support public decision-making.

---

## Key Features

* Geospatial data processing with **GeoPandas**
* Interactive choropleth maps
* Municipal-level territorial indicators
* Accessibility analysis
* Composite Opportunity Index
* Interactive dashboard built with Dash
* Fully reproducible data pipeline

---

## Methodology

The project combines several dimensions of territorial development, including:

* Demographic characteristics
* Accessibility to healthcare
* Accessibility to higher education
* Accessibility to transportation infrastructure
* Labour market indicators
* Additional territorial variables (future versions)

Each indicator is standardised before being aggregated into a composite **Regional Opportunity Index**.

The weighting scheme is transparent and can be easily modified for sensitivity analyses or alternative policy scenarios.

---

## Project Structure

```text
regional-opportunity-index/

│
├── assets/
├── dashboard/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── download.py
│   ├── preprocess.py
│   ├── indicators.py
│   ├── roi.py
│   └── maps.py
│
├── README.md
├── requirements.txt
└── LICENSE
```

---

## Technologies

* Python
* Pandas
* GeoPandas
* NumPy
* Plotly
* Dash
* Folium
* Contextily
* Matplotlib
* Scikit-learn

---

## Data Sources

The project relies exclusively on publicly available datasets, including:

* Spanish National Statistics Institute (INE)
* National Geographic Institute (IGN)
* OpenStreetMap
* Spanish Government Open Data Portal
* Additional official public datasets

---

## Dashboard

The interactive dashboard includes:

* Regional Opportunity Index map
* Municipality explorer
* Territorial rankings
* Spatial analysis
* Interactive visualisations
* Indicator comparison

---

## Project Status

🚧 This project is currently under development.

Future releases will incorporate additional socioeconomic indicators, improved accessibility metrics and expanded spatial analysis.

---

## Motivation

Territorial inequalities remain one of the major challenges for evidence-based public policy.

This project demonstrates how open data, GIS and data science can be combined to generate transparent, reproducible and interpretable indicators that support territorial analysis and informed decision-making.

---

## Author

**Luis Miguel**

Computational Social Data Scientist

GitHub Portfolio: *https://lm-hcor.github.io/lmhcor.github.io/*

LinkedIn: *https://www.linkedin.com/in/lmhcor/*

---

## License

This project is released under the Apache 2.0 License.
