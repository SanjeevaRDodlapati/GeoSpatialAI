"""
Step 4 Section 4: Field Deployment Integration
==============================================
Final integration with previous conservation systems for Madagascar field deployment.
"""

import sys
import os
import json
import time
import asyncio
import numpy as np
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import requests
import aiohttp
from PIL import Image

# Import from previous sections
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
from step4_section1_test import SpeciesConfidence, MadagascarSpecies, SpeciesDetection
from step4_section2_test import EnsembleSpeciesClassifier
from step4_section3_test import OptimizedSpeciesDetector, RealTimeSpeciesMonitor

# Import from previous conservation systems
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
try:
    from step2_section4_test import ConservationMemoryStore
    from step3_section4_test import ConservationReasoner, ConservationEvent, EventType, ThreatLevel
except ImportError:
    print("⚠️  Previous conservation systems not available - using mock implementations")
    
    class ConservationMemoryStore:
        def __init__(self):
            self.events = []
        
        def store_event(self, event):
            self.events.append(event)
        
        def get_relevant_events(self, query, limit=5):
            return self.events[-limit:]
    
    @dataclass
    class ConservationEvent:
        event_id: str
        event_type: str
        species: str
        location: str
        timestamp: datetime
        confidence: float
        threat_level: str = "low"
        metadata: Dict[str, Any] = None

@dataclass
class FieldDeploymentConfig:
    """Configuration for Madagascar field deployment."""
    site_name: str
    site_coordinates: Tuple[float, float]  # (latitude, longitude)
    research_station: str
    deployment_date: datetime
    camera_trap_id: str
    detection_threshold: float = 0.7
    alert_threshold: float = 0.8
    species_of_interest: List[MadagascarSpecies] = None
    conservation_priority: str = "high"
    
    def __post_init__(self):
        if self.species_of_interest is None:
            # Default high-priority Madagascar species
            self.species_of_interest = [
                MadagascarSpecies.INDRI_INDRI,          # Critically endangered
                MadagascarSpecies.PROPITHECUS_DIADEMA,  # Critically endangered  
                MadagascarSpecies.MICROCEBUS_MURINUS,   # Vulnerable
                MadagascarSpecies.BROOKESIA_MICRA       # Near threatened
            ]

