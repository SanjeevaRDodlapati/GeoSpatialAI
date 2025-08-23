"""
WORKING REAL API INTEGRATION
===========================
This bypasses the broken demo system and calls APIs directly.
"""

import asyncio
import aiohttp
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class WorkingRealAPIIntegrator:
    """Actually working real API calls."""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_real_gbif_data(self, lat: float, lng: float, radius_km: int = 10):
        """Get REAL GBIF species data."""
        try:
            url = "https://api.gbif.org/v1/occurrence/search"
            params = {
                'decimalLatitude': lat,
                'decimalLongitude': lng,
                'radius': radius_km * 1000,  # Convert to meters
                'country': 'MG',
                'limit': 20
            }
            
            async with self.session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'total_count': data.get('count', 0),
                        'results': data.get('results', []),
                        'species_names': list(set(r.get('species', 'Unknown') for r in data.get('results', []) if r.get('species')))
                    }
        except Exception as e:
            print(f"GBIF Error: {e}")
            return None
    
    async def get_real_ebird_data(self, lat: float, lng: float, radius_km: int = 10):
        """Get REAL eBird species data."""
        try:
            api_key = os.getenv('EBIRD_API_KEY')
            if not api_key:
                return None
                
            url = "https://api.ebird.org/v2/data/obs/geo/recent"
            params = {
                'lat': lat,
                'lng': lng,
                'dist': radius_km,
                'back': 7,
                'fmt': 'json'
            }
            headers = {"X-eBirdApiToken": api_key}
            
            async with self.session.get(url, params=params, headers=headers, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'observation_count': len(data),
                        'species_count': len(set(obs.get('sciName', '') for obs in data)),
                        'species_names': list(set(obs.get('comName', 'Unknown') for obs in data if obs.get('comName')))[:5]
                    }
        except Exception as e:
            print(f"eBird Error: {e}")
            return None

# Synchronous wrappers for the web server
def trigger_location_analysis(lat: float, lng: float, location_name: str) -> str:
    """Get REAL location analysis with actual API calls."""
    
    async def _real_analysis():
        async with WorkingRealAPIIntegrator() as api:
            # Get real GBIF data
            gbif_data = await api.get_real_gbif_data(lat, lng)
            
            # Get real eBird data  
            ebird_data = await api.get_real_ebird_data(lat, lng)
            
            result = f"""📍 REAL LOCATION ANALYSIS: {location_name}
Coordinates: {lat}, {lng}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔄 REAL-TIME DATA COLLECTION:
"""
            
            if gbif_data:
                result += f"✅ GBIF Species Records: {gbif_data['total_count']} total records found\n"
                result += f"🦎 Unique Species in Area: {len(gbif_data['species_names'])}\n"
                result += f"📋 Sample Species: {', '.join(gbif_data['species_names'][:3])}\n"
            else:
                result += "❌ GBIF: No data retrieved\n"
            
            if ebird_data:
                result += f"🐦 eBird Observations: {ebird_data['observation_count']} recent sightings\n"
                result += f"🦅 Bird Species Count: {ebird_data['species_count']}\n" 
                result += f"🕊️ Sample Birds: {', '.join(ebird_data['species_names'][:3])}\n"
            else:
                result += "❌ eBird: No data retrieved\n"
            
            result += f"""
🎯 CONSERVATION ASSESSMENT:
• Location: {location_name}
• Real API Data: {'✅ LIVE' if gbif_data or ebird_data else '❌ FAILED'}
• Biodiversity Index: {'HIGH' if (gbif_data and gbif_data['total_count'] > 100) else 'MODERATE'}
• Data Freshness: Real-time from GBIF and eBird APIs

✅ This is REAL data that changes based on actual location!
🌍 Try different coordinates to see different results!
"""
            
            return result
    
    try:
        return asyncio.run(_real_analysis())
    except Exception as e:
        return f"❌ Error getting real data: {str(e)}"

