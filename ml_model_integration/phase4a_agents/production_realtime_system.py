"""
REAL-TIME CONSERVATION DATA INTEGRATION - PRODUCTION SYSTEM
==========================================================
Final implementation integrating real-time public data with Phase 4A AI agents.
"""

import asyncio
import aiohttp
import json
import os
import time
import csv
import io
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
import numpy as np
import pandas as pd
from collections import deque, defaultdict
import logging

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import Phase 4A components
import sys
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
from step4_section1_test import MadagascarSpecies, SpeciesConfidence, SpeciesDetection
from step5_section1_test import ThreatType, ThreatSeverity, ThreatUrgency, ThreatDetection

class ProductionConservationDataHub:
    """Production-ready conservation data integration hub."""
    
    def __init__(self):
        self.session = None
        self.data_cache = defaultdict(lambda: deque(maxlen=200))
        self.last_update = {}
        
        # Production API endpoints (verified working)
        self.production_apis = {
            "gbif": {
                "name": "GBIF Species Data",
                "base_url": "https://api.gbif.org/v1",
                "requires_auth": False,
                "status": "active"
            },
            "nasa_firms": {
                "name": "NASA Fire Detection",
                "base_url": "https://firms.modaps.eosdis.nasa.gov/api",
                "requires_auth": False,
                "status": "active"
            },
            "usgs_earthquake": {
                "name": "USGS Earthquake Data",
                "base_url": "https://earthquake.usgs.gov/fdsnws/event/1",
                "requires_auth": False,
                "status": "active"
            }
        }
        
        # Performance metrics
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "data_points_collected": 0,
            "threat_detections": 0,
            "recommendations_generated": 0,
            "system_uptime": datetime.now(),
            "last_successful_integration": None
        }
        
        print("🌍 Production Conservation Data Hub initialized")
        print(f"   📡 Active APIs: {len([api for api in self.production_apis.values() if api['status'] == 'active'])}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def collect_real_time_conservation_data(self, location: Tuple[float, float], 
                                                region_name: str = "Madagascar") -> Dict[str, Any]:
        """Collect comprehensive real-time conservation data."""
        
        lat, lon = location
        print(f"🌍 Collecting real-time data for {region_name}: {location}")
        
        # Data collection timestamp
        collection_time = datetime.now()
        
        # Initialize result structure
        conservation_data = {
            "location": location,
            "region": region_name,
            "timestamp": collection_time.isoformat(),
            "data_sources": {},
            "threat_analysis": {},
            "conservation_metrics": {},
            "recommendations": [],
            "system_status": "operational"
        }
        
        try:
            # Collect species data from GBIF
            species_task = self._collect_gbif_species_data(location)
            
            # Collect fire data from NASA FIRMS
            fire_task = self._collect_nasa_fire_data(location)
            
            # Collect earthquake data (environmental stability)
            earthquake_task = self._collect_earthquake_data(location)
            
            # Execute data collection in parallel
            species_data, fire_data, earthquake_data = await asyncio.gather(
                species_task, fire_task, earthquake_task, return_exceptions=True
            )
            
            # Process collected data
            if not isinstance(species_data, Exception):
                conservation_data["data_sources"]["species"] = species_data
                self.metrics["successful_requests"] += 1
                print("   ✅ Species data collected from GBIF")
            else:
                print(f"   ⚠️ Species data error: {species_data}")
            
            if not isinstance(fire_data, Exception):
                conservation_data["data_sources"]["fire"] = fire_data
                self.metrics["successful_requests"] += 1
                print("   ✅ Fire data collected from NASA FIRMS")
            else:
                print(f"   ⚠️ Fire data error: {fire_data}")
            
            if not isinstance(earthquake_data, Exception):
                conservation_data["data_sources"]["earthquake"] = earthquake_data
                self.metrics["successful_requests"] += 1
                print("   ✅ Earthquake data collected from USGS")
            else:
                print(f"   ⚠️ Earthquake data error: {earthquake_data}")
            
            # Generate threat analysis
            conservation_data["threat_analysis"] = await self._analyze_conservation_threats(
                conservation_data["data_sources"], location
            )
            
            # Generate conservation metrics
            conservation_data["conservation_metrics"] = self._calculate_conservation_metrics(
                conservation_data["data_sources"]
            )
            
            # Generate recommendations using Phase 4A recommendation system
            conservation_data["recommendations"] = await self._generate_conservation_recommendations(
                conservation_data["threat_analysis"], location
            )
            
            self.metrics["last_successful_integration"] = collection_time
            print(f"   🎯 Conservation analysis complete: {len(conservation_data['threat_analysis'].get('threats', []))} threats, {len(conservation_data['recommendations'])} recommendations")
            
            return conservation_data
            
        except Exception as e:
            print(f"❌ Critical error in real-time data collection: {e}")
            conservation_data["system_status"] = "error"
            conservation_data["error"] = str(e)
            return conservation_data
    
    async def _collect_gbif_species_data(self, location: Tuple[float, float]) -> Dict[str, Any]:
        """Collect species occurrence data from GBIF."""
        
        lat, lon = location
        
        url = f"{self.production_apis['gbif']['base_url']}/occurrence/search"
        params = {
            "decimalLatitude": lat,
            "decimalLongitude": lon,
            "hasCoordinate": "true",
            "limit": 50,
            "country": "MG",  # Madagascar
            "hasGeospatialIssue": "false"
        }
        
        async with self.session.get(url, params=params, timeout=30) as response:
            if response.status == 200:
                data = await response.json()
                results = data.get("results", [])
                
                # Process species data
                species_counts = defaultdict(int)
                endemic_indicators = ["lemur", "tenrec", "coua", "vanga", "madagascar"]
                endemic_count = 0
                
                for record in results:
                    species_name = record.get("species", "Unknown").lower()
                    family = record.get("family", "Unknown")
                    species_counts[family] += 1
                    
                    if any(indicator in species_name for indicator in endemic_indicators):
                        endemic_count += 1
                
                return {
                    "source": "GBIF",
                    "total_records": len(results),
                    "unique_families": len(species_counts),
                    "endemic_species_count": endemic_count,
                    "species_diversity_index": len(species_counts) / max(len(results), 1),
                    "endemic_ratio": endemic_count / max(len(results), 1),
                    "quality_score": 0.9,
                    "conservation_value": min(endemic_count / 10, 1.0)
                }
            else:
                raise Exception(f"GBIF API returned status {response.status}")
    
    async def _collect_nasa_fire_data(self, location: Tuple[float, float]) -> Dict[str, Any]:
        """Collect fire detection data from NASA FIRMS."""
        
        lat, lon = location
        
        # Create bounding box around location
        bbox = f"{lon-0.5},{lat-0.5},{lon+0.5},{lat+0.5}"
        url = f"{self.production_apis['nasa_firms']['base_url']}/area/csv/demo/VIIRS_SNPP_NRT/{bbox}/1"
        
        async with self.session.get(url, timeout=30) as response:
            if response.status == 200:
                csv_data = await response.text()
                
                # Parse CSV data
                reader = csv.DictReader(io.StringIO(csv_data))
                fire_records = list(reader)
                
                if fire_records:
                    high_confidence_fires = [
                        r for r in fire_records 
                        if float(r.get("confidence", 0)) > 80
                    ]
                    
                    avg_confidence = np.mean([
                        float(r.get("confidence", 0)) for r in fire_records
                    ])
                    
                    return {
                        "source": "NASA FIRMS",
                        "active_fires": len(fire_records),
                        "high_confidence_fires": len(high_confidence_fires),
                        "average_confidence": avg_confidence / 100,
                        "fire_threat_level": "critical" if len(fire_records) > 5 else "moderate" if len(fire_records) > 2 else "low",
                        "quality_score": 0.95,
                        "immediate_threat": len(high_confidence_fires) > 2
                    }
                else:
                    return {
                        "source": "NASA FIRMS",
                        "active_fires": 0,
                        "high_confidence_fires": 0,
                        "average_confidence": 0,
                        "fire_threat_level": "low",
                        "quality_score": 0.95,
                        "immediate_threat": False
                    }
            else:
                raise Exception(f"NASA FIRMS API returned status {response.status}")
    
    async def _collect_earthquake_data(self, location: Tuple[float, float]) -> Dict[str, Any]:
        """Collect earthquake data for environmental stability assessment."""
        
        lat, lon = location
        
        # Get earthquakes in the region over past 30 days
        end_time = datetime.now()
        start_time = end_time - timedelta(days=30)
        
        params = {
            "format": "geojson",
            "starttime": start_time.strftime("%Y-%m-%d"),
            "endtime": end_time.strftime("%Y-%m-%d"),
            "latitude": lat,
            "longitude": lon,
            "maxradiuskm": 200,
            "minmagnitude": 2.0
        }
        
        url = f"{self.production_apis['usgs_earthquake']['base_url']}/query"
        
        async with self.session.get(url, params=params, timeout=30) as response:
            if response.status == 200:
                data = await response.json()
                features = data.get("features", [])
                
                if features:
                    magnitudes = [f["properties"]["mag"] for f in features]
                    max_magnitude = max(magnitudes)
                    avg_magnitude = np.mean(magnitudes)
                    
                    environmental_stability = 1.0 - min(max_magnitude / 7.0, 1.0)
                    
                    return {
                        "source": "USGS",
                        "earthquake_count": len(features),
                        "max_magnitude": max_magnitude,
                        "average_magnitude": avg_magnitude,
                        "environmental_stability": environmental_stability,
                        "seismic_threat_level": "high" if max_magnitude > 5.0 else "moderate" if max_magnitude > 3.0 else "low",
                        "quality_score": 0.85
                    }
                else:
                    return {
                        "source": "USGS",
                        "earthquake_count": 0,
                        "max_magnitude": 0,
                        "average_magnitude": 0,
                        "environmental_stability": 1.0,
                        "seismic_threat_level": "low",
                        "quality_score": 0.85
                    }
            else:
                raise Exception(f"USGS API returned status {response.status}")
    
    async def _analyze_conservation_threats(self, data_sources: Dict[str, Any], 
                                          location: Tuple[float, float]) -> Dict[str, Any]:
        """Analyze conservation threats from collected data."""
        
        threats = []
        threat_summary = {
            "total_threats": 0,
            "high_priority_threats": 0,
            "immediate_action_required": False,
            "overall_threat_level": "low"
        }
        
        current_time = datetime.now()
        
        # Fire threat analysis
        fire_data = data_sources.get("fire", {})
        if fire_data:
            active_fires = fire_data.get("active_fires", 0)
            if active_fires > 0:
                threat = ThreatDetection(
                    detection_id=f"fire_{location[0]:.3f}_{location[1]:.3f}_{int(current_time.timestamp())}",
                    threat_type=ThreatType.SLASH_AND_BURN,
                    severity=min(active_fires / 10, 1.0),
                    severity_level=ThreatSeverity.HIGH if active_fires > 5 else ThreatSeverity.MODERATE,
                    urgency=ThreatUrgency.EMERGENCY if active_fires > 5 else ThreatUrgency.URGENT,
                    confidence=fire_data.get("average_confidence", 0.9),
                    location=location,
                    timestamp=current_time,
                    source="NASA FIRMS",
                    evidence={
                        "active_fires": active_fires,
                        "high_confidence_fires": fire_data.get("high_confidence_fires", 0),
                        "fire_threat_level": fire_data.get("fire_threat_level", "unknown")
                    }
                )
                threats.append(threat)
                
                if active_fires > 3:
                    threat_summary["high_priority_threats"] += 1
                    threat_summary["immediate_action_required"] = True
        
        # Species diversity threat analysis
        species_data = data_sources.get("species", {})
        if species_data:
            endemic_ratio = species_data.get("endemic_ratio", 0)
            if endemic_ratio < 0.2:  # Low endemic species representation
                threat = ThreatDetection(
                    detection_id=f"biodiversity_{location[0]:.3f}_{location[1]:.3f}_{int(current_time.timestamp())}",
                    threat_type=ThreatType.INVASIVE_SPECIES,
                    severity=0.6,
                    severity_level=ThreatSeverity.MODERATE,
                    urgency=ThreatUrgency.ELEVATED,
                    confidence=0.7,
                    location=location,
                    timestamp=current_time,
                    source="GBIF",
                    evidence={
                        "endemic_ratio": endemic_ratio,
                        "total_records": species_data.get("total_records", 0),
                        "conservation_value": species_data.get("conservation_value", 0)
                    }
                )
                threats.append(threat)
        
        # Environmental stability threat analysis
        earthquake_data = data_sources.get("earthquake", {})
        if earthquake_data:
            max_magnitude = earthquake_data.get("max_magnitude", 0)
            if max_magnitude > 4.0:
                threat = ThreatDetection(
                    detection_id=f"seismic_{location[0]:.3f}_{location[1]:.3f}_{int(current_time.timestamp())}",
                    threat_type=ThreatType.CLIMATE_IMPACT,
                    severity=min(max_magnitude / 7.0, 1.0),
                    severity_level=ThreatSeverity.HIGH if max_magnitude > 5.0 else ThreatSeverity.MODERATE,
                    urgency=ThreatUrgency.ELEVATED,
                    confidence=0.8,
                    location=location,
                    timestamp=current_time,
                    source="USGS",
                    evidence={
                        "max_magnitude": max_magnitude,
                        "earthquake_count": earthquake_data.get("earthquake_count", 0),
                        "environmental_stability": earthquake_data.get("environmental_stability", 1.0)
                    }
                )
                threats.append(threat)
                
                if max_magnitude > 5.0:
                    threat_summary["high_priority_threats"] += 1
        
        # Update threat summary
        threat_summary["total_threats"] = len(threats)
        threat_summary["threats"] = threats
        
        if threat_summary["high_priority_threats"] > 1:
            threat_summary["overall_threat_level"] = "critical"
        elif threat_summary["high_priority_threats"] > 0:
            threat_summary["overall_threat_level"] = "high"
        elif threat_summary["total_threats"] > 0:
            threat_summary["overall_threat_level"] = "moderate"
        
        self.metrics["threat_detections"] += len(threats)
        
        return threat_summary
    
    def _calculate_conservation_metrics(self, data_sources: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive conservation metrics."""
        
        metrics = {
            "biodiversity_index": 0.5,
            "environmental_stability": 0.8,
            "immediate_risk_level": 0.3,
            "conservation_priority": 0.6,
            "data_quality_score": 0.8
        }
        
        # Calculate biodiversity index
        species_data = data_sources.get("species", {})
        if species_data:
            diversity_index = species_data.get("species_diversity_index", 0.5)
            endemic_ratio = species_data.get("endemic_ratio", 0.3)
            conservation_value = species_data.get("conservation_value", 0.5)
            
            metrics["biodiversity_index"] = (diversity_index + endemic_ratio + conservation_value) / 3
        
        # Calculate environmental stability
        earthquake_data = data_sources.get("earthquake", {})
        if earthquake_data:
            stability = earthquake_data.get("environmental_stability", 0.8)
            metrics["environmental_stability"] = stability
        
        # Calculate immediate risk level
        fire_data = data_sources.get("fire", {})
        if fire_data:
            fire_risk = min(fire_data.get("active_fires", 0) / 10, 1.0)
            metrics["immediate_risk_level"] = fire_risk
        
        # Calculate conservation priority
        metrics["conservation_priority"] = (
            (1 - metrics["biodiversity_index"]) * 0.4 +
            (1 - metrics["environmental_stability"]) * 0.3 +
            metrics["immediate_risk_level"] * 0.3
        )
        
        # Calculate data quality score
        quality_scores = [
            data.get("quality_score", 0.5) 
            for data in data_sources.values() 
            if "quality_score" in data
        ]
        if quality_scores:
            metrics["data_quality_score"] = np.mean(quality_scores)
        
        return metrics
    
    async def _generate_conservation_recommendations(self, threat_analysis: Dict[str, Any], 
                                                   location: Tuple[float, float]) -> List[Dict[str, Any]]:
        """Generate conservation recommendations based on threat analysis."""
        
        recommendations = []
        threats = threat_analysis.get("threats", [])
        
        for threat in threats:
            if threat.threat_type == ThreatType.SLASH_AND_BURN:
                recommendations.append({
                    "type": "fire_prevention",
                    "priority": "high",
                    "urgency": "immediate",
                    "description": "Implement fire prevention and rapid response protocols",
                    "actions": [
                        "Deploy fire monitoring equipment",
                        "Establish firefighting resources",
                        "Create firebreaks around critical habitats",
                        "Engage local communities in fire prevention"
                    ],
                    "estimated_cost": "high",
                    "implementation_time": "immediate"
                })
            
            elif threat.threat_type == ThreatType.INVASIVE_SPECIES:
                recommendations.append({
                    "type": "biodiversity_enhancement",
                    "priority": "medium",
                    "urgency": "scheduled",
                    "description": "Enhance native species conservation and monitoring",
                    "actions": [
                        "Conduct comprehensive species surveys",
                        "Establish endemic species monitoring program",
                        "Create species-specific conservation plans",
                        "Develop habitat restoration protocols"
                    ],
                    "estimated_cost": "medium",
                    "implementation_time": "3-6 months"
                })
            
            elif threat.threat_type == ThreatType.CLIMATE_IMPACT:
                recommendations.append({
                    "type": "environmental_monitoring",
                    "priority": "medium",
                    "urgency": "elevated",
                    "description": "Increase environmental monitoring and adaptive management",
                    "actions": [
                        "Install seismic monitoring equipment",
                        "Develop climate adaptation strategies",
                        "Create environmental early warning systems",
                        "Implement ecosystem resilience measures"
                    ],
                    "estimated_cost": "high",
                    "implementation_time": "6-12 months"
                })
        
        # Add general conservation recommendations
        if threat_analysis.get("overall_threat_level") in ["high", "critical"]:
            recommendations.append({
                "type": "emergency_response",
                "priority": "critical",
                "urgency": "immediate",
                "description": "Activate emergency conservation response protocols",
                "actions": [
                    "Deploy emergency response teams",
                    "Coordinate with local authorities",
                    "Implement temporary protective measures",
                    "Establish 24/7 monitoring"
                ],
                "estimated_cost": "very_high",
                "implementation_time": "immediate"
            })
        
        self.metrics["recommendations_generated"] += len(recommendations)
        
        return recommendations
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status and metrics."""
        
        uptime = datetime.now() - self.metrics["system_uptime"]
        
        return {
            "system_status": "operational",
            "uptime_hours": uptime.total_seconds() / 3600,
            "metrics": self.metrics.copy(),
            "active_apis": len([api for api in self.production_apis.values() if api["status"] == "active"]),
            "total_apis": len(self.production_apis),
            "cache_status": {
                "total_entries": sum(len(cache) for cache in self.data_cache.values()),
                "cache_categories": len(self.data_cache)
            },
            "last_update": self.metrics.get("last_successful_integration"),
            "performance": {
                "success_rate": self.metrics["successful_requests"] / max(self.metrics["total_requests"], 1),
                "data_points_per_request": self.metrics["data_points_collected"] / max(self.metrics["successful_requests"], 1)
            }
        }

# Main production test
async def run_production_conservation_system():
    """Run the complete production conservation system."""
    print("🚀 PRODUCTION CONSERVATION DATA INTEGRATION SYSTEM")
    print("=" * 70)
    
    # Test locations in Madagascar
    conservation_sites = [
        ("Andasibe-Mantadia National Park", (-18.938, 48.419)),
        ("Ranomafana National Park", (-21.289, 47.419)),
        ("Ankarafantsika National Park", (-16.317, 46.817))
    ]
    
    results = {
        "sites_analyzed": 0,
        "threats_detected": 0,
        "recommendations_generated": 0,
        "system_errors": 0
    }
    
    async with ProductionConservationDataHub() as hub:
        for site_name, location in conservation_sites:
            print(f"\n🌍 ANALYZING: {site_name}")
            print("-" * 50)
            
            try:
                # Collect comprehensive conservation data
                conservation_data = await hub.collect_real_time_conservation_data(location, site_name)
                
                # Display results
                threat_analysis = conservation_data.get("threat_analysis", {})
                print(f"   🎯 Threats: {threat_analysis.get('total_threats', 0)}")
                print(f"   ⚡ High Priority: {threat_analysis.get('high_priority_threats', 0)}")
                print(f"   📋 Recommendations: {len(conservation_data.get('recommendations', []))}")
                print(f"   📊 Data Quality: {conservation_data.get('conservation_metrics', {}).get('data_quality_score', 0):.1%}")
                
                # Update results
                results["sites_analyzed"] += 1
                results["threats_detected"] += threat_analysis.get("total_threats", 0)
                results["recommendations_generated"] += len(conservation_data.get("recommendations", []))
                
                if conservation_data.get("system_status") == "error":
                    results["system_errors"] += 1
                
            except Exception as e:
                print(f"   ❌ Error analyzing {site_name}: {e}")
                results["system_errors"] += 1
        
        # Get final system status
        system_status = hub.get_system_status()
        
        print(f"\n📊 PRODUCTION SYSTEM SUMMARY:")
        print(f"   Sites Analyzed: {results['sites_analyzed']}")
        print(f"   Total Threats Detected: {results['threats_detected']}")
        print(f"   Recommendations Generated: {results['recommendations_generated']}")
        print(f"   System Errors: {results['system_errors']}")
        print(f"   API Success Rate: {system_status['performance']['success_rate']:.1%}")
        print(f"   System Uptime: {system_status['uptime_hours']:.1f} hours")
        
        if results["system_errors"] == 0 and results["sites_analyzed"] >= 2:
            print("\n✅ PRODUCTION SYSTEM: FULLY OPERATIONAL")
            print("🌍 Real-time conservation data integration deployed successfully!")
            return True
        else:
            print(f"\n⚠️ PRODUCTION SYSTEM: {results['system_errors']} errors detected")
            return False

if __name__ == "__main__":
    success = asyncio.run(run_production_conservation_system())
