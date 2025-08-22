"""
Step 6 Section 2: Recommendation Generation Algorithms
======================================================
Implement intelligent algorithms for generating conservation recommendations.
"""

import sys
import os
import json
import time
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
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

@dataclass
class ConservationContext:
    """Context information for generating conservation recommendations."""
    location: Tuple[float, float]  # GPS coordinates
    ecosystem_type: str  # rainforest, dry_forest, coastal, etc.
    protected_area_status: bool = False
    community_presence: bool = True
    accessibility: float = 0.5  # 0.0 to 1.0, where 1.0 is easily accessible
    infrastructure_quality: float = 0.3  # 0.0 to 1.0
    local_governance_strength: float = 0.6  # 0.0 to 1.0
    economic_conditions: str = "low_income"  # low_income, middle_income, stable
    historical_success_rate: float = 0.7  # success rate of past interventions
    seasonal_factors: Dict[str, Any] = field(default_factory=dict)
    stakeholder_capacity: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.seasonal_factors:
            self.seasonal_factors = {
                "dry_season_months": [4, 5, 6, 7, 8, 9, 10],
                "cyclone_season": [11, 12, 1, 2, 3],
                "accessibility_variation": 0.3
            }
        if not self.stakeholder_capacity:
            self.stakeholder_capacity = {
                "local_government": 0.5,
                "community_organizations": 0.7,
                "conservation_ngos": 0.8,
                "international_partners": 0.6
            }

@dataclass
class RecommendationScore:
    """Scoring system for ranking conservation recommendations."""
    feasibility_score: float = 0.0  # 0.0 to 1.0
    impact_score: float = 0.0  # 0.0 to 1.0
    urgency_score: float = 0.0  # 0.0 to 1.0
    cost_effectiveness_score: float = 0.0  # 0.0 to 1.0
    stakeholder_support_score: float = 0.0  # 0.0 to 1.0
    sustainability_score: float = 0.0  # 0.0 to 1.0
    total_score: float = 0.0
    confidence_level: float = 0.0  # 0.0 to 1.0
    
    def calculate_total_score(self, weights: Dict[str, float] = None) -> float:
        """Calculate weighted total score."""
        if weights is None:
            weights = {
                "feasibility": 0.20,
                "impact": 0.25,
                "urgency": 0.20,
                "cost_effectiveness": 0.15,
                "stakeholder_support": 0.15,
                "sustainability": 0.05
            }
        
        self.total_score = (
            self.feasibility_score * weights["feasibility"] +
            self.impact_score * weights["impact"] +
            self.urgency_score * weights["urgency"] +
            self.cost_effectiveness_score * weights["cost_effectiveness"] +
            self.stakeholder_support_score * weights["stakeholder_support"] +
            self.sustainability_score * weights["sustainability"]
        )
        
        return self.total_score

