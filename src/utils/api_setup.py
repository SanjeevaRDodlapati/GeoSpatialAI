#!/usr/bin/env python3
"""
🔑 API KEY ACQUISITION GUIDE
===========================
Step-by-step guide to get all missing API keys for real conservation data.
"""

import webbrowser
import os

def open_api_registration_pages():
    """Open API registration pages in browser."""
    
    print("🔑 API KEY ACQUISITION GUIDE")
    print("=" * 50)
    print("Opening registration pages for missing API keys...\n")
    
    # NASA FIRMS API Key
    print("1️⃣ NASA FIRMS (Fire Detection)")
    print("   Current: Using 'demo' key")
    print("   Need: Real API key for fire detection")
    print("   URL: https://firms.modaps.eosdis.nasa.gov/api/")
    print("   Cost: FREE")
    print("   Process: Register → Get Map Key")
    
    try:
        webbrowser.open("https://firms.modaps.eosdis.nasa.gov/api/")
        print("   ✅ Opened in browser")
    except:
        print("   ❌ Could not open browser")
    
    input("\nPress Enter when you have the NASA FIRMS key...")
    
    # eBird API Key (verify current one)
    print("\n2️⃣ eBird API (Bird Observations)")
    print("   Current: v74vv5t0s8d9 (seems short)")
    print("   URL: https://ebird.org/api/keygen")
    print("   Cost: FREE")
    print("   Process: Register → Generate Key")
    
    try:
        webbrowser.open("https://ebird.org/api/keygen")
        print("   ✅ Opened in browser")
    except:
        print("   ❌ Could not open browser")
    
    input("\nPress Enter when you have verified/updated eBird key...")
    
    # USGS Earthquake API (if needed)
    print("\n3️⃣ USGS Earthquake API (Optional)")
    print("   Current: Using public endpoint")
    print("   URL: https://earthquake.usgs.gov/fdsnws/event/1/")
    print("   Cost: FREE (no key needed)")
    print("   Status: ✅ Already working")
    
    # Global Forest Watch API
    print("\n4️⃣ Global Forest Watch (Deforestation)")
    print("   Current: Using base URL only")
    print("   URL: https://www.globalforestwatch.org/")
    print("   Cost: FREE")
    print("   Process: Contact for API access")
    
    print("\n" + "=" * 50)
    print("🎯 PRIORITY ORDER:")
    print("1. NASA FIRMS (Most important - fire detection)")
    print("2. eBird verification (Bird monitoring)")
    print("3. Global Forest Watch (Deforestation monitoring)")

def test_current_api_keys():
    """Test which API keys are currently working."""
    
    print("\n🧪 TESTING CURRENT API KEYS")
    print("=" * 40)
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    apis_status = []
    
    # Test GBIF (no key needed)
    try:
        import requests
        response = requests.get("https://api.gbif.org/v1/occurrence/search?limit=1", timeout=5)
        if response.status_code == 200:
            apis_status.append("✅ GBIF: Working (no key needed)")
        else:
            apis_status.append("❌ GBIF: Failed")
    except:
        apis_status.append("❌ GBIF: Connection failed")
    
    # Test eBird
    ebird_key = os.getenv('EBIRD_API_KEY')
    if ebird_key:
        try:
            headers = {"X-eBirdApiToken": ebird_key}
            response = requests.get("https://api.ebird.org/v2/data/obs/US/recent?back=1", headers=headers, timeout=5)
            if response.status_code == 200:
                apis_status.append("✅ eBird: Working")
            else:
                apis_status.append(f"❌ eBird: Failed (HTTP {response.status_code})")
        except:
            apis_status.append("❌ eBird: Connection failed")
    else:
        apis_status.append("❌ eBird: No API key")
    
    # Test NASA FIRMS
    nasa_key = os.getenv('NASA_FIRMS_MAP_KEY')
    if nasa_key and nasa_key != "demo":
        try:
            url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{nasa_key}/VIIRS_SNPP_NRT/0,0,1,1/1"
            response = requests.head(url, timeout=5)
            if response.status_code in [200, 404]:  # 404 is OK, means key is valid but no data
                apis_status.append("✅ NASA FIRMS: Working")
            else:
                apis_status.append(f"❌ NASA FIRMS: Failed (HTTP {response.status_code})")
        except:
            apis_status.append("❌ NASA FIRMS: Connection failed")
    else:
        apis_status.append("❌ NASA FIRMS: Using demo key")
    
    # Test Sentinel Hub
    sentinel_key = os.getenv('SENTINEL_HUB_API_KEY')
    if sentinel_key:
        apis_status.append("✅ Sentinel Hub: API key present")
    else:
        apis_status.append("❌ Sentinel Hub: No API key")
    
    print("\n📊 API STATUS SUMMARY:")
    for status in apis_status:
        print(f"  {status}")
    
    working_count = sum(1 for status in apis_status if "✅" in status)
    total_count = len(apis_status)
    
    print(f"\n🎯 WORKING APIs: {working_count}/{total_count}")
    
    if working_count >= 3:
        print("✅ Good! You have enough APIs for basic functionality")
    else:
        print("⚠️ Need more API keys for full functionality")

def update_env_file():
    """Guide to update .env file with new keys."""
    
    print("\n🔧 UPDATING .ENV FILE")
    print("=" * 30)
    print("Once you get the API keys, update your .env file:")
    print()
    print("1. Open: /Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/.env")
    print("2. Find line: NASA_FIRMS_MAP_KEY=demo")
    print("3. Replace with: NASA_FIRMS_MAP_KEY=your_actual_key_here")
    print("4. Save file")
    print("5. Restart the server")
    print()
    print("🔄 After updating, run this script again to test!")

if __name__ == "__main__":
    print("🌍 Madagascar Conservation AI - API Key Setup")
    print("=" * 60)
    
    # Test current status
    test_current_api_keys()
    
    # Guide to get missing keys
    print("\n" + "=" * 60)
    choice = input("Do you want to open API registration pages? (y/n): ")
    
    if choice.lower() == 'y':
        open_api_registration_pages()
    
    # Show update instructions
    update_env_file()
    
    print("\n✅ Setup guide complete!")
    print("🎯 Priority: Get NASA FIRMS key first for fire detection")
    print("🔄 After getting keys, restart your server to test!")
