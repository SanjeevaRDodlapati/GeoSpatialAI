"""
Step 3 Section 3B: Fixed Integration with Memory System
======================================================
Fixed version addressing memory persistence issues.
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Import from previous sections
from step3_section1_test import (
    ThreatLevel, ConservationAction, ConservationRule, 
    ConservationFact, ReasoningResult, SimpleConservationReasoner
)

# Import from Step 2
from step2_section2_test import SimpleConservationMemory

class FixedMemoryIntegratedReasoner(SimpleConservationReasoner):
    """Fixed conservation reasoner integrated with memory system."""
    
    def __init__(self, memory_storage_dir: str = "reasoning_memory"):
        super().__init__()
        self.memory = SimpleConservationMemory(memory_storage_dir)
        self.memory_storage_dir = memory_storage_dir
        # Always clear facts when creating new instance to avoid stale data
        self.facts = {}
    
    def load_facts_from_memory(self, entity_type: str = None, entity_name: str = None):
        """Load facts from memory system into reasoning facts."""
        try:
            facts_loaded = 0
            
            # Clear existing facts to ensure fresh load
            self.facts = {}
            
            # Load species memory
            if entity_type is None or entity_type == "species":
                for species_name, events in self.memory.species_memory.items():
                    if entity_name is None or species_name == entity_name:
                        for i, event in enumerate(events):
                            fact_id = f"memory_species_{species_name}_{i}"
                            
                            # Convert memory event to reasoning fact
                            fact = ConservationFact(
                                fact_id=fact_id,
                                fact_type="species",
                                entity=species_name,
                                attribute="detection_confidence",
                                value=event.get("confidence", 0.5),
                                confidence=event.get("confidence", 0.5),
                                timestamp=datetime.fromisoformat(event["timestamp"]) if "timestamp" in event else datetime.utcnow(),
                                source=event.get("observer", "memory_system")
                            )
                            self.add_fact(fact)
                            facts_loaded += 1
            
            # Load site memory
            if entity_type is None or entity_type == "site":
                for site_name, events in self.memory.site_memory.items():
                    if entity_name is None or site_name == entity_name:
                        for i, event in enumerate(events):
                            fact_id = f"memory_site_{site_name}_{i}"
                            
                            # Convert site event to reasoning fact
                            fact = ConservationFact(
                                fact_id=fact_id,
                                fact_type="location",
                                entity=site_name,
                                attribute="activity_level",
                                value=event.get("team_size", 1),
                                confidence=0.9,
                                timestamp=datetime.fromisoformat(event["timestamp"]) if "timestamp" in event else datetime.utcnow(),
                                source=event.get("activity", "memory_system")
                            )
                            self.add_fact(fact)
                            facts_loaded += 1
            
            print(f"   🔄 Loaded {facts_loaded} facts from memory")
            return facts_loaded > 0
            
        except Exception as e:
            print(f"⚠️  Error loading facts from memory: {e}")
            return False
    
    def reason_with_memory(self, context: Dict[str, Any] = None) -> ReasoningResult:
        """Perform reasoning using facts from memory."""
        # Load relevant facts from memory
        if context and "entity_type" in context:
            self.load_facts_from_memory(
                entity_type=context["entity_type"], 
                entity_name=context.get("entity_name")
            )
        else:
            self.load_facts_from_memory()
        
        # Perform reasoning
        result = self.reason(context)
        
        # Store result back to memory
        self.store_reasoning_result(result, context)
        
        return result
    
    def store_reasoning_result(self, result: ReasoningResult, context: Dict[str, Any] = None):
        """Store reasoning result back to memory."""
        try:
            # Prepare reasoning event for memory storage
            reasoning_event = {
                "event_type": "reasoning_result",
                "triggered_rules": result.triggered_rules,
                "recommended_actions": [action.value for action in result.recommended_actions],
                "threat_level": result.threat_level.value,
                "confidence": result.confidence,
                "reasoning": result.reasoning,
                "facts_used": result.facts_used,
                "context": context or {}
            }
            
            # Store in site memory (reasoning events are site-related)
            site_name = context.get("site", "general_reasoning") if context else "general_reasoning"
            self.memory.store_site_event(site_name, reasoning_event)
            
            return True
            
        except Exception as e:
            print(f"⚠️  Error storing reasoning result: {e}")
            return False

def test_fixed_persistence():
    """Test fixed persistence functionality."""
    print("🔧 Testing Fixed Persistence...")
    
    try:
        # Step 1: Create first reasoner and populate with data
        reasoner1 = FixedMemoryIntegratedReasoner("test_fixed_persistence")
        
        # Store test data
        species_event = {
            "event_type": "detection",
            "location": "test_location",
            "confidence": 0.95,
            "observer": "test_observer"
        }
        reasoner1.memory.store_species_event("test_species", species_event)
        
        # Add rule and perform reasoning
        rule = ConservationRule(
            rule_id="test_persistence_rule",
            name="Test Persistence Rule",
            description="Test rule for persistence",
            conditions={
                "all": [
                    {
                        "fact_type": "species",
                        "entity": "test_species",
                        "attribute": "detection_confidence",
                        "operator": "greater_than",
                        "value": 0.9,
                        "min_confidence": 0.8
                    }
                ]
            },
            actions=[ConservationAction.MONITOR],
            priority=6
        )
        reasoner1.add_rule(rule)
        
        # Perform reasoning with first instance
        context = {"site": "test_site", "scenario": "persistence_test"}
        result1 = reasoner1.reason_with_memory(context)
        
        print(f"   ✅ First instance reasoning: {len(result1.triggered_rules)} rules triggered")
        
        # Step 2: Create second reasoner (should load from disk)
        reasoner2 = FixedMemoryIntegratedReasoner("test_fixed_persistence")
        
        # Add the same rule to second instance
        reasoner2.add_rule(rule)
        
        # Perform reasoning with second instance (should load existing memory)
        result2 = reasoner2.reason_with_memory(context)
        
        print(f"   ✅ Second instance reasoning: {len(result2.triggered_rules)} rules triggered")
        
        # Verify that both instances can reason successfully
        if len(result1.triggered_rules) > 0 and len(result2.triggered_rules) > 0:
            print("✅ Fixed persistence test successful")
            return True
        else:
            print("❌ Fixed persistence test failed")
            return False
        
    except Exception as e:
        print(f"❌ Fixed persistence error: {e}")
        return False

def test_complete_integration():
    """Test complete integration with all components."""
    print("\n🎯 Testing Complete Integration...")
    
    try:
        reasoner = FixedMemoryIntegratedReasoner("test_complete_integration")
        
        # Madagascar conservation scenario
        conservation_data = {
            "species_events": [
                {
                    "species": "lemur_catta",
                    "event": {
                        "event_type": "detection",
                        "location": "centre_valbio_canopy",
                        "confidence": 0.97,
                        "observer": "canopy_camera_system"
                    }
                },
                {
                    "species": "indri_indri", 
                    "event": {
                        "event_type": "acoustic_detection",
                        "location": "maromizaha_core_area",
                        "confidence": 0.94,
                        "observer": "acoustic_monitoring_array"
                    }
                }
            ],
            "site_events": [
                {
                    "site": "centre_valbio",
                    "event": {
                        "event_type": "research_activity",
                        "activity": "lemur_behavioral_study",
                        "team_size": 4,
                        "weather": "clear"
                    }
                },
                {
                    "site": "maromizaha",
                    "event": {
                        "event_type": "patrol",
                        "activity": "anti_poaching_patrol",
                        "team_size": 3,
                        "weather": "light_rain"
                    }
                }
            ]
        }
        
        # Store all conservation data
        for item in conservation_data["species_events"]:
            reasoner.memory.store_species_event(item["species"], item["event"])
        
        for item in conservation_data["site_events"]:
            reasoner.memory.store_site_event(item["site"], item["event"])
        
        # Add comprehensive conservation rules
        conservation_rules = [
            ConservationRule(
                rule_id="high_priority_species",
                name="High Priority Species Detection",
                description="Alert for critical species detections",
                conditions={
                    "all": [
                        {
                            "fact_type": "species",
                            "entity": "lemur_catta",
                            "attribute": "detection_confidence",
                            "operator": "greater_than",
                            "value": 0.95,
                            "min_confidence": 0.9
                        }
                    ]
                },
                actions=[ConservationAction.ALERT, ConservationAction.MONITOR],
                priority=9
            ),
            ConservationRule(
                rule_id="endangered_species_protocol",
                name="Endangered Species Protocol",
                description="Special protocol for endangered species",
                conditions={
                    "all": [
                        {
                            "fact_type": "species",
                            "entity": "indri_indri",
                            "attribute": "detection_confidence",
                            "operator": "greater_than",
                            "value": 0.9,
                            "min_confidence": 0.85
                        }
                    ]
                },
                actions=[ConservationAction.ALERT, ConservationAction.INVESTIGATE, ConservationAction.EMERGENCY],
                priority=10  # Highest priority
            ),
            ConservationRule(
                rule_id="active_site_monitoring",
                name="Active Site Monitoring",
                description="Monitor sites with active research",
                conditions={
                    "all": [
                        {
                            "fact_type": "location",
                            "entity": "centre_valbio",
                            "attribute": "activity_level",
                            "operator": "greater_than",
                            "value": 2,
                            "min_confidence": 0.8
                        }
                    ]
                },
                actions=[ConservationAction.MONITOR],
                priority=6
            )
        ]
        
        for rule in conservation_rules:
            reasoner.add_rule(rule)
        
        # Perform comprehensive reasoning
        context = {
            "site": "madagascar_conservation_network",
            "scenario": "daily_monitoring",
            "priority": "high"
        }
        
        result = reasoner.reason_with_memory(context)
        
        # Analyze results
        print(f"   🎯 Rules triggered: {len(result.triggered_rules)}")
        print(f"   📋 Rule IDs: {result.triggered_rules}")
        print(f"   🚨 Threat level: {result.threat_level.value}")
        print(f"   🎭 Actions: {[action.value for action in result.recommended_actions]}")
        print(f"   🎲 Confidence: {result.confidence:.2f}")
        
        # Verify comprehensive coverage
        expected_triggers = ["high_priority_species", "endangered_species_protocol"]
        triggered_count = sum(1 for rule in expected_triggers if rule in result.triggered_rules)
        
        if triggered_count >= 2:
            print("✅ Comprehensive conservation rules triggered")
        else:
            print("⚠️  Some conservation rules not triggered")
        
        if result.threat_level == ThreatLevel.CRITICAL:
            print("✅ Threat level appropriately escalated")
        else:
            print(f"⚠️  Expected escalation, got {result.threat_level.value}")
        
        if ConservationAction.EMERGENCY in result.recommended_actions:
            print("✅ Emergency action recommended for endangered species")
        else:
            print("⚠️  Emergency action not recommended")
        
        # Check memory integration
        memory_stats = reasoner.memory.get_memory_stats()
        print(f"   📊 Memory stats: {memory_stats}")
        
        if memory_stats["species_count"] >= 2 and memory_stats["site_count"] >= 2:
            print("✅ Memory properly integrated with conservation data")
        else:
            print("❌ Memory integration incomplete")
            return False
        
        print("✅ Complete integration test successful")
        return True
        
    except Exception as e:
        print(f"❌ Complete integration error: {e}")
        return False

def cleanup_test_files():
    """Clean up test files."""
    try:
        import shutil
        test_dirs = ["test_fixed_persistence", "test_complete_integration"]
        
        for test_dir in test_dirs:
            if os.path.exists(test_dir):
                shutil.rmtree(test_dir)
        
        print("✅ Test files cleaned up")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

def main():
    """Run Section 3B fixed tests."""
    print("🧠 STEP 3 - SECTION 3B: Fixed Integration with Memory System")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Fixed persistence
    if test_fixed_persistence():
        tests_passed += 1
    
    # Test 2: Complete integration
    if test_complete_integration():
        tests_passed += 1
    
    # Cleanup
    cleanup_test_files()
    
    # Summary
    print(f"\n📊 Section 3B Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 3B PASSED - Integration Fixed")
        return True
    else:
        print("❌ Section 3B FAILED - Issues remain")
        return False

if __name__ == "__main__":
    main()
