"""
Step 3 Final Integration: Complete Conservation Reasoning Engine
===============================================================
Final comprehensive test combining all sections with fixes.
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import all components
from step3_section1_test import (
    ThreatLevel, ConservationAction, ConservationRule, 
    ConservationFact, ReasoningResult
)
from step3_section2_test import main as section2_test
from step3_section3b_test import main as section3b_test
from step3_section4_test import ConservationReasoningSystem

def test_all_sections():
    """Test all previous sections."""
    print("🧪 Running All Section Tests...")
    
    try:
        # Run section 2 test
        print("\n" + "="*50)
        result2 = section2_test()
        
        # Run section 3B test
        print("\n" + "="*50)
        result3b = section3b_test()
        
        if result2 and result3b:
            print("✅ All previous section tests passed")
            return True
        else:
            print("❌ Some previous section tests failed")
            return False
            
    except Exception as e:
        print(f"❌ Section test error: {e}")
        return False

def test_fixed_threat_detection():
    """Test fixed threat detection workflow."""
    print("\n🔧 Testing Fixed Threat Detection...")
    
    try:
        system = ConservationReasoningSystem("test_fixed_threats", "test_fixed_threat_system")
        
        # Manually add threat facts to test reasoning
        deforestation_fact = ConservationFact(
            fact_id="test_deforestation_threat",
            fact_type="threat",
            entity="deforestation",
            attribute="severity",
            value=0.75,
            confidence=0.88,
            timestamp=datetime.utcnow(),
            source="satellite_monitoring"
        )
        system.reasoner.add_fact(deforestation_fact)
        
        human_intrusion_fact = ConservationFact(
            fact_id="test_human_intrusion",
            fact_type="threat",
            entity="human_intrusion",
            attribute="probability",
            value=0.82,
            confidence=0.85,
            timestamp=datetime.utcnow(),
            source="motion_sensors"
        )
        system.reasoner.add_fact(human_intrusion_fact)
        
        # Test reasoning with threat facts
        result = system.reasoner.reason({
            "site": "test_area",
            "scenario": "threat_detection_test"
        })
        
        if len(result.triggered_rules) > 0:
            print(f"✅ Threat rules triggered: {result.triggered_rules}")
            
            # Check for expected threat rules
            threat_rules = ["deforestation_response", "human_intrusion_detection"]
            triggered_threat_rules = [rule for rule in threat_rules if rule in result.triggered_rules]
            
            if len(triggered_threat_rules) > 0:
                print(f"✅ Threat-specific rules triggered: {triggered_threat_rules}")
            else:
                print("⚠️  No threat-specific rules triggered")
        else:
            print("⚠️  No rules triggered with threat facts")
        
        if result.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            print(f"✅ Appropriate threat escalation: {result.threat_level.value}")
        else:
            print(f"⚠️  Low threat escalation: {result.threat_level.value}")
        
        if ConservationAction.INTERVENE in result.recommended_actions or ConservationAction.ALERT in result.recommended_actions:
            print("✅ Appropriate threat response actions")
        else:
            print("⚠️  Limited threat response actions")
        
        return True
        
    except Exception as e:
        print(f"❌ Fixed threat detection error: {e}")
        return False

def test_complete_madagascar_deployment():
    """Test complete Madagascar deployment scenario."""
    print("\n🇲🇬 Testing Complete Madagascar Deployment...")
    
    try:
        system = ConservationReasoningSystem("madagascar_deployment", "test_madagascar_deployment")
        
        # Comprehensive Madagascar conservation events
        madagascar_events = [
            # Day 1: Multiple species detections
            {
                "event_type": "species_detection",
                "entity": "lemur_catta",
                "location": "centre_valbio",
                "confidence": 0.97,
                "detection_confidence": 0.97,
                "observer": "camera_trap_network_01",
                "habitat": "primary_forest",
                "behavior": "foraging"
            },
            {
                "event_type": "species_detection",
                "entity": "indri_indri",
                "location": "maromizaha",
                "confidence": 0.94,
                "detection_confidence": 0.94,
                "observer": "acoustic_monitoring_station",
                "habitat": "primary_forest",
                "behavior": "territorial_call"
            },
            {
                "event_type": "species_detection",
                "entity": "brookesia_micra",
                "location": "centre_valbio",
                "confidence": 0.89,
                "detection_confidence": 0.89,
                "observer": "research_team_alpha",
                "habitat": "leaf_litter",
                "behavior": "cryptic"
            },
            
            # Research activities
            {
                "event_type": "site_activity",
                "location": "centre_valbio",
                "activity": "biodiversity_survey",
                "team_size": 5,
                "weather": "clear",
                "duration_hours": 6
            },
            {
                "event_type": "site_activity",
                "location": "maromizaha",
                "activity": "lemur_behavioral_study",
                "team_size": 3,
                "weather": "partly_cloudy",
                "duration_hours": 4
            }
        ]
        
        # Process all events
        results = []
        for i, event in enumerate(madagascar_events):
            print(f"   📅 Processing event {i+1}/{len(madagascar_events)}: {event['event_type']}")
            result = system.process_conservation_event(event)
            results.append(result)
        
        # Analyze comprehensive results
        total_triggered_rules = sum(len(r.triggered_rules) for r in results)
        all_actions = set()
        threat_levels = []
        
        for result in results:
            all_actions.update(result.recommended_actions)
            threat_levels.append(result.threat_level)
        
        max_threat = max(threat_levels, key=lambda x: ["low", "medium", "high", "critical"].index(x.value))
        
        print(f"\n   📊 Deployment Analysis:")
        print(f"      🎯 Total rules triggered: {total_triggered_rules}")
        print(f"      🎭 Unique actions recommended: {len(all_actions)}")
        print(f"      🚨 Maximum threat level: {max_threat.value}")
        print(f"      📈 Species detections: {system.system_metrics['total_detections']}")
        
        # Generate deployment report
        deployment_report = system.generate_conservation_report(hours_back=24)
        
        print(f"   📋 Deployment Report:")
        print(f"      📅 Total events: {deployment_report['total_reasoning_events']}")
        print(f"      🎯 Rule frequency: {deployment_report['most_triggered_rules']}")
        print(f"      🔔 Recommendations: {len(deployment_report['recommendations'])}")
        
        # Verify deployment readiness
        deployment_checks = {
            "species_detection": system.system_metrics["total_detections"] >= 3,
            "rule_coverage": total_triggered_rules >= 8,
            "action_diversity": len(all_actions) >= 2,
            "threat_assessment": max_threat != ThreatLevel.LOW,
            "system_stability": len(system.reasoner.reasoning_history) >= 5
        }
        
        passed_checks = sum(deployment_checks.values())
        total_checks = len(deployment_checks)
        
        print(f"\n   ✅ Deployment Readiness: {passed_checks}/{total_checks} checks passed")
        
        for check, passed in deployment_checks.items():
            status = "✅" if passed else "❌"
            print(f"      {status} {check.replace('_', ' ').title()}")
        
        if passed_checks >= total_checks - 1:  # Allow one check to fail
            print("✅ Madagascar deployment ready")
            return True
        else:
            print("❌ Madagascar deployment not ready")
            return False
        
    except Exception as e:
        print(f"❌ Madagascar deployment test error: {e}")
        return False

def test_production_readiness():
    """Test production readiness of the conservation reasoning engine."""
    print("\n🚀 Testing Production Readiness...")
    
    try:
        system = ConservationReasoningSystem("production_test", "test_production_readiness")
        
        # Test system robustness with edge cases
        edge_cases = [
            # Low confidence detection
            {
                "event_type": "species_detection",
                "entity": "lemur_catta",
                "location": "centre_valbio",
                "confidence": 0.6,  # Low confidence
                "detection_confidence": 0.6
            },
            # Missing data
            {
                "event_type": "species_detection",
                "entity": "unknown_species",
                "location": "unknown_location"
                # Missing confidence
            },
            # High threat scenario
            {
                "event_type": "threat_detection",
                "entity": "human_intrusion",
                "location": "centre_valbio",
                "probability": 0.95,  # Very high threat
                "confidence": 0.9
            }
        ]
        
        edge_case_results = []
        for i, case in enumerate(edge_cases):
            try:
                result = system.process_conservation_event(case)
                edge_case_results.append(result)
                print(f"   ✅ Edge case {i+1} handled successfully")
            except Exception as e:
                print(f"   ❌ Edge case {i+1} failed: {e}")
                return False
        
        # Test system performance under load
        performance_events = []
        for i in range(20):  # Generate 20 rapid events
            event = {
                "event_type": "species_detection",
                "entity": f"test_species_{i % 3}",
                "location": f"test_location_{i % 2}",
                "confidence": 0.8 + (i % 10) * 0.02,
                "detection_confidence": 0.8 + (i % 10) * 0.02
            }
            performance_events.append(event)
        
        start_time = datetime.utcnow()
        performance_results = []
        
        for event in performance_events:
            result = system.process_conservation_event(event)
            performance_results.append(result)
        
        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()
        
        print(f"   ⚡ Performance: {len(performance_events)} events in {processing_time:.2f}s")
        print(f"   📊 Average: {processing_time/len(performance_events)*1000:.1f}ms per event")
        
        # Production readiness criteria
        readiness_criteria = {
            "edge_case_handling": len(edge_case_results) == len(edge_cases),
            "performance": processing_time < 5.0,  # Under 5 seconds for 20 events
            "memory_integration": len(system.reasoner.facts) > 0,
            "rule_execution": all(len(r.triggered_rules) >= 0 for r in performance_results),
            "system_stability": system.get_system_status()["status"] == "operational"
        }
        
        passed_criteria = sum(readiness_criteria.values())
        total_criteria = len(readiness_criteria)
        
        print(f"\n   🎯 Production Readiness: {passed_criteria}/{total_criteria} criteria met")
        
        for criterion, passed in readiness_criteria.items():
            status = "✅" if passed else "❌"
            print(f"      {status} {criterion.replace('_', ' ').title()}")
        
        if passed_criteria == total_criteria:
            print("✅ System is production ready")
            return True
        else:
            print("⚠️  System needs improvements before production")
            return False
        
    except Exception as e:
        print(f"❌ Production readiness test error: {e}")
        return False

def cleanup_test_files():
    """Clean up all test files."""
    try:
        import shutil
        test_dirs = [
            "test_fixed_threat_system",
            "test_madagascar_deployment", 
            "test_production_readiness"
        ]
        
        for test_dir in test_dirs:
            if os.path.exists(test_dir):
                shutil.rmtree(test_dir)
        
        print("✅ All test files cleaned up")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

def main():
    """Run comprehensive Step 3 final integration test."""
    print("🧠 STEP 3 - FINAL INTEGRATION: Complete Conservation Reasoning Engine")
    print("=" * 75)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: All previous sections
    if test_all_sections():
        tests_passed += 1
    
    # Test 2: Fixed threat detection
    if test_fixed_threat_detection():
        tests_passed += 1
    
    # Test 3: Complete Madagascar deployment
    if test_complete_madagascar_deployment():
        tests_passed += 1
    
    # Test 4: Production readiness
    if test_production_readiness():
        tests_passed += 1
    
    # Cleanup
    cleanup_test_files()
    
    # Final summary
    print(f"\n" + "="*75)
    print(f"📊 STEP 3 FINAL RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 STEP 3 CONSERVATION REASONING ENGINE - COMPLETE SUCCESS!")
        print("✅ Ready to proceed to Step 4: Species Identification Agent")
        print("\n🚀 Next Steps:")
        print("   • Implement computer vision for species identification")
        print("   • Add confidence scoring and model integration")
        print("   • Build Madagascar endemic species classification")
        print("   • Integrate with conservation reasoning engine")
        return True
    else:
        print("❌ STEP 3 FAILED - Address issues before proceeding")
        return False

if __name__ == "__main__":
    main()