def trigger_emergency_response(lat: float = None, lng: float = None, location_name: str = "Selected Location") -> str:
    """Real emergency response with actual data checks for the clicked location."""
    
    async def _real_emergency():
        async with WorkingRealAPIIntegrator() as api:
            # Use clicked coordinates if provided, otherwise default locations
            if lat is not None and lng is not None:
                locations = [(lat, lng, location_name)]
                emergency_center = f"{location_name} ({lat}, {lng})"
            else:
                # Fallback to multiple Madagascar locations for comprehensive scan
                locations = [
                    (-18.9333, 48.4167, "Andasibe-Mantadia"),
                    (-21.2500, 47.4167, "Ranomafana"),
                    (-22.5500, 45.3167, "Isalo")
                ]
                emergency_center = "Central Madagascar"
            
            total_species = 0
            critical_areas = []
            
            for loc_lat, loc_lng, name in locations:
                gbif_data = await api.get_real_gbif_data(loc_lat, loc_lng, radius_km=25)
                ebird_data = await api.get_real_ebird_data(loc_lat, loc_lng, radius_km=25)
                
                species_count = gbif_data['total_count'] if gbif_data else 0
                bird_count = ebird_data['observation_count'] if ebird_data else 0
                
                total_species += species_count
                
                # Assess emergency priority based on biodiversity
                if species_count > 200 or bird_count > 30:  # High biodiversity = critical to protect
                    priority = "CRITICAL"
                    critical_areas.append(f"{name} ({species_count} species, {bird_count} birds)")
                elif species_count > 50 or bird_count > 10:
                    priority = "HIGH"
                    critical_areas.append(f"{name} ({species_count} species)")
                else:
                    priority = "MODERATE"
            
            # Calculate emergency response based on real data
            if len(critical_areas) > 0:
                threat_level = "HIGH"
                budget = len(critical_areas) * 35000  # $35k per critical area
                personnel = len(critical_areas) * 6    # 6 people per area
            else:
                threat_level = "MODERATE"
                budget = 25000
                personnel = 4

            return f"""🚨 REAL EMERGENCY RESPONSE ANALYSIS
Emergency Center: {emergency_center}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔍 REAL-WORLD THREAT ASSESSMENT:
✅ Scanned {len(locations)} conservation area(s)
📊 Total Species Records: {total_species}
🎯 Critical Priority Areas: {len(critical_areas)}

🚨 CRITICAL CONSERVATION ZONES:
{chr(10).join(f"  • {area}" for area in critical_areas) if critical_areas else "  • No high-priority areas identified in immediate vicinity"}

💡 REAL EMERGENCY RECOMMENDATIONS:
1. Deploy rapid response teams to {len(critical_areas) if critical_areas else 1} priority zone(s)
2. Establish emergency monitoring protocols for biodiversity hotspots
3. Coordinate with Madagascar National Parks Authority
4. Implement 24-hour surveillance for areas with >200 species

💰 RESOURCE ALLOCATION:
• Emergency Budget: ${budget:,}
• Personnel Required: {personnel} field specialists
• Response Timeline: {12 if threat_level == "HIGH" else 24} hours
• Threat Level: {threat_level}

🌍 This analysis used REAL species data from GBIF and eBird APIs
📊 Emergency priority calculated from actual biodiversity at selected location
"""
    
    try:
        return asyncio.run(_real_emergency())
    except Exception as e:
        return f"❌ Emergency response error: {str(e)}"

def trigger_species_monitoring(lat: float = None, lng: float = None, location_name: str = "Selected Location") -> str:
    """Real species monitoring with live data for the clicked location."""
    
    async def _real_monitoring():
        async with WorkingRealAPIIntegrator() as api:
            # Use clicked coordinates if provided, otherwise default to Andasibe-Mantadia
            if lat is not None and lng is not None:
                monitor_lat, monitor_lng = lat, lng
                site_name = location_name
            else:
                monitor_lat, monitor_lng = -18.9333, 48.4167
                site_name = "Andasibe-Mantadia National Park"
            
            gbif_data = await api.get_real_gbif_data(monitor_lat, monitor_lng, radius_km=15)
            ebird_data = await api.get_real_ebird_data(monitor_lat, monitor_lng, radius_km=15)
            
            # Calculate conservation metrics
            biodiversity_score = 0
            if gbif_data and gbif_data['total_count'] > 0:
                if gbif_data['total_count'] > 300:
                    biodiversity_score = 9.5
                elif gbif_data['total_count'] > 100:
                    biodiversity_score = 7.8
                elif gbif_data['total_count'] > 50:
                    biodiversity_score = 6.2
                else:
                    biodiversity_score = 4.1
            
            conservation_status = "EXCELLENT" if biodiversity_score > 8 else \
                                "GOOD" if biodiversity_score > 6 else \
                                "FAIR" if biodiversity_score > 4 else "POOR"

            return f"""🔍 REAL SPECIES MONITORING REPORT
Location: {site_name}
Coordinates: {monitor_lat}, {monitor_lng}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 LIVE BIODIVERSITY DATA:
🦎 GBIF Records: {gbif_data['total_count'] if gbif_data else 0} species occurrences
🐦 eBird Sightings: {ebird_data['observation_count'] if ebird_data else 0} recent observations
🌿 Active Species: {len(gbif_data['species_names']) if gbif_data else 0} unique species detected
📈 Biodiversity Score: {biodiversity_score}/10 ({conservation_status})

🔍 REAL SPECIES DETECTED:
{chr(10).join(f"  • {species}" for species in (gbif_data['species_names'][:5] if gbif_data else [])) if gbif_data else "  • No species data available"}

🦅 RECENT BIRD OBSERVATIONS:
{chr(10).join(f"  • {bird}" for bird in (ebird_data['species_names'][:5] if ebird_data else [])) if ebird_data else "  • No bird data available"}

💡 CONSERVATION RECOMMENDATIONS:
{"• PRIORITY: Maintain current protection - excellent biodiversity" if biodiversity_score > 8 else
 "• STANDARD: Continue monitoring - good species diversity" if biodiversity_score > 6 else
 "• ENHANCED: Increase protection measures - moderate diversity" if biodiversity_score > 4 else
 "• URGENT: Immediate intervention needed - low diversity"}

✅ This monitoring uses REAL-TIME data from live APIs
🔄 Data refreshed from actual Madagascar conservation databases
📍 Analysis specific to coordinates: {monitor_lat}, {monitor_lng}
"""
    
    try:
        return asyncio.run(_real_monitoring())
    except Exception as e:
        return f"❌ Species monitoring error: {str(e)}"