class RecommendationGenerator:
    """Core algorithm for generating conservation recommendations."""
    
    def __init__(self):
        self.knowledge_base = MadagascarConservationKnowledgeBase()
        self.scoring_weights = self._initialize_scoring_weights()
        self.action_compatibility_matrix = self._build_action_compatibility_matrix()
        self.resource_requirements_db = self._initialize_resource_requirements()
        self.success_probability_model = self._initialize_success_model()
    
    def _initialize_scoring_weights(self) -> Dict[str, Dict[str, float]]:
        """Initialize scoring weights for different scenarios."""
        return {
            "emergency_response": {
                "feasibility": 0.30,
                "impact": 0.25,
                "urgency": 0.35,
                "cost_effectiveness": 0.05,
                "stakeholder_support": 0.05,
                "sustainability": 0.00
            },
            "long_term_conservation": {
                "feasibility": 0.15,
                "impact": 0.30,
                "urgency": 0.10,
                "cost_effectiveness": 0.20,
                "stakeholder_support": 0.20,
                "sustainability": 0.05
            },
            "community_based": {
                "feasibility": 0.20,
                "impact": 0.20,
                "urgency": 0.15,
                "cost_effectiveness": 0.15,
                "stakeholder_support": 0.25,
                "sustainability": 0.05
            },
            "research_focused": {
                "feasibility": 0.25,
                "impact": 0.15,
                "urgency": 0.10,
                "cost_effectiveness": 0.20,
                "stakeholder_support": 0.10,
                "sustainability": 0.20
            }
        }
    
    def _build_action_compatibility_matrix(self) -> Dict[ConservationAction, Dict[ConservationAction, float]]:
        """Build compatibility matrix for conservation actions."""
        actions = list(ConservationAction)
        compatibility = {}
        
        for action1 in actions:
            compatibility[action1] = {}
            for action2 in actions:
                if action1 == action2:
                    compatibility[action1][action2] = 1.0
                else:
                    # Calculate compatibility based on action types
                    compatibility[action1][action2] = self._calculate_action_compatibility(action1, action2)
        
        return compatibility
    
    def _calculate_action_compatibility(self, action1: ConservationAction, action2: ConservationAction) -> float:
        """Calculate compatibility score between two actions."""
        # Define action categories
        action_categories = {
            "immediate": [ConservationAction.DEPLOY_PATROL_TEAM, ConservationAction.EMERGENCY_SPECIES_RELOCATION],
            "habitat": [ConservationAction.REFORESTATION, ConservationAction.HABITAT_CORRIDOR_CREATION, 
                       ConservationAction.INVASIVE_SPECIES_REMOVAL, ConservationAction.WATER_SOURCE_PROTECTION],
            "community": [ConservationAction.ALTERNATIVE_LIVELIHOOD_PROGRAM, ConservationAction.COMMUNITY_CONSERVATION_TRAINING,
                         ConservationAction.ECOTOURISM_DEVELOPMENT, ConservationAction.SUSTAINABLE_AGRICULTURE_SUPPORT],
            "research": [ConservationAction.POPULATION_SURVEY, ConservationAction.GENETIC_ANALYSIS,
                        ConservationAction.BEHAVIOR_STUDY, ConservationAction.LONG_TERM_MONITORING],
            "enforcement": [ConservationAction.LAW_ENFORCEMENT_STRENGTHENING, ConservationAction.DEPLOY_PATROL_TEAM],
            "policy": [ConservationAction.POLICY_DEVELOPMENT, ConservationAction.PROTECTED_AREA_DESIGNATION,
                      ConservationAction.INTERNATIONAL_COOPERATION]
        }
        
        # Find categories for each action
        action1_categories = [cat for cat, actions in action_categories.items() if action1 in actions]
        action2_categories = [cat for cat, actions in action_categories.items() if action2 in actions]
        
        # Calculate compatibility based on category overlap and complementarity
        if any(cat in action2_categories for cat in action1_categories):
            return 0.8  # Same category - high compatibility
        elif ("immediate" in action1_categories and "enforcement" in action2_categories) or \
             ("enforcement" in action1_categories and "immediate" in action2_categories):
            return 0.9  # Immediate + enforcement - very high compatibility
        elif ("habitat" in action1_categories and "community" in action2_categories) or \
             ("community" in action1_categories and "habitat" in action2_categories):
            return 0.7  # Habitat + community - good compatibility
        elif ("research" in action1_categories and any(cat in action2_categories for cat in ["habitat", "community"])):
            return 0.6  # Research + implementation - moderate compatibility
        else:
            return 0.4  # Different areas - lower compatibility
    
    def _initialize_resource_requirements(self) -> Dict[ConservationAction, Dict[str, Any]]:
        """Initialize resource requirements for each conservation action."""
        return {
            ConservationAction.DEPLOY_PATROL_TEAM: {
                "personnel": 5,
                "equipment": 2,
                "vehicles": 1,
                "duration_days": 30,
                "cost_usd": 15000,
                "expertise_required": ["field_operations", "wildlife_protection"]
            },
            ConservationAction.REFORESTATION: {
                "personnel": 10,
                "equipment": 5,
                "vehicles": 2,
                "duration_days": 180,
                "cost_usd": 50000,
                "expertise_required": ["forestry", "botany", "community_engagement"]
            },
            ConservationAction.COMMUNITY_CONSERVATION_TRAINING: {
                "personnel": 3,
                "equipment": 1,
                "vehicles": 1,
                "duration_days": 14,
                "cost_usd": 8000,
                "expertise_required": ["education", "community_development", "conservation"]
            },
            ConservationAction.POPULATION_SURVEY: {
                "personnel": 4,
                "equipment": 3,
                "vehicles": 1,
                "duration_days": 45,
                "cost_usd": 25000,
                "expertise_required": ["wildlife_biology", "data_analysis", "field_research"]
            },
            ConservationAction.LAW_ENFORCEMENT_STRENGTHENING: {
                "personnel": 8,
                "equipment": 4,
                "vehicles": 3,
                "duration_days": 90,
                "cost_usd": 40000,
                "expertise_required": ["law_enforcement", "legal_affairs", "investigation"]
            },
            ConservationAction.ALTERNATIVE_LIVELIHOOD_PROGRAM: {
                "personnel": 6,
                "equipment": 2,
                "vehicles": 1,
                "duration_days": 365,
                "cost_usd": 75000,
                "expertise_required": ["economic_development", "skills_training", "microfinance"]
            },
            ConservationAction.HABITAT_CORRIDOR_CREATION: {
                "personnel": 12,
                "equipment": 8,
                "vehicles": 3,
                "duration_days": 270,
                "cost_usd": 120000,
                "expertise_required": ["landscape_planning", "forestry", "wildlife_ecology"]
            },
            ConservationAction.ECOTOURISM_DEVELOPMENT: {
                "personnel": 8,
                "equipment": 3,
                "vehicles": 2,
                "duration_days": 540,
                "cost_usd": 100000,
                "expertise_required": ["tourism_development", "marketing", "hospitality"]
            }
        }
    
    def _initialize_success_model(self) -> Dict[str, Any]:
        """Initialize model for predicting conservation success probability."""
        return {
            "base_success_rates": {
                ConservationStrategy.HABITAT_PROTECTION: 0.75,
                ConservationStrategy.SPECIES_RECOVERY: 0.65,
                ConservationStrategy.COMMUNITY_ENGAGEMENT: 0.80,
                ConservationStrategy.LAW_ENFORCEMENT: 0.60,
                ConservationStrategy.RESEARCH_MONITORING: 0.85,
                ConservationStrategy.ECOSYSTEM_RESTORATION: 0.55,
                ConservationStrategy.SUSTAINABLE_DEVELOPMENT: 0.70
            },
            "context_modifiers": {
                "protected_area": 1.2,
                "community_support": 1.3,
                "government_backing": 1.25,
                "adequate_funding": 1.4,
                "experienced_team": 1.15,
                "stakeholder_conflict": 0.7,
                "limited_access": 0.8,
                "political_instability": 0.6
            }
        }
    
    def generate_recommendations(self, 
                               threats: List[ThreatDetection],
                               species_detections: List[SpeciesDetection],
                               context: ConservationContext,
                               available_resources: List[ConservationResource],
                               max_recommendations: int = 5) -> List[ConservationRecommendation]:
        """Generate prioritized conservation recommendations."""
        
        print(f"🧠 Generating recommendations for {len(threats)} threats, {len(species_detections)} species...")
        
        # Step 1: Analyze threats and species
        threat_analysis = self._analyze_threats(threats)
        species_analysis = self._analyze_species(species_detections)
        
        # Step 2: Generate candidate recommendations
        candidates = self._generate_candidate_recommendations(threat_analysis, species_analysis, context)
        
        # Step 3: Score and rank recommendations
        scored_recommendations = []
        for candidate in candidates:
            score = self._score_recommendation(candidate, context, available_resources)
            candidate.confidence_score = score.confidence_level
            scored_recommendations.append((candidate, score))
        
        # Step 4: Optimize recommendation portfolio
        optimized_portfolio = self._optimize_recommendation_portfolio(
            scored_recommendations, available_resources, max_recommendations
        )
        
        # Step 5: Finalize recommendations with implementation details
        final_recommendations = []
        for recommendation, score in optimized_portfolio:
            self._add_implementation_details(recommendation, context, available_resources)
            final_recommendations.append(recommendation)
        
        print(f"✅ Generated {len(final_recommendations)} prioritized recommendations")
        return final_recommendations
    
    def _analyze_threats(self, threats: List[ThreatDetection]) -> Dict[str, Any]:
        """Analyze threat patterns and priorities."""
        if not threats:
            return {"total_threats": 0, "primary_threats": [], "urgency_distribution": {}}
        
        threat_counts = defaultdict(int)
        severity_sum = defaultdict(float)
        urgency_counts = defaultdict(int)
        
        for threat in threats:
            threat_counts[threat.threat_type] += 1
            severity_sum[threat.threat_type] += threat.severity
            urgency_counts[threat.urgency] += 1
        
        # Calculate average severity by threat type
        avg_severity = {
            threat_type: severity_sum[threat_type] / threat_counts[threat_type]
            for threat_type in threat_counts.keys()
        }
        
        # Rank threats by combined frequency and severity
        threat_priorities = []
        for threat_type, count in threat_counts.items():
            priority_score = count * avg_severity[threat_type]
            threat_priorities.append((threat_type, priority_score, count, avg_severity[threat_type]))
        
        threat_priorities.sort(key=lambda x: x[1], reverse=True)
        
        return {
            "total_threats": len(threats),
            "threat_counts": dict(threat_counts),
            "average_severity": dict(avg_severity),
            "primary_threats": [tp[0] for tp in threat_priorities[:3]],
            "urgency_distribution": dict(urgency_counts),
            "highest_priority": threat_priorities[0] if threat_priorities else None
        }
    
    def _analyze_species(self, species_detections: List[SpeciesDetection]) -> Dict[str, Any]:
        """Analyze species detection patterns and conservation needs."""
        if not species_detections:
            return {"total_detections": 0, "species_diversity": 0, "conservation_priorities": []}
        
        species_counts = defaultdict(int)
        confidence_sum = defaultdict(float)
        
        for detection in species_detections:
            # Map Madagascar species to conservation types
            species_type = self._map_species_to_type(detection.species)
            species_counts[species_type] += 1
            confidence_sum[species_type] += detection.confidence
        
        # Calculate average confidence by species type
        avg_confidence = {
            species_type: confidence_sum[species_type] / species_counts[species_type]
            for species_type in species_counts.keys()
        }
        
        # Determine conservation priorities based on species presence and status
        conservation_priorities = []
        for species_type, count in species_counts.items():
            # Assign conservation status based on species type
            status = self._get_conservation_status(species_type)
            urgency = self._calculate_species_urgency(species_type, status, count, avg_confidence[species_type])
            conservation_priorities.append((species_type, status, urgency, count))
        
        conservation_priorities.sort(key=lambda x: x[2], reverse=True)
        
        return {
            "total_detections": len(species_detections),
            "species_diversity": len(species_counts),
            "species_counts": dict(species_counts),
            "average_confidence": dict(avg_confidence),
            "conservation_priorities": conservation_priorities[:5]  # Top 5 priority species
        }
    
    def _map_species_to_type(self, madagascar_species: MadagascarSpecies) -> SpeciesType:
        """Map Madagascar species to general species types."""
        species_mapping = {
            MadagascarSpecies.LEMUR_CATTA: SpeciesType.LEMUR,
            MadagascarSpecies.INDRI_INDRI: SpeciesType.LEMUR,
            MadagascarSpecies.EULEMUR_FULVUS: SpeciesType.LEMUR,
            MadagascarSpecies.PROPITHECUS_DIADEMA: SpeciesType.LEMUR,
            MadagascarSpecies.MICROCEBUS_MURINUS: SpeciesType.LEMUR,
            MadagascarSpecies.BROOKESIA_MICRA: SpeciesType.CHAMELEON,
            MadagascarSpecies.FURCIFER_PARDALIS: SpeciesType.CHAMELEON,
            MadagascarSpecies.UROPLATUS_PHANTASTICUS: SpeciesType.REPTILE,
            MadagascarSpecies.UNKNOWN_SPECIES: SpeciesType.UNKNOWN
        }
        return species_mapping.get(madagascar_species, SpeciesType.UNKNOWN)
    
    def _get_conservation_status(self, species_type: SpeciesType) -> ConservationStatus:
        """Get conservation status for species type."""
        status_mapping = {
            SpeciesType.LEMUR: ConservationStatus.ENDANGERED,
            SpeciesType.FOSSA: ConservationStatus.VULNERABLE,
            SpeciesType.CHAMELEON: ConservationStatus.NEAR_THREATENED,
            SpeciesType.TENREC: ConservationStatus.LEAST_CONCERN,
            SpeciesType.BAOBAB: ConservationStatus.ENDANGERED,
            SpeciesType.BIRD: ConservationStatus.NEAR_THREATENED,
            SpeciesType.REPTILE: ConservationStatus.VULNERABLE
        }
        return status_mapping.get(species_type, ConservationStatus.DATA_DEFICIENT)
    
    def _calculate_species_urgency(self, species_type: SpeciesType, status: ConservationStatus, 
                                 count: int, confidence: float) -> float:
        """Calculate urgency score for species conservation."""
        # Base urgency from conservation status
        status_urgency = {
            ConservationStatus.CRITICALLY_ENDANGERED: 1.0,
            ConservationStatus.ENDANGERED: 0.8,
            ConservationStatus.VULNERABLE: 0.6,
            ConservationStatus.NEAR_THREATENED: 0.4,
            ConservationStatus.LEAST_CONCERN: 0.2,
            ConservationStatus.DATA_DEFICIENT: 0.5
        }
        
        base_urgency = status_urgency.get(status, 0.5)
        
        # Adjust based on detection count (fewer detections = higher urgency)
        detection_factor = max(0.2, 1.0 - (count - 1) * 0.1)
        
        # Adjust based on confidence (higher confidence = higher urgency)
        confidence_factor = confidence
        
        return min(1.0, base_urgency * detection_factor * confidence_factor)
    
    def _generate_candidate_recommendations(self, threat_analysis: Dict[str, Any], 
                                          species_analysis: Dict[str, Any],
                                          context: ConservationContext) -> List[ConservationRecommendation]:
        """Generate candidate conservation recommendations."""
        candidates = []
        
        # Generate threat-based recommendations
        for threat_type in threat_analysis.get("primary_threats", []):
            threat_plan = self.knowledge_base.get_threat_mitigation_plan(threat_type, 0.8)
            if "immediate_actions" in threat_plan:
                recommendation = self._create_threat_recommendation(threat_type, threat_plan, context)
                if recommendation:
                    candidates.append(recommendation)
        
        # Generate species-based recommendations
        for species_data in species_analysis.get("conservation_priorities", []):
            species_type, status, urgency, count = species_data
            species_plan = self.knowledge_base.get_species_conservation_plan(species_type, status)
            if "recommended_actions" in species_plan:
                recommendation = self._create_species_recommendation(species_type, species_plan, context)
                if recommendation:
                    candidates.append(recommendation)
        
        # Generate integrated ecosystem recommendations
        if threat_analysis.get("total_threats", 0) > 0 and species_analysis.get("species_diversity", 0) > 0:
            ecosystem_recommendation = self._create_ecosystem_recommendation(
                threat_analysis, species_analysis, context
            )
            if ecosystem_recommendation:
                candidates.append(ecosystem_recommendation)
        
        return candidates
    
    def _create_threat_recommendation(self, threat_type: ThreatType, threat_plan: Dict[str, Any],
                                    context: ConservationContext) -> Optional[ConservationRecommendation]:
        """Create recommendation for specific threat."""
        try:
            # Determine priority based on threat urgency
            urgency_priority_mapping = {
                ThreatUrgency.CRISIS: ConservationPriority.EMERGENCY,
                ThreatUrgency.EMERGENCY: ConservationPriority.CRITICAL,
                ThreatUrgency.URGENT: ConservationPriority.HIGH,
                ThreatUrgency.ELEVATED: ConservationPriority.MEDIUM,
                ThreatUrgency.ROUTINE: ConservationPriority.LOW
            }
            
            priority = ConservationPriority.HIGH  # Default
            
            # Select primary strategy
            strategies = threat_plan.get("primary_strategies", [])
            primary_strategy = strategies[0] if strategies else ConservationStrategy.HABITAT_PROTECTION
            
            # Select actions
            immediate_actions = threat_plan.get("immediate_actions", [])
            long_term_actions = threat_plan.get("long_term_actions", [])
            
            # Combine immediate and long-term actions (limit to 5)
            all_actions = immediate_actions + long_term_actions
            selected_actions = all_actions[:5]
            
            recommendation_id = f"threat_{threat_type.value}_{int(datetime.utcnow().timestamp())}"
            
            recommendation = ConservationRecommendation(
                recommendation_id=recommendation_id,
                priority=priority,
                strategy=primary_strategy,
                actions=selected_actions,
                target_threats=[threat_type],
                target_location=context.location,
                estimated_cost=self._estimate_total_cost(selected_actions)
            )
            
            return recommendation
            
        except Exception as e:
            print(f"⚠️  Error creating threat recommendation: {e}")
            return None
    
    def _create_species_recommendation(self, species_type: SpeciesType, species_plan: Dict[str, Any],
                                     context: ConservationContext) -> Optional[ConservationRecommendation]:
        """Create recommendation for specific species."""
        try:
            # Determine priority based on conservation status
            priority = ConservationPriority.MEDIUM  # Default
            
            # Select primary strategy
            strategies = species_plan.get("key_strategies", [])
            primary_strategy = strategies[0] if strategies else ConservationStrategy.SPECIES_RECOVERY
            
            # Select actions
            recommended_actions = species_plan.get("recommended_actions", [])
            selected_actions = recommended_actions[:4]  # Limit to 4 actions
            
            recommendation_id = f"species_{species_type.value}_{int(datetime.utcnow().timestamp())}"
            
            recommendation = ConservationRecommendation(
                recommendation_id=recommendation_id,
                priority=priority,
                strategy=primary_strategy,
                actions=selected_actions,
                target_species=[species_type.value],
                target_location=context.location,
                estimated_cost=self._estimate_total_cost(selected_actions)
            )
            
            return recommendation
            
        except Exception as e:
            print(f"⚠️  Error creating species recommendation: {e}")
            return None
    
    def _create_ecosystem_recommendation(self, threat_analysis: Dict[str, Any], 
                                       species_analysis: Dict[str, Any],
                                       context: ConservationContext) -> Optional[ConservationRecommendation]:
        """Create integrated ecosystem recommendation."""
        try:
            recommendation_id = f"ecosystem_{context.ecosystem_type}_{int(datetime.utcnow().timestamp())}"
            
            # Integrated approach combining habitat protection and community engagement
            actions = [
                ConservationAction.HABITAT_CORRIDOR_CREATION,
                ConservationAction.COMMUNITY_CONSERVATION_TRAINING,
                ConservationAction.LONG_TERM_MONITORING,
                ConservationAction.SUSTAINABLE_AGRICULTURE_SUPPORT
            ]
            
            # Determine priority based on threat severity and species diversity
            threat_severity = len(threat_analysis.get("primary_threats", []))
            species_diversity = species_analysis.get("species_diversity", 0)
            
            if threat_severity >= 3 or species_diversity >= 4:
                priority = ConservationPriority.HIGH
            elif threat_severity >= 2 or species_diversity >= 2:
                priority = ConservationPriority.MEDIUM
            else:
                priority = ConservationPriority.LOW
            
            recommendation = ConservationRecommendation(
                recommendation_id=recommendation_id,
                priority=priority,
                strategy=ConservationStrategy.ECOSYSTEM_RESTORATION,
                actions=actions,
                target_species=[sp[0].value for sp in species_analysis.get("conservation_priorities", [])[:3]],
                target_threats=threat_analysis.get("primary_threats", [])[:3],
                target_location=context.location,
                estimated_cost=self._estimate_total_cost(actions)
            )
            
            return recommendation
            
        except Exception as e:
            print(f"⚠️  Error creating ecosystem recommendation: {e}")
            return None
    
    def _estimate_total_cost(self, actions: List[ConservationAction]) -> float:
        """Estimate total cost for a list of actions."""
        total_cost = 0.0
        for action in actions:
            if action in self.resource_requirements_db:
                total_cost += self.resource_requirements_db[action].get("cost_usd", 10000)
        return total_cost
    
    def _score_recommendation(self, recommendation: ConservationRecommendation,
                            context: ConservationContext,
                            available_resources: List[ConservationResource]) -> RecommendationScore:
        """Score a conservation recommendation."""
        score = RecommendationScore()
        
        # Calculate feasibility score
        score.feasibility_score = self._calculate_feasibility(recommendation, context, available_resources)
        
        # Calculate impact score
        score.impact_score = self._calculate_impact(recommendation, context)
        
        # Calculate urgency score
        score.urgency_score = self._calculate_urgency(recommendation)
        
        # Calculate cost-effectiveness score
        score.cost_effectiveness_score = self._calculate_cost_effectiveness(recommendation)
        
        # Calculate stakeholder support score
        score.stakeholder_support_score = self._calculate_stakeholder_support(recommendation, context)
        
        # Calculate sustainability score
        score.sustainability_score = self._calculate_sustainability(recommendation, context)
        
        # Calculate total weighted score
        weights = self._select_scoring_weights(recommendation, context)
        score.calculate_total_score(weights)
        
        # Calculate confidence level
        score.confidence_level = self._calculate_confidence(recommendation, context)
        
        return score
    
    def _calculate_feasibility(self, recommendation: ConservationRecommendation,
                             context: ConservationContext, 
                             available_resources: List[ConservationResource]) -> float:
        """Calculate feasibility score for recommendation."""
        # Base feasibility from accessibility and infrastructure
        base_feasibility = (context.accessibility + context.infrastructure_quality) / 2
        
        # Adjust for resource availability
        resource_availability = self._check_resource_availability(recommendation, available_resources)
        
        # Adjust for governance and community factors
        governance_factor = context.local_governance_strength
        
        # Combine factors
        feasibility = (base_feasibility * 0.4 + resource_availability * 0.4 + governance_factor * 0.2)
        
        return min(1.0, max(0.0, feasibility))
    
    def _calculate_impact(self, recommendation: ConservationRecommendation, 
                        context: ConservationContext) -> float:
        """Calculate potential impact score."""
        # Base impact from strategy type
        strategy_impact = {
            ConservationStrategy.HABITAT_PROTECTION: 0.85,
            ConservationStrategy.SPECIES_RECOVERY: 0.75,
            ConservationStrategy.COMMUNITY_ENGAGEMENT: 0.80,
            ConservationStrategy.LAW_ENFORCEMENT: 0.70,
            ConservationStrategy.ECOSYSTEM_RESTORATION: 0.90,
            ConservationStrategy.SUSTAINABLE_DEVELOPMENT: 0.75
        }
        
        base_impact = strategy_impact.get(recommendation.strategy, 0.7)
        
        # Adjust for number of actions (more comprehensive = higher impact)
        action_factor = min(1.2, 1.0 + len(recommendation.actions) * 0.05)
        
        # Adjust for protected area status
        protection_factor = 1.1 if context.protected_area_status else 1.0
        
        impact = base_impact * action_factor * protection_factor
        
        return min(1.0, max(0.0, impact))
    
    def _calculate_urgency(self, recommendation: ConservationRecommendation) -> float:
        """Calculate urgency score."""
        priority_urgency = {
            ConservationPriority.EMERGENCY: 1.0,
            ConservationPriority.CRITICAL: 0.9,
            ConservationPriority.HIGH: 0.7,
            ConservationPriority.MEDIUM: 0.5,
            ConservationPriority.LOW: 0.3
        }
        
        return priority_urgency.get(recommendation.priority, 0.5)
    
    def _calculate_cost_effectiveness(self, recommendation: ConservationRecommendation) -> float:
        """Calculate cost-effectiveness score."""
        # Higher cost-effectiveness for lower costs and high impact strategies
        if recommendation.estimated_cost <= 0:
            return 0.5  # Default if cost not estimated
        
        # Normalize cost (assuming typical range 1k - 200k USD)
        normalized_cost = min(1.0, recommendation.estimated_cost / 200000)
        
        # Cost-effectiveness is inverse of cost (lower cost = higher score)
        cost_effectiveness = 1.0 - normalized_cost
        
        return max(0.1, cost_effectiveness)  # Minimum score of 0.1
    
    def _calculate_stakeholder_support(self, recommendation: ConservationRecommendation,
                                     context: ConservationContext) -> float:
        """Calculate stakeholder support score."""
        # Base support from community engagement actions
        community_actions = [
            ConservationAction.COMMUNITY_CONSERVATION_TRAINING,
            ConservationAction.ALTERNATIVE_LIVELIHOOD_PROGRAM,
            ConservationAction.ECOTOURISM_DEVELOPMENT,
            ConservationAction.SUSTAINABLE_AGRICULTURE_SUPPORT
        ]
        
        community_focus = sum(1 for action in recommendation.actions if action in community_actions)
        community_score = min(1.0, community_focus * 0.3)
        
        # Add stakeholder capacity factors
        avg_stakeholder_capacity = sum(context.stakeholder_capacity.values()) / len(context.stakeholder_capacity)
        
        # Combine factors
        support_score = (community_score * 0.6 + avg_stakeholder_capacity * 0.4)
        
        return min(1.0, max(0.2, support_score))
    
    def _calculate_sustainability(self, recommendation: ConservationRecommendation,
                                context: ConservationContext) -> float:
        """Calculate sustainability score."""
        # Base sustainability from strategy
        strategy_sustainability = {
            ConservationStrategy.COMMUNITY_ENGAGEMENT: 0.9,
            ConservationStrategy.SUSTAINABLE_DEVELOPMENT: 0.85,
            ConservationStrategy.ECOSYSTEM_RESTORATION: 0.8,
            ConservationStrategy.HABITAT_PROTECTION: 0.75,
            ConservationStrategy.RESEARCH_MONITORING: 0.7,
            ConservationStrategy.LAW_ENFORCEMENT: 0.6,
            ConservationStrategy.SPECIES_RECOVERY: 0.65
        }
        
        base_sustainability = strategy_sustainability.get(recommendation.strategy, 0.7)
        
        # Adjust for historical success rate
        success_factor = context.historical_success_rate
        
        # Adjust for economic conditions
        economic_factor = {"low_income": 0.8, "middle_income": 0.9, "stable": 1.0}.get(context.economic_conditions, 0.8)
        
        sustainability = base_sustainability * success_factor * economic_factor
        
        return min(1.0, max(0.0, sustainability))
    
    def _select_scoring_weights(self, recommendation: ConservationRecommendation,
                              context: ConservationContext) -> Dict[str, float]:
        """Select appropriate scoring weights based on recommendation and context."""
        # Emergency situations prioritize urgency and feasibility
        if recommendation.priority in [ConservationPriority.EMERGENCY, ConservationPriority.CRITICAL]:
            return self.scoring_weights["emergency_response"]
        
        # Community-focused strategies
        if recommendation.strategy == ConservationStrategy.COMMUNITY_ENGAGEMENT:
            return self.scoring_weights["community_based"]
        
        # Research and monitoring strategies
        if recommendation.strategy == ConservationStrategy.RESEARCH_MONITORING:
            return self.scoring_weights["research_focused"]
        
        # Default to long-term conservation
        return self.scoring_weights["long_term_conservation"]
    
    def _calculate_confidence(self, recommendation: ConservationRecommendation,
                            context: ConservationContext) -> float:
        """Calculate confidence level in recommendation."""
        # Base confidence from historical success rate
        base_confidence = context.historical_success_rate
        
        # Adjust for completeness of information
        info_completeness = 0.8  # Assume good information quality
        
        # Adjust for strategy familiarity
        strategy_confidence = self.success_probability_model["base_success_rates"].get(
            recommendation.strategy, 0.7
        )
        
        confidence = (base_confidence * 0.4 + info_completeness * 0.3 + strategy_confidence * 0.3)
        
        return min(1.0, max(0.3, confidence))
    
    def _check_resource_availability(self, recommendation: ConservationRecommendation,
                                   available_resources: List[ConservationResource]) -> float:
        """Check if required resources are available."""
        total_requirement_score = 0.0
        total_availability_score = 0.0
        
        for action in recommendation.actions:
            if action in self.resource_requirements_db:
                requirements = self.resource_requirements_db[action]
                
                # Check personnel availability
                personnel_needed = requirements.get("personnel", 0)
                personnel_available = sum(
                    r.get_available_capacity() for r in available_resources 
                    if r.resource_type == "field_personnel"
                )
                
                personnel_score = min(1.0, personnel_available / max(1, personnel_needed))
                
                # Check funding availability
                cost_needed = requirements.get("cost_usd", 0)
                funding_available = sum(
                    r.get_available_capacity() for r in available_resources 
                    if r.resource_type == "conservation_funding"
                )
                
                funding_score = min(1.0, funding_available / max(1, cost_needed))
                
                # Average resource availability for this action
                action_availability = (personnel_score + funding_score) / 2
                
                total_requirement_score += 1.0
                total_availability_score += action_availability
        
        if total_requirement_score == 0:
            return 0.7  # Default availability if no requirements specified
        
        return total_availability_score / total_requirement_score
    
    def _optimize_recommendation_portfolio(self, scored_recommendations: List[Tuple[ConservationRecommendation, RecommendationScore]],
                                         available_resources: List[ConservationResource],
                                         max_recommendations: int) -> List[Tuple[ConservationRecommendation, RecommendationScore]]:
        """Optimize portfolio of recommendations considering resource constraints and synergies."""
        if len(scored_recommendations) <= max_recommendations:
            return scored_recommendations
        
        # Sort by total score
        scored_recommendations.sort(key=lambda x: x[1].total_score, reverse=True)
        
        # Simple greedy selection for now (can be enhanced with more sophisticated optimization)
        selected = []
        remaining_resources = {r.resource_type: r.get_available_capacity() for r in available_resources}
        
        for recommendation, score in scored_recommendations:
            if len(selected) >= max_recommendations:
                break
            
            # Check if recommendation can be accommodated with remaining resources
            can_accommodate = True
            resource_needs = {}
            
            for action in recommendation.actions:
                if action in self.resource_requirements_db:
                    requirements = self.resource_requirements_db[action]
                    
                    personnel_needed = requirements.get("personnel", 0)
                    cost_needed = requirements.get("cost_usd", 0)
                    
                    resource_needs["field_personnel"] = resource_needs.get("field_personnel", 0) + personnel_needed
                    resource_needs["conservation_funding"] = resource_needs.get("conservation_funding", 0) + cost_needed
            
            # Check if we have enough resources
            for resource_type, needed in resource_needs.items():
                if needed > remaining_resources.get(resource_type, 0):
                    can_accommodate = False
                    break
            
            if can_accommodate:
                selected.append((recommendation, score))
                # Update remaining resources
                for resource_type, needed in resource_needs.items():
                    remaining_resources[resource_type] -= needed
        
        return selected
    
    def _add_implementation_details(self, recommendation: ConservationRecommendation,
                                  context: ConservationContext,
                                  available_resources: List[ConservationResource]):
        """Add detailed implementation information to recommendation."""
        # Calculate resource requirements
        total_personnel = 0
        total_cost = 0
        total_duration = 0
        required_expertise = set()
        
        for action in recommendation.actions:
            if action in self.resource_requirements_db:
                requirements = self.resource_requirements_db[action]
                total_personnel += requirements.get("personnel", 0)
                total_cost += requirements.get("cost_usd", 0)
                total_duration = max(total_duration, requirements.get("duration_days", 0))
                required_expertise.update(requirements.get("expertise_required", []))
        
        recommendation.required_resources = {
            "field_personnel": total_personnel,
            "conservation_funding": total_cost,
            "duration_days": total_duration,
            "expertise_required": list(required_expertise)
        }
        
        recommendation.estimated_cost = total_cost
        
        # Add expected outcomes
        recommendation.expected_outcomes = {
            "threat_reduction_expected": "medium",
            "species_conservation_impact": "moderate",
            "community_benefit_level": "moderate",
            "habitat_improvement": "significant",
            "implementation_probability": recommendation.confidence_score
        }

