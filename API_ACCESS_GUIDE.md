# Real-Time Conservation Data API Access Guide
=====================================

## Overview
This guide provides detailed instructions for obtaining API keys and accessing real-time environmental datasets for conservation monitoring.

## 🌍 **CURRENTLY INTEGRATED APIS (NO KEY REQUIRED)**

### 1. **GBIF - Global Biodiversity Information Facility**
- **Website**: https://www.gbif.org/
- **API Documentation**: https://www.gbif.org/developer
- **Data Type**: Species occurrence records worldwide
- **Access**: **FREE - No API key required**
- **Rate Limits**: No strict limits for reasonable use
- **Madagascar Coverage**: Excellent (comprehensive species records)
- **Usage in System**: Real-time biodiversity monitoring and endemic species tracking

**API Endpoint**: `https://api.gbif.org/v1/occurrence/search`
**Current Status**: ✅ **ACTIVE AND WORKING**

### 2. **NASA FIRMS - Fire Information for Resource Management System**
- **Website**: https://firms.modaps.eosdis.nasa.gov/
- **API Documentation**: https://firms.modaps.eosdis.nasa.gov/api/
- **Data Type**: Real-time active fire detection from satellites
- **Access**: **FREE - Uses demo key by default**
- **Rate Limits**: Reasonable usage allowed
- **Madagascar Coverage**: Global satellite coverage
- **Usage in System**: Real-time fire threat detection and forest monitoring

**API Endpoint**: `https://firms.modaps.eosdis.nasa.gov/api/area/csv/demo/VIIRS_SNPP_NRT/`
**Current Status**: ✅ **ACTIVE AND WORKING**

### 3. **USGS Earthquake Hazards Program**
- **Website**: https://earthquake.usgs.gov/
- **API Documentation**: https://earthquake.usgs.gov/fdsnws/event/1/
- **Data Type**: Real-time earthquake and seismic activity data
- **Access**: **FREE - No API key required**
- **Rate Limits**: No strict limits
- **Madagascar Coverage**: Global seismic monitoring
- **Usage in System**: Environmental stability assessment

**API Endpoint**: `https://earthquake.usgs.gov/fdsnws/event/1/query`
**Current Status**: ✅ **ACTIVE AND WORKING**

## 🔑 **PREMIUM APIs (REQUIRE REGISTRATION)**

### 4. **Sentinel Hub (Copernicus)**
- **Website**: https://www.sentinel-hub.com/
- **API Documentation**: https://docs.sentinel-hub.com/api/latest/
- **Data Type**: Satellite imagery, forest monitoring, land use changes
- **Access**: **FREE TIER AVAILABLE** (up to 1,000 requests/month)
- **Registration**: Required for API key
- **Madagascar Coverage**: Excellent satellite coverage

**How to Get API Key:**
1. Go to https://www.sentinel-hub.com/
2. Create free account
3. Navigate to User Dashboard
4. Generate API key under "OAuth clients"
5. Add to `.env` file: `SENTINEL_HUB_API_KEY=your_key_here`

### 5. **eBird API (Cornell Lab)**
- **Website**: https://ebird.org/api/keygen
- **API Documentation**: https://documenter.getpostman.com/view/664302/S1ENwy59
- **Data Type**: Real-time bird observation data
- **Access**: **FREE** with registration
- **Madagascar Coverage**: Good (citizen science data)

**How to Get API Key:**
1. Go to https://ebird.org/api/keygen
2. Submit API key request with project description
3. Receive key via email (usually within 24 hours)
4. Add to `.env` file: `EBIRD_API_KEY=your_key_here`

### 6. **Global Forest Watch API**
- **Website**: https://www.globalforestwatch.org/
- **API Documentation**: https://production-api.globalforestwatch.org/
- **Data Type**: Forest loss alerts, deforestation data
- **Access**: **FREE** but registration recommended
- **Madagascar Coverage**: Excellent forest monitoring

**How to Get API Key:**
1. Go to https://www.globalforestwatch.org/
2. Create account
3. Access developer portal
4. Generate API token
5. Add to `.env` file: `GFW_API_KEY=your_key_here`

### 7. **NASA Earthdata**
- **Website**: https://earthdata.nasa.gov/
- **API Documentation**: https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html
- **Data Type**: Climate data, atmospheric conditions, environmental parameters
- **Access**: **FREE** with NASA Earthdata account
- **Madagascar Coverage**: Global coverage

**How to Get API Key:**
1. Go to https://urs.earthdata.nasa.gov/
2. Create NASA Earthdata account
3. Generate application token
4. Add to `.env` file: `NASA_EARTHDATA_TOKEN=your_token_here`

