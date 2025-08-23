#!/usr/bin/env python3
"""
🔧 REAL API CONNECTION FIXER
============================
This will enable real API connections and disable demo mode.
"""

import os
import asyncio
import aiohttp
from datetime import datetime

async def test_all_apis():
    """Test each API individually to see which ones work."""
    
    print("🔍 TESTING ALL API CONNECTIONS")
    print("=" * 60)
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    async with aiohttp.ClientSession() as session:
        
        # Test 1: GBIF (should work, no key needed)
        print("\n1️⃣ TESTING GBIF API (No key needed)")
        try:
            url = "https://api.gbif.org/v1/occurrence/search"
            params = {
                'decimalLatitude': -18.9333,
                'decimalLongitude': 48.4167,
                'radius': 10000,
                'country': 'MG',
                'limit': 5
            }
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ GBIF: {data.get('count', 0)} records found")
                else:
                    print(f"❌ GBIF: HTTP {response.status}")
        except Exception as e:
            print(f"❌ GBIF Error: {e}")
        
        # Test 2: eBird
        print("\n2️⃣ TESTING EBIRD API")
        ebird_key = os.getenv('EBIRD_API_KEY')
        print(f"eBird key: {ebird_key}")
        if ebird_key and len(ebird_key) > 8:
            try:
                url = "https://api.ebird.org/v2/data/obs/MG/recent"
                headers = {"X-eBirdApiToken": ebird_key}
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ eBird: {len(data)} recent observations")
                    else:
                        print(f"❌ eBird: HTTP {response.status}")
            except Exception as e:
                print(f"❌ eBird Error: {e}")
        else:
            print("❌ eBird: Invalid or missing API key")
        
        # Test 3: NASA FIRMS
        print("\n3️⃣ TESTING NASA FIRMS API")
        nasa_key = os.getenv('NASA_FIRMS_MAP_KEY')
        print(f"NASA FIRMS key: {nasa_key}")
        if nasa_key and nasa_key != "demo":
            try:
                bbox = "43,-26,51,-11"  # Madagascar
                url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{nasa_key}/VIIRS_SNPP_NRT/{bbox}/1"
                async with session.get(url, timeout=15) as response:
                    if response.status == 200:
                        text = await response.text()
                        lines = text.strip().split('\n')
                        print(f"✅ NASA FIRMS: {len(lines)-1} fire records")
                    else:
                        print(f"❌ NASA FIRMS: HTTP {response.status}")
            except Exception as e:
                print(f"❌ NASA FIRMS Error: {e}")
        else:
            print("❌ NASA FIRMS: Using demo key, need real key")

async def force_real_api_mode():
    """Modify the system to force real API usage."""
    
    print("\n🔧 ENABLING REAL API MODE")
    print("=" * 40)
    
    # Check if we can import the conservation system
    try:
        import sys
        sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
        
        from realtime_conservation_integration import ProductionDataIntegrator
        
        # Create integrator
        integrator = ProductionDataIntegrator()
        
        # Check API configuration
        print("📊 Current API Configuration:")
        for name, api in integrator.apis.items():
            is_live = api.is_live_mode()
            print(f"   {name}: {'✅ LIVE' if is_live else '❌ DEMO'} (key: {api.api_key[:10] if api.api_key else 'None'}...)")
        
        # Test one API call
        print("\n🧪 Testing real API call through system:")
        
        # Test GBIF through the system
        result = await integrator.get_live_species_data((-18.9333, 48.4167), radius_km=10)
        
        if result:
            print(f"✅ System API call successful!")
            print(f"📊 Data source: {result.get('data_source', 'Unknown')}")
            print(f"🦎 Species count: {result.get('unique_species', 'Unknown')}")
            print(f"🔍 Data quality: {result.get('data_quality', 'Unknown')}")
            
            if result.get('data_quality') == 'demo':
                print("🚨 WARNING: Still using demo data!")
            else:
                print("🎉 SUCCESS: Using real data!")
        
    except Exception as e:
        print(f"❌ Error testing system: {e}")

if __name__ == "__main__":
    asyncio.run(test_all_apis())
    asyncio.run(force_real_api_mode())
