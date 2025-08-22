"""
Step 3 Section 1: Basic Rule Engine Foundation
==============================================
Build the foundation for conservation reasoning with basic rule engine.
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

def test_basic_imports():
    """Test basic imports for rule engine."""
    print("🧪 Testing Basic Rule Engine Imports...")
    
    try:
        from dataclasses import dataclass
        from enum import Enum
        from typing import Dict, List, Any, Optional, Tuple
        print("✅ Core Python imports successful")
        
        # Test JSON for rule storage
        import json
        print("✅ JSON rule storage import successful")
        
        # Test datetime for temporal rules
        from datetime import datetime, timedelta
        print("✅ DateTime imports successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

class ThreatLevel(Enum):
    """Enumeration for threat severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ConservationAction(Enum):
    """Enumeration for conservation actions."""
    MONITOR = "monitor"
    INVESTIGATE = "investigate"
    INTERVENE = "intervene"
    ALERT = "alert"
    EMERGENCY = "emergency"

@dataclass
class ConservationRule:
    """Basic conservation rule structure."""
    rule_id: str
    name: str
    description: str
    conditions: Dict[str, Any]
    actions: List[ConservationAction]
    priority: int
    active: bool = True

@dataclass
class ConservationFact:
    """Basic conservation fact structure."""
    fact_id: str
    fact_type: str  # "species", "threat", "location", "environmental"
    entity: str     # specific entity name
    attribute: str  # what we know about it
    value: Any      # the actual value
    confidence: float
    timestamp: datetime
    source: str

@dataclass
class ReasoningResult:
    """Result of conservation reasoning."""
    triggered_rules: List[str]
    recommended_actions: List[ConservationAction]
    threat_level: ThreatLevel
    confidence: float
    reasoning: str
    facts_used: List[str]

class SimpleConservationReasoner:
    """Simple rule-based conservation reasoning engine."""
    
    def __init__(self):
        self.rules: List[ConservationRule] = []
        self.facts: Dict[str, ConservationFact] = {}
        self.reasoning_history: List[ReasoningResult] = []
    
    def add_rule(self, rule: ConservationRule):
        """Add a conservation rule."""
        self.rules.append(rule)
    
    def add_fact(self, fact: ConservationFact):
        """Add a conservation fact."""
        self.facts[fact.fact_id] = fact
    
    def evaluate_condition(self, condition: Dict[str, Any], facts: Dict[str, ConservationFact]) -> bool:
        """Evaluate a single condition against available facts."""
        try:
            fact_type = condition.get("fact_type")
            entity = condition.get("entity")
            attribute = condition.get("attribute")
            operator = condition.get("operator", "equals")
            expected_value = condition.get("value")
            min_confidence = condition.get("min_confidence", 0.0)
            
            # Find matching facts
            matching_facts = [
                fact for fact in facts.values()
                if (fact.fact_type == fact_type and 
                    fact.entity == entity and 
                    fact.attribute == attribute and
                    fact.confidence >= min_confidence)
            ]
            
            if not matching_facts:
                return False
            
            # Use the most confident fact
            best_fact = max(matching_facts, key=lambda f: f.confidence)
            
            # Apply operator
            if operator == "equals":
                return best_fact.value == expected_value
            elif operator == "greater_than":
                return float(best_fact.value) > float(expected_value)
            elif operator == "less_than":
                return float(best_fact.value) < float(expected_value)
            elif operator == "contains":
                return str(expected_value).lower() in str(best_fact.value).lower()
            else:
                return False
                
        except Exception as e:
            print(f"⚠️  Condition evaluation error: {e}")
            return False
    
    def evaluate_rule(self, rule: ConservationRule) -> Tuple[bool, List[str]]:
        """Evaluate if a rule should trigger."""
        if not rule.active:
            return False, []
        
        used_facts = []
        
        # Check all conditions (AND logic for now)
        for condition in rule.conditions.get("all", []):
            if not self.evaluate_condition(condition, self.facts):
                return False, used_facts
            
            # Track which facts were used
            fact_type = condition.get("fact_type")
            entity = condition.get("entity")
            attribute = condition.get("attribute")
            fact_key = f"{fact_type}_{entity}_{attribute}"
            used_facts.append(fact_key)
        
        return True, used_facts
    
    def reason(self, context: Dict[str, Any] = None) -> ReasoningResult:
        """Perform conservation reasoning."""
        triggered_rules = []
        all_actions = []
        all_facts_used = []
        max_priority = 0
        
        # Evaluate all rules
        for rule in self.rules:
            should_trigger, facts_used = self.evaluate_rule(rule)
            if should_trigger:
                triggered_rules.append(rule.rule_id)
                all_actions.extend(rule.actions)
                all_facts_used.extend(facts_used)
                max_priority = max(max_priority, rule.priority)
        
        # Determine threat level based on triggered rules
        if max_priority >= 9:
            threat_level = ThreatLevel.CRITICAL
        elif max_priority >= 7:
            threat_level = ThreatLevel.HIGH
        elif max_priority >= 5:
            threat_level = ThreatLevel.MEDIUM
        else:
            threat_level = ThreatLevel.LOW
        
        # Deduplicate actions
        unique_actions = list(set(all_actions))
        
        # Calculate confidence (simplified)
        confidence = min(1.0, len(triggered_rules) * 0.3) if triggered_rules else 0.0
        
        # Create reasoning explanation
        reasoning = f"Triggered {len(triggered_rules)} rules with max priority {max_priority}"
        if triggered_rules:
            reasoning += f". Rules: {', '.join(triggered_rules)}"
        
        result = ReasoningResult(
            triggered_rules=triggered_rules,
            recommended_actions=unique_actions,
            threat_level=threat_level,
            confidence=confidence,
            reasoning=reasoning,
            facts_used=list(set(all_facts_used))
        )
        
        self.reasoning_history.append(result)
        return result