## 🚀 **ADDITIONAL HIGH-VALUE APIS**

### 8. **NOAA Climate Data API**
- **Website**: https://www.ncdc.noaa.gov/cdo-web/webservices/v2
- **Data Type**: Climate and weather data
- **Access**: **FREE** with registration
- **How to Get**: Request token at https://www.ncdc.noaa.gov/cdo-web/token

### 9. **European Space Agency (ESA) APIs**
- **Website**: https://scihub.copernicus.eu/
- **Data Type**: Copernicus satellite data
- **Access**: **FREE** with registration
- **Madagascar Coverage**: Excellent

### 10. **IUCN Red List API**
- **Website**: https://apiv3.iucnredlist.org/
- **Data Type**: Species conservation status
- **Access**: **FREE** with registration
- **How to Get**: Request token at IUCN website

## 🔧 **SETUP INSTRUCTIONS**

### Current .env Configuration
```bash
# NASA APIs (some require registration)
NASA_FIRMS_MAP_KEY=demo  # Upgrade to personal key for higher limits
NASA_EARTHDATA_TOKEN=your_token_here

# Biodiversity APIs
EBIRD_API_KEY=your_key_here
GBIF_USER=your_username  # Optional for enhanced access
IUCN_API_TOKEN=your_token_here

# Satellite/Earth Observation APIs
SENTINEL_HUB_API_KEY=your_key_here
ESA_SCIHUB_USERNAME=your_username
ESA_SCIHUB_PASSWORD=your_password

# Forest Monitoring APIs
GFW_API_KEY=your_key_here

# Climate APIs
NOAA_CDO_TOKEN=your_token_here

# Database URLs (if using direct database access)
GBIF_DATABASE_URL=postgresql://user:pass@host:port/gbif
CONSERVATION_DB_URL=postgresql://user:pass@host:port/conservation
```

### Quick Start (No Registration Required)
Our current system works with **NO API KEYS** required! The following are already operational:
- ✅ GBIF Species Data
- ✅ NASA FIRMS Fire Detection  
- ✅ USGS Earthquake Data

### Enhanced Access (With Registration)
For enhanced capabilities and higher rate limits:
1. Register for eBird API (bird biodiversity)
2. Get Sentinel Hub key (satellite imagery)
3. Register for Global Forest Watch (deforestation alerts)

## 📊 **API COMPARISON TABLE**

| API | Data Type | Free Tier | Rate Limit | Madagascar Coverage | Registration |
|-----|-----------|-----------|------------|-------------------|--------------|
| GBIF | Species | Unlimited | None | Excellent | No |
| NASA FIRMS | Fire Detection | Good | Reasonable | Global | No |
| USGS | Earthquakes | Unlimited | None | Global | No |
| Sentinel Hub | Satellite | 1K req/month | 1000/month | Excellent | Yes |
| eBird | Birds | Good | 100 req/hour | Good | Yes |
| GFW | Forest Loss | Good | 1000/day | Excellent | Recommended |

## 🌍 **MADAGASCAR-SPECIFIC DATA SOURCES**

### National Databases
- **Madagascar National Parks**: https://www.parcs-madagascar.com/
- **Missouri Botanical Garden Madagascar**: https://www.tropicos.org/
- **Kew Madagascar**: https://www.kew.org/science/our-science/projects/madagascar-conservation-centre

### Regional Conservation APIs
- **Western Indian Ocean Commission**: https://www.commissionoceanindien.org/
- **UNEP-WCMC Madagascar**: https://www.unep-wcmc.org/

## ⚡ **CURRENT SYSTEM STATUS**

**Working APIs (No keys needed):**
- ✅ GBIF: Species occurrence data
- ✅ NASA FIRMS: Fire detection
- ✅ USGS: Earthquake monitoring

**Available for Enhancement:**
- 🔑 Sentinel Hub: Satellite imagery (free tier)
- 🔑 eBird: Bird observations (free)
- 🔑 Global Forest Watch: Deforestation alerts (free)

**Recommendation**: Start with the working APIs (no registration) and add premium APIs as needed for enhanced capabilities.

## 📝 **NEXT STEPS**

1. **Immediate**: System works with current APIs (no keys needed)
2. **Short-term**: Register for eBird and Sentinel Hub (free tiers)
3. **Long-term**: Add specialized Madagascar conservation databases
4. **Advanced**: Integrate with local monitoring stations and IoT sensors

The system is **production-ready** with current APIs and can be enhanced incrementally by adding premium data sources.
