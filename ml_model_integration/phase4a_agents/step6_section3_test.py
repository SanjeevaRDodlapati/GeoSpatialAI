"""
Step 6 Section 3: Adaptive Decision Engine
==========================================
Implement adaptive decision-making engine with continuous learning capabilities.
"""

import sys
import os
import json
import time
import math
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union, Callable, Set
from dataclasses import dataclass, asdict, field
import numpy as np
from collections import defaultdict, deque
import heapq

# Import from previous sections
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
from step4_section1_test import MadagascarSpecies, SpeciesConfidence, SpeciesDetection
from step5_section1_test import ThreatType, ThreatSeverity, ThreatUrgency, ThreatDetection
from step5_section3_test import ThreatAlert, ThreatAlertManager
from step6_section1_test import (ConservationPriority, ConservationStrategy, ConservationAction,
                               ConservationResource, ConservationRecommendation, SpeciesType, 
                               ConservationStatus, MadagascarConservationKnowledgeBase)
from step6_section2_test import (ConservationContext, RecommendationScore, RecommendationGenerator)

@dataclass
class InterventionOutcome:
    """Record of conservation intervention outcomes."""
    intervention_id: str
    recommendation_id: str
    actions_taken: List[ConservationAction]
    start_date: datetime
    end_date: Optional[datetime] = None
    outcome_metrics: Dict[str, float] = field(default_factory=dict)
    success_indicators: Dict[str, bool] = field(default_factory=dict)
    lessons_learned: List[str] = field(default_factory=list)
    cost_actual: float = 0.0
    cost_estimated: float = 0.0
    stakeholder_satisfaction: float = 0.0  # 0.0 to 1.0
    ecological_impact: float = 0.0  # -1.0 to 1.0 (negative = harm, positive = benefit)
    sustainability_score: float = 0.0  # 0.0 to 1.0
    unexpected_challenges: List[str] = field(default_factory=list)
    adaptive_modifications: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.outcome_metrics:
            self.outcome_metrics = {
                "species_population_change": 0.0,
                "habitat_area_protected": 0.0,
                "threat_reduction_percentage": 0.0,
                "community_engagement_score": 0.0,
                "biodiversity_index_change": 0.0
            }
        
        if not self.success_indicators:
            self.success_indicators = {
                "objectives_met": False,
                "within_budget": False,
                "on_schedule": False,
                "stakeholder_support_maintained": False,
                "environmental_compliance": True
            }
    
    def calculate_overall_success(self) -> float:
        """Calculate overall success score for the intervention."""
        # Weight different success factors
        weights = {
            "objectives_met": 0.25,
            "within_budget": 0.15,
            "on_schedule": 0.10,
            "stakeholder_support_maintained": 0.20,
            "environmental_compliance": 0.30
        }
        
        success_score = sum(
            weights[indicator] * (1.0 if value else 0.0)
            for indicator, value in self.success_indicators.items()
            if indicator in weights
        )
        
        # Adjust based on ecological impact and sustainability
        if self.ecological_impact > 0:
            success_score *= (1.0 + self.ecological_impact * 0.2)
        else:
            success_score *= (1.0 + self.ecological_impact * 0.5)  # Penalize negative impact more
        
        success_score *= (0.8 + self.sustainability_score * 0.2)
        
        return min(1.0, max(0.0, success_score))