def test_recommendation_generator_initialization():
    """Test recommendation generator initialization."""
    print("🧠 Testing Recommendation Generator Initialization...")
    
    try:
        generator = RecommendationGenerator()
        
        # Test knowledge base initialization
        if generator.knowledge_base:
            print("✅ Knowledge base initialized")
        else:
            print("❌ Knowledge base initialization failed")
            return False
        
        # Test scoring weights
        if len(generator.scoring_weights) >= 4:
            print(f"✅ Scoring weights: {len(generator.scoring_weights)} scenarios")
        else:
            print("❌ Scoring weights insufficient")
            return False
        
        # Test action compatibility matrix
        action_count = len(list(ConservationAction))
        matrix_size = len(generator.action_compatibility_matrix)
        if matrix_size == action_count:
            print(f"✅ Action compatibility matrix: {matrix_size}x{matrix_size}")
        else:
            print(f"❌ Action compatibility matrix incomplete: {matrix_size}/{action_count}")
            return False
        
        # Test resource requirements database
        if len(generator.resource_requirements_db) >= 5:
            print(f"✅ Resource requirements: {len(generator.resource_requirements_db)} actions")
        else:
            print("❌ Resource requirements insufficient")
            return False
        
        # Test success probability model
        if "base_success_rates" in generator.success_probability_model:
            success_rates = len(generator.success_probability_model["base_success_rates"])
            print(f"✅ Success probability model: {success_rates} strategies")
        else:
            print("❌ Success probability model missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Recommendation generator initialization error: {e}")
        return False

