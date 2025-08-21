# 🌍 GeoSpatialAI - Intelligent Geospatial Data Analysis

A comprehensive hands-on tutorial series covering geographic data analysis, visualization, machine learning, and AI applications in the geospatial domain.

## Overview

This repository contains a structured learning path for geospatial data science, starting with fundamental analysis and visualization techniques in Phase 1, and progressing to machine learning applications in later phases.

## Phase 1: Geospatial & Geographic Data Analysis

Phase 1 focuses on building core skills in geospatial data handling, analysis, and visualization without machine learning components. Each project is designed to teach specific concepts while building toward a comprehensive understanding of geospatial data science.

### Learning Objectives

- Master common geospatial Python libraries (GeoPandas, Shapely, PyProj, Rasterio, etc.)
- Understand coordinate reference systems (CRS) and projections
- Learn spatial data visualization and cartographic design
- Practice data cleaning and quality assurance for geospatial data
- Explore various geospatial data sources and formats
- Develop reproducible geospatial analysis workflows

### Project Structure

Each project follows a consistent folder structure:

```
project_name/
├── data/
│   ├── raw/           # Downloads as-is
│   ├── interim/       # Cleaned, joined data
│   └── processed/     # Analysis-ready data
├── notebooks/         # Main analysis notebook + exploratory notebooks
├── outputs/
│   ├── figures/       # PNGs/SVGs for maps/plots
│   ├── tables/        # CSVs/PNGs for summary tables
│   └── maps/          # GeoJSON/Shapefile/MBTiles if needed
└── README.md          # Project documentation
```

### Quality Assurance Checklist

Every project implements the following QA/QC procedures:

- ✅ Confirm CRS and units before any distance/area operation
- ✅ Validate geometry (fix self-intersections; drop empties)
- ✅ Inspect joins (row counts pre/post; unmatched keys; spatial join sanity checks)
- ✅ Record all filters and thresholds in README with rationale
- ✅ Cite all datasets with version/date and URL

### CRS Best Practices

- Use equal-area CRS for area/aggregation calculations
  - EPSG:5070 for CONUS (Continental United States)
  - EPSG:6933 for global analysis
- Use Web Mercator (EPSG:3857) only for basemap overlays
- Always document CRS choices and transformations

## Projects

### Project 0: Projection & Cartography Practice (Optional Warm-up)
**Status**: 📋 Planned
- **Aim**: Master projection handling and cartographic design basics
- **Data**: Natural Earth Admin boundaries, populated places
- **Skills**: CRS transformations, map styling, export workflows

### Project 1: Neighborhood Socio-Demographic Mapping
**Status**: 📋 Planned
- **Aim**: Explore spatial inequality using U.S. Census data
- **Data**: TIGER/Line boundaries, American Community Survey
- **Skills**: Tabular-geographic joins, choropleth mapping, classification schemes

### Project 2: Street Networks, Amenities, and Walkability
**Status**: 📋 Planned
- **Aim**: Analyze local accessibility using OpenStreetMap data
- **Data**: OSM street networks and points of interest
- **Skills**: Network analysis, accessibility metrics, spatial buffers

### Project 3: Air Quality Exploratory Analysis and Spatial Interpolation
**Status**: 📋 Planned
- **Aim**: Explore pollution patterns using sensor data
- **Data**: OpenAQ observations and station metadata
- **Skills**: Time series analysis, spatial interpolation, environmental data

### Project 4: Global Land Cover Snapshot and Change Analysis
**Status**: 📋 Planned
- **Aim**: Work with raster datasets for land cover analysis
- **Data**: ESA WorldCover or MODIS Land Cover
- **Skills**: Raster processing, change detection, zonal statistics

### Project 5: Species Occurrence Mapping and Environmental Context
**Status**: 📋 Planned
- **Aim**: Map biodiversity data and environmental relationships
- **Data**: GBIF species occurrences, environmental layers
- **Skills**: Point pattern analysis, environmental data extraction

### Project 6: Hazard Exposure Overlay Analysis
**Status**: 📋 Planned
- **Aim**: Assess population exposure to natural hazards
- **Data**: Flood/wildfire hazard maps, population grids
- **Skills**: Raster overlay analysis, exposure assessment

## Getting Started

### Prerequisites

- Python 3.8+ with conda or pip package manager
- Basic familiarity with pandas and matplotlib
- Understanding of coordinate systems (helpful but not required)

### Required Libraries

Core geospatial libraries:
```bash
# Essential geospatial stack
geopandas>=0.13.0
shapely>=2.0.0
pyproj>=3.4.0
rasterio>=1.3.0
rioxarray>=0.13.0
xarray>=2022.12.0

# Visualization and analysis
matplotlib>=3.6.0
contextily>=1.3.0
mapclassify>=2.4.0
folium>=0.14.0

# Network analysis
osmnx>=1.6.0

# Additional utilities
requests>=2.28.0
scipy>=1.9.0
```

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd GeoSpatial
```

2. **Quick Setup (Recommended)**:
```bash
# Create virtual environment and install packages
python3 -m venv geospatial_env
source geospatial_env/bin/activate  # On Windows: geospatial_env\Scripts\activate
pip install -r requirements.txt

# Register Jupyter kernel
python -m ipykernel install --user --name geospatial --display-name "Geospatial Python"

# Test installation
python test_environment.py
```

3. **Alternative: Using the activation script**:
```bash
# Make executable and run
chmod +x activate_env.sh
source activate_env.sh
```

4. **Alternative: Using Conda**:
```bash
conda create -n geospatial python=3.10
conda activate geospatial
conda install -c conda-forge geopandas rasterio xarray matplotlib contextily mapclassify osmnx folium jupyter
```

## Data Sources

This tutorial uses publicly available datasets from reputable sources:

- **Natural Earth**: Free vector and raster map data
- **U.S. Census Bureau**: Demographic and boundary data
- **OpenStreetMap**: Crowdsourced geographic data
- **OpenAQ**: Air quality measurements
- **ESA/NASA**: Satellite-derived environmental data
- **GBIF**: Biodiversity occurrence records

All data sources are properly attributed and cited in individual project READMEs.

## Contributing

This is an educational resource. Contributions that improve clarity, fix errors, or add valuable examples are welcome. Please:

1. Follow the established project structure
2. Include proper data citations
3. Test all code before submitting
4. Update documentation as needed

## License

This tutorial content is available under the MIT License. Individual datasets may have their own licenses - please check each project's README for specific attribution requirements.

## Acknowledgments

This tutorial is inspired by:
- "Geographic Data Science with Python" by Rey, Arribas-Bel & Wolf
- Natural Earth's commitment to free cartographic data
- The open source geospatial Python ecosystem
- Various public data providers committed to open science

---

**Next Steps**: After completing Phase 1, learners will progress to Phase 2 (Machine Learning Applications) covering spatial clustering, prediction models, and advanced geospatial AI techniques.
