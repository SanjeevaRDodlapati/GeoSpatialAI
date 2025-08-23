#!/usr/bin/env python3
"""
Test script to verify geospatial environment setup
"""

import sys
import importlib
from pathlib import Path

def test_import(package_name, display_name=None):
    """Test importing a package and display version if available"""
    if display_name is None:
        display_name = package_name
    
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {display_name:20} {version}")
        return True
    except ImportError as e:
        print(f"❌ {display_name:20} Import failed: {e}")
        return False

def main():
    print("🔍 GEOSPATIAL ENVIRONMENT TEST")
    print("=" * 60)
    
    # Core Python libraries
    print("\n📦 Core Libraries:")
    core_packages = [
        ('numpy', 'NumPy'),
        ('pandas', 'Pandas'), 
        ('matplotlib', 'Matplotlib'),
        ('scipy', 'SciPy'),
        ('requests', 'Requests')
    ]
    
    core_results = []
    for pkg, name in core_packages:
        core_results.append(test_import(pkg, name))
    
    # Geospatial libraries
    print("\n🌍 Geospatial Libraries:")
    geo_packages = [
        ('geopandas', 'GeoPandas'),
        ('shapely', 'Shapely'),
        ('pyproj', 'PyProj'),
        ('rasterio', 'Rasterio'),
        ('xarray', 'xarray'),
        ('rioxarray', 'rioxarray')
    ]
    
    geo_results = []
    for pkg, name in geo_packages:
        geo_results.append(test_import(pkg, name))
    
    # Visualization libraries
    print("\n🎨 Visualization Libraries:")
    viz_packages = [
        ('contextily', 'Contextily'),
        ('cartopy', 'Cartopy'),
        ('folium', 'Folium'),
        ('plotly', 'Plotly'),
        ('seaborn', 'Seaborn')
    ]
    
    viz_results = []
    for pkg, name in viz_packages:
        viz_results.append(test_import(pkg, name))
    
    # Analysis libraries
    print("\n📊 Analysis Libraries:")
    analysis_packages = [
        ('mapclassify', 'MapClassify'),
        ('sklearn', 'Scikit-learn'),
        ('osmnx', 'OSMnx')
    ]
    
    analysis_results = []
    for pkg, name in analysis_packages:
        analysis_results.append(test_import(pkg, name))
    
    # Jupyter libraries
    print("\n📓 Jupyter Environment:")
    jupyter_packages = [
        ('jupyter', 'Jupyter'),
        ('IPython', 'IPython'),
        ('ipykernel', 'IPython Kernel')
    ]
    
    jupyter_results = []
    for pkg, name in jupyter_packages:
        jupyter_results.append(test_import(pkg, name))
    
    # Summary
    print("\n" + "=" * 60)
    total_packages = len(core_packages) + len(geo_packages) + len(viz_packages) + len(analysis_packages) + len(jupyter_packages)
    successful_imports = sum(core_results + geo_results + viz_results + analysis_results + jupyter_results)
    
    if successful_imports == total_packages:
        print(f"🎉 SUCCESS: All {total_packages} packages imported successfully!")
        print("\n✅ Your geospatial environment is ready!")
        print("✅ You can now start with Project 0: Cartography Practice")
        
        # Test basic functionality
        print("\n🔧 Quick Functionality Test:")
        try:
            import geopandas as gpd
            import matplotlib.pyplot as plt
            import numpy as np
            
            # Create a simple point
            from shapely.geometry import Point
            point = Point(0, 0)
            print(f"✅ Created geometry: {point}")
            
            # Test coordinate transformation
            import pyproj
            transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
            x, y = transformer.transform(0, 0)
            print(f"✅ Coordinate transformation works: (0,0) → ({x:.1f},{y:.1f})")
            
            print("✅ Basic functionality test passed!")
            
        except Exception as e:
            print(f"⚠️  Basic functionality test failed: {e}")
        
        return 0
    else:
        failed_count = total_packages - successful_imports
        print(f"❌ ISSUES FOUND: {failed_count}/{total_packages} packages failed to import")
        print(f"✅ Successfully imported: {successful_imports}/{total_packages} packages")
        print("\n🔧 Try reinstalling the failed packages:")
        print("   pip install <package_name>")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