def test_threat_and_species_analysis():
    """Test threat and species analysis algorithms."""
    print("\n📊 Testing Threat and Species Analysis...")
    
    try:
        generator = RecommendationGenerator()
        
        # Create test threats
        test_threats = [
            ThreatDetection(
                detection_id="test_threat_1",
                threat_type=ThreatType.DEFORESTATION,
                severity=0.8,
                severity_level=ThreatSeverity.HIGH,
                urgency=ThreatUrgency.URGENT,
                confidence=0.9
            ),
            ThreatDetection(
                detection_id="test_threat_2",
                threat_type=ThreatType.POACHING,
                severity=0.95,
                severity_level=ThreatSeverity.CRITICAL,
                urgency=ThreatUrgency.EMERGENCY,
                confidence=0.85
            ),
            ThreatDetection(
                detection_id="test_threat_3",
                threat_type=ThreatType.DEFORESTATION,
                severity=0.7,
                severity_level=ThreatSeverity.HIGH,
                urgency=ThreatUrgency.ELEVATED,
                confidence=0.8
            )
        ]
        
        # Test threat analysis
        threat_analysis = generator._analyze_threats(test_threats)
        
        if threat_analysis["total_threats"] == 3:
            print("✅ Threat count analysis correct")
        else:
            print(f"❌ Threat count incorrect: {threat_analysis['total_threats']}")
            return False
        
        if len(threat_analysis["primary_threats"]) > 0:
            print(f"✅ Primary threats identified: {threat_analysis['primary_threats']}")
        else:
            print("❌ No primary threats identified")
            return False
        
        if ThreatType.DEFORESTATION in threat_analysis["threat_counts"]:
            print(f"✅ Threat frequency tracking: deforestation count = {threat_analysis['threat_counts'][ThreatType.DEFORESTATION]}")
        else:
            print("❌ Threat frequency tracking failed")
            return False
        
        # Create test species detections
        test_species = [
            SpeciesDetection(
                detection_id="species_1",
                species=MadagascarSpecies.LEMUR_CATTA,
                confidence=0.95,
                confidence_level=SpeciesConfidence.VERY_HIGH,
                timestamp=datetime.utcnow(),
                source="test_camera"
            ),
            SpeciesDetection(
                detection_id="species_2",
                species=MadagascarSpecies.FURCIFER_PARDALIS,
                confidence=0.8,
                confidence_level=SpeciesConfidence.HIGH,
                timestamp=datetime.utcnow(),
                source="test_camera"
            )
        ]
        
        # Test species analysis
        species_analysis = generator._analyze_species(test_species)
        
        if species_analysis["total_detections"] == 2:
            print("✅ Species detection count correct")
        else:
            print(f"❌ Species detection count incorrect: {species_analysis['total_detections']}")
            return False
        
        if species_analysis["species_diversity"] > 0:
            print(f"✅ Species diversity calculated: {species_analysis['species_diversity']}")
        else:
            print("❌ Species diversity calculation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Threat and species analysis error: {e}")
        return False

