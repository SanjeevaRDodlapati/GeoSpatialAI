# Geospatial Analysis Environment Setup

This document provides installation instructions for the geospatial data science tutorial environment.

## Quick Setup (Recommended)

### Option 1: Using Conda (Recommended)

```bash
# Create a new conda environment
conda create -n geospatial python=3.10

# Activate the environment
conda activate geospatial

# Install core geospatial packages from conda-forge
conda install -c conda-forge geopandas rasterio xarray matplotlib contextily mapclassify osmnx folium jupyter

# Install additional packages
conda install -c conda-forge cartopy matplotlib-scalebar rioxarray pyproj shapely requests

# Install optional packages for advanced features
conda install -c conda-forge pykrige scikit-learn seaborn plotly
```

### Option 2: Using pip

```bash
# Create virtual environment (optional but recommended)
python -m venv geospatial_env

# Activate (Windows)
geospatial_env\Scripts\activate

# Activate (macOS/Linux) 
source geospatial_env/bin/activate

# Install packages
pip install geopandas[complete] rasterio xarray matplotlib contextily mapclassify osmnx folium jupyter
pip install cartopy matplotlib-scalebar rioxarray pyproj shapely requests
pip install pykrige scikit-learn seaborn plotly
```

## Package List and Purposes

### Core Geospatial Libraries
- **geopandas** (≥0.13.0): Primary library for vector geospatial data
- **shapely** (≥2.0.0): Geometric operations and spatial relationships
- **pyproj** (≥3.4.0): Coordinate reference system transformations
- **rasterio** (≥1.3.0): Read/write raster datasets
- **rioxarray** (≥0.13.0): Raster operations with xarray integration
- **xarray** (≥2022.12.0): N-dimensional labeled arrays

### Visualization and Cartography
- **matplotlib** (≥3.6.0): Core plotting library
- **contextily** (≥1.3.0): Add basemap tiles to matplotlib maps
- **cartopy** (≥0.21.0): Advanced cartographic projections
- **folium** (≥0.14.0): Interactive web maps
- **plotly** (≥5.11.0): Interactive visualizations

### Analysis and Classification
- **mapclassify** (≥2.4.0): Statistical data classification for maps
- **scikit-learn** (≥1.1.0): Machine learning algorithms
- **scipy** (≥1.9.0): Scientific computing functions

### Network Analysis
- **osmnx** (≥1.6.0): Work with OpenStreetMap street networks

### Utilities
- **requests** (≥2.28.0): HTTP library for data downloads
- **pandas** (≥1.5.0): Data manipulation (automatically installed with geopandas)
- **numpy** (≥1.21.0): Numerical computing (automatically installed)

## Verification Script

Save this as `test_installation.py` and run it to verify your setup:

```python
import sys
import importlib

required_packages = [
    'geopandas', 'pandas', 'numpy', 'matplotlib', 'shapely',
    'pyproj', 'rasterio', 'xarray', 'rioxarray', 'contextily',
    'mapclassify', 'osmnx', 'folium', 'cartopy', 'requests'
]

print("Testing geospatial environment setup...")
print("=" * 50)

failed_imports = []

for package in required_packages:
    try:
        mod = importlib.import_module(package)
        version = getattr(mod, '__version__', 'unknown')
        print(f"✅ {package}: {version}")
    except ImportError as e:
        print(f"❌ {package}: Import failed - {e}")
        failed_imports.append(package)

print("=" * 50)

if failed_imports:
    print(f"❌ Failed to import: {', '.join(failed_imports)}")
    print("Please install missing packages before continuing.")
    sys.exit(1)
else:
    print("🎉 All packages successfully imported!")
    print("You're ready to start the geospatial tutorial!")
```

## Common Installation Issues

### 1. GDAL/GEOS/PROJ Dependencies
If you encounter issues with GDAL, GEOS, or PROJ:

**Conda solution (recommended):**
```bash
conda install -c conda-forge gdal geos proj
```

**System-level installation (macOS):**
```bash
brew install gdal geos proj
```

**System-level installation (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install gdal-bin libgdal-dev libgeos-dev libproj-dev
```

### 2. Cartopy Installation Issues
Cartopy can be challenging to install. Use conda-forge:

```bash
conda install -c conda-forge cartopy
```

### 3. OSMnx Requirements
OSMnx requires specific versions of dependencies:

```bash
conda install -c conda-forge osmnx
# or
pip install osmnx
```

### 4. Jupyter Setup
To use Jupyter notebooks:

```bash
# Install Jupyter
conda install jupyter
# or pip install jupyter

# Register the kernel
python -m ipykernel install --user --name geospatial --display-name "Geospatial Python"

# Start Jupyter
jupyter notebook
```

## Environment File

You can also create an environment from this `environment.yml` file:

```yaml
name: geospatial
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - geopandas>=0.13.0
  - rasterio>=1.3.0
  - xarray>=2022.12.0
  - rioxarray>=0.13.0
  - shapely>=2.0.0
  - pyproj>=3.4.0
  - matplotlib>=3.6.0
  - contextily>=1.3.0
  - mapclassify>=2.4.0
  - cartopy>=0.21.0
  - folium>=0.14.0
  - osmnx>=1.6.0
  - jupyter
  - requests>=2.28.0
  - scipy>=1.9.0
  - scikit-learn>=1.1.0
  - seaborn
  - plotly
  - matplotlib-scalebar
  - pykrige
```

Save as `environment.yml` and create with:
```bash
conda env create -f environment.yml
conda activate geospatial
```

## Platform-Specific Notes

### Windows
- Use Anaconda or Miniconda for easiest setup
- Some packages may require Visual Studio Build Tools
- Consider using Windows Subsystem for Linux (WSL) for better compatibility

### macOS
- Install Homebrew first for system dependencies
- Use conda-forge channel for geospatial packages
- M1/M2 Macs: ensure you're using arm64 versions

### Linux
- Install system-level geospatial libraries first
- Ubuntu/Debian users should install build essentials
- CentOS/RHEL users may need EPEL repository

## Getting Help

If you encounter installation issues:

1. Check the [GeoPandas installation guide](https://geopandas.org/en/stable/getting_started/install.html)
2. Visit the [Cartopy installation docs](https://scitools.org.uk/cartopy/docs/latest/installing.html)
3. Search issues on package GitHub repositories
4. Ask questions on [GIS Stack Exchange](https://gis.stackexchange.com/)

---

**Next Step**: Once your environment is set up, start with `Project 0: Cartography Practice` to verify everything works correctly!
