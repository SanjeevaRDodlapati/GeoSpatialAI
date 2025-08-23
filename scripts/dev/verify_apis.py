#!/usr/bin/env python3
"""
🔍 REAL API VERIFICATION TEST
============================
This will test if we're actually hitting real APIs or just getting simulated data.
"""

import requests
import os
from datetime import datetime
import json

def test_real_gbif_api():
    """Test direct connection to GBIF API"""
    print("🔍 TESTING REAL GBIF API CONNECTION")
    print("=" * 50)
    
    # Test with different coordinates
    coords = [
        (-18.9333, 48.4167, "Andasibe-Mantadia"),
        (-21.2500, 47.4167, "Ranomafana"), 
        (-22.5500, 45.3167, "Isalo"),
        (-15.7000, 50.2333, "Masoala")
    ]
    
    for lat, lng, name in coords:
        print(f"\n📍 Testing location: {name} ({lat}, {lng})")
        
        # Direct GBIF API call
        url = f"https://api.gbif.org/v1/occurrence/search"
        params = {
            'decimalLatitude': lat,
            'decimalLongitude': lng,
            'radius': 10000,  # 10km radius
            'limit': 20,
            'country': 'MG'  # Madagascar
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                results = data.get('results', [])
                
                print(f"✅ GBIF Response: {count} total records")
                print(f"📊 Retrieved: {len(results)} records in this batch")
                
                # Show actual species names
                species_seen = set()
                for record in results[:5]:
                    species = record.get('species', 'Unknown')
                    if species and species != 'Unknown':
                        species_seen.add(species)
                
                print(f"🦎 Real species found: {', '.join(list(species_seen)[:3])}...")
                
                # Check if we get different results for different locations
                if count > 0:
                    print(f"🎯 This location has REAL data: {count} records")
                else:
                    print("⚠️ No records found for this location")
                    
            else:
                print(f"❌ GBIF API Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Connection Error: {e}")

def test_real_ebird_api():
    """Test direct connection to eBird API"""
    print("\n🐦 TESTING REAL EBIRD API CONNECTION")
    print("=" * 50)
    
    # Check if we have eBird API key
    api_key = os.getenv('EBIRD_API_KEY')
    
    if not api_key:
        print("❌ No eBird API key found in environment")
        return
    
    # Test Madagascar region
    url = "https://api.ebird.org/v2/data/obs/MG/recent"
    headers = {'X-eBirdApiToken': api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ eBird Response: {len(data)} recent observations")
            
            # Show actual species
            species_names = [obs.get('comName', 'Unknown') for obs in data[:5]]
            print(f"🐦 Real birds found: {', '.join(species_names)}")
            
        else:
            print(f"❌ eBird API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def test_real_nasa_firms():
    """Test NASA FIRMS fire detection API"""
    print("\n🔥 TESTING REAL NASA FIRMS API CONNECTION") 
    print("=" * 50)
    
    # Madagascar bounding box
    bbox = "43,-26,51,-11"  # Madagascar bounds
    
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/your_api_key/VIIRS_SNPP_NRT/{bbox}/1"
    
    try:
        # Note: This needs a real API key, so we'll test the endpoint
        response = requests.head("https://firms.modaps.eosdis.nasa.gov", timeout=5)
        print(f"✅ NASA FIRMS endpoint reachable: {response.status_code}")
        
    except Exception as e:
        print(f"❌ NASA FIRMS Connection Error: {e}")

def compare_our_system_vs_real_api():
    """Compare what our system returns vs real API"""
    print("\n🔍 COMPARING OUR SYSTEM VS REAL APIs")
    print("=" * 60)
    
    # First, test real GBIF
    print("1️⃣ REAL GBIF API:")
    test_real_gbif_api()
    
    print("\n2️⃣ REAL eBird API:")
    test_real_ebird_api()
    
    print("\n3️⃣ REAL NASA FIRMS API:")
    test_real_nasa_firms()
    
    print("\n" + "=" * 60)
    print("🎯 CONCLUSION:")
    print("If our system returns the SAME numbers every time,")
    print("but real APIs show DIFFERENT data, then our system")
    print("is using simulated/hardcoded responses!")

if __name__ == "__main__":
    print("🔍 REAL-WORLD API VERIFICATION TEST")
    print("🌍 Testing direct connections to conservation databases")
    print("⏰ Timestamp:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)
    
    compare_our_system_vs_real_api()
    
    print("\n" + "=" * 70)
    print("✅ Test complete! Compare these results with your system output.")