def test_recommendation_scoring():
    """Test recommendation scoring system."""
    print("\n🎯 Testing Recommendation Scoring...")
    
    try:
        generator = RecommendationGenerator()
        
        # Create test recommendation
        test_recommendation = ConservationRecommendation(
            recommendation_id="test_score_001",
            priority=ConservationPriority.HIGH,
            strategy=ConservationStrategy.HABITAT_PROTECTION,
            actions=[
                ConservationAction.DEPLOY_PATROL_TEAM,
                ConservationAction.REFORESTATION,
                ConservationAction.COMMUNITY_CONSERVATION_TRAINING
            ],
            estimated_cost=50000.0
        )
        
        # Create test context
        test_context = ConservationContext(
            location=(-18.947, 48.458),
            ecosystem_type="rainforest",
            protected_area_status=True,
            accessibility=0.7,
            infrastructure_quality=0.6,
            local_governance_strength=0.8
        )
        
        # Create test resources
        test_resources = [
            ConservationResource(
                resource_type="field_personnel",
                availability=0.8,
                capacity=20,
                cost_per_unit=100.0
            ),
            ConservationResource(
                resource_type="conservation_funding",
                availability=1.0,
                capacity=100000,
                cost_per_unit=1.0
            )
        ]
        
        # Test scoring
        score = generator._score_recommendation(test_recommendation, test_context, test_resources)
        
        # Check score components
        score_components = [
            ("feasibility", score.feasibility_score),
            ("impact", score.impact_score),
            ("urgency", score.urgency_score),
            ("cost_effectiveness", score.cost_effectiveness_score),
            ("stakeholder_support", score.stakeholder_support_score),
            ("sustainability", score.sustainability_score)
        ]
        
        valid_scores = 0
        for component_name, component_score in score_components:
            if 0.0 <= component_score <= 1.0:
                valid_scores += 1
                print(f"✅ {component_name}: {component_score:.2f}")
            else:
                print(f"❌ {component_name}: {component_score:.2f} (out of range)")
        
        if valid_scores == len(score_components):
            print(f"✅ All score components valid")
        else:
            print(f"❌ Score validation failed: {valid_scores}/{len(score_components)}")
            return False
        
        # Check total score
        if 0.0 <= score.total_score <= 1.0:
            print(f"✅ Total score: {score.total_score:.2f}")
        else:
            print(f"❌ Total score out of range: {score.total_score:.2f}")
            return False
        
        # Check confidence level
        if 0.0 <= score.confidence_level <= 1.0:
            print(f"✅ Confidence level: {score.confidence_level:.2f}")
        else:
            print(f"❌ Confidence level out of range: {score.confidence_level:.2f}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Recommendation scoring error: {e}")
        return False