def test_enum_definitions():
    """Test enumeration definitions."""
    print("\n📋 Testing Enum Definitions...")
    
    try:
        # Test ThreatLevel
        threat = ThreatLevel.HIGH
        print(f"✅ ThreatLevel enum: {threat.value}")
        
        # Test ConservationAction
        action = ConservationAction.INVESTIGATE
        print(f"✅ ConservationAction enum: {action.value}")
        
        # Test all values
        threat_levels = [level.value for level in ThreatLevel]
        actions = [action.value for action in ConservationAction]
        
        print(f"✅ Threat levels: {threat_levels}")
        print(f"✅ Conservation actions: {actions}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enum test error: {e}")
        return False

def test_dataclass_definitions():
    """Test dataclass definitions."""
    print("\n📊 Testing Dataclass Definitions...")
    
    try:
        # Test ConservationRule
        rule = ConservationRule(
            rule_id="test_rule_001",
            name="Test Species Detection",
            description="Test rule for species detection",
            conditions={"all": []},
            actions=[ConservationAction.MONITOR],
            priority=5
        )
        print(f"✅ ConservationRule created: {rule.name}")
        
        # Test ConservationFact
        fact = ConservationFact(
            fact_id="test_fact_001",
            fact_type="species",
            entity="lemur_catta",
            attribute="detection_confidence",
            value=0.95,
            confidence=0.9,
            timestamp=datetime.utcnow(),
            source="field_camera_01"
        )
        print(f"✅ ConservationFact created: {fact.entity}")
        
        # Test ReasoningResult
        result = ReasoningResult(
            triggered_rules=["test_rule_001"],
            recommended_actions=[ConservationAction.MONITOR],
            threat_level=ThreatLevel.LOW,
            confidence=0.8,
            reasoning="Test reasoning",
            facts_used=["test_fact_001"]
        )
        print(f"✅ ReasoningResult created: {result.threat_level.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Dataclass test error: {e}")
        return False

def test_simple_reasoner_creation():
    """Test creating simple conservation reasoner."""
    print("\n🧠 Testing Simple Reasoner Creation...")
    
    try:
        reasoner = SimpleConservationReasoner()
        print("✅ SimpleConservationReasoner created")
        
        # Test initial state
        if len(reasoner.rules) == 0:
            print("✅ Initial rules list empty")
        
        if len(reasoner.facts) == 0:
            print("✅ Initial facts dict empty")
        
        if len(reasoner.reasoning_history) == 0:
            print("✅ Initial reasoning history empty")
        
        return reasoner
        
    except Exception as e:
        print(f"❌ Reasoner creation error: {e}")
        return None

def test_basic_rule_addition():
    """Test adding basic rules to reasoner."""
    print("\n📝 Testing Basic Rule Addition...")
    
    try:
        reasoner = SimpleConservationReasoner()
        
        # Create a simple rule
        rule = ConservationRule(
            rule_id="lemur_detection_rule",
            name="Lemur Detection Alert",
            description="Alert when lemur is detected with high confidence",
            conditions={
                "all": [
                    {
                        "fact_type": "species",
                        "entity": "lemur_catta",
                        "attribute": "detection_confidence",
                        "operator": "greater_than",
                        "value": 0.8,
                        "min_confidence": 0.7
                    }
                ]
            },
            actions=[ConservationAction.MONITOR, ConservationAction.ALERT],
            priority=6
        )
        
        reasoner.add_rule(rule)
        print("✅ Rule added successfully")
        
        if len(reasoner.rules) == 1:
            print("✅ Rule count correct")
        
        if reasoner.rules[0].rule_id == "lemur_detection_rule":
            print("✅ Rule ID matches")
        
        return reasoner
        
    except Exception as e:
        print(f"❌ Rule addition error: {e}")
        return None

def test_basic_fact_addition():
    """Test adding basic facts to reasoner."""
    print("\n📊 Testing Basic Fact Addition...")
    
    try:
        reasoner = SimpleConservationReasoner()
        
        # Create a simple fact
        fact = ConservationFact(
            fact_id="lemur_detection_001",
            fact_type="species",
            entity="lemur_catta",
            attribute="detection_confidence",
            value=0.95,
            confidence=0.9,
            timestamp=datetime.utcnow(),
            source="field_camera_trap_01"
        )
        
        reasoner.add_fact(fact)
        print("✅ Fact added successfully")
        
        if len(reasoner.facts) == 1:
            print("✅ Fact count correct")
        
        if "lemur_detection_001" in reasoner.facts:
            print("✅ Fact ID found in facts dict")
        
        return reasoner
        
    except Exception as e:
        print(f"❌ Fact addition error: {e}")
        return None

def main():
    """Run Section 1 tests."""
    print("🧠 STEP 3 - SECTION 1: Basic Rule Engine Foundation")
    print("=" * 55)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Basic imports
    if test_basic_imports():
        tests_passed += 1
    
    # Test 2: Enum definitions
    if test_enum_definitions():
        tests_passed += 1
    
    # Test 3: Dataclass definitions
    if test_dataclass_definitions():
        tests_passed += 1
    
    # Test 4: Reasoner creation
    if test_simple_reasoner_creation():
        tests_passed += 1
    
    # Test 5: Rule addition
    if test_basic_rule_addition():
        tests_passed += 1
    
    # Test 6: Fact addition
    if test_basic_fact_addition():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Section 1 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 1 PASSED - Ready for Section 2")
        return True
    else:
        print("❌ Section 1 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
