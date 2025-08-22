"""
Step 3 Section 3: Integration with Memory System
================================================
Integrate conservation reasoning with the memory system from Step 2.
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

def test_memory_system_imports():
    """Test importing memory system components."""
    print("🧪 Testing Memory System Imports...")
    
    try:
        from step2_section2_test import SimpleConservationMemory
        print("✅ SimpleConservationMemory imported successfully")
        
        from step2_section3_test import create_memory_app, ConservationEvent
        print("✅ Memory API components imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Memory system import error: {e}")
        return False

class MemoryIntegratedReasoner(SimpleConservationReasoner):
    """Conservation reasoner integrated with memory system."""
    
    def __init__(self, memory_storage_dir: str = "reasoning_memory"):
        super().__init__()
        self.memory = SimpleConservationMemory(memory_storage_dir)
        self.memory_storage_dir = memory_storage_dir
    
    def load_facts_from_memory(self, entity_type: str = None, entity_name: str = None):
        """Load facts from memory system into reasoning facts."""
        try:
            # Load species memory
            if entity_type is None or entity_type == "species":
                for species_name, events in self.memory.species_memory.items():
                    if entity_name is None or species_name == entity_name:
                        for event in events:
                            fact_id = f"memory_species_{species_name}_{len(self.facts)}"
                            
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
            
            # Load site memory
            if entity_type is None or entity_type == "site":
                for site_name, events in self.memory.site_memory.items():
                    if entity_name is None or site_name == entity_name:
                        for event in events:
                            fact_id = f"memory_site_{site_name}_{len(self.facts)}"
                            
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
            
            return True
            
        except Exception as e:
            print(f"⚠️  Error loading facts from memory: {e}")
            return False
    
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

def test_memory_integrated_reasoner_creation():
    """Test creating memory-integrated reasoner."""
    print("\n🧠 Testing Memory-Integrated Reasoner Creation...")
    
    try:
        reasoner = MemoryIntegratedReasoner("test_reasoning_memory")
        print("✅ MemoryIntegratedReasoner created")
        
        # Check components
        if hasattr(reasoner, 'memory'):
            print("✅ Memory system integrated")
        else:
            print("❌ Memory system not integrated")
            return False
        
        if hasattr(reasoner, 'rules') and hasattr(reasoner, 'facts'):
            print("✅ Reasoning components present")
        else:
            print("❌ Reasoning components missing")
            return False
        
        return reasoner
        
    except Exception as e:
        print(f"❌ Memory-integrated reasoner creation error: {e}")
        return None

def test_memory_fact_loading():
    """Test loading facts from memory into reasoning system."""
    print("\n📥 Testing Memory Fact Loading...")
    
    try:
        reasoner = MemoryIntegratedReasoner("test_fact_loading")
        
        # First, store some data in memory
        species_event = {
            "event_type": "detection",
            "location": "centre_valbio",
            "confidence": 0.92,
            "observer": "camera_trap_02"
        }
        reasoner.memory.store_species_event("lemur_catta", species_event)
        
        site_event = {
            "event_type": "monitoring",
            "activity": "biodiversity_survey",
            "team_size": 4,
            "weather": "clear"
        }
        reasoner.memory.store_site_event("maromizaha", site_event)
        
        # Load facts from memory
        initial_fact_count = len(reasoner.facts)
        success = reasoner.load_facts_from_memory()
        
        if success:
            print("✅ Facts loaded from memory successfully")
        else:
            print("❌ Failed to load facts from memory")
            return False
        
        final_fact_count = len(reasoner.facts)
        if final_fact_count > initial_fact_count:
            print(f"✅ Fact count increased: {initial_fact_count} → {final_fact_count}")
        else:
            print("❌ No facts were loaded")
            return False
        
        # Check fact content
        species_facts = [f for f in reasoner.facts.values() if f.fact_type == "species"]
        site_facts = [f for f in reasoner.facts.values() if f.fact_type == "location"]
        
        if len(species_facts) > 0:
            print(f"✅ Species facts loaded: {len(species_facts)}")
        else:
            print("❌ No species facts loaded")
            return False
        
        if len(site_facts) > 0:
            print(f"✅ Site facts loaded: {len(site_facts)}")
        else:
            print("❌ No site facts loaded")
            return False
        
        return reasoner
        
    except Exception as e:
        print(f"❌ Memory fact loading error: {e}")
        return None

def test_reasoning_result_storage():
    """Test storing reasoning results back to memory."""
    print("\n📤 Testing Reasoning Result Storage...")
    
    try:
        reasoner = MemoryIntegratedReasoner("test_result_storage")
        
        # Add a simple rule and fact for reasoning
        fact = ConservationFact(
            fact_id="storage_test_fact",
            fact_type="species",
            entity="lemur_catta",
            attribute="detection_confidence",
            value=0.94,
            confidence=0.9,
            timestamp=datetime.utcnow(),
            source="test_camera"
        )
        reasoner.add_fact(fact)
        
        rule = ConservationRule(
            rule_id="storage_test_rule",
            name="Storage Test Rule",
            description="Test rule for result storage",
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
            actions=[ConservationAction.MONITOR],
            priority=6
        )
        reasoner.add_rule(rule)
        
        # Perform reasoning
        result = reasoner.reason()
        
        # Store result with context
        context = {"site": "centre_valbio", "scenario": "test_storage"}
        storage_success = reasoner.store_reasoning_result(result, context)
        
        if storage_success:
            print("✅ Reasoning result stored successfully")
        else:
            print("❌ Failed to store reasoning result")
            return False
        
        # Verify storage by checking memory
        site_memory = reasoner.memory.get_site_memory("centre_valbio")
        reasoning_events = [event for event in site_memory if event.get("event_type") == "reasoning_result"]
        
        if len(reasoning_events) > 0:
            print(f"✅ Reasoning events found in memory: {len(reasoning_events)}")
            latest_event = reasoning_events[-1]
            if "triggered_rules" in latest_event and "threat_level" in latest_event:
                print("✅ Reasoning event structure correct")
            else:
                print("❌ Reasoning event structure incorrect")
                return False
        else:
            print("❌ No reasoning events found in memory")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Reasoning result storage error: {e}")
        return False

def test_integrated_reasoning_workflow():
    """Test complete integrated reasoning workflow."""
    print("\n🔄 Testing Integrated Reasoning Workflow...")
    
    try:
        reasoner = MemoryIntegratedReasoner("test_integrated_workflow")
        
        # Step 1: Store conservation data in memory
        print("   📊 Step 1: Storing conservation data...")
        
        # Store multiple species detections
        species_events = [
            {
                "event_type": "detection",
                "location": "centre_valbio_area_a",
                "confidence": 0.96,
                "observer": "camera_trap_01"
            },
            {
                "event_type": "detection", 
                "location": "centre_valbio_area_b",
                "confidence": 0.89,
                "observer": "camera_trap_02"
            }
        ]
        
        for event in species_events:
            reasoner.memory.store_species_event("lemur_catta", event)
        
        # Store site activity
        site_events = [
            {
                "event_type": "monitoring",
                "activity": "morning_survey",
                "team_size": 3,
                "weather": "clear"
            },
            {
                "event_type": "threat_assessment",
                "activity": "perimeter_check", 
                "team_size": 2,
                "weather": "overcast"
            }
        ]
        
        for event in site_events:
            reasoner.memory.store_site_event("centre_valbio", event)
        
        print("   ✅ Conservation data stored")
        
        # Step 2: Add reasoning rules
        print("   📋 Step 2: Adding reasoning rules...")
        
        rules = [
            ConservationRule(
                rule_id="high_confidence_species",
                name="High Confidence Species Detection",
                description="Alert for high confidence species detections",
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
            ),
            ConservationRule(
                rule_id="site_activity_monitoring",
                name="Site Activity Monitoring",
                description="Monitor sites with regular activity",
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
                priority=5
            )
        ]
        
        for rule in rules:
            reasoner.add_rule(rule)
        
        print("   ✅ Reasoning rules added")
        
        # Step 3: Perform integrated reasoning
        print("   🧠 Step 3: Performing integrated reasoning...")
        
        context = {
            "site": "centre_valbio",
            "scenario": "integrated_workflow_test",
            "entity_type": "species",
            "entity_name": "lemur_catta"
        }
        
        result = reasoner.reason_with_memory(context)
        
        if len(result.triggered_rules) > 0:
            print(f"   ✅ Rules triggered: {result.triggered_rules}")
        else:
            print("   ❌ No rules triggered")
            return False
        
        if len(result.recommended_actions) > 0:
            print(f"   ✅ Actions recommended: {[a.value for a in result.recommended_actions]}")
        else:
            print("   ❌ No actions recommended")
            return False
        
        print(f"   ✅ Threat level: {result.threat_level.value}")
        print(f"   ✅ Confidence: {result.confidence:.2f}")
        
        # Step 4: Verify result storage
        print("   💾 Step 4: Verifying result storage...")
        
        site_memory = reasoner.memory.get_site_memory("centre_valbio")
        reasoning_events = [event for event in site_memory if event.get("event_type") == "reasoning_result"]
        
        if len(reasoning_events) > 0:
            print(f"   ✅ Reasoning results stored: {len(reasoning_events)}")
        else:
            print("   ❌ No reasoning results stored")
            return False
        
        # Step 5: Verify memory persistence
        print("   🔄 Step 5: Testing persistence...")
        
        # Create new reasoner instance (should load from disk)
        new_reasoner = MemoryIntegratedReasoner("test_integrated_workflow")
        
        # Load facts and reason again
        new_result = new_reasoner.reason_with_memory(context)
        
        if len(new_result.triggered_rules) > 0:
            print("   ✅ Persistence verified - new instance can reason with stored data")
        else:
            print("   ❌ Persistence failed")
            return False
        
        print("✅ Complete integrated workflow successful")
        return True
        
    except Exception as e:
        print(f"❌ Integrated workflow error: {e}")
        return False

def test_madagascar_integrated_scenarios():
    """Test integrated reasoning with Madagascar conservation scenarios."""
    print("\n🇲🇬 Testing Madagascar Integrated Scenarios...")
    
    try:
        reasoner = MemoryIntegratedReasoner("test_madagascar_integrated")
        
        # Scenario 1: Multi-day lemur monitoring at Centre ValBio
        print("\n   📅 Day 1: Initial Detection")
        
        day1_event = {
            "event_type": "species_detection",
            "location": "centre_valbio_trail_a",
            "confidence": 0.94,
            "observer": "field_researcher_jane",
            "notes": "Adult ring-tailed lemur with infant"
        }
        reasoner.memory.store_species_event("lemur_catta", day1_event)
        
        # Add monitoring rule
        monitoring_rule = ConservationRule(
            rule_id="lemur_family_monitoring",
            name="Lemur Family Monitoring Protocol",
            description="Enhanced monitoring for lemur families",
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
            actions=[ConservationAction.MONITOR, ConservationAction.INVESTIGATE],
            priority=8
        )
        reasoner.add_rule(monitoring_rule)
        
        day1_result = reasoner.reason_with_memory({
            "site": "centre_valbio",
            "day": "day_1",
            "entity_type": "species"
        })
        
        if "lemur_family_monitoring" in day1_result.triggered_rules:
            print("   ✅ Day 1 monitoring triggered")
        else:
            print("   ❌ Day 1 monitoring failed")
            return False
        
        # Scenario 2: Day 2 - Threat detection
        print("\n   🚨 Day 2: Threat Detection")
        
        threat_event = {
            "event_type": "threat_detection",
            "location": "centre_valbio_perimeter",
            "confidence": 0.87,
            "observer": "security_patrol",
            "notes": "Unusual human activity near protected area"
        }
        reasoner.memory.store_site_event("centre_valbio", threat_event)
        
        # Add threat response rule
        threat_rule = ConservationRule(
            rule_id="human_intrusion_response",
            name="Human Intrusion Response",
            description="Respond to potential human threats",
            conditions={
                "all": [
                    {
                        "fact_type": "location",
                        "entity": "centre_valbio",
                        "attribute": "activity_level",
                        "operator": "greater_than",
                        "value": 0,
                        "min_confidence": 0.8
                    }
                ]
            },
            actions=[ConservationAction.ALERT, ConservationAction.INVESTIGATE, ConservationAction.INTERVENE],
            priority=9
        )
        reasoner.add_rule(threat_rule)
        
        day2_result = reasoner.reason_with_memory({
            "site": "centre_valbio",
            "day": "day_2",
            "entity_type": "site"
        })
        
        if day2_result.threat_level == ThreatLevel.CRITICAL:
            print("   ✅ Day 2 threat escalation correct")
        else:
            print(f"   ⚠️  Expected CRITICAL, got {day2_result.threat_level.value}")
        
        # Scenario 3: Day 3 - Follow-up monitoring
        print("\n   📊 Day 3: Follow-up Analysis")
        
        followup_event = {
            "event_type": "follow_up_survey",
            "activity": "comprehensive_area_assessment",
            "team_size": 6,
            "weather": "clear",
            "notes": "Post-incident monitoring survey"
        }
        reasoner.memory.store_site_event("centre_valbio", followup_event)
        
        day3_result = reasoner.reason_with_memory({
            "site": "centre_valbio",
            "day": "day_3"
        })
        
        # Check reasoning history
        if len(reasoner.reasoning_history) >= 3:
            print(f"   ✅ Multi-day reasoning history: {len(reasoner.reasoning_history)} entries")
        else:
            print("   ❌ Insufficient reasoning history")
            return False
        
        # Analyze trend
        threat_levels = [r.threat_level for r in reasoner.reasoning_history[-3:]]
        print(f"   📈 Threat level trend: {[level.value for level in threat_levels]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Madagascar integrated scenario error: {e}")
        return False

def cleanup_test_files():
    """Clean up test files."""
    try:
        import shutil
        test_dirs = [
            "test_reasoning_memory", 
            "test_fact_loading", 
            "test_result_storage",
            "test_integrated_workflow",
            "test_madagascar_integrated"
        ]
        
        for test_dir in test_dirs:
            if os.path.exists(test_dir):
                shutil.rmtree(test_dir)
        
        print("✅ Test files cleaned up")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

def main():
    """Run Section 3 tests."""
    print("🧠 STEP 3 - SECTION 3: Integration with Memory System")
    print("=" * 55)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Memory system imports
    if test_memory_system_imports():
        tests_passed += 1
    
    # Test 2: Memory-integrated reasoner creation
    if test_memory_integrated_reasoner_creation():
        tests_passed += 1
    
    # Test 3: Memory fact loading
    if test_memory_fact_loading():
        tests_passed += 1
    
    # Test 4: Reasoning result storage
    if test_reasoning_result_storage():
        tests_passed += 1
    
    # Test 5: Integrated workflow
    if test_integrated_reasoning_workflow():
        tests_passed += 1
    
    # Test 6: Madagascar integrated scenarios
    if test_madagascar_integrated_scenarios():
        tests_passed += 1
    
    # Cleanup
    cleanup_test_files()
    
    # Summary
    print(f"\n📊 Section 3 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 3 PASSED - Ready for Section 4")
        return True
    else:
        print("❌ Section 3 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