def test_recommendation_generation_workflow():
    """Test complete recommendation generation workflow."""
    print("\n🔄 Testing Recommendation Generation Workflow...")
    
    try:
        generator = RecommendationGenerator()
        
        # Create comprehensive test data
        test_threats = [
            ThreatDetection(
                detection_id="workflow_threat_1",
                threat_type=ThreatType.DEFORESTATION,
                severity=0.85,
                severity_level=ThreatSeverity.HIGH,
                urgency=ThreatUrgency.URGENT,
                confidence=0.9
            ),
            ThreatDetection(
                detection_id="workflow_threat_2",
                threat_type=ThreatType.POACHING,
                severity=0.7,
                severity_level=ThreatSeverity.HIGH,
                urgency=ThreatUrgency.ELEVATED,
                confidence=0.8
            )
        ]
        
        test_species = [
            SpeciesDetection(
                detection_id="workflow_species_1",
                species=MadagascarSpecies.LEMUR_CATTA,
                confidence=0.95,
                confidence_level=SpeciesConfidence.VERY_HIGH,
                timestamp=datetime.utcnow(),
                source="test_workflow"
            ),
            SpeciesDetection(
                detection_id="workflow_species_2",
                species=MadagascarSpecies.PROPITHECUS_DIADEMA,
                confidence=0.85,
                confidence_level=SpeciesConfidence.HIGH,
                timestamp=datetime.utcnow(),
                source="test_workflow"
            )
        ]
        
        test_context = ConservationContext(
            location=(-18.947, 48.458),
            ecosystem_type="rainforest",
            protected_area_status=True,
            community_presence=True,
            accessibility=0.7,
            infrastructure_quality=0.5,
            local_governance_strength=0.6
        )
        
        test_resources = [
            ConservationResource(
                resource_type="field_personnel",
                availability=0.8,
                capacity=30,
                cost_per_unit=100.0
            ),
            ConservationResource(
                resource_type="conservation_funding",
                availability=1.0,
                capacity=200000,
                cost_per_unit=1.0
            ),
            ConservationResource(
                resource_type="monitoring_equipment",
                availability=0.7,
                capacity=15,
                cost_per_unit=500.0
            )
        ]
        
        # Generate recommendations
        recommendations = generator.generate_recommendations(
            threats=test_threats,
            species_detections=test_species,
            context=test_context,
            available_resources=test_resources,
            max_recommendations=3
        )
        
        # Validate results
        if len(recommendations) > 0:
            print(f"✅ Recommendations generated: {len(recommendations)}")
        else:
            print("❌ No recommendations generated")
            return False
        
        # Check recommendation quality
        valid_recommendations = 0
        for i, rec in enumerate(recommendations):
            print(f"   • Recommendation {i+1}: {rec.strategy.value}, Priority: {rec.priority.value}, Actions: {len(rec.actions)}")
            
            # Validate recommendation structure
            if (rec.recommendation_id and rec.strategy and rec.actions and 
                0.0 <= rec.confidence_score <= 1.0):
                valid_recommendations += 1
            
            # Check implementation details
            if hasattr(rec, 'required_resources') and rec.required_resources:
                print(f"     ✅ Implementation details added")
            
            if hasattr(rec, 'expected_outcomes') and rec.expected_outcomes:
                print(f"     ✅ Expected outcomes defined")
        
        if valid_recommendations == len(recommendations):
            print(f"✅ All recommendations properly structured")
        else:
            print(f"❌ Recommendation structure issues: {valid_recommendations}/{len(recommendations)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Recommendation generation workflow error: {e}")
        return False