class MadagascarFieldAgent:
    """Integrated field deployment agent for Madagascar conservation."""
    
    def __init__(self, config: FieldDeploymentConfig):
        self.config = config
        self.detector = None
        self.monitor = None
        self.memory_store = ConservationMemoryStore()
        self.reasoner = None
        self.deployment_stats = {
            "total_detections": 0,
            "high_priority_detections": 0,
            "conservation_alerts": 0,
            "deployment_start": datetime.utcnow(),
            "last_activity": datetime.utcnow()
        }
        
        print(f"🌿 Madagascar Field Agent initialized for {config.site_name}")
        print(f"📍 Location: {config.site_coordinates}")
        print(f"🏢 Research Station: {config.research_station}")
    
    async def initialize_systems(self):
        """Initialize all integrated systems."""
        try:
            print("🔄 Initializing integrated conservation systems...")
            
            # Initialize species detector
            self.detector = OptimizedSpeciesDetector(
                model_type="ensemble", 
                enable_gpu=False  # Field deployment typically CPU-only
            )
            
            if not self.detector.initialize_model():
                raise RuntimeError("Failed to initialize species detector")
            
            print("✅ Species detector initialized")
            
            # Initialize real-time monitor
            self.monitor = RealTimeSpeciesMonitor(self.detector, max_queue_size=50)
            self.monitor.start_monitoring()
            print("✅ Real-time monitoring started")
            
            # Initialize conservation reasoner
            try:
                self.reasoner = ConservationReasoner(self.memory_store)
                print("✅ Conservation reasoner initialized")
            except:
                print("⚠️  Using basic conservation logic (reasoner not available)")
            
            # Test system integration
            await self._test_system_integration()
            print("✅ System integration verified")
            
            return True
            
        except Exception as e:
            print(f"❌ System initialization error: {e}")
            return False
    
    async def _test_system_integration(self):
        """Test integration between all systems."""
        # Create test detection event
        test_detection = SpeciesDetection(
            detection_id="integration_test",
            species=MadagascarSpecies.INDRI_INDRI,
            confidence=0.95,
            confidence_level=SpeciesConfidence.VERY_HIGH,
            source="integration_test",
            metadata={"test": True}
        )
        
        # Process through conservation pipeline
        await self.process_detection(test_detection)
        print("✅ Integration test completed")
    
    async def process_detection(self, detection: SpeciesDetection) -> Dict[str, Any]:
        """Process species detection through full conservation pipeline."""
        try:
            processing_start = time.time()
            
            # Update deployment stats
            self.deployment_stats["total_detections"] += 1
            self.deployment_stats["last_activity"] = datetime.utcnow()
            
            # Check if species is of conservation interest
            conservation_priority = self._assess_conservation_priority(detection)
            
            if conservation_priority["is_priority"]:
                self.deployment_stats["high_priority_detections"] += 1
            
            # Create conservation event
            conservation_event = ConservationEvent(
                event_id=f"field_{detection.detection_id}",
                event_type="species_detection",
                species=detection.species.value,
                location=f"{self.config.site_name}_{self.config.camera_trap_id}",
                timestamp=detection.timestamp,
                confidence=detection.confidence,
                threat_level=conservation_priority["threat_level"],
                metadata={
                    "detection_metadata": detection.metadata,
                    "conservation_priority": conservation_priority,
                    "site_coordinates": self.config.site_coordinates,
                    "research_station": self.config.research_station
                }
            )
            
            # Store in conservation memory
            self.memory_store.store_event(conservation_event)
            
            # Process through conservation reasoner
            reasoning_result = None
            if self.reasoner:
                try:
                    reasoning_result = self.reasoner.process_event(conservation_event)
                except:
                    print("⚠️  Conservation reasoning unavailable")
            
            # Generate alerts if needed
            alerts = await self._generate_conservation_alerts(detection, conservation_priority)
            
            if alerts:
                self.deployment_stats["conservation_alerts"] += len(alerts)
            
            processing_time = (time.time() - processing_start) * 1000
            
            # Create comprehensive result
            result = {
                "detection": asdict(detection),
                "conservation_event": asdict(conservation_event),
                "conservation_priority": conservation_priority,
                "reasoning_result": reasoning_result,
                "alerts": alerts,
                "processing_time_ms": processing_time,
                "deployment_stats": self.deployment_stats.copy()
            }
            
            return result
            
        except Exception as e:
            print(f"⚠️  Detection processing error: {e}")
            return {"error": str(e), "detection_id": detection.detection_id}
    
    def _assess_conservation_priority(self, detection: SpeciesDetection) -> Dict[str, Any]:
        """Assess conservation priority of detected species."""
        # Conservation status mapping for Madagascar species
        conservation_status = {
            MadagascarSpecies.INDRI_INDRI: {"status": "critically_endangered", "priority": 10},
            MadagascarSpecies.PROPITHECUS_DIADEMA: {"status": "critically_endangered", "priority": 10},
            MadagascarSpecies.MICROCEBUS_MURINUS: {"status": "vulnerable", "priority": 7},
            MadagascarSpecies.BROOKESIA_MICRA: {"status": "near_threatened", "priority": 6},
            MadagascarSpecies.FURCIFER_PARDALIS: {"status": "least_concern", "priority": 4},
            MadagascarSpecies.LEMUR_CATTA: {"status": "endangered", "priority": 8},
            MadagascarSpecies.EULEMUR_FULVUS: {"status": "vulnerable", "priority": 7},
            MadagascarSpecies.UROPLATUS_PHANTASTICUS: {"status": "least_concern", "priority": 3},
            MadagascarSpecies.UNKNOWN_SPECIES: {"status": "unknown", "priority": 2}
        }
        
        species_info = conservation_status.get(detection.species, {"status": "unknown", "priority": 1})
        
        # Determine threat level based on confidence and conservation status
        if detection.confidence >= self.config.alert_threshold and species_info["priority"] >= 8:
            threat_level = "high"
        elif detection.confidence >= self.config.detection_threshold and species_info["priority"] >= 6:
            threat_level = "medium"
        else:
            threat_level = "low"
        
        is_priority = (
            detection.species in self.config.species_of_interest and 
            detection.confidence >= self.config.detection_threshold
        )
        
        return {
            "is_priority": is_priority,
            "conservation_status": species_info["status"],
            "priority_score": species_info["priority"],
            "threat_level": threat_level,
            "requires_immediate_attention": (
                threat_level == "high" and 
                detection.confidence >= self.config.alert_threshold
            ),
            "field_recommendations": self._generate_field_recommendations(detection.species, species_info)
        }
    
    def _generate_field_recommendations(self, species: MadagascarSpecies, species_info: Dict) -> List[str]:
        """Generate field-specific recommendations for detected species."""
        recommendations = []
        
        if species == MadagascarSpecies.INDRI_INDRI:
            recommendations.extend([
                "Document vocalization patterns if audio available",
                "Record GPS coordinates for territory mapping",
                "Note group size and composition",
                "Check for signs of habitat disturbance"
            ])
        elif species == MadagascarSpecies.PROPITHECUS_DIADEMA:
            recommendations.extend([
                "Monitor feeding behavior and tree species preference",
                "Document vertical forest usage patterns",
                "Record group dynamics and social interactions",
                "Assess canopy connectivity for movement corridors"
            ])
        elif species == MadagascarSpecies.BROOKESIA_MICRA:
            recommendations.extend([
                "Document microhabitat preferences",
                "Record temperature and humidity conditions",
                "Note vegetation structure at detection site",
                "Survey for other micro-chameleon species"
            ])
        elif species_info["priority"] >= 6:
            recommendations.extend([
                "Record behavioral observations",
                "Document habitat characteristics",
                "Note time of activity for behavioral patterns",
                "Check for human activity indicators nearby"
            ])
        
        # General Madagascar conservation recommendations
        recommendations.extend([
            "Update species occurrence database",
            "Coordinate with local conservation partners",
            "Document any threats or disturbances observed"
        ])
        
        return recommendations
    
    async def _generate_conservation_alerts(self, detection: SpeciesDetection, priority: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate conservation alerts for high-priority detections."""
        alerts = []
        
        if priority["requires_immediate_attention"]:
            alert = {
                "alert_id": f"alert_{detection.detection_id}",
                "alert_type": "high_priority_species_detection",
                "species": detection.species.value,
                "confidence": detection.confidence,
                "location": self.config.site_name,
                "coordinates": self.config.site_coordinates,
                "timestamp": detection.timestamp.isoformat(),
                "conservation_status": priority["conservation_status"],
                "recommended_actions": priority["field_recommendations"],
                "research_station": self.config.research_station,
                "camera_trap_id": self.config.camera_trap_id
            }
            alerts.append(alert)
        
        # Additional alerts based on patterns
        if detection.confidence >= 0.9 and detection.species != MadagascarSpecies.UNKNOWN_SPECIES:
            alert = {
                "alert_id": f"confidence_alert_{detection.detection_id}",
                "alert_type": "high_confidence_detection",
                "species": detection.species.value,
                "confidence": detection.confidence,
                "message": f"Very high confidence {detection.species.value} detection",
                "location": self.config.site_name,
                "coordinates": self.config.site_coordinates,
                "timestamp": detection.timestamp.isoformat(),
                "research_station": self.config.research_station,
                "camera_trap_id": self.config.camera_trap_id
            }
            alerts.append(alert)
        
        return alerts
    
    async def process_image_file(self, image_path: str) -> Dict[str, Any]:
        """Process a single image file through the complete pipeline."""
        try:
            print(f"📸 Processing image: {os.path.basename(image_path)}")
            
            # Add image to monitoring queue
            if not self.monitor.add_image(image_path):
                return {"error": "Failed to add image to processing queue"}
            
            # Wait for processing (with timeout)
            max_wait_time = 10  # seconds
            wait_start = time.time()
            
            while (time.time() - wait_start) < max_wait_time:
                results = self.monitor.get_results()
                
                # Find result for our image
                for detection in results:
                    if detection.image_path == image_path:
                        # Process through conservation pipeline
                        return await self.process_detection(detection)
                
                await asyncio.sleep(0.1)  # Brief pause
            
            return {"error": "Processing timeout", "image_path": image_path}
            
        except Exception as e:
            print(f"⚠️  Image processing error: {e}")
            return {"error": str(e), "image_path": image_path}
    
    async def batch_process_images(self, image_paths: List[str]) -> List[Dict[str, Any]]:
        """Process multiple images through the conservation pipeline."""
        results = []
        
        print(f"📸 Processing batch of {len(image_paths)} images...")
        
        # Add all images to monitoring queue
        for image_path in image_paths:
            self.monitor.add_image(image_path)
        
        # Wait for all results
        processed_count = 0
        max_wait_time = 30  # seconds for batch
        wait_start = time.time()
        
        while processed_count < len(image_paths) and (time.time() - wait_start) < max_wait_time:
            detections = self.monitor.get_results()
            
            for detection in detections:
                if detection.image_path in image_paths:
                    # Process through conservation pipeline
                    result = await self.process_detection(detection)
                    results.append(result)
                    processed_count += 1
            
            await asyncio.sleep(0.2)  # Brief pause
        
        print(f"✅ Batch processing complete: {processed_count}/{len(image_paths)} images processed")
        return results
    
    def get_deployment_summary(self) -> Dict[str, Any]:
        """Generate comprehensive deployment summary."""
        runtime = datetime.utcnow() - self.deployment_stats["deployment_start"]
        
        # Get recent events from memory
        recent_events = self.memory_store.get_relevant_events("recent activity", limit=10)
        
        # Performance metrics from detector
        performance_report = self.detector.get_performance_report() if self.detector else {}
        
        return {
            "deployment_info": {
                "site_name": self.config.site_name,
                "coordinates": self.config.site_coordinates,
                "research_station": self.config.research_station,
                "deployment_date": self.config.deployment_date.isoformat(),
                "runtime_hours": runtime.total_seconds() / 3600
            },
            "detection_statistics": self.deployment_stats.copy(),
            "performance_metrics": performance_report,
            "recent_activity": [asdict(event) for event in recent_events],
            "conservation_priorities": {
                "species_of_interest": [s.value for s in self.config.species_of_interest],
                "detection_threshold": self.config.detection_threshold,
                "alert_threshold": self.config.alert_threshold
            }
        }
    
    async def shutdown_systems(self):
        """Gracefully shutdown all systems."""
        print("🔄 Shutting down field deployment systems...")
        
        if self.monitor:
            self.monitor.stop_monitoring()
            print("✅ Monitoring system stopped")
        
        # Save final deployment summary
        summary = self.get_deployment_summary()
        
        # Create deployment logs directory if it doesn't exist
        deployment_dir = Path("deployment/logs")
        deployment_dir.mkdir(parents=True, exist_ok=True)
        
        # Save to deployment logs directory
        summary_file = deployment_dir / f"deployment_summary_{self.config.site_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"✅ Deployment summary saved: {summary_file}")
        print("🌿 Madagascar Field Agent shutdown complete")

async def test_field_deployment_config():
    """Test field deployment configuration."""
    print("🌍 Testing Field Deployment Config...")
    
    try:
        # Create Madagascar field deployment configuration
        config = FieldDeploymentConfig(
            site_name="Maromizaha_Reserve",
            site_coordinates=(-18.9667, 48.4500),  # Maromizaha coordinates
            research_station="Centre_ValBio",
            deployment_date=datetime.utcnow(),
            camera_trap_id="CAM_001",
            detection_threshold=0.75,
            alert_threshold=0.85,
            conservation_priority="critical"
        )
        
        print(f"✅ Site configured: {config.site_name}")
        print(f"✅ Coordinates: {config.site_coordinates}")
        print(f"✅ Species of interest: {len(config.species_of_interest)} species")
        print(f"✅ Detection threshold: {config.detection_threshold}")
        print(f"✅ Alert threshold: {config.alert_threshold}")
        
        # Verify species priorities
        priority_species = [species.value for species in config.species_of_interest]
        expected_priorities = ["indri_indri", "propithecus_diadema", "microcebus_murinus", "brookesia_micra"]
        
        for species in expected_priorities:
            if species in priority_species:
                print(f"✅ Priority species included: {species}")
            else:
                print(f"❌ Priority species missing: {species}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Field deployment config error: {e}")
        return False

async def test_madagascar_field_agent():
    """Test Madagascar field agent initialization and basic operations."""
    print("\n🇲🇬 Testing Madagascar Field Agent...")
    
    try:
        # Create configuration
        config = FieldDeploymentConfig(
            site_name="Andasibe_Mantadia",
            site_coordinates=(-18.9333, 48.4167),
            research_station="Centre_ValBio", 
            deployment_date=datetime.utcnow(),
            camera_trap_id="CAM_TEST_001"
        )
        
        # Initialize field agent
        agent = MadagascarFieldAgent(config)
        
        # Initialize systems
        if await agent.initialize_systems():
            print("✅ Field agent systems initialized")
        else:
            print("❌ Field agent initialization failed")
            return False
        
        # Test conservation priority assessment
        test_detection = SpeciesDetection(
            detection_id="test_field_001",
            species=MadagascarSpecies.INDRI_INDRI,
            confidence=0.92,
            confidence_level=SpeciesConfidence.VERY_HIGH,
            source="field_test"
        )
        
        priority = agent._assess_conservation_priority(test_detection)
        
        if priority["is_priority"] and priority["conservation_status"] == "critically_endangered":
            print("✅ Conservation priority assessment working")
        else:
            print("❌ Conservation priority assessment failed")
            return False
        
        # Test field recommendations
        recommendations = priority["field_recommendations"]
        if len(recommendations) >= 3:
            print(f"✅ Field recommendations generated: {len(recommendations)} items")
        else:
            print("❌ Insufficient field recommendations")
            return False
        
        # Test deployment summary
        summary = agent.get_deployment_summary()
        
        if ("deployment_info" in summary and 
            "detection_statistics" in summary and
            summary["deployment_info"]["site_name"] == config.site_name):
            print("✅ Deployment summary generated")
        else:
            print("❌ Deployment summary incomplete")
            return False
        
        # Shutdown systems
        await agent.shutdown_systems()
        
        return True
        
    except Exception as e:
        print(f"❌ Madagascar field agent error: {e}")
        return False

async def test_full_pipeline_integration():
    """Test complete pipeline from image to conservation action."""
    print("\n🔄 Testing Full Pipeline Integration...")
    
    try:
        # Create field configuration
        config = FieldDeploymentConfig(
            site_name="Masoala_National_Park",
            site_coordinates=(-15.7, 50.2),
            research_station="Masoala_Research_Station",
            deployment_date=datetime.utcnow(),
            camera_trap_id="CAM_PIPELINE_001"
        )
        
        # Initialize field agent
        agent = MadagascarFieldAgent(config)
        
        if not await agent.initialize_systems():
            print("❌ Pipeline initialization failed")
            return False
        
        # Create test images for different Madagascar species
        test_images = []
        species_tests = [
            ("indri", MadagascarSpecies.INDRI_INDRI),
            ("sifaka", MadagascarSpecies.PROPITHECUS_DIADEMA),
            ("mouse_lemur", MadagascarSpecies.MICROCEBUS_MURINUS),
            ("chameleon", MadagascarSpecies.BROOKESIA_MICRA)
        ]
        
        for species_name, species_enum in species_tests:
            image_path = f"test_pipeline_{species_name}.jpg"
            test_image = Image.new('RGB', (224, 224), color='green')
            test_image.save(image_path)
            test_images.append(image_path)
        
        print(f"✅ Created {len(test_images)} test images")
        
        # Process images through full pipeline
        results = await agent.batch_process_images(test_images)
        
        successful_results = [r for r in results if "error" not in r]
        print(f"✅ Pipeline processing: {len(successful_results)}/{len(test_images)} successful")
        
        # Verify pipeline components
        for result in successful_results:
            if ("detection" in result and 
                "conservation_event" in result and
                "conservation_priority" in result):
                print("✅ Complete pipeline data structure verified")
            else:
                print("❌ Incomplete pipeline result")
                return False
        
        # Check for high-priority detections
        high_priority_results = [r for r in successful_results 
                               if r.get("conservation_priority", {}).get("is_priority", False)]
        
        if high_priority_results:
            print(f"✅ High-priority detections: {len(high_priority_results)}")
        
        # Check for conservation alerts
        total_alerts = sum(len(r.get("alerts", [])) for r in successful_results)
        if total_alerts > 0:
            print(f"✅ Conservation alerts generated: {total_alerts}")
        
        # Verify deployment statistics
        final_summary = agent.get_deployment_summary()
        stats = final_summary["detection_statistics"]
        
        if stats["total_detections"] > 0:
            print(f"✅ Deployment statistics: {stats['total_detections']} total detections")
        
        # Cleanup
        for image_path in test_images:
            if os.path.exists(image_path):
                os.remove(image_path)
        
        await agent.shutdown_systems()
        
        # Check if summary file was created
        summary_files = [f for f in os.listdir('.') if f.startswith('deployment_summary_')]
        if summary_files:
            print(f"✅ Deployment summary saved: {summary_files[-1]}")
            # Cleanup summary file
            os.remove(summary_files[-1])
        
        return True
        
    except Exception as e:
        print(f"❌ Full pipeline integration error: {e}")
        return False

async def test_conservation_workflow():
    """Test conservation-specific workflow components."""
    print("\n🌿 Testing Conservation Workflow...")
    
    try:
        config = FieldDeploymentConfig(
            site_name="Ranomafana_National_Park",
            site_coordinates=(-21.25, 47.42),
            research_station="Centre_ValBio",
            deployment_date=datetime.utcnow(),
            camera_trap_id="CAM_CONSERVATION_001"
        )
        
        agent = MadagascarFieldAgent(config)
        
        # Test conservation priority assessment for all Madagascar species
        species_results = {}
        
        for species in MadagascarSpecies:
            test_detection = SpeciesDetection(
                detection_id=f"conservation_test_{species.value}",
                species=species,
                confidence=0.85,
                confidence_level=SpeciesConfidence.HIGH,
                source="conservation_workflow_test"
            )
            
            priority = agent._assess_conservation_priority(test_detection)
            species_results[species.value] = priority
            
            # Verify critical species are flagged as high priority
            if species in [MadagascarSpecies.INDRI_INDRI, MadagascarSpecies.PROPITHECUS_DIADEMA]:
                if priority["conservation_status"] == "critically_endangered":
                    print(f"✅ {species.value}: Correctly identified as critically endangered")
                else:
                    print(f"❌ {species.value}: Conservation status incorrect")
                    return False
        
        # Test alert generation
        high_confidence_detection = SpeciesDetection(
            detection_id="alert_test",
            species=MadagascarSpecies.INDRI_INDRI,
            confidence=0.95,
            confidence_level=SpeciesConfidence.VERY_HIGH,
            source="alert_test"
        )
        
        priority = agent._assess_conservation_priority(high_confidence_detection)
        alerts = await agent._generate_conservation_alerts(high_confidence_detection, priority)
        
        if len(alerts) >= 1:
            print(f"✅ Conservation alerts generated: {len(alerts)} alerts")
            
            # Check alert structure
            for alert in alerts:
                required_fields = ["alert_id", "alert_type", "species", "confidence", "timestamp"]
                if all(field in alert for field in required_fields):
                    print("✅ Alert structure valid")
                else:
                    print("❌ Alert structure incomplete")
                    return False
        else:
            print("❌ No alerts generated for high-priority detection")
            return False
        
        # Test field recommendations
        all_recommendations = set()
        for species_result in species_results.values():
            all_recommendations.update(species_result["field_recommendations"])
        
        if len(all_recommendations) >= 10:  # Expect diverse recommendations
            print(f"✅ Field recommendations comprehensive: {len(all_recommendations)} unique recommendations")
        else:
            print("❌ Insufficient field recommendations diversity")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Conservation workflow error: {e}")
        return False

async def test_performance_under_load():
    """Test system performance under simulated field conditions."""
    print("\n⚡ Testing Performance Under Load...")
    
    try:
        config = FieldDeploymentConfig(
            site_name="Performance_Test_Site",
            site_coordinates=(-20.0, 47.0),
            research_station="Test_Station",
            deployment_date=datetime.utcnow(),
            camera_trap_id="CAM_PERF_001"
        )
        
        agent = MadagascarFieldAgent(config)
        
        if not await agent.initialize_systems():
            print("❌ Performance test initialization failed")
            return False
        
        # Create multiple test images
        test_images = []
        for i in range(20):  # Simulate 20 camera trap images
            image_path = f"perf_test_{i}.jpg"
            test_image = Image.new('RGB', (224, 224), color=['red', 'green', 'blue'][i % 3])
            test_image.save(image_path)
            test_images.append(image_path)
        
        # Measure processing time
        start_time = time.time()
        results = await agent.batch_process_images(test_images)
        total_time = time.time() - start_time
        
        successful_results = [r for r in results if "error" not in r]
        
        # Performance metrics
        throughput = len(successful_results) / total_time if total_time > 0 else 0
        average_time_per_image = total_time / len(test_images) if test_images else 0
        
        print(f"✅ Performance metrics:")
        print(f"   • Total processing time: {total_time:.2f}s")
        print(f"   • Successful results: {len(successful_results)}/{len(test_images)}")
        print(f"   • Throughput: {throughput:.2f} images/second")
        print(f"   • Average time per image: {average_time_per_image:.2f}s")
        
        # Performance thresholds for field deployment
        if throughput >= 0.5:  # At least 0.5 images per second
            print("✅ Throughput acceptable for field deployment")
        else:
            print("⚠️  Throughput may be low for high-activity sites")
        
        if average_time_per_image <= 5.0:  # Less than 5 seconds per image
            print("✅ Processing latency acceptable")
        else:
            print("❌ Processing latency too high")
            return False
        
        # Check final deployment statistics
        final_summary = agent.get_deployment_summary()
        stats = final_summary["detection_statistics"]
        
        if stats["total_detections"] >= len(successful_results):
            print("✅ Deployment statistics tracking correctly")
        else:
            print("❌ Deployment statistics inconsistent")
            return False
        
        # Cleanup
        for image_path in test_images:
            if os.path.exists(image_path):
                os.remove(image_path)
        
        await agent.shutdown_systems()
        
        return True
        
    except Exception as e:
        print(f"❌ Performance under load error: {e}")
        return False

async def main():
    """Run Section 4 tests."""
    print("🌿 STEP 4 - SECTION 4: Field Deployment Integration")
    print("=" * 52)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Field deployment configuration
    if await test_field_deployment_config():
        tests_passed += 1
    
    # Test 2: Madagascar field agent
    if await test_madagascar_field_agent():
        tests_passed += 1
    
    # Test 3: Full pipeline integration
    if await test_full_pipeline_integration():
        tests_passed += 1
    
    # Test 4: Conservation workflow
    if await test_conservation_workflow():
        tests_passed += 1
    
    # Test 5: Performance under load
    if await test_performance_under_load():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Section 4 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 4 PASSED - Field Deployment Ready")
        print("\n🎉 STEP 4 COMPLETE: Species Identification Agent")
        print("🌍 Ready for Madagascar field deployment!")
        return True
    else:
        print("❌ Section 4 FAILED - Fix issues before deployment")
        return False

if __name__ == "__main__":
    asyncio.run(main())
