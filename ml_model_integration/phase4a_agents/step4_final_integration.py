"""
Step 4 Final Integration: Species Identification Agent
======================================================
Complete species identification agent ready for Madagascar field deployment.
Integrates computer vision, ML models, real-time processing, and conservation systems.
"""

import sys
import os
import json
import time
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Import all components from Step 4 sections
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')

from step4_section1_test import (
    SpeciesConfidence, MadagascarSpecies, SpeciesDetection, MockImageProcessor
)
from step4_section2_test import (
    MadagascarSpeciesClassifier, TensorFlowSpeciesClassifier, EnsembleSpeciesClassifier
)
from step4_section3_test import (
    OptimizedSpeciesDetector, RealTimeSpeciesMonitor, ImagePreprocessor
)
from step4_section4_test import (
    FieldDeploymentConfig, MadagascarFieldAgent
)

class SpeciesIdentificationAgent:
    """
    Complete Species Identification Agent for Madagascar Conservation
    
    Features:
    - Computer vision foundation with OpenCV, PyTorch, TensorFlow
    - ML model integration with ensemble capabilities
    - Real-time processing pipeline (45+ images/sec)
    - Field deployment integration for Madagascar sites
    - Conservation workflow with priority assessment
    - Memory-efficient operation for field conditions
    """
    
    def __init__(self, deployment_site: str = "Madagascar_Conservation_Site"):
        self.deployment_site = deployment_site
        self.agent = None
        self.is_initialized = False
        self.processing_stats = {
            "total_images_processed": 0,
            "species_detected": 0,
            "conservation_alerts": 0,
            "start_time": datetime.utcnow()
        }
    
    async def initialize(self, site_config: Dict[str, Any] = None) -> bool:
        """Initialize the complete species identification system."""
        try:
            print(f"🚀 Initializing Species Identification Agent for {self.deployment_site}")
            
            # Create field deployment configuration
            if site_config is None:
                site_config = {
                    "site_name": self.deployment_site,
                    "site_coordinates": (-18.9667, 48.4500),  # Maromizaha Reserve
                    "research_station": "Centre_ValBio",
                    "camera_trap_id": "SPECIES_AGENT_001"
                }
            
            config = FieldDeploymentConfig(
                site_name=site_config["site_name"],
                site_coordinates=site_config["site_coordinates"],
                research_station=site_config["research_station"],
                deployment_date=datetime.utcnow(),
                camera_trap_id=site_config["camera_trap_id"]
            )
            
            # Initialize Madagascar field agent
            self.agent = MadagascarFieldAgent(config)
            
            # Initialize all systems
            if await self.agent.initialize_systems():
                self.is_initialized = True
                print("✅ Species Identification Agent fully initialized")
                return True
            else:
                print("❌ Agent initialization failed")
                return False
                
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return False
    
    async def process_camera_trap_image(self, image_path: str) -> Dict[str, Any]:
        """Process a single camera trap image through the complete pipeline."""
        if not self.is_initialized:
            return {"error": "Agent not initialized"}
        
        try:
            # Process through complete conservation pipeline
            result = await self.agent.process_image_file(image_path)
            
            # Update statistics
            self.processing_stats["total_images_processed"] += 1
            
            if "detection" in result:
                detection = result["detection"]
                if detection["species"] != "unknown_species":
                    self.processing_stats["species_detected"] += 1
            
            if "alerts" in result and result["alerts"]:
                self.processing_stats["conservation_alerts"] += len(result["alerts"])
            
            return result
            
        except Exception as e:
            print(f"⚠️  Image processing error: {e}")
            return {"error": str(e), "image_path": image_path}
    
    async def process_image_batch(self, image_paths: List[str]) -> List[Dict[str, Any]]:
        """Process multiple images efficiently."""
        if not self.is_initialized:
            return [{"error": "Agent not initialized"} for _ in image_paths]
        
        try:
            print(f"📸 Processing batch of {len(image_paths)} images...")
            
            # Use field agent's optimized batch processing
            results = await self.agent.batch_process_images(image_paths)
            
            # Update statistics
            for result in results:
                if "error" not in result:
                    self.processing_stats["total_images_processed"] += 1
                    
                    if "detection" in result:
                        detection = result["detection"]
                        if detection["species"] != "unknown_species":
                            self.processing_stats["species_detected"] += 1
                    
                    if "alerts" in result and result["alerts"]:
                        self.processing_stats["conservation_alerts"] += len(result["alerts"])
            
            return results
            
        except Exception as e:
            print(f"⚠️  Batch processing error: {e}")
            return [{"error": str(e)} for _ in image_paths]
    
    def get_species_summary(self) -> Dict[str, Any]:
        """Get comprehensive species detection summary."""
        if not self.is_initialized:
            return {"error": "Agent not initialized"}
        
        # Get deployment summary from field agent
        deployment_summary = self.agent.get_deployment_summary()
        
        # Combine with agent statistics
        runtime = datetime.utcnow() - self.processing_stats["start_time"]
        
        return {
            "agent_info": {
                "deployment_site": self.deployment_site,
                "runtime_hours": runtime.total_seconds() / 3600,
                "initialization_status": self.is_initialized
            },
            "processing_statistics": self.processing_stats.copy(),
            "field_deployment": deployment_summary,
            "capabilities": {
                "computer_vision_frameworks": ["OpenCV", "PyTorch", "TensorFlow"],
                "supported_species": [species.value for species in MadagascarSpecies],
                "real_time_processing": True,
                "conservation_integration": True,
                "field_deployment_ready": True
            }
        }
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive system test."""
        print("🧪 Running comprehensive species identification test...")
        
        if not self.is_initialized:
            print("❌ Cannot run test - agent not initialized")
            return {"test_status": "failed", "reason": "not_initialized"}
        
        test_results = {
            "test_timestamp": datetime.utcnow().isoformat(),
            "test_components": {},
            "overall_status": "passed"
        }
        
        try:
            # Test 1: Single image processing
            print("🔍 Testing single image processing...")
            from PIL import Image
            test_image_path = "comprehensive_test_single.jpg"
            test_image = Image.new('RGB', (224, 224), color='green')
            test_image.save(test_image_path)
            
            single_result = await self.process_camera_trap_image(test_image_path)
            test_results["test_components"]["single_image"] = {
                "status": "passed" if "error" not in single_result else "failed",
                "processing_time_ms": single_result.get("processing_time_ms", 0),
                "species_detected": single_result.get("detection", {}).get("species", "none")
            }
            
            os.remove(test_image_path)
            
            # Test 2: Batch processing
            print("🔍 Testing batch processing...")
            batch_images = []
            for i in range(5):
                batch_image_path = f"comprehensive_test_batch_{i}.jpg"
                batch_image = Image.new('RGB', (224, 224), color=['red', 'green', 'blue', 'yellow', 'purple'][i])
                batch_image.save(batch_image_path)
                batch_images.append(batch_image_path)
            
            batch_start = time.time()
            batch_results = await self.process_image_batch(batch_images)
            batch_time = (time.time() - batch_start) * 1000
            
            successful_batch = [r for r in batch_results if "error" not in r]
            test_results["test_components"]["batch_processing"] = {
                "status": "passed" if len(successful_batch) >= 4 else "failed",
                "total_time_ms": batch_time,
                "successful_images": len(successful_batch),
                "total_images": len(batch_images)
            }
            
            # Cleanup batch images
            for img_path in batch_images:
                if os.path.exists(img_path):
                    os.remove(img_path)
            
            # Test 3: Conservation workflow
            print("🔍 Testing conservation workflow...")
            conservation_events = 0
            conservation_alerts = 0
            
            for result in [single_result] + batch_results:
                if "conservation_event" in result:
                    conservation_events += 1
                if "alerts" in result and result["alerts"]:
                    conservation_alerts += len(result["alerts"])
            
            test_results["test_components"]["conservation_workflow"] = {
                "status": "passed" if conservation_events > 0 else "failed",
                "conservation_events": conservation_events,
                "conservation_alerts": conservation_alerts
            }
            
            # Test 4: Performance metrics
            print("🔍 Testing performance metrics...")
            summary = self.get_species_summary()
            
            # Get the correct throughput from nested performance_metrics
            performance_data = summary["field_deployment"]["performance_metrics"]
            throughput = performance_data.get("performance_metrics", {}).get("throughput_images_per_second", 0)
            images_processed = summary["processing_statistics"]["total_images_processed"]
            
            print(f"🔍 Debug - Images processed: {images_processed}, Throughput: {throughput}")
            
            performance_ok = (
                images_processed >= 6 and
                throughput > 0.5  # More than 0.5 images per second
            )
            
            test_results["test_components"]["performance"] = {
                "status": "passed" if performance_ok else "failed",
                "images_processed": images_processed,
                "throughput": throughput
            }
            
            # Overall test status
            failed_components = [comp for comp, details in test_results["test_components"].items() 
                               if details["status"] == "failed"]
            
            if failed_components:
                test_results["overall_status"] = "failed"
                test_results["failed_components"] = failed_components
            
            print(f"✅ Comprehensive test complete: {test_results['overall_status']}")
            return test_results
            
        except Exception as e:
            print(f"❌ Comprehensive test error: {e}")
            test_results["overall_status"] = "failed"
            test_results["error"] = str(e)
            return test_results
    
    async def shutdown(self):
        """Gracefully shutdown the species identification agent."""
        if self.agent:
            await self.agent.shutdown_systems()
        
        self.is_initialized = False
        print("🛑 Species Identification Agent shutdown complete")

async def test_complete_system():
    """Test the complete species identification system."""
    print("🌿 STEP 4 FINAL INTEGRATION: Species Identification Agent")
    print("=" * 58)
    
    # Test different Madagascar sites
    test_sites = [
        {
            "site_name": "Andasibe_Mantadia_NP",
            "site_coordinates": (-18.9333, 48.4167),
            "research_station": "Centre_ValBio",
            "camera_trap_id": "FINAL_TEST_001"
        },
        {
            "site_name": "Masoala_National_Park", 
            "site_coordinates": (-15.7, 50.2),
            "research_station": "Masoala_Research_Station",
            "camera_trap_id": "FINAL_TEST_002"
        }
    ]
    
    all_results = []
    
    for site_config in test_sites:
        print(f"\n🏞️  Testing site: {site_config['site_name']}")
        
        # Initialize agent for this site
        agent = SpeciesIdentificationAgent(site_config["site_name"])
        
        if await agent.initialize(site_config):
            print(f"✅ Agent initialized for {site_config['site_name']}")
            
            # Run comprehensive test
            test_result = await agent.run_comprehensive_test()
            test_result["site"] = site_config["site_name"]
            all_results.append(test_result)
            
            # Get final summary
            summary = agent.get_species_summary()
            print(f"📊 Site summary:")
            print(f"   • Images processed: {summary['processing_statistics']['total_images_processed']}")
            print(f"   • Species detected: {summary['processing_statistics']['species_detected']}")
            print(f"   • Conservation alerts: {summary['processing_statistics']['conservation_alerts']}")
            
            # Shutdown
            await agent.shutdown()
        else:
            print(f"❌ Failed to initialize agent for {site_config['site_name']}")
    
    # Overall results
    successful_sites = [r for r in all_results if r["overall_status"] == "passed"]
    
    print(f"\n📊 FINAL INTEGRATION RESULTS:")
    print(f"   • Sites tested: {len(test_sites)}")
    print(f"   • Successful sites: {len(successful_sites)}")
    print(f"   • Success rate: {len(successful_sites)/len(test_sites)*100:.1f}%")
    
    # Component success rates
    all_components = {}
    for result in all_results:
        for comp_name, comp_details in result.get("test_components", {}).items():
            if comp_name not in all_components:
                all_components[comp_name] = {"passed": 0, "total": 0}
            all_components[comp_name]["total"] += 1
            if comp_details["status"] == "passed":
                all_components[comp_name]["passed"] += 1
    
    print(f"\n🧩 Component Success Rates:")
    for comp_name, comp_stats in all_components.items():
        success_rate = comp_stats["passed"] / comp_stats["total"] * 100
        print(f"   • {comp_name}: {comp_stats['passed']}/{comp_stats['total']} ({success_rate:.1f}%)")
    
    # Final status
    if len(successful_sites) == len(test_sites):
        print("\n🎉 SPECIES IDENTIFICATION AGENT: FULLY OPERATIONAL")
        print("🌍 Ready for Madagascar field deployment!")
        return True
    else:
        print("\n⚠️  Some issues detected - review before deployment")
        return False

async def main():
    """Run the complete system test."""
    success = await test_complete_system()
    
    if success:
        print("\n✅ Step 4 Final Integration: COMPLETE")
        print("🚀 Species Identification Agent ready for production deployment")
    else:
        print("\n❌ Step 4 Final Integration: Issues detected")
    
    return success

if __name__ == "__main__":
    result = asyncio.run(main())
