#!/usr/bin/env python3
"""
🔧 FIX THE REAL API CONNECTION
=============================
This will configure your system to use REAL APIs instead of demo data.
"""

import os
from pathlib import Path

def setup_real_api_keys():
    """Configure real API keys for live data."""
    
    print("🔧 SETTING UP REAL API ACCESS")
    print("=" * 50)
    
    # Check current .env file
    env_path = Path("/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/.env")
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            content = f.read()
        print("📄 Current .env file contents:")
        print(content)
    else:
        print("❌ No .env file found")
    
    print("\n🎯 REQUIRED CHANGES TO GET REAL DATA:")
    print("1. Replace 'your_api_key_here' with actual API keys")
    print("2. Get real API keys from:")
    print("   • GBIF: No key needed (public API)")
    print("   • eBird: https://ebird.org/api/keygen")
    print("   • NASA FIRMS: https://firms.modaps.eosdis.nasa.gov/api/")
    print("   • Copernicus: https://scihub.copernicus.eu/")
    
    print("\n🔍 TESTING WHAT HAPPENS WITH REAL GBIF:")
    
    # Test direct GBIF call to prove we can get real data
    import requests
    
    url = "https://api.gbif.org/v1/occurrence/search"
    params = {
        'decimalLatitude': -18.9333,
        'decimalLongitude': 48.4167,
        'radius': 10000,
        'country': 'MG',
        'limit': 5
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            results = data.get('results', [])
            
            print(f"✅ REAL GBIF API Result: {count} total species records")
            print(f"📊 Sample species:")
            for i, record in enumerate(results[:3]):
                species = record.get('species', 'Unknown')
                print(f"   {i+1}. {species}")
            
            print(f"\n🚨 COMPARE: Your system says '184 species' EVERY TIME")
            print(f"🎯 REAL GBIF says: {count} species for this location")
            print("📝 Different locations should show different counts!")
            
    except Exception as e:
        print(f"❌ Error testing real GBIF: {e}")

if __name__ == "__main__":
    setup_real_api_keys()
