"""
Step 3 Section 2: Rule Evaluation Logic
=======================================
Test rule evaluation and basic reasoning functionality.
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Import from Section 1
from step3_section1_test import (
    ThreatLevel, ConservationAction, ConservationRule, 
    ConservationFact, ReasoningResult, SimpleConservationReasoner
)

def test_condition_evaluation():
    """Test individual condition evaluation logic."""
    print("🧪 Testing Condition Evaluation Logic...")
    
    try:
        reasoner = SimpleConservationReasoner()
        
        # Add a test fact
        fact = ConservationFact(
            fact_id="test_detection",
            fact_type="species",
            entity="lemur_catta",
            attribute="detection_confidence",
            value=0.92,
            confidence=0.88,
            timestamp=datetime.utcnow(),
            source="camera_trap_01"
        )
        reasoner.add_fact(fact)
        
        # Test equals condition
        condition1 = {
            "fact_type": "species",
            "entity": "lemur_catta",
            "attribute": "detection_confidence",
            "operator": "equals",
            "value": 0.92,
            "min_confidence": 0.8
        }
        
        result1 = reasoner.evaluate_condition(condition1, reasoner.facts)
        if result1:
            print("✅ Equals condition evaluation working")
        else:
            print("❌ Equals condition evaluation failed")
            return False
        
        # Test greater_than condition
        condition2 = {
            "fact_type": "species",
            "entity": "lemur_catta",
            "attribute": "detection_confidence",
            "operator": "greater_than",
            "value": 0.9,
            "min_confidence": 0.8
        }
        
        result2 = reasoner.evaluate_condition(condition2, reasoner.facts)
        if result2:
            print("✅ Greater_than condition evaluation working")
        else:
            print("❌ Greater_than condition evaluation failed")
            return False
        
        # Test less_than condition (should fail)
        condition3 = {
            "fact_type": "species",
            "entity": "lemur_catta",
            "attribute": "detection_confidence",
            "operator": "less_than",
            "value": 0.9,
            "min_confidence": 0.8
        }
        
        result3 = reasoner.evaluate_condition(condition3, reasoner.facts)
        if not result3:
            print("✅ Less_than condition evaluation working (correctly failed)")
        else:
            print("❌ Less_than condition evaluation incorrect")
            return False
        
        # Test nonexistent fact
        condition4 = {
            "fact_type": "species",
            "entity": "nonexistent_species",
            "attribute": "detection_confidence",
            "operator": "equals",
            "value": 0.5,
            "min_confidence": 0.8
        }
        
        result4 = reasoner.evaluate_condition(condition4, reasoner.facts)
        if not result4:
            print("✅ Nonexistent fact condition correctly failed")
        else:
            print("❌ Nonexistent fact condition should have failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Condition evaluation error: {e}")
        return False

def test_rule_evaluation():
    """Test complete rule evaluation."""
    print("\n📋 Testing Rule Evaluation...")
    
    try:
        reasoner = SimpleConservationReasoner()
        
        # Add facts
        fact1 = ConservationFact(
            fact_id="lemur_detection",
            fact_type="species",
            entity="lemur_catta",
            attribute="detection_confidence",
            value=0.95,
            confidence=0.9,
            timestamp=datetime.utcnow(),
            source="camera_trap_01"
        )
        
        fact2 = ConservationFact(
            fact_id="location_check",
            fact_type="location",
            entity="centre_valbio",
            attribute="threat_level",
            value="low",
            confidence=0.85,
            timestamp=datetime.utcnow(),
            source="security_system"
        )
        
        reasoner.add_fact(fact1)
        reasoner.add_fact(fact2)
        
        # Add rule that should trigger
        rule1 = ConservationRule(
            rule_id="high_confidence_detection",
            name="High Confidence Species Detection",
            description="Trigger when species detected with high confidence",
            conditions={
                "all": [
                    {
                        "fact_type": "species",
                        "entity": "lemur_catta",
                        "attribute": "detection_confidence",
                        "operator": "greater_than",
                        "value": 0.9,
                        "min_confidence": 0.8
                    }
                ]
            },
            actions=[ConservationAction.MONITOR, ConservationAction.ALERT],
            priority=7
        )
        
        reasoner.add_rule(rule1)
        
        # Test rule evaluation
        should_trigger, facts_used = reasoner.evaluate_rule(rule1)
        if should_trigger:
            print("✅ Rule correctly triggered")
            print(f"   📊 Facts used: {facts_used}")
        else:
            print("❌ Rule should have triggered")
            return False
        
        # Add rule that should NOT trigger
        rule2 = ConservationRule(
            rule_id="low_confidence_detection",
            name="Low Confidence Detection",
            description="Trigger only for low confidence",
            conditions={
                "all": [
                    {
                        "fact_type": "species",
                        "entity": "lemur_catta",
                        "attribute": "detection_confidence",
                        "operator": "less_than",
                        "value": 0.5,
                        "min_confidence": 0.8
                    }
                ]
            },
            actions=[ConservationAction.INVESTIGATE],
            priority=3
        )
        
        reasoner.add_rule(rule2)
        
        should_trigger2, facts_used2 = reasoner.evaluate_rule(rule2)
        if not should_trigger2:
            print("✅ Rule correctly did not trigger")
        else:
            print("❌ Rule should not have triggered")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Rule evaluation error: {e}")
        return False

def test_basic_reasoning():
    """Test complete reasoning process."""
    print("\n🧠 Testing Basic Reasoning Process...")
    
    try:
        reasoner = SimpleConservationReasoner()
        
        # Add conservation facts
        facts = [
            ConservationFact(
                fact_id="lemur_sighting",
                fact_type="species",
                entity="lemur_catta",
                attribute="detection_confidence",
                value=0.94,
                confidence=0.9,
                timestamp=datetime.utcnow(),
                source="field_researcher"
            ),
            ConservationFact(
                fact_id="threat_assessment",
                fact_type="threat",
                entity="deforestation",
                attribute="risk_level",
                value="medium",
                confidence=0.8,
                timestamp=datetime.utcnow(),
                source="satellite_analysis"
            ),
            ConservationFact(
                fact_id="site_status",
                fact_type="location",
                entity="maromizaha",
                attribute="protection_status",
                value="active",
                confidence=0.95,
                timestamp=datetime.utcnow(),
                source="park_authority"
            )
        ]
        
        for fact in facts:
            reasoner.add_fact(fact)
        
        # Add conservation rules
        rules = [
            ConservationRule(
                rule_id="species_monitoring",
                name="Species Monitoring Alert",
                description="Monitor high-confidence species detections",
                conditions={
                    "all": [
                        {
                            "fact_type": "species",
                            "entity": "lemur_catta",
                            "attribute": "detection_confidence",
                            "operator": "greater_than",
                            "value": 0.9,
                            "min_confidence": 0.85
                        }
                    ]
                },
                actions=[ConservationAction.MONITOR],
                priority=5
            ),
            ConservationRule(
                rule_id="threat_response",
                name="Threat Response Protocol",
                description="Respond to medium or high threats",
                conditions={
                    "all": [
                        {
                            "fact_type": "threat",
                            "entity": "deforestation",
                            "attribute": "risk_level",
                            "operator": "contains",
                            "value": "medium",
                            "min_confidence": 0.7
                        }
                    ]
                },
                actions=[ConservationAction.INVESTIGATE, ConservationAction.ALERT],
                priority=8
            )
        ]
        
        for rule in rules:
            reasoner.add_rule(rule)
        
        # Perform reasoning
        result = reasoner.reason()
        
        # Validate results
        if len(result.triggered_rules) > 0:
            print(f"✅ Reasoning triggered {len(result.triggered_rules)} rules")
            print(f"   📋 Rules: {result.triggered_rules}")
        else:
            print("❌ No rules triggered")
            return False
        
        if len(result.recommended_actions) > 0:
            print(f"✅ Recommended {len(result.recommended_actions)} actions")
            print(f"   🎯 Actions: {[action.value for action in result.recommended_actions]}")
        else:
            print("❌ No actions recommended")
            return False
        
        if result.threat_level:
            print(f"✅ Threat level assessed: {result.threat_level.value}")
        else:
            print("❌ No threat level assessed")
            return False
        
        if result.confidence > 0:
            print(f"✅ Confidence calculated: {result.confidence:.2f}")
        else:
            print("❌ No confidence calculated")
            return False
        
        if result.reasoning:
            print(f"✅ Reasoning explanation: {result.reasoning}")
        else:
            print("❌ No reasoning explanation")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Basic reasoning error: {e}")
        return False

def test_madagascar_scenarios():
    """Test reasoning with Madagascar conservation scenarios."""
    print("\n🇲🇬 Testing Madagascar Conservation Scenarios...")
    
    try:
        reasoner = SimpleConservationReasoner()
        
        # Scenario 1: Ring-tailed lemur detection at Centre ValBio
        print("\n📸 Scenario 1: Lemur Detection at Centre ValBio")
        
        lemur_fact = ConservationFact(
            fact_id="valbio_lemur_detection",
            fact_type="species",
            entity="lemur_catta",
            attribute="detection_confidence",
            value=0.96,
            confidence=0.92,
            timestamp=datetime.utcnow(),
            source="centre_valbio_camera_trap_03"
        )
        reasoner.add_fact(lemur_fact)
        
        lemur_rule = ConservationRule(
            rule_id="valbio_lemur_monitoring",
            name="Centre ValBio Lemur Monitoring",
            description="Monitor lemur activity at research station",
            conditions={
                "all": [
                    {
                        "fact_type": "species",
                        "entity": "lemur_catta",
                        "attribute": "detection_confidence",
                        "operator": "greater_than",
                        "value": 0.9,
                        "min_confidence": 0.85
                    }
                ]
            },
            actions=[ConservationAction.MONITOR, ConservationAction.ALERT],
            priority=6
        )
        reasoner.add_rule(lemur_rule)
        
        result1 = reasoner.reason()
        if "valbio_lemur_monitoring" in result1.triggered_rules:
            print("✅ Lemur detection scenario triggered correctly")
        else:
            print("❌ Lemur detection scenario failed")
            return False
        
        # Scenario 2: Deforestation threat at Maromizaha
        print("\n🌳 Scenario 2: Deforestation Threat at Maromizaha")
        
        threat_fact = ConservationFact(
            fact_id="maromizaha_deforestation",
            fact_type="threat",
            entity="deforestation",
            attribute="severity",
            value=0.75,
            confidence=0.88,
            timestamp=datetime.utcnow(),
            source="satellite_monitoring_system"
        )
        reasoner.add_fact(threat_fact)
        
        threat_rule = ConservationRule(
            rule_id="deforestation_alert",
            name="Deforestation Alert System",
            description="Alert on high deforestation risk",
            conditions={
                "all": [
                    {
                        "fact_type": "threat",
                        "entity": "deforestation",
                        "attribute": "severity",
                        "operator": "greater_than",
                        "value": 0.7,
                        "min_confidence": 0.8
                    }
                ]
            },
            actions=[ConservationAction.ALERT, ConservationAction.INTERVENE],
            priority=9
        )
        reasoner.add_rule(threat_rule)
        
        result2 = reasoner.reason()
        if "deforestation_alert" in result2.triggered_rules:
            print("✅ Deforestation threat scenario triggered correctly")
            print(f"   🚨 Threat level: {result2.threat_level.value}")
        else:
            print("❌ Deforestation threat scenario failed")
            return False
        
        # Verify threat escalation
        if result2.threat_level == ThreatLevel.CRITICAL:
            print("✅ Threat level correctly escalated to CRITICAL")
        else:
            print(f"⚠️  Expected CRITICAL, got {result2.threat_level.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Madagascar scenario error: {e}")
        return False

def test_multiple_conditions():
    """Test rules with multiple conditions."""
    print("\n🔗 Testing Multiple Condition Rules...")
    
    try:
        reasoner = SimpleConservationReasoner()
        
        # Add multiple facts
        facts = [
            ConservationFact(
                fact_id="species_detected",
                fact_type="species",
                entity="indri_indri",
                attribute="detection_confidence",
                value=0.91,
                confidence=0.89,
                timestamp=datetime.utcnow(),
                source="acoustic_sensor"
            ),
            ConservationFact(
                fact_id="time_of_day",
                fact_type="environmental",
                entity="observation_time",
                attribute="hour",
                value=6,  # Early morning
                confidence=1.0,
                timestamp=datetime.utcnow(),
                source="system_clock"
            ),
            ConservationFact(
                fact_id="weather_status",
                fact_type="environmental",
                entity="weather",
                attribute="condition",
                value="clear",
                confidence=0.95,
                timestamp=datetime.utcnow(),
                source="weather_station"
            )
        ]
        
        for fact in facts:
            reasoner.add_fact(fact)
        
        # Rule requiring multiple conditions
        complex_rule = ConservationRule(
            rule_id="optimal_observation",
            name="Optimal Observation Conditions",
            description="Trigger when species detected under optimal conditions",
            conditions={
                "all": [
                    {
                        "fact_type": "species",
                        "entity": "indri_indri",
                        "attribute": "detection_confidence",
                        "operator": "greater_than",
                        "value": 0.9,
                        "min_confidence": 0.8
                    },
                    {
                        "fact_type": "environmental",
                        "entity": "observation_time",
                        "attribute": "hour",
                        "operator": "less_than",
                        "value": 8,  # Before 8 AM
                        "min_confidence": 0.9
                    },
                    {
                        "fact_type": "environmental",
                        "entity": "weather",
                        "attribute": "condition",
                        "operator": "equals",
                        "value": "clear",
                        "min_confidence": 0.9
                    }
                ]
            },
            actions=[ConservationAction.MONITOR, ConservationAction.INVESTIGATE],
            priority=7
        )
        
        reasoner.add_rule(complex_rule)
        
        result = reasoner.reason()
        
        if "optimal_observation" in result.triggered_rules:
            print("✅ Multiple condition rule triggered correctly")
            print(f"   📊 Facts used: {len(result.facts_used)}")
        else:
            print("❌ Multiple condition rule failed")
            return False
        
        # Test partial condition failure
        # Remove one fact to break the rule
        del reasoner.facts["weather_status"]
        
        result2 = reasoner.reason()
        if "optimal_observation" not in result2.triggered_rules:
            print("✅ Rule correctly failed with missing condition")
        else:
            print("❌ Rule should have failed with missing condition")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Multiple condition test error: {e}")
        return False

def test_reasoning_history():
    """Test reasoning history tracking."""
    print("\n📚 Testing Reasoning History...")
    
    try:
        reasoner = SimpleConservationReasoner()
        
        # Add a simple fact and rule
        fact = ConservationFact(
            fact_id="history_test",
            fact_type="species",
            entity="test_species",
            attribute="confidence",
            value=0.95,
            confidence=0.9,
            timestamp=datetime.utcnow(),
            source="test_source"
        )
        reasoner.add_fact(fact)
        
        rule = ConservationRule(
            rule_id="history_rule",
            name="History Test Rule",
            description="Test rule for history tracking",
            conditions={
                "all": [
                    {
                        "fact_type": "species",
                        "entity": "test_species",
                        "attribute": "confidence",
                        "operator": "greater_than",
                        "value": 0.9,
                        "min_confidence": 0.8
                    }
                ]
            },
            actions=[ConservationAction.MONITOR],
            priority=5
        )
        reasoner.add_rule(rule)
        
        # Perform multiple reasoning cycles
        initial_history_length = len(reasoner.reasoning_history)
        
        result1 = reasoner.reason()
        result2 = reasoner.reason()
        result3 = reasoner.reason()
        
        final_history_length = len(reasoner.reasoning_history)
        
        if final_history_length == initial_history_length + 3:
            print("✅ Reasoning history correctly tracked")
            print(f"   📈 History entries: {final_history_length}")
        else:
            print(f"❌ History tracking failed: expected {initial_history_length + 3}, got {final_history_length}")
            return False
        
        # Check history content
        latest_result = reasoner.reasoning_history[-1]
        if latest_result.triggered_rules == result3.triggered_rules:
            print("✅ Latest history entry matches current result")
        else:
            print("❌ History entry mismatch")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Reasoning history error: {e}")
        return False

def main():
    """Run Section 2 tests."""
    print("🧠 STEP 3 - SECTION 2: Rule Evaluation Logic")
    print("=" * 48)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Condition evaluation
    if test_condition_evaluation():
        tests_passed += 1
    
    # Test 2: Rule evaluation
    if test_rule_evaluation():
        tests_passed += 1
    
    # Test 3: Basic reasoning
    if test_basic_reasoning():
        tests_passed += 1
    
    # Test 4: Madagascar scenarios
    if test_madagascar_scenarios():
        tests_passed += 1
    
    # Test 5: Multiple conditions
    if test_multiple_conditions():
        tests_passed += 1
    
    # Test 6: Reasoning history
    if test_reasoning_history():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Section 2 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 2 PASSED - Ready for Section 3")
        return True
    else:
        print("❌ Section 2 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