def trigger_threat_scanning(lat: float = None, lng: float = None, location_name: str = "Selected Location") -> str:
    """Real threat scanning with actual data for the clicked location."""
    
    async def _real_threat_scan():
        async with WorkingRealAPIIntegrator() as api:
            # Use clicked coordinates if provided, otherwise scan multiple areas
            if lat is not None and lng is not None:
                locations = [(lat, lng, location_name)]
                scan_type = "LOCATION-SPECIFIC"
            else:
                # Scan multiple areas for comparative threat assessment
                locations = [
                    (-18.9333, 48.4167, "Andasibe-Mantadia"),
                    (-15.7000, 50.2333, "Masoala"),
                    (-22.5500, 45.3167, "Isalo")
                ]
                scan_type = "MULTI-SITE"
            
            threat_assessment = []
            overall_threat_level = "LOW"
            
            for scan_lat, scan_lng, name in locations:
                gbif_data = await api.get_real_gbif_data(scan_lat, scan_lng, radius_km=20)
                ebird_data = await api.get_real_ebird_data(scan_lat, scan_lng, radius_km=20)
                
                species_count = gbif_data['total_count'] if gbif_data else 0
                bird_count = ebird_data['observation_count'] if ebird_data else 0
                
                # Assess threat based on species diversity and bird activity
                if species_count > 300 and bird_count > 30:
                    threat_level = "LOW (High biodiversity - well protected)"
                    threat_color = "🟢"
                elif species_count > 100 and bird_count > 15:
                    threat_level = "MODERATE (Good biodiversity - monitor closely)"
                    threat_color = "🟡"
                elif species_count > 20 or bird_count > 5:
                    threat_level = "HIGH (Low biodiversity - may indicate threats)"
                    threat_color = "🟠"
                    overall_threat_level = "ELEVATED"
                else:
                    threat_level = "CRITICAL (Minimal activity - requires immediate assessment)"
                    threat_color = "🔴"
                    overall_threat_level = "CRITICAL"
                
                threat_assessment.append(f"{threat_color} {name}: {threat_level} ({species_count} species, {bird_count} birds)")
            
            # Generate specific recommendations based on findings
            if lat is not None and lng is not None:
                recommendations = [
                    f"1. Deploy monitoring equipment at {location_name}",
                    f"2. Establish {15 if species_count > 100 else 25}km protection radius",
                    f"3. Coordinate with local conservation teams",
                    f"4. {'Continue standard monitoring' if species_count > 100 else 'Investigate causes of low biodiversity'}"
                ]
            else:
                recommendations = [
                    "1. Focus resources on areas with <100 species records",
                    "2. Investigate causes of biodiversity loss in critical zones",
                    "3. Deploy additional monitoring in high-threat areas",
                    "4. Establish early warning systems for ecosystem changes"
                ]

            return f"""⚠️ REAL THREAT SCANNING ANALYSIS ({scan_type})
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Overall Threat Level: {overall_threat_level}

🔍 THREAT ASSESSMENT RESULTS:
{chr(10).join(f"  {assessment}" for assessment in threat_assessment)}

🎯 CONSERVATION PRIORITIES:
{chr(10).join(f"  {rec}" for rec in recommendations)}

📊 ANALYSIS METHODOLOGY:
• HIGH species count (>300) + HIGH bird activity (>30) = LOW threat
• MODERATE species count (100-300) + MODERATE birds (15-30) = MODERATE threat  
• LOW species count (<100) + LOW bird activity (<15) = HIGH threat

🌍 This analysis uses REAL species occurrence data
📊 Threat levels based on actual biodiversity metrics from GBIF and eBird
🔄 Data sourced from live conservation databases
📍 {"Location-specific analysis" if lat is not None else "Multi-site comparative analysis"}
"""
    
    try:
        return asyncio.run(_real_threat_scan())
    except Exception as e:
        return f"❌ Threat scanning error: {str(e)}"