def test_portfolio_optimization():
    """Test recommendation portfolio optimization."""
    print("\n🎯 Testing Portfolio Optimization...")
    
    try:
        generator = RecommendationGenerator()
        
        # Create mock scored recommendations
        mock_recommendations = []
        for i in range(6):  # Create more than max to test selection
            rec = ConservationRecommendation(
                recommendation_id=f"portfolio_test_{i}",
                priority=ConservationPriority.HIGH,
                strategy=ConservationStrategy.HABITAT_PROTECTION,
                actions=[ConservationAction.DEPLOY_PATROL_TEAM, ConservationAction.REFORESTATION],
                estimated_cost=25000.0
            )
            
            score = RecommendationScore()
            score.total_score = 0.9 - (i * 0.1)  # Decreasing scores
            score.feasibility_score = 0.8
            score.impact_score = 0.9 - (i * 0.1)
            score.confidence_level = 0.8
            
            mock_recommendations.append((rec, score))
        
        # Create limited resources
        limited_resources = [
            ConservationResource(
                resource_type="field_personnel",
                availability=0.8,
                capacity=15,  # Limited capacity
                cost_per_unit=100.0
            ),
            ConservationResource(
                resource_type="conservation_funding",
                availability=1.0,
                capacity=80000,  # Limited funding
                cost_per_unit=1.0
            )
        ]
        
        # Test optimization
        optimized = generator._optimize_recommendation_portfolio(
            mock_recommendations,
            limited_resources,
            max_recommendations=3
        )
        
        if len(optimized) <= 3:
            print(f"✅ Portfolio size optimized: {len(optimized)}/3 max")
        else:
            print(f"❌ Portfolio optimization failed: {len(optimized)} > 3")
            return False
        
        # Check that highest scored recommendations are selected
        selected_scores = [score.total_score for _, score in optimized]
        if selected_scores == sorted(selected_scores, reverse=True):
            print("✅ Highest scoring recommendations selected")
        else:
            print("❌ Optimization not prioritizing highest scores")
            return False
        
        # Check resource constraint compliance
        total_cost = sum(rec.estimated_cost for rec, _ in optimized)
        available_funding = sum(r.get_available_capacity() for r in limited_resources 
                              if r.resource_type == "conservation_funding")
        
        if total_cost <= available_funding:
            print(f"✅ Resource constraints respected: ${total_cost:,.0f} ≤ ${available_funding:,.0f}")
        else:
            print(f"❌ Resource constraints violated: ${total_cost:,.0f} > ${available_funding:,.0f}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Portfolio optimization error: {e}")
        return False

def main():
    """Run Section 2 tests."""
    print("🧠 STEP 6 - SECTION 2: Recommendation Generation Algorithms")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Recommendation generator initialization
    if test_recommendation_generator_initialization():
        tests_passed += 1
    
    # Test 2: Threat and species analysis
    if test_threat_and_species_analysis():
        tests_passed += 1
    
    # Test 3: Recommendation scoring
    if test_recommendation_scoring():
        tests_passed += 1
    
    # Test 4: Recommendation generation workflow
    if test_recommendation_generation_workflow():
        tests_passed += 1
    
    # Test 5: Portfolio optimization
    if test_portfolio_optimization():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Section 2 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 2 PASSED - Ready for Section 3")
        print("\n🎯 Next: Implement adaptive recommendation system and continuous learning")
        return True
    else:
        print("❌ Section 2 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
