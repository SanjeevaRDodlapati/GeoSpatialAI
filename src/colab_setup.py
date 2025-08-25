"""
Universal Google Colab Setup Utility for GeoSpatialAI Projects
==============================================================

This module provides automatic package installation and environment setup
for running GeoSpatialAI notebooks in Google Colab.

Usage:
    # Add this at the beginning of any notebook
    import sys
    if 'google.colab' in sys.modules:
        !pip install git+https://github.com/SanjeevaRDodlapati/GeoSpatialAI.git
        from src.colab_setup import setup_colab_environment
        setup_colab_environment()
"""

import sys
import subprocess
import os
from pathlib import Path

def check_colab_environment():
    """Check if running in Google Colab"""
    return 'google.colab' in sys.modules

def install_packages_colab():
    """Install required packages for Colab environment"""
    print("🚀 Setting up Google Colab environment for GeoSpatialAI...")
    print("⏱️ Installing packages... (this may take 2-3 minutes)")
    
    # Core geospatial packages
    packages = [
        # Geospatial core
        "geopandas",
        "folium", 
        "contextily",
        "rasterio",
        
        # Visualization
        "plotly",
        "seaborn",
        "mapclassify",
        
        # Machine learning
        "scikit-learn",
        
        # Spatial analysis
        "libpysal",
        "esda",
        "pysal",
        
        # Additional utilities
        "requests",
        "beautifulsoup4",
        "openpyxl",
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
            print(f"  ✅ {package}")
        except subprocess.CalledProcessError:
            print(f"  ⚠️ Failed to install {package}")
    
    print("📦 Package installation complete!")

def setup_colab_directories():
    """Create necessary directories for Colab environment"""
    directories = [
        "data/raw",
        "data/processed", 
        "outputs/figures",
        "outputs/maps",
        "models"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("📁 Directory structure created")

def configure_matplotlib():
    """Configure matplotlib for Colab"""
    import matplotlib.pyplot as plt
    import warnings
    
    # Set up plotting backend and style
    plt.style.use('default')
    warnings.filterwarnings('ignore', category=FutureWarning)
    
    print("🎨 Matplotlib configured")

def setup_colab_environment(project_name="GeoSpatialAI", show_info=True):
    """
    Complete Colab environment setup
    
    Args:
        project_name (str): Name of the project
        show_info (bool): Whether to display setup information
    """
    if not check_colab_environment():
        if show_info:
            print("💻 Running in local environment - no Colab setup needed")
        return False
    
    if show_info:
        print(f"🚀 {project_name} - Google Colab Environment Setup")
        print("=" * 60)
    
    # Install packages
    install_packages_colab()
    
    # Setup directories
    setup_colab_directories()
    
    # Configure visualization
    configure_matplotlib()
    
    if show_info:
        print("✅ Colab environment setup complete!")
        print("📍 Note: Files saved in Colab are temporary unless downloaded")
        print("🔗 For persistent storage, mount Google Drive if needed")
        print()
    
    return True

def get_colab_badge_html(notebook_path):
    """
    Generate Colab badge HTML for a notebook
    
    Args:
        notebook_path (str): Path to notebook relative to repo root
        
    Returns:
        str: HTML for Colab badge
    """
    colab_url = f"https://colab.research.google.com/github/SanjeevaRDodlapati/GeoSpatialAI/blob/main/{notebook_path}"
    
    badge_html = f"""[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})"""
    
    return badge_html

def print_environment_info():
    """Print current environment information"""
    print(f"🐍 Python version: {sys.version}")
    print(f"📍 Environment: {'Google Colab' if check_colab_environment() else 'Local'}")
    print(f"📂 Working directory: {os.getcwd()}")

if __name__ == "__main__":
    # Example usage
    setup_colab_environment()
    print_environment_info()
