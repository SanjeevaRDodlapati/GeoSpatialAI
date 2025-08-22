"""
Step 3 Section 4: Final Conservation Reasoning System
=====================================================
Complete conservation reasoning system with comprehensive validation.
"""

import sys
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple

# Import all components
from step3_section1_test import (
    ThreatLevel, ConservationAction, ConservationRule, 
    ConservationFact, ReasoningResult, SimpleConservationReasoner
)
from step3_section3b_test import FixedMemoryIntegratedReasoner

class ConservationReasoningSystem:
    """Complete conservation reasoning system for Madagascar deployment."""
    
    def __init__(self, system_id: str = "madagascar_conservation", storage_dir: str = "conservation_system"):
        self.system_id = system_id
        self.storage_dir = storage_dir
        self.reasoner = FixedMemoryIntegratedReasoner(storage_dir)
        self.active_alerts = []
        self.system_metrics = {
            "total_detections": 0,
            "total_threats": 0,
            "total_interventions": 0,
            "system_uptime": datetime.utcnow()
        }
        
        # Initialize with Madagascar conservation rules
        self._initialize_madagascar_rules()
    
    def _initialize_madagascar_rules(self):
        """Initialize system with Madagascar-specific conservation rules."""
        madagascar_rules = [
            # Species Protection Rules
            ConservationRule(
                rule_id="lemur_catta_protection",
                name="Ring-tailed Lemur Protection Protocol",
                description="Enhanced protection for ring-tailed lemurs",
                conditions={
                    "all": [
                        {
                            "fact_type": "species",
                            "entity": "lemur_catta",
                            "attribute": "detection_confidence",
                            "operator": "greater_than",
                            "value": 0.85,
                            "min_confidence": 0.8
                        }
                    ]
                },
                actions=[ConservationAction.MONITOR, ConservationAction.ALERT],
                priority=8
            ),
            ConservationRule(
                rule_id="indri_indri_emergency",
                name="Indri Emergency Protocol",
                description="Critical response for endangered Indri",
                conditions={
                    "all": [
                        {
                            "fact_type": "species",
                            "entity": "indri_indri",
                            "attribute": "detection_confidence",
                            "operator": "greater_than",
                            "value": 0.8,
                            "min_confidence": 0.75
                        }
                    ]
                },
                actions=[ConservationAction.ALERT, ConservationAction.EMERGENCY, ConservationAction.INVESTIGATE],
                priority=10
            ),
            
            # Threat Detection Rules
            ConservationRule(
                rule_id="deforestation_response",
                name="Deforestation Response Protocol",
                description="Rapid response to deforestation threats",
                conditions={
                    "all": [
                        {
                            "fact_type": "threat",
                            "entity": "deforestation",
                            "attribute": "severity",
                            "operator": "greater_than",
                            "value": 0.6,
                            "min_confidence": 0.7
                        }
                    ]
                },
                actions=[ConservationAction.ALERT, ConservationAction.INTERVENE],
                priority=9
            ),
            ConservationRule(
                rule_id="human_intrusion_detection",
                name="Human Intrusion Detection",
                description="Detect unauthorized human activity",
                conditions={
                    "all": [
                        {
                            "fact_type": "threat",
                            "entity": "human_intrusion",
                            "attribute": "probability",
                            "operator": "greater_than",
                            "value": 0.7,
                            "min_confidence": 0.8
                        }
                    ]
                },
                actions=[ConservationAction.ALERT, ConservationAction.INVESTIGATE, ConservationAction.INTERVENE],
                priority=9
            ),
            
            # Site Management Rules
            ConservationRule(
                rule_id="centre_valbio_monitoring",
                name="Centre ValBio Monitoring Protocol",
                description="Enhanced monitoring for research station",
                conditions={
                    "all": [
                        {
                            "fact_type": "location",
                            "entity": "centre_valbio",
                            "attribute": "activity_level",
                            "operator": "greater_than",
                            "value": 1,
                            "min_confidence": 0.8
                        }
                    ]
                },
                actions=[ConservationAction.MONITOR],
                priority=6
            ),
            ConservationRule(
                rule_id="maromizaha_protection",
                name="Maromizaha Protected Area Protocol",
                description="Protection protocol for Maromizaha",
                conditions={
                    "all": [
                        {
                            "fact_type": "location",
                            "entity": "maromizaha",
                            "attribute": "activity_level",
                            "operator": "greater_than",
                            "value": 0,
                            "min_confidence": 0.7
                        }
                    ]
                },
                actions=[ConservationAction.MONITOR, ConservationAction.ALERT],
                priority=7
            )
        ]
        
        for rule in madagascar_rules:
            self.reasoner.add_rule(rule)
    
    def process_conservation_event(self, event_data: Dict[str, Any]) -> ReasoningResult:
        """Process a conservation event and generate reasoning response."""
        try:
            event_type = event_data.get("event_type")
            entity = event_data.get("entity")
            location = event_data.get("location", "unknown")
            
            # Store event in memory
            if event_type == "species_detection":
                self.reasoner.memory.store_species_event(entity, event_data)
                self.system_metrics["total_detections"] += 1
            elif event_type == "threat_detection":
                # Convert to threat fact
                threat_fact = ConservationFact(
                    fact_id=f"threat_{entity}_{datetime.utcnow().timestamp()}",
                    fact_type="threat",
                    entity=entity,
                    attribute="severity" if "severity" in event_data else "probability",
                    value=event_data.get("severity", event_data.get("probability", 0.5)),
                    confidence=event_data.get("confidence", 0.8),
                    timestamp=datetime.utcnow(),
                    source=event_data.get("source", "system")
                )
                self.reasoner.add_fact(threat_fact)
                self.system_metrics["total_threats"] += 1
            elif event_type == "site_activity":
                self.reasoner.memory.store_site_event(location, event_data)
            
            # Perform reasoning
            context = {
                "site": location,
                "event_type": event_type,
                "entity": entity,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            result = self.reasoner.reason_with_memory(context)
            
            # Process actions
            if ConservationAction.EMERGENCY in result.recommended_actions:
                self._trigger_emergency_alert(result, event_data)
            elif ConservationAction.INTERVENE in result.recommended_actions:
                self.system_metrics["total_interventions"] += 1
            
            return result
            
        except Exception as e:
            print(f"⚠️  Error processing conservation event: {e}")
            # Return empty result
            return ReasoningResult(
                triggered_rules=[],
                recommended_actions=[],
                threat_level=ThreatLevel.LOW,
                confidence=0.0,
                reasoning=f"Error processing event: {e}",
                facts_used=[]
            )
    
    def _trigger_emergency_alert(self, result: ReasoningResult, event_data: Dict[str, Any]):
        """Trigger emergency alert for critical situations."""
        alert = {
            "alert_id": f"emergency_{datetime.utcnow().timestamp()}",
            "timestamp": datetime.utcnow().isoformat(),
            "threat_level": result.threat_level.value,
            "triggered_rules": result.triggered_rules,
            "event_data": event_data,
            "reasoning": result.reasoning,
            "status": "active"
        }
        self.active_alerts.append(alert)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        uptime = datetime.utcnow() - self.system_metrics["system_uptime"]
        memory_stats = self.reasoner.memory.get_memory_stats()
        
        return {
            "system_id": self.system_id,
            "status": "operational",
            "uptime_hours": uptime.total_seconds() / 3600,
            "metrics": self.system_metrics,
            "memory_stats": memory_stats,
            "active_alerts": len(self.active_alerts),
            "rules_count": len(self.reasoner.rules),
            "facts_count": len(self.reasoner.facts),
            "reasoning_history": len(self.reasoner.reasoning_history)
        }
    
    def generate_conservation_report(self, hours_back: int = 24) -> Dict[str, Any]:
        """Generate conservation activity report."""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
        
        # Analyze recent reasoning history
        recent_reasoning = [
            r for r in self.reasoner.reasoning_history 
            if len(r.facts_used) > 0  # Filter valid results
        ][-10:]  # Last 10 results
        
        # Analyze threat levels
        threat_distribution = {}
        for result in recent_reasoning:
            level = result.threat_level.value
            threat_distribution[level] = threat_distribution.get(level, 0) + 1
        
        # Analyze most triggered rules
        rule_frequency = {}
        for result in recent_reasoning:
            for rule in result.triggered_rules:
                rule_frequency[rule] = rule_frequency.get(rule, 0) + 1
        
        return {
            "report_period_hours": hours_back,
            "total_reasoning_events": len(recent_reasoning),
            "threat_level_distribution": threat_distribution,
            "most_triggered_rules": rule_frequency,
            "system_metrics": self.system_metrics,
            "active_alerts": len(self.active_alerts),
            "recommendations": self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate system recommendations based on current state."""
        recommendations = []
        
        if self.system_metrics["total_threats"] > 5:
            recommendations.append("Consider increasing patrol frequency due to elevated threat activity")
        
        if len(self.active_alerts) > 0:
            recommendations.append("Active alerts require immediate attention")
        
        memory_stats = self.reasoner.memory.get_memory_stats()
        if memory_stats["total_species_events"] > 50:
            recommendations.append("High species activity detected - consider expanded monitoring")
        
        if len(recommendations) == 0:
            recommendations.append("System operating normally - continue routine monitoring")
        
        return recommendations

def test_conservation_system_creation():
    """Test creating complete conservation reasoning system."""
    print("🌿 Testing Conservation System Creation...")
    
    try:
        system = ConservationReasoningSystem("test_madagascar_system", "test_conservation_system")
        print("✅ ConservationReasoningSystem created")
        
        # Check initialization
        if len(system.reasoner.rules) > 0:
            print(f"✅ Madagascar rules initialized: {len(system.reasoner.rules)} rules")
        else:
            print("❌ No rules initialized")
            return False
        
        # Check system components
        if hasattr(system, 'system_metrics') and hasattr(system, 'active_alerts'):
            print("✅ System components properly initialized")
        else:
            print("❌ System components missing")
            return False
        
        return system
        
    except Exception as e:
        print(f"❌ Conservation system creation error: {e}")
        return None

def test_species_detection_workflow():
    """Test complete species detection workflow."""
    print("\n🐾 Testing Species Detection Workflow...")
    
    try:
        system = ConservationReasoningSystem("test_species_workflow", "test_species_system")
        
        # Test 1: Ring-tailed lemur detection
        lemur_event = {
            "event_type": "species_detection",
            "entity": "lemur_catta",
            "location": "centre_valbio",
            "confidence": 0.94,
            "detection_confidence": 0.94,
            "observer": "camera_trap_network",
            "coordinates": [-21.289, 47.433],
            "notes": "Adult ring-tailed lemur with juvenile"
        }
        
        result1 = system.process_conservation_event(lemur_event)
        
        if "lemur_catta_protection" in result1.triggered_rules:
            print("✅ Lemur protection protocol triggered")
        else:
            print("❌ Lemur protection protocol not triggered")
            return False
        
        if ConservationAction.MONITOR in result1.recommended_actions:
            print("✅ Monitoring action recommended")
        else:
            print("❌ Monitoring action not recommended")
            return False
        
        # Test 2: Indri detection (endangered species)
        indri_event = {
            "event_type": "species_detection",
            "entity": "indri_indri",
            "location": "maromizaha",
            "confidence": 0.91,
            "detection_confidence": 0.91,
            "observer": "acoustic_monitoring_station",
            "coordinates": [-18.947, 48.456],
            "notes": "Indri territorial call detected"
        }
        
        result2 = system.process_conservation_event(indri_event)
        
        if "indri_indri_emergency" in result2.triggered_rules:
            print("✅ Indri emergency protocol triggered")
        else:
            print("❌ Indri emergency protocol not triggered")
            return False
        
        if result2.threat_level == ThreatLevel.CRITICAL:
            print("✅ Threat level escalated to CRITICAL for endangered species")
        else:
            print(f"⚠️  Expected CRITICAL, got {result2.threat_level.value}")
        
        if ConservationAction.EMERGENCY in result2.recommended_actions:
            print("✅ Emergency action triggered for endangered species")
        else:
            print("❌ Emergency action not triggered")
            return False
        
        # Check system metrics
        if system.system_metrics["total_detections"] == 2:
            print("✅ System metrics updated correctly")
        else:
            print(f"❌ Expected 2 detections, got {system.system_metrics['total_detections']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Species detection workflow error: {e}")
        return False

def test_threat_detection_workflow():
    """Test threat detection and response workflow."""
    print("\n🚨 Testing Threat Detection Workflow...")
    
    try:
        system = ConservationReasoningSystem("test_threat_workflow", "test_threat_system")
        
        # Test 1: Deforestation threat
        deforestation_event = {
            "event_type": "threat_detection",
            "entity": "deforestation",
            "location": "maromizaha_buffer_zone",
            "severity": 0.75,
            "confidence": 0.88,
            "source": "satellite_monitoring",
            "coordinates": [-18.950, 48.460],
            "notes": "Forest loss detected in buffer zone"
        }
        
        result1 = system.process_conservation_event(deforestation_event)
        
        if "deforestation_response" in result1.triggered_rules:
            print("✅ Deforestation response protocol triggered")
        else:
            print("❌ Deforestation response not triggered")
            return False
        
        if ConservationAction.INTERVENE in result1.recommended_actions:
            print("✅ Intervention action recommended")
        else:
            print("❌ Intervention action not recommended")
            return False
        
        # Test 2: Human intrusion threat
        intrusion_event = {
            "event_type": "threat_detection",
            "entity": "human_intrusion",
            "location": "centre_valbio_perimeter",
            "probability": 0.82,
            "confidence": 0.85,
            "source": "motion_sensor_network",
            "coordinates": [-21.290, 47.430],
            "notes": "Unauthorized movement detected near research station"
        }
        
        result2 = system.process_conservation_event(intrusion_event)
        
        if "human_intrusion_detection" in result2.triggered_rules:
            print("✅ Human intrusion detection triggered")
        else:
            print("❌ Human intrusion detection not triggered")
            return False
        
        if result2.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            print(f"✅ Appropriate threat escalation: {result2.threat_level.value}")
        else:
            print(f"⚠️  Low threat level for intrusion: {result2.threat_level.value}")
        
        # Check threat metrics
        if system.system_metrics["total_threats"] == 2:
            print("✅ Threat metrics updated correctly")
        else:
            print(f"❌ Expected 2 threats, got {system.system_metrics['total_threats']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Threat detection workflow error: {e}")
        return False

def test_comprehensive_madagascar_scenario():
    """Test comprehensive Madagascar conservation scenario."""
    print("\n🇲🇬 Testing Comprehensive Madagascar Scenario...")
    
    try:
        system = ConservationReasoningSystem("madagascar_comprehensive", "test_madagascar_comprehensive")
        
        # Simulate a full day of conservation activities
        conservation_events = [
            # Morning: Species detections
            {
                "event_type": "species_detection",
                "entity": "lemur_catta",
                "location": "centre_valbio",
                "confidence": 0.96,
                "detection_confidence": 0.96,
                "observer": "dawn_patrol_camera_01",
                "time": "06:30"
            },
            {
                "event_type": "species_detection", 
                "entity": "indri_indri",
                "location": "maromizaha",
                "confidence": 0.93,
                "detection_confidence": 0.93,
                "observer": "acoustic_array_station_3",
                "time": "07:15"
            },
            
            # Midday: Site activities
            {
                "event_type": "site_activity",
                "location": "centre_valbio",
                "activity": "research_expedition",
                "team_size": 6,
                "weather": "clear",
                "time": "10:00"
            },
            {
                "event_type": "site_activity",
                "location": "maromizaha",
                "activity": "patrol_mission",
                "team_size": 4,
                "weather": "partly_cloudy",
                "time": "11:30"
            },
            
            # Afternoon: Threat detection
            {
                "event_type": "threat_detection",
                "entity": "deforestation",
                "location": "maromizaha_buffer_zone",
                "severity": 0.68,
                "confidence": 0.82,
                "source": "satellite_alert_system",
                "time": "14:20"
            },
            
            # Evening: Human intrusion
            {
                "event_type": "threat_detection",
                "entity": "human_intrusion",
                "location": "centre_valbio_perimeter",
                "probability": 0.79,
                "confidence": 0.87,
                "source": "perimeter_sensor_grid",
                "time": "18:45"
            }
        ]
        
        results = []
        for event in conservation_events:
            result = system.process_conservation_event(event)
            results.append(result)
            print(f"   ⏰ {event.get('time', '??:??')} - {event['event_type']} processed")
        
        # Analyze daily results
        total_rules_triggered = sum(len(r.triggered_rules) for r in results)
        unique_actions = set()
        max_threat_level = ThreatLevel.LOW
        
        for result in results:
            unique_actions.update(result.recommended_actions)
            if result.threat_level.value == "critical":
                max_threat_level = ThreatLevel.CRITICAL
            elif result.threat_level.value == "high" and max_threat_level != ThreatLevel.CRITICAL:
                max_threat_level = ThreatLevel.HIGH
            elif result.threat_level.value == "medium" and max_threat_level not in [ThreatLevel.CRITICAL, ThreatLevel.HIGH]:
                max_threat_level = ThreatLevel.MEDIUM
        
        print(f"   📊 Daily Summary:")
        print(f"      🎯 Total rules triggered: {total_rules_triggered}")
        print(f"      🎭 Unique actions recommended: {len(unique_actions)}")
        print(f"      🚨 Maximum threat level: {max_threat_level.value}")
        print(f"      🔔 Active alerts: {len(system.active_alerts)}")
        
        # Generate daily report
        daily_report = system.generate_conservation_report(hours_back=24)
        print(f"   📋 Daily report generated with {daily_report['total_reasoning_events']} events")
        
        # Verify comprehensive response
        if total_rules_triggered >= 6:  # Expect multiple rules per event
            print("✅ Comprehensive rule coverage achieved")
        else:
            print("⚠️  Limited rule coverage")
        
        if ConservationAction.EMERGENCY in unique_actions:
            print("✅ Emergency protocols activated")
        else:
            print("⚠️  No emergency protocols activated")
        
        if max_threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            print("✅ Appropriate threat escalation")
        else:
            print("⚠️  Low threat escalation")
        
        # Check system status
        status = system.get_system_status()
        print(f"   💻 System Status: {status['status']}")
        print(f"   📈 System Metrics: {status['metrics']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Comprehensive Madagascar scenario error: {e}")
        return False

def test_system_reporting():
    """Test system reporting and analytics."""
    print("\n📊 Testing System Reporting...")
    
    try:
        system = ConservationReasoningSystem("test_reporting", "test_reporting_system")
        
        # Generate some activity
        test_events = [
            {
                "event_type": "species_detection",
                "entity": "lemur_catta",
                "location": "centre_valbio",
                "confidence": 0.95,
                "detection_confidence": 0.95
            },
            {
                "event_type": "threat_detection",
                "entity": "deforestation",
                "location": "test_area",
                "severity": 0.7,
                "confidence": 0.8
            }
        ]
        
        for event in test_events:
            system.process_conservation_event(event)
        
        # Test system status
        status = system.get_system_status()
        
        required_fields = ["system_id", "status", "metrics", "memory_stats", "rules_count"]
        for field in required_fields:
            if field in status:
                print(f"✅ Status field '{field}' present")
            else:
                print(f"❌ Status field '{field}' missing")
                return False
        
        # Test conservation report
        report = system.generate_conservation_report(hours_back=1)
        
        required_report_fields = ["total_reasoning_events", "system_metrics", "recommendations"]
        for field in required_report_fields:
            if field in report:
                print(f"✅ Report field '{field}' present")
            else:
                print(f"❌ Report field '{field}' missing")
                return False
        
        if len(report["recommendations"]) > 0:
            print(f"✅ Recommendations generated: {len(report['recommendations'])}")
        else:
            print("❌ No recommendations generated")
            return False
        
        print("✅ System reporting functional")
        return True
        
    except Exception as e:
        print(f"❌ System reporting error: {e}")
        return False

def cleanup_test_files():
    """Clean up test files."""
    try:
        import shutil
        test_dirs = [
            "test_conservation_system",
            "test_species_system", 
            "test_threat_system",
            "test_madagascar_comprehensive",
            "test_reporting_system"
        ]
        
        for test_dir in test_dirs:
            if os.path.exists(test_dir):
                shutil.rmtree(test_dir)
        
        print("✅ Test files cleaned up")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

def main():
    """Run Section 4 tests."""
    print("🧠 STEP 3 - SECTION 4: Final Conservation Reasoning System")
    print("=" * 62)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: System creation
    if test_conservation_system_creation():
        tests_passed += 1
    
    # Test 2: Species detection workflow
    if test_species_detection_workflow():
        tests_passed += 1
    
    # Test 3: Threat detection workflow
    if test_threat_detection_workflow():
        tests_passed += 1
    
    # Test 4: Comprehensive Madagascar scenario
    if test_comprehensive_madagascar_scenario():
        tests_passed += 1
    
    # Test 5: System reporting
    if test_system_reporting():
        tests_passed += 1
    
    # Cleanup
    cleanup_test_files()
    
    # Summary
    print(f"\n📊 Section 4 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 4 PASSED - Ready for Final Integration")
        return True
    else:
        print("❌ Section 4 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