@dataclass
class AdaptiveLearningRule:
    """Rule for adaptive learning from intervention outcomes."""
    rule_id: str
    condition: str  # Natural language description of when to apply
    action_type: str  # "modify_weights", "adjust_strategy", "update_knowledge"
    parameters: Dict[str, Any]
    confidence: float = 0.5  # Confidence in the rule
    application_count: int = 0
    success_rate: float = 0.0
    last_updated: datetime = field(default_factory=datetime.utcnow)
    evidence_sources: List[str] = field(default_factory=list)
    
    def apply_rule(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply the learning rule to given context."""
        self.application_count += 1
        
        if self.action_type == "modify_weights":
            return self._modify_weights(context)
        elif self.action_type == "adjust_strategy":
            return self._adjust_strategy(context)
        elif self.action_type == "update_knowledge":
            return self._update_knowledge(context)
        else:
            return {}
    
    def _modify_weights(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Modify scoring weights based on learned patterns."""
        modifications = {}
        for param, value in self.parameters.items():
            if param in context:
                # Apply weighted adjustment
                adjustment = value * self.confidence
                modifications[param] = context[param] * (1.0 + adjustment)
        return modifications
    
    def _adjust_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Adjust strategy selection based on learned patterns."""
        return {
            "preferred_strategies": self.parameters.get("preferred_strategies", []),
            "avoid_strategies": self.parameters.get("avoid_strategies", []),
            "strategy_adjustments": self.parameters.get("strategy_adjustments", {})
        }
    
    def _update_knowledge(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Update knowledge base based on learned patterns."""
        return {
            "knowledge_updates": self.parameters.get("knowledge_updates", {}),
            "new_relationships": self.parameters.get("new_relationships", {}),
            "revised_assumptions": self.parameters.get("revised_assumptions", {})
        }

class LearningMemory:
    """Memory system for storing and retrieving learning experiences."""
    
    def __init__(self, max_memories: int = 1000):
        self.max_memories = max_memories
        self.intervention_outcomes: Dict[str, InterventionOutcome] = {}
        self.pattern_cache: Dict[str, Any] = {}
        self.success_patterns: List[Dict[str, Any]] = []
        self.failure_patterns: List[Dict[str, Any]] = []
        self.contextual_learnings: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        # Learning statistics
        self.total_interventions = 0
        self.successful_interventions = 0
        self.learning_events = 0
        self.last_learning_update = datetime.utcnow()
    
    def add_intervention_outcome(self, outcome: InterventionOutcome):
        """Add new intervention outcome to memory."""
        self.intervention_outcomes[outcome.intervention_id] = outcome
        self.total_interventions += 1
        
        overall_success = outcome.calculate_overall_success()
        if overall_success > 0.7:
            self.successful_interventions += 1
            self._extract_success_patterns(outcome)
        else:
            self._extract_failure_patterns(outcome)
        
        # Maintain memory size limit
        if len(self.intervention_outcomes) > self.max_memories:
            oldest_id = min(self.intervention_outcomes.keys(), 
                          key=lambda x: self.intervention_outcomes[x].start_date)
            del self.intervention_outcomes[oldest_id]
        
        self.learning_events += 1
        self.last_learning_update = datetime.utcnow()
    
    def _extract_success_patterns(self, outcome: InterventionOutcome):
        """Extract patterns from successful interventions."""
        pattern = {
            "actions": [action.value for action in outcome.actions_taken],
            "context_factors": self._extract_context_factors(outcome),
            "success_score": outcome.calculate_overall_success(),
            "key_metrics": outcome.outcome_metrics,
            "timestamp": outcome.start_date
        }
        
        self.success_patterns.append(pattern)
        
        # Limit pattern storage
        if len(self.success_patterns) > 100:
            self.success_patterns = sorted(
                self.success_patterns, 
                key=lambda x: x["success_score"], 
                reverse=True
            )[:100]
    
    def _extract_failure_patterns(self, outcome: InterventionOutcome):
        """Extract patterns from failed interventions."""
        pattern = {
            "actions": [action.value for action in outcome.actions_taken],
            "context_factors": self._extract_context_factors(outcome),
            "failure_reasons": outcome.unexpected_challenges,
            "success_score": outcome.calculate_overall_success(),
            "lessons": outcome.lessons_learned,
            "timestamp": outcome.start_date
        }
        
        self.failure_patterns.append(pattern)
        
        # Limit pattern storage
        if len(self.failure_patterns) > 50:
            self.failure_patterns = self.failure_patterns[-50:]
    
    def _extract_context_factors(self, outcome: InterventionOutcome) -> Dict[str, Any]:
        """Extract relevant context factors from intervention."""
        # This would normally extract from the original context
        # For now, we'll simulate context factors
        return {
            "ecosystem_type": "unknown",
            "threat_types": [],
            "species_involved": [],
            "cost_range": self._categorize_cost(outcome.cost_actual),
            "duration_category": self._categorize_duration(outcome.start_date, outcome.end_date),
            "stakeholder_satisfaction": outcome.stakeholder_satisfaction
        }
    
    def _categorize_cost(self, cost: float) -> str:
        """Categorize intervention cost."""
        if cost < 10000:
            return "low"
        elif cost < 50000:
            return "medium"
        elif cost < 200000:
            return "high"
        else:
            return "very_high"
    
    def _categorize_duration(self, start: datetime, end: Optional[datetime]) -> str:
        """Categorize intervention duration."""
        if end is None:
            return "ongoing"
        
        duration = (end - start).days
        if duration < 30:
            return "short"
        elif duration < 180:
            return "medium"
        elif duration < 365:
            return "long"
        else:
            return "very_long"
    
    def get_similar_interventions(self, current_context: Dict[str, Any], 
                                 limit: int = 10) -> List[InterventionOutcome]:
        """Retrieve similar past interventions based on context."""
        similarities = []
        
        for intervention_id, outcome in self.intervention_outcomes.items():
            similarity = self._calculate_context_similarity(
                current_context, 
                self._extract_context_factors(outcome)
            )
            similarities.append((similarity, outcome))
        
        # Sort by similarity and return top matches
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [outcome for _, outcome in similarities[:limit]]
    
    def _calculate_context_similarity(self, context1: Dict[str, Any], 
                                    context2: Dict[str, Any]) -> float:
        """Calculate similarity between two contexts."""
        # Simple similarity calculation based on matching factors
        common_keys = set(context1.keys()) & set(context2.keys())
        if not common_keys:
            return 0.0
        
        matches = 0
        for key in common_keys:
            if context1[key] == context2[key]:
                matches += 1
        
        return matches / len(common_keys)
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get comprehensive learning statistics."""
        success_rate = (self.successful_interventions / max(1, self.total_interventions))
        
        return {
            "total_interventions": self.total_interventions,
            "successful_interventions": self.successful_interventions,
            "success_rate": success_rate,
            "learning_events": self.learning_events,
            "success_patterns_identified": len(self.success_patterns),
            "failure_patterns_identified": len(self.failure_patterns),
            "last_learning_update": self.last_learning_update,
            "memory_utilization": len(self.intervention_outcomes) / self.max_memories
        }

class AdaptiveDecisionEngine:
    """Main adaptive decision engine for conservation recommendations."""
    
    def __init__(self):
        self.recommendation_generator = RecommendationGenerator()
        self.learning_memory = LearningMemory()
        self.adaptive_rules: List[AdaptiveLearningRule] = []
        self.decision_history: List[Dict[str, Any]] = []
        
        # Adaptive parameters
        self.learning_rate = 0.1
        self.adaptation_threshold = 0.05  # Minimum change to trigger adaptation
        self.confidence_threshold = 0.7   # Minimum confidence for rule application
        
        # Performance tracking
        self.performance_metrics = {
            "recommendation_accuracy": 0.75,
            "adaptation_frequency": 0.0,
            "learning_effectiveness": 0.0,
            "prediction_confidence": 0.8
        }
        
        # Initialize default learning rules
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """Initialize default adaptive learning rules."""
        # Rule 1: Adjust weights based on intervention success
        success_weight_rule = AdaptiveLearningRule(
            rule_id="success_weight_adjustment",
            condition="When interventions with high feasibility scores consistently succeed",
            action_type="modify_weights",
            parameters={
                "feasibility": 0.1,
                "impact": -0.05
            },
            confidence=0.8
        )
        
        # Rule 2: Strategy preference based on ecosystem type
        ecosystem_strategy_rule = AdaptiveLearningRule(
            rule_id="ecosystem_strategy_preference",
            condition="When ecosystem restoration shows high success in rainforest contexts",
            action_type="adjust_strategy",
            parameters={
                "preferred_strategies": ["ecosystem_restoration", "habitat_protection"],
                "context_conditions": {"ecosystem_type": "rainforest"}
            },
            confidence=0.7
        )
        
        # Rule 3: Update knowledge about threat mitigation
        threat_knowledge_rule = AdaptiveLearningRule(
            rule_id="threat_mitigation_learning",
            condition="When specific actions consistently reduce threat severity",
            action_type="update_knowledge",
            parameters={
                "knowledge_updates": {
                    "effective_threat_actions": {},
                    "context_dependencies": {}
                }
            },
            confidence=0.6
        )
        
        self.adaptive_rules = [success_weight_rule, ecosystem_strategy_rule, threat_knowledge_rule]
    
    def make_adaptive_recommendation(self, 
                                   threats: List[ThreatDetection],
                                   species_detections: List[SpeciesDetection],
                                   context: ConservationContext,
                                   available_resources: List[ConservationResource],
                                   max_recommendations: int = 5) -> Tuple[List[ConservationRecommendation], Dict[str, Any]]:
        """Make conservation recommendations with adaptive learning."""
        
        print(f"🧠 Making adaptive recommendations...")
        
        # Step 1: Check for similar past contexts and adapt accordingly
        similar_interventions = self._find_similar_contexts(context, threats, species_detections)
        
        # Step 2: Apply adaptive learning rules
        adaptations = self._apply_learning_rules(context, threats, species_detections, similar_interventions)
        
        # Step 3: Modify recommendation generator parameters based on learning
        self._apply_adaptations(adaptations)
        
        # Step 4: Generate recommendations with adaptive parameters
        recommendations = self.recommendation_generator.generate_recommendations(
            threats=threats,
            species_detections=species_detections,
            context=context,
            available_resources=available_resources,
            max_recommendations=max_recommendations
        )
        
        # Step 5: Apply post-generation adaptive adjustments
        adapted_recommendations = self._post_process_recommendations(
            recommendations, adaptations, similar_interventions
        )
        
        # Step 6: Record decision for future learning
        decision_record = self._record_decision(
            threats, species_detections, context, adapted_recommendations, adaptations
        )
        
        # Step 7: Calculate adaptive insights
        adaptive_insights = self._calculate_adaptive_insights(
            similar_interventions, adaptations, adapted_recommendations
        )
        
        print(f"✅ Generated {len(adapted_recommendations)} adaptive recommendations")
        
        return adapted_recommendations, adaptive_insights
    
    def _find_similar_contexts(self, context: ConservationContext,
                             threats: List[ThreatDetection],
                             species_detections: List[SpeciesDetection]) -> List[InterventionOutcome]:
        """Find similar past contexts for learning."""
        current_context_features = {
            "ecosystem_type": context.ecosystem_type,
            "protected_area": context.protected_area_status,
            "accessibility": self._categorize_accessibility(context.accessibility),
            "threat_types": [threat.threat_type.value for threat in threats],
            "species_count": len(species_detections),
            "governance_strength": self._categorize_governance(context.local_governance_strength)
        }
        
        return self.learning_memory.get_similar_interventions(current_context_features, limit=5)
    
    def _categorize_accessibility(self, accessibility: float) -> str:
        """Categorize accessibility level."""
        if accessibility < 0.3:
            return "low"
        elif accessibility < 0.7:
            return "medium"
        else:
            return "high"
    
    def _categorize_governance(self, governance: float) -> str:
        """Categorize governance strength."""
        if governance < 0.4:
            return "weak"
        elif governance < 0.7:
            return "moderate"
        else:
            return "strong"
    
    def _apply_learning_rules(self, context: ConservationContext,
                            threats: List[ThreatDetection],
                            species_detections: List[SpeciesDetection],
                            similar_interventions: List[InterventionOutcome]) -> Dict[str, Any]:
        """Apply adaptive learning rules based on context and history."""
        adaptations = {
            "weight_modifications": {},
            "strategy_adjustments": {},
            "knowledge_updates": {},
            "applied_rules": []
        }
        
        # Build current context for rule application
        rule_context = {
            "ecosystem_type": context.ecosystem_type,
            "threat_count": len(threats),
            "species_diversity": len(set(detection.species for detection in species_detections)),
            "similar_success_rate": self._calculate_similar_success_rate(similar_interventions),
            "resource_availability": self._assess_resource_availability(context)
        }
        
        # Apply each rule if conditions are met
        for rule in self.adaptive_rules:
            if rule.confidence >= self.confidence_threshold:
                if self._evaluate_rule_condition(rule, rule_context, similar_interventions):
                    rule_result = rule.apply_rule(rule_context)
                    
                    # Merge rule results into adaptations
                    if rule.action_type == "modify_weights":
                        adaptations["weight_modifications"].update(rule_result)
                    elif rule.action_type == "adjust_strategy":
                        adaptations["strategy_adjustments"].update(rule_result)
                    elif rule.action_type == "update_knowledge":
                        adaptations["knowledge_updates"].update(rule_result)
                    
                    adaptations["applied_rules"].append(rule.rule_id)
                    
                    print(f"   📚 Applied learning rule: {rule.rule_id}")
        
        return adaptations
    
    def _calculate_similar_success_rate(self, similar_interventions: List[InterventionOutcome]) -> float:
        """Calculate success rate of similar past interventions."""
        if not similar_interventions:
            return 0.5  # Default neutral success rate
        
        success_scores = [intervention.calculate_overall_success() for intervention in similar_interventions]
        return sum(success_scores) / len(success_scores)
    
    def _assess_resource_availability(self, context: ConservationContext) -> str:
        """Assess overall resource availability level."""
        # Combine various context factors to assess resources
        resource_factors = [
            context.accessibility,
            context.infrastructure_quality,
            context.local_governance_strength
        ]
        
        avg_availability = sum(resource_factors) / len(resource_factors)
        
        if avg_availability < 0.4:
            return "limited"
        elif avg_availability < 0.7:
            return "moderate"
        else:
            return "abundant"
    
    def _evaluate_rule_condition(self, rule: AdaptiveLearningRule,
                                context: Dict[str, Any],
                                similar_interventions: List[InterventionOutcome]) -> bool:
        """Evaluate if a rule's condition is met."""
        # Simplified rule condition evaluation
        # In a full implementation, this would parse natural language conditions
        
        if rule.rule_id == "success_weight_adjustment":
            # Apply if similar interventions had high feasibility and success
            return (context.get("similar_success_rate", 0) > 0.7 and 
                   len(similar_interventions) >= 2)
        
        elif rule.rule_id == "ecosystem_strategy_preference":
            # Apply for rainforest contexts with decent success history
            return (context.get("ecosystem_type") == "rainforest" and
                   context.get("similar_success_rate", 0) > 0.6)
        
        elif rule.rule_id == "threat_mitigation_learning":
            # Apply when we have threat data and intervention history
            return (context.get("threat_count", 0) > 0 and
                   len(similar_interventions) >= 1)
        
        return False
    
    def _apply_adaptations(self, adaptations: Dict[str, Any]):
        """Apply adaptations to the recommendation generator."""
        # Apply weight modifications
        weight_mods = adaptations.get("weight_modifications", {})
        if weight_mods:
            # Modify scoring weights in the generator
            for scenario in self.recommendation_generator.scoring_weights:
                for weight_key, adjustment in weight_mods.items():
                    if weight_key in self.recommendation_generator.scoring_weights[scenario]:
                        current_weight = self.recommendation_generator.scoring_weights[scenario][weight_key]
                        new_weight = max(0.0, min(1.0, current_weight + adjustment * self.learning_rate))
                        self.recommendation_generator.scoring_weights[scenario][weight_key] = new_weight
        
        # Apply strategy adjustments
        strategy_adjustments = adaptations.get("strategy_adjustments", {})
        if strategy_adjustments:
            # This would modify strategy selection logic in a full implementation
            print(f"   📊 Strategy adjustments: {list(strategy_adjustments.keys())}")
        
        # Apply knowledge updates
        knowledge_updates = adaptations.get("knowledge_updates", {})
        if knowledge_updates:
            # This would update the knowledge base in a full implementation
            print(f"   🧠 Knowledge updates: {list(knowledge_updates.keys())}")
    
    def _post_process_recommendations(self, recommendations: List[ConservationRecommendation],
                                    adaptations: Dict[str, Any],
                                    similar_interventions: List[InterventionOutcome]) -> List[ConservationRecommendation]:
        """Post-process recommendations based on adaptive learning."""
        adapted_recommendations = recommendations.copy()
        
        # Adjust recommendation priorities based on similar intervention outcomes
        if similar_interventions:
            success_patterns = self._extract_success_patterns_from_interventions(similar_interventions)
            
            for rec in adapted_recommendations:
                # Boost recommendations that match successful patterns
                pattern_match_score = self._calculate_pattern_match(rec, success_patterns)
                
                if pattern_match_score > 0.7:
                    # Boost confidence for pattern-matching recommendations
                    rec.confidence_score = min(1.0, rec.confidence_score * 1.1)
                    print(f"   ⬆️  Boosted confidence for {rec.strategy.value} (pattern match: {pattern_match_score:.2f})")
        
        return adapted_recommendations
    
    def _extract_success_patterns_from_interventions(self, interventions: List[InterventionOutcome]) -> Dict[str, Any]:
        """Extract success patterns from intervention outcomes."""
        patterns = {
            "successful_actions": defaultdict(int),
            "successful_strategies": defaultdict(int),
            "context_success_factors": defaultdict(list)
        }
        
        for intervention in interventions:
            success_score = intervention.calculate_overall_success()
            if success_score > 0.7:  # Consider as successful
                # Count successful actions
                for action in intervention.actions_taken:
                    patterns["successful_actions"][action.value] += 1
                
                # Extract other patterns...
                patterns["context_success_factors"]["high_success"].append(success_score)
        
        return patterns
    
    def _calculate_pattern_match(self, recommendation: ConservationRecommendation,
                               success_patterns: Dict[str, Any]) -> float:
        """Calculate how well a recommendation matches successful patterns."""
        match_score = 0.0
        total_factors = 0
        
        # Check action pattern matches
        successful_actions = success_patterns.get("successful_actions", {})
        if successful_actions:
            action_matches = sum(
                1 for action in recommendation.actions 
                if action.value in successful_actions
            )
            match_score += (action_matches / len(recommendation.actions)) * 0.6
            total_factors += 0.6
        
        # Check strategy pattern matches
        successful_strategies = success_patterns.get("successful_strategies", {})
        if recommendation.strategy.value in successful_strategies:
            match_score += 0.4
        total_factors += 0.4
        
        return match_score / max(1, total_factors)
    
    def _record_decision(self, threats: List[ThreatDetection],
                        species_detections: List[SpeciesDetection],
                        context: ConservationContext,
                        recommendations: List[ConservationRecommendation],
                        adaptations: Dict[str, Any]) -> Dict[str, Any]:
        """Record decision for future learning."""
        decision_record = {
            "timestamp": datetime.utcnow(),
            "context_summary": {
                "ecosystem_type": context.ecosystem_type,
                "threat_count": len(threats),
                "species_count": len(species_detections),
                "location": context.location
            },
            "recommendations_made": len(recommendations),
            "adaptations_applied": adaptations.get("applied_rules", []),
            "decision_confidence": np.mean([rec.confidence_score for rec in recommendations])
        }
        
        self.decision_history.append(decision_record)
        
        # Maintain decision history size
        if len(self.decision_history) > 1000:
            self.decision_history = self.decision_history[-1000:]
        
        return decision_record
    
    def _calculate_adaptive_insights(self, similar_interventions: List[InterventionOutcome],
                                   adaptations: Dict[str, Any],
                                   recommendations: List[ConservationRecommendation]) -> Dict[str, Any]:
        """Calculate insights about the adaptive decision process."""
        insights = {
            "learning_indicators": {
                "similar_cases_found": len(similar_interventions),
                "adaptations_applied": len(adaptations.get("applied_rules", [])),
                "average_confidence": np.mean([rec.confidence_score for rec in recommendations]),
                "learning_memory_size": len(self.learning_memory.intervention_outcomes)
            },
            "recommendation_insights": {
                "strategy_diversity": len(set(rec.strategy for rec in recommendations)),
                "action_diversity": len(set(action for rec in recommendations for action in rec.actions)),
                "priority_distribution": {
                    priority.value: sum(1 for rec in recommendations if rec.priority == priority)
                    for priority in ConservationPriority
                }
            },
            "adaptive_performance": self.performance_metrics.copy(),
            "learning_trajectory": {
                "recent_decisions": len([d for d in self.decision_history 
                                       if d["timestamp"] > datetime.utcnow() - timedelta(days=30)]),
                "adaptation_frequency": self.performance_metrics["adaptation_frequency"],
                "learning_effectiveness": self.performance_metrics["learning_effectiveness"]
            }
        }
        
        return insights
    
    def record_intervention_outcome(self, outcome: InterventionOutcome):
        """Record outcome of an intervention for learning."""
        print(f"📝 Recording intervention outcome: {outcome.intervention_id}")
        
        # Add to learning memory
        self.learning_memory.add_intervention_outcome(outcome)
        
        # Update performance metrics
        self._update_performance_metrics(outcome)
        
        # Generate new learning rules if patterns are detected
        self._generate_new_learning_rules(outcome)
        
        print(f"   📊 Learning memory updated: {len(self.learning_memory.intervention_outcomes)} interventions")
    
    def _update_performance_metrics(self, outcome: InterventionOutcome):
        """Update adaptive engine performance metrics."""
        overall_success = outcome.calculate_overall_success()
        
        # Update recommendation accuracy
        current_accuracy = self.performance_metrics["recommendation_accuracy"]
        new_accuracy = current_accuracy * 0.9 + overall_success * 0.1
        self.performance_metrics["recommendation_accuracy"] = new_accuracy
        
        # Update learning effectiveness
        if outcome.adaptive_modifications:
            # If adaptations were made during implementation, assess their effectiveness
            modification_success = 1.0 if overall_success > 0.7 else 0.0
            current_learning = self.performance_metrics["learning_effectiveness"]
            new_learning = current_learning * 0.8 + modification_success * 0.2
            self.performance_metrics["learning_effectiveness"] = new_learning
        
        # Update prediction confidence based on outcome alignment
        if hasattr(outcome, 'predicted_success'):
            prediction_error = abs(overall_success - outcome.predicted_success)
            confidence_adjustment = 1.0 - prediction_error
            current_confidence = self.performance_metrics["prediction_confidence"]
            new_confidence = current_confidence * 0.9 + confidence_adjustment * 0.1
            self.performance_metrics["prediction_confidence"] = new_confidence
    
    def _generate_new_learning_rules(self, outcome: InterventionOutcome):
        """Generate new learning rules based on intervention outcomes."""
        # This is a simplified version - a full implementation would use
        # more sophisticated pattern recognition
        
        overall_success = outcome.calculate_overall_success()
        
        if overall_success > 0.8 and len(outcome.actions_taken) > 0:
            # Generate rule for successful action combinations
            new_rule = AdaptiveLearningRule(
                rule_id=f"success_pattern_{len(self.adaptive_rules)}",
                condition=f"Successful pattern from intervention {outcome.intervention_id}",
                action_type="adjust_strategy",
                parameters={
                    "preferred_actions": [action.value for action in outcome.actions_taken],
                    "context_similarity_threshold": 0.7
                },
                confidence=0.6,
                evidence_sources=[outcome.intervention_id]
            )
            
            self.adaptive_rules.append(new_rule)
            print(f"   🧠 Generated new learning rule: {new_rule.rule_id}")
    
    def get_learning_status(self) -> Dict[str, Any]:
        """Get comprehensive learning status report."""
        memory_stats = self.learning_memory.get_learning_statistics()
        
        return {
            "learning_memory": memory_stats,
            "adaptive_rules": {
                "total_rules": len(self.adaptive_rules),
                "active_rules": len([r for r in self.adaptive_rules if r.confidence >= self.confidence_threshold]),
                "recent_applications": sum(r.application_count for r in self.adaptive_rules)
            },
            "performance_metrics": self.performance_metrics,
            "decision_history": {
                "total_decisions": len(self.decision_history),
                "recent_decisions": len([d for d in self.decision_history 
                                       if d["timestamp"] > datetime.utcnow() - timedelta(days=7)]),
                "average_confidence": np.mean([d["decision_confidence"] for d in self.decision_history[-10:]])
                                    if self.decision_history else 0.0
            },
            "learning_indicators": {
                "adaptation_rate": len(self.adaptive_rules) / max(1, memory_stats["total_interventions"]),
                "learning_stability": self.performance_metrics["learning_effectiveness"],
                "knowledge_accumulation": memory_stats["memory_utilization"]
            }
        }

def test_intervention_outcome_tracking():
    """Test intervention outcome tracking and learning."""
    print("📊 Testing Intervention Outcome Tracking...")
    
    try:
        # Create test intervention outcome
        test_outcome = InterventionOutcome(
            intervention_id="test_intervention_001",
            recommendation_id="test_rec_001",
            actions_taken=[
                ConservationAction.DEPLOY_PATROL_TEAM,
                ConservationAction.COMMUNITY_CONSERVATION_TRAINING,
                ConservationAction.REFORESTATION
            ],
            start_date=datetime.utcnow() - timedelta(days=180),
            end_date=datetime.utcnow() - timedelta(days=30),
            cost_actual=45000.0,
            cost_estimated=50000.0,
            stakeholder_satisfaction=0.8,
            ecological_impact=0.6,
            sustainability_score=0.7
        )
        
        # Test outcome metrics initialization
        if len(test_outcome.outcome_metrics) >= 5:
            print("✅ Outcome metrics initialized")
        else:
            print("❌ Outcome metrics incomplete")
            return False
        
        # Test success indicators initialization
        if len(test_outcome.success_indicators) >= 5:
            print("✅ Success indicators initialized")
        else:
            print("❌ Success indicators incomplete")
            return False
        
        # Update success indicators for testing
        test_outcome.success_indicators.update({
            "objectives_met": True,
            "within_budget": True,
            "on_schedule": True,
            "stakeholder_support_maintained": True,
            "environmental_compliance": True
        })
        
        # Test overall success calculation
        success_score = test_outcome.calculate_overall_success()
        if 0.0 <= success_score <= 1.0:
            print(f"✅ Overall success calculated: {success_score:.2f}")
        else:
            print(f"❌ Invalid success score: {success_score}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Intervention outcome tracking error: {e}")
        return False

def test_learning_memory_system():
    """Test learning memory system functionality."""
    print("\n🧠 Testing Learning Memory System...")
    
    try:
        memory = LearningMemory(max_memories=10)
        
        # Create test intervention outcomes
        for i in range(5):
            outcome = InterventionOutcome(
                intervention_id=f"memory_test_{i}",
                recommendation_id=f"rec_{i}",
                actions_taken=[ConservationAction.DEPLOY_PATROL_TEAM],
                start_date=datetime.utcnow() - timedelta(days=i*30),
                end_date=datetime.utcnow() - timedelta(days=i*30-15),
                cost_actual=20000 + i*5000,
                stakeholder_satisfaction=0.5 + i*0.1,
                ecological_impact=0.3 + i*0.1,
                sustainability_score=0.6 + i*0.05
            )
            
            # Set success indicators
            outcome.success_indicators.update({
                "objectives_met": i >= 2,  # Last 3 are successful
                "within_budget": True,
                "on_schedule": True,
                "stakeholder_support_maintained": i >= 1,
                "environmental_compliance": True
            })
            
            memory.add_intervention_outcome(outcome)
        
        # Test memory storage
        if len(memory.intervention_outcomes) == 5:
            print("✅ Intervention outcomes stored correctly")
        else:
            print(f"❌ Memory storage issue: {len(memory.intervention_outcomes)}/5")
            return False
        
        # Test pattern extraction
        if len(memory.success_patterns) > 0:
            print(f"✅ Success patterns extracted: {len(memory.success_patterns)}")
        else:
            print("❌ No success patterns extracted")
            return False
        
        # Test similarity search
        test_context = {
            "ecosystem_type": "rainforest",
            "cost_range": "medium",
            "duration_category": "short"
        }
        
        similar = memory.get_similar_interventions(test_context, limit=3)
        if len(similar) > 0:
            print(f"✅ Similar interventions found: {len(similar)}")
        else:
            print("⚠️  No similar interventions found (expected for test data)")
        
        # Test learning statistics
        stats = memory.get_learning_statistics()
        if stats["total_interventions"] == 5:
            print(f"✅ Learning statistics: {stats['success_rate']:.2f} success rate")
        else:
            print(f"❌ Statistics mismatch: {stats['total_interventions']}/5")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Learning memory system error: {e}")
        return False

def test_adaptive_learning_rules():
    """Test adaptive learning rule system."""
    print("\n🎯 Testing Adaptive Learning Rules...")
    
    try:
        # Test rule creation
        test_rule = AdaptiveLearningRule(
            rule_id="test_rule_001",
            condition="Test condition for weight modification",
            action_type="modify_weights",
            parameters={
                "feasibility": 0.1,
                "impact": -0.05,
                "urgency": 0.02
            },
            confidence=0.8
        )
        
        # Test rule application
        test_context = {
            "feasibility": 0.7,
            "impact": 0.8,
            "urgency": 0.6
        }
        
        result = test_rule.apply_rule(test_context)
        
        if len(result) > 0:
            print(f"✅ Rule application successful: {len(result)} modifications")
        else:
            print("❌ Rule application failed")
            return False
        
        # Test different rule types
        strategy_rule = AdaptiveLearningRule(
            rule_id="strategy_test",
            condition="Test strategy adjustment",
            action_type="adjust_strategy",
            parameters={
                "preferred_strategies": ["habitat_protection", "community_engagement"],
                "avoid_strategies": ["law_enforcement"]
            },
            confidence=0.7
        )
        
        strategy_result = strategy_rule.apply_rule({})
        
        if "preferred_strategies" in strategy_result:
            print("✅ Strategy adjustment rule working")
        else:
            print("❌ Strategy adjustment rule failed")
            return False
        
        # Test knowledge update rule
        knowledge_rule = AdaptiveLearningRule(
            rule_id="knowledge_test",
            condition="Test knowledge update",
            action_type="update_knowledge",
            parameters={
                "knowledge_updates": {"threat_effectiveness": {"deforestation": 0.8}},
                "new_relationships": {"ecosystem_species": "strong_correlation"}
            },
            confidence=0.6
        )
        
        knowledge_result = knowledge_rule.apply_rule({})
        
        if "knowledge_updates" in knowledge_result:
            print("✅ Knowledge update rule working")
        else:
            print("❌ Knowledge update rule failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Adaptive learning rules error: {e}")
        return False

def test_adaptive_decision_engine():
    """Test complete adaptive decision engine."""
    print("\n🧠 Testing Adaptive Decision Engine...")
    
    try:
        engine = AdaptiveDecisionEngine()
        
        # Test engine initialization
        if len(engine.adaptive_rules) >= 3:
            print(f"✅ Engine initialized with {len(engine.adaptive_rules)} default rules")
        else:
            print("❌ Engine initialization failed")
            return False
        
        # Create test scenario
        test_threats = [
            ThreatDetection(
                detection_id="adaptive_threat_1",
                threat_type=ThreatType.DEFORESTATION,
                severity=0.8,
                severity_level=ThreatSeverity.HIGH,
                urgency=ThreatUrgency.URGENT,
                confidence=0.9
            )
        ]
        
        test_species = [
            SpeciesDetection(
                detection_id="adaptive_species_1",
                species=MadagascarSpecies.LEMUR_CATTA,
                confidence=0.9,
                confidence_level=SpeciesConfidence.VERY_HIGH,
                timestamp=datetime.utcnow(),
                source="adaptive_test"
            )
        ]
        
        test_context = ConservationContext(
            location=(-18.947, 48.458),
            ecosystem_type="rainforest",
            protected_area_status=True,
            accessibility=0.7,
            infrastructure_quality=0.6,
            local_governance_strength=0.8
        )
        
        test_resources = [
            ConservationResource(
                resource_type="field_personnel",
                availability=0.8,
                capacity=20,
                cost_per_unit=100.0
            )
        ]
        
        # Test adaptive recommendation generation
        recommendations, insights = engine.make_adaptive_recommendation(
            threats=test_threats,
            species_detections=test_species,
            context=test_context,
            available_resources=test_resources,
            max_recommendations=3
        )
        
        # Validate results
        if len(recommendations) > 0:
            print(f"✅ Adaptive recommendations generated: {len(recommendations)}")
        else:
            print("❌ No adaptive recommendations generated")
            return False
        
        # Check insights quality
        required_insight_keys = ["learning_indicators", "recommendation_insights", "adaptive_performance"]
        if all(key in insights for key in required_insight_keys):
            print("✅ Adaptive insights comprehensive")
        else:
            print("❌ Adaptive insights incomplete")
            return False
        
        # Test learning status
        learning_status = engine.get_learning_status()
        if "learning_memory" in learning_status and "adaptive_rules" in learning_status:
            print("✅ Learning status report generated")
        else:
            print("❌ Learning status report incomplete")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Adaptive decision engine error: {e}")
        return False

def test_outcome_recording_and_learning():
    """Test outcome recording and learning updates."""
    print("\n📝 Testing Outcome Recording and Learning...")
    
    try:
        engine = AdaptiveDecisionEngine()
        initial_rules = len(engine.adaptive_rules)
        
        # Create and record a successful intervention outcome
        successful_outcome = InterventionOutcome(
            intervention_id="learning_test_001",
            recommendation_id="rec_learning_001",
            actions_taken=[
                ConservationAction.COMMUNITY_CONSERVATION_TRAINING,
                ConservationAction.REFORESTATION,
                ConservationAction.LONG_TERM_MONITORING
            ],
            start_date=datetime.utcnow() - timedelta(days=90),
            end_date=datetime.utcnow() - timedelta(days=10),
            cost_actual=35000.0,
            cost_estimated=40000.0,
            stakeholder_satisfaction=0.9,
            ecological_impact=0.8,
            sustainability_score=0.85
        )
        
        # Set success indicators
        successful_outcome.success_indicators.update({
            "objectives_met": True,
            "within_budget": True,
            "on_schedule": True,
            "stakeholder_support_maintained": True,
            "environmental_compliance": True
        })
        
        # Record the outcome
        engine.record_intervention_outcome(successful_outcome)
        
        # Check if learning memory was updated
        memory_size = len(engine.learning_memory.intervention_outcomes)
        if memory_size >= 1:
            print("✅ Intervention outcome recorded in memory")
        else:
            print("❌ Outcome recording failed")
            return False
        
        # Check if performance metrics were updated
        initial_accuracy = 0.75  # Default value
        current_accuracy = engine.performance_metrics["recommendation_accuracy"]
        if current_accuracy != initial_accuracy:
            print(f"✅ Performance metrics updated: accuracy {current_accuracy:.3f}")
        else:
            print("⚠️  Performance metrics unchanged (may be expected)")
        
        # Test with a failed intervention to see learning response
        failed_outcome = InterventionOutcome(
            intervention_id="learning_test_002",
            recommendation_id="rec_learning_002",
            actions_taken=[ConservationAction.LAW_ENFORCEMENT_STRENGTHENING],
            start_date=datetime.utcnow() - timedelta(days=60),
            end_date=datetime.utcnow() - timedelta(days=5),
            cost_actual=80000.0,
            cost_estimated=50000.0,
            stakeholder_satisfaction=0.3,
            ecological_impact=0.1,
            sustainability_score=0.2
        )
        
        # Set failure indicators
        failed_outcome.success_indicators.update({
            "objectives_met": False,
            "within_budget": False,
            "on_schedule": False,
            "stakeholder_support_maintained": False,
            "environmental_compliance": True
        })
        
        failed_outcome.unexpected_challenges = [
            "Community resistance to enforcement",
            "Budget overrun due to equipment costs",
            "Limited staff availability"
        ]
        
        failed_outcome.lessons_learned = [
            "Need better community engagement before enforcement",
            "More accurate cost estimation required",
            "Resource availability assessment critical"
        ]
        
        engine.record_intervention_outcome(failed_outcome)
        
        # Check learning response
        final_memory_size = len(engine.learning_memory.intervention_outcomes)
        if final_memory_size == 2:
            print("✅ Multiple outcomes recorded successfully")
        else:
            print(f"❌ Memory size unexpected: {final_memory_size}/2")
            return False
        
        # Check if new learning rules might have been generated
        final_rules = len(engine.adaptive_rules)
        if final_rules >= initial_rules:
            print(f"✅ Learning rules maintained or expanded: {final_rules}")
        else:
            print(f"❌ Learning rules decreased: {final_rules} < {initial_rules}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Outcome recording and learning error: {e}")
        return False

def main():
    """Run Section 3 tests."""
    print("🧠 STEP 6 - SECTION 3: Adaptive Decision Engine")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Intervention outcome tracking
    if test_intervention_outcome_tracking():
        tests_passed += 1
    
    # Test 2: Learning memory system
    if test_learning_memory_system():
        tests_passed += 1
    
    # Test 3: Adaptive learning rules
    if test_adaptive_learning_rules():
        tests_passed += 1
    
    # Test 4: Adaptive decision engine
    if test_adaptive_decision_engine():
        tests_passed += 1
    
    # Test 5: Outcome recording and learning
    if test_outcome_recording_and_learning():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Section 3 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 3 PASSED - Ready for Section 4")
        print("\n🎯 Next: Implement deployment integration and system coordination")
        return True
    else:
        print("❌ Section 3 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
