"""
Step 6 Section 1: Conservation Strategy Foundation
=================================================
Implement foundation for conservation recommendation system with Madagascar-specific strategies.
"""

import sys
import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict, field
from enum import Enum
import numpy as np
from collections import defaultdict, deque

# Import from previous steps
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
from step4_section1_test import MadagascarSpecies, SpeciesConfidence, SpeciesDetection
from step5_section1_test import ThreatType, ThreatSeverity, ThreatUrgency, ThreatDetection

class SpeciesType(Enum):
    """Species types for conservation planning (adapted from MadagascarSpecies)."""
    LEMUR = "lemur"
    TENREC = "tenrec"
    FOSSA = "fossa"
    CHAMELEON = "chameleon"
    BAOBAB = "baobab"
    BIRD = "bird"
    REPTILE = "reptile"
    UNKNOWN = "unknown"

class ConservationStatus(Enum):
    """IUCN conservation status categories."""
    CRITICALLY_ENDANGERED = "critically_endangered"
    ENDANGERED = "endangered"
    VULNERABLE = "vulnerable"
    NEAR_THREATENED = "near_threatened"
    LEAST_CONCERN = "least_concern"
    DATA_DEFICIENT = "data_deficient"

class ConservationPriority(Enum):
    """Conservation priority levels for recommendations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class ConservationStrategy(Enum):
    """Types of conservation strategies available."""
    HABITAT_PROTECTION = "habitat_protection"
    SPECIES_RECOVERY = "species_recovery"
    COMMUNITY_ENGAGEMENT = "community_engagement"
    LAW_ENFORCEMENT = "law_enforcement"
    RESEARCH_MONITORING = "research_monitoring"
    ECOSYSTEM_RESTORATION = "ecosystem_restoration"
    SUSTAINABLE_DEVELOPMENT = "sustainable_development"
    EDUCATION_OUTREACH = "education_outreach"
    CLIMATE_ADAPTATION = "climate_adaptation"
    INVASIVE_CONTROL = "invasive_control"

class ConservationAction(Enum):
    """Specific conservation actions that can be recommended."""
    # Immediate Response Actions
    DEPLOY_PATROL_TEAM = "deploy_patrol_team"
    ESTABLISH_BUFFER_ZONE = "establish_buffer_zone"
    INSTALL_MONITORING_EQUIPMENT = "install_monitoring_equipment"
    EMERGENCY_SPECIES_RELOCATION = "emergency_species_relocation"
    
    # Habitat Management Actions
    REFORESTATION = "reforestation"
    HABITAT_CORRIDOR_CREATION = "habitat_corridor_creation"
    INVASIVE_SPECIES_REMOVAL = "invasive_species_removal"
    WATER_SOURCE_PROTECTION = "water_source_protection"
    ECOSYSTEM_RESTORATION = "ecosystem_restoration"
    
    # Community Actions
    ALTERNATIVE_LIVELIHOOD_PROGRAM = "alternative_livelihood_program"
    COMMUNITY_CONSERVATION_TRAINING = "community_conservation_training"
    ECOTOURISM_DEVELOPMENT = "ecotourism_development"
    SUSTAINABLE_AGRICULTURE_SUPPORT = "sustainable_agriculture_support"
    
    # Research and Monitoring
    POPULATION_SURVEY = "population_survey"
    GENETIC_ANALYSIS = "genetic_analysis"
    BEHAVIOR_STUDY = "behavior_study"
    LONG_TERM_MONITORING = "long_term_monitoring"
    
    # Policy and Legal
    POLICY_DEVELOPMENT = "policy_development"
    LAW_ENFORCEMENT_STRENGTHENING = "law_enforcement_strengthening"
    PROTECTED_AREA_DESIGNATION = "protected_area_designation"
    INTERNATIONAL_COOPERATION = "international_cooperation"

@dataclass
class ConservationResource:
    """Available conservation resources for implementing recommendations."""
    resource_type: str  # funding, personnel, equipment, expertise
    availability: float  # 0.0 to 1.0
    capacity: int  # maximum units available
    current_allocation: int = 0  # currently allocated units
    location: Optional[Tuple[float, float]] = None  # GPS if location-specific
    constraints: List[str] = field(default_factory=list)
    cost_per_unit: float = 0.0
    
    def get_available_capacity(self) -> int:
        """Get remaining available capacity."""
        return max(0, self.capacity - self.current_allocation)
    
    def allocate_resources(self, amount: int) -> bool:
        """Allocate resources if available."""
        if amount <= self.get_available_capacity():
            self.current_allocation += amount
            return True
        return False

@dataclass
class ConservationRecommendation:
    """A specific conservation recommendation with implementation details."""
    recommendation_id: str
    priority: ConservationPriority
    strategy: ConservationStrategy
    actions: List[ConservationAction]
    target_species: List[str] = field(default_factory=list)
    target_threats: List[ThreatType] = field(default_factory=list)
    target_location: Optional[Tuple[float, float]] = None
    implementation_timeline: Dict[str, Any] = field(default_factory=dict)
    required_resources: Dict[str, int] = field(default_factory=dict)
    expected_outcomes: Dict[str, Any] = field(default_factory=dict)
    success_metrics: List[str] = field(default_factory=list)
    estimated_cost: float = 0.0
    confidence_score: float = 0.0
    created_timestamp: datetime = field(default_factory=datetime.utcnow)
    status: str = "pending"  # pending, approved, implementing, completed, cancelled
    
    def __post_init__(self):
        if not self.implementation_timeline:
            self._generate_default_timeline()
        if not self.success_metrics:
            self._generate_default_metrics()
    
    def _generate_default_timeline(self):
        """Generate default implementation timeline."""
        self.implementation_timeline = {
            "immediate_actions": "0-1 weeks",
            "short_term_goals": "1-3 months", 
            "medium_term_goals": "3-12 months",
            "long_term_goals": "1-5 years",
            "evaluation_periods": ["3 months", "1 year", "3 years"]
        }
    
    def _generate_default_metrics(self):
        """Generate default success metrics."""
        base_metrics = [
            "threat_reduction_percentage",
            "species_population_stability",
            "habitat_quality_improvement",
            "community_engagement_level"
        ]
        
        # Add strategy-specific metrics
        strategy_metrics = {
            ConservationStrategy.HABITAT_PROTECTION: ["protected_area_coverage", "habitat_connectivity"],
            ConservationStrategy.SPECIES_RECOVERY: ["population_growth_rate", "genetic_diversity"],
            ConservationStrategy.COMMUNITY_ENGAGEMENT: ["local_participation_rate", "livelihood_improvement"],
            ConservationStrategy.LAW_ENFORCEMENT: ["illegal_activity_reduction", "prosecution_rate"]
        }
        
        self.success_metrics = base_metrics + strategy_metrics.get(self.strategy, [])

class MadagascarConservationKnowledgeBase:
    """Knowledge base of Madagascar-specific conservation strategies and best practices."""
    
    def __init__(self):
        self.species_conservation_strategies = self._initialize_species_strategies()
        self.threat_mitigation_strategies = self._initialize_threat_strategies()
        self.habitat_restoration_protocols = self._initialize_habitat_protocols()
        self.community_engagement_models = self._initialize_community_models()
        self.success_case_studies = self._initialize_success_cases()
    
    def _initialize_species_strategies(self) -> Dict[SpeciesType, Dict[str, Any]]:
        """Initialize species-specific conservation strategies."""
        return {
            SpeciesType.LEMUR: {
                "primary_threats": [ThreatType.DEFORESTATION, ThreatType.POACHING, ThreatType.HUMAN_INTRUSION],
                "key_strategies": [
                    ConservationStrategy.HABITAT_PROTECTION,
                    ConservationStrategy.COMMUNITY_ENGAGEMENT,
                    ConservationStrategy.RESEARCH_MONITORING
                ],
                "recommended_actions": [
                    ConservationAction.HABITAT_CORRIDOR_CREATION,
                    ConservationAction.COMMUNITY_CONSERVATION_TRAINING,
                    ConservationAction.POPULATION_SURVEY,
                    ConservationAction.ECOTOURISM_DEVELOPMENT
                ],
                "habitat_requirements": {
                    "forest_canopy_coverage": 0.8,
                    "fruit_tree_density": 50,  # trees per hectare
                    "water_source_proximity": 500,  # meters
                    "human_disturbance_threshold": 0.2
                },
                "population_recovery_factors": {
                    "breeding_success_rate": 0.6,
                    "juvenile_survival_rate": 0.7,
                    "habitat_connectivity": 0.8,
                    "food_resource_availability": 0.9
                }
            },
            SpeciesType.TENREC: {
                "primary_threats": [ThreatType.CLIMATE_IMPACT, ThreatType.INVASIVE_SPECIES],
                "key_strategies": [
                    ConservationStrategy.HABITAT_PROTECTION,
                    ConservationStrategy.INVASIVE_CONTROL,
                    ConservationStrategy.RESEARCH_MONITORING
                ],
                "recommended_actions": [
                    ConservationAction.INVASIVE_SPECIES_REMOVAL,
                    ConservationAction.HABITAT_CORRIDOR_CREATION,
                    ConservationAction.LONG_TERM_MONITORING
                ],
                "habitat_requirements": {
                    "soil_quality": 0.7,
                    "insect_abundance": 100,  # insects per square meter
                    "vegetation_density": 0.6,
                    "temperature_stability": 0.8
                }
            },
            SpeciesType.FOSSA: {
                "primary_threats": [ThreatType.DEFORESTATION, ThreatType.POACHING, ThreatType.HUMAN_INTRUSION],
                "key_strategies": [
                    ConservationStrategy.HABITAT_PROTECTION,
                    ConservationStrategy.LAW_ENFORCEMENT,
                    ConservationStrategy.RESEARCH_MONITORING
                ],
                "recommended_actions": [
                    ConservationAction.DEPLOY_PATROL_TEAM,
                    ConservationAction.ESTABLISH_BUFFER_ZONE,
                    ConservationAction.BEHAVIOR_STUDY,
                    ConservationAction.LAW_ENFORCEMENT_STRENGTHENING
                ],
                "habitat_requirements": {
                    "territory_size": 1000,  # hectares
                    "prey_density": 20,  # lemurs per square km
                    "forest_connectivity": 0.9,
                    "human_presence": 0.1
                }
            },
            SpeciesType.CHAMELEON: {
                "primary_threats": [ThreatType.DEFORESTATION, ThreatType.CLIMATE_IMPACT, ThreatType.INVASIVE_SPECIES],
                "key_strategies": [
                    ConservationStrategy.HABITAT_PROTECTION,
                    ConservationStrategy.CLIMATE_ADAPTATION,
                    ConservationStrategy.ECOSYSTEM_RESTORATION
                ],
                "recommended_actions": [
                    ConservationAction.REFORESTATION,
                    ConservationAction.WATER_SOURCE_PROTECTION,
                    ConservationAction.INVASIVE_SPECIES_REMOVAL
                ],
                "habitat_requirements": {
                    "microclimate_stability": 0.8,
                    "vegetation_layers": 3,  # understory, midstory, canopy
                    "humidity_level": 0.75,
                    "insect_diversity": 50  # species count
                }
            },
            SpeciesType.BAOBAB: {
                "primary_threats": [ThreatType.DEFORESTATION, ThreatType.CLIMATE_IMPACT, ThreatType.HUMAN_INTRUSION],
                "key_strategies": [
                    ConservationStrategy.HABITAT_PROTECTION,
                    ConservationStrategy.CLIMATE_ADAPTATION,
                    ConservationStrategy.COMMUNITY_ENGAGEMENT
                ],
                "recommended_actions": [
                    ConservationAction.PROTECTED_AREA_DESIGNATION,
                    ConservationAction.COMMUNITY_CONSERVATION_TRAINING,
                    ConservationAction.SUSTAINABLE_AGRICULTURE_SUPPORT
                ],
                "habitat_requirements": {
                    "soil_drainage": 0.9,
                    "annual_rainfall": 800,  # mm
                    "fire_protection": 0.95,
                    "grazing_pressure": 0.2
                }
            }
        }
    
    def _initialize_threat_strategies(self) -> Dict[ThreatType, Dict[str, Any]]:
        """Initialize threat-specific mitigation strategies."""
        return {
            ThreatType.DEFORESTATION: {
                "urgency_multiplier": 1.5,
                "primary_strategies": [
                    ConservationStrategy.LAW_ENFORCEMENT,
                    ConservationStrategy.COMMUNITY_ENGAGEMENT,
                    ConservationStrategy.SUSTAINABLE_DEVELOPMENT
                ],
                "immediate_actions": [
                    ConservationAction.DEPLOY_PATROL_TEAM,
                    ConservationAction.ESTABLISH_BUFFER_ZONE,
                    ConservationAction.LAW_ENFORCEMENT_STRENGTHENING
                ],
                "long_term_actions": [
                    ConservationAction.ALTERNATIVE_LIVELIHOOD_PROGRAM,
                    ConservationAction.SUSTAINABLE_AGRICULTURE_SUPPORT,
                    ConservationAction.REFORESTATION
                ],
                "success_indicators": [
                    "forest_cover_stability",
                    "illegal_logging_incidents_reduction",
                    "community_compliance_rate"
                ]
            },
            ThreatType.POACHING: {
                "urgency_multiplier": 2.0,
                "primary_strategies": [
                    ConservationStrategy.LAW_ENFORCEMENT,
                    ConservationStrategy.COMMUNITY_ENGAGEMENT,
                    ConservationStrategy.RESEARCH_MONITORING
                ],
                "immediate_actions": [
                    ConservationAction.DEPLOY_PATROL_TEAM,
                    ConservationAction.INSTALL_MONITORING_EQUIPMENT,
                    ConservationAction.LAW_ENFORCEMENT_STRENGTHENING
                ],
                "long_term_actions": [
                    ConservationAction.COMMUNITY_CONSERVATION_TRAINING,
                    ConservationAction.ALTERNATIVE_LIVELIHOOD_PROGRAM,
                    ConservationAction.POLICY_DEVELOPMENT
                ],
                "success_indicators": [
                    "poaching_incidents_reduction",
                    "species_population_stability",
                    "community_reporting_rate"
                ]
            },
            ThreatType.ILLEGAL_LOGGING: {
                "urgency_multiplier": 1.8,
                "primary_strategies": [
                    ConservationStrategy.LAW_ENFORCEMENT,
                    ConservationStrategy.HABITAT_PROTECTION,
                    ConservationStrategy.SUSTAINABLE_DEVELOPMENT
                ],
                "immediate_actions": [
                    ConservationAction.DEPLOY_PATROL_TEAM,
                    ConservationAction.LAW_ENFORCEMENT_STRENGTHENING,
                    ConservationAction.ESTABLISH_BUFFER_ZONE
                ],
                "long_term_actions": [
                    ConservationAction.SUSTAINABLE_AGRICULTURE_SUPPORT,
                    ConservationAction.ALTERNATIVE_LIVELIHOOD_PROGRAM,
                    ConservationAction.POLICY_DEVELOPMENT
                ]
            },
            ThreatType.SLASH_AND_BURN: {
                "urgency_multiplier": 1.3,
                "primary_strategies": [
                    ConservationStrategy.COMMUNITY_ENGAGEMENT,
                    ConservationStrategy.SUSTAINABLE_DEVELOPMENT,
                    ConservationStrategy.RESEARCH_MONITORING
                ],
                "immediate_actions": [
                    ConservationAction.COMMUNITY_CONSERVATION_TRAINING,
                    ConservationAction.SUSTAINABLE_AGRICULTURE_SUPPORT
                ],
                "long_term_actions": [
                    ConservationAction.ALTERNATIVE_LIVELIHOOD_PROGRAM,
                    ConservationAction.POLICY_DEVELOPMENT,
                    ConservationAction.LONG_TERM_MONITORING
                ]
            },
            ThreatType.MINING: {
                "urgency_multiplier": 2.5,
                "primary_strategies": [
                    ConservationStrategy.LAW_ENFORCEMENT,
                    ConservationStrategy.HABITAT_PROTECTION,
                    ConservationStrategy.ECOSYSTEM_RESTORATION
                ],
                "immediate_actions": [
                    ConservationAction.LAW_ENFORCEMENT_STRENGTHENING,
                    ConservationAction.PROTECTED_AREA_DESIGNATION,
                    ConservationAction.EMERGENCY_SPECIES_RELOCATION
                ],
                "long_term_actions": [
                    ConservationAction.ECOSYSTEM_RESTORATION,
                    ConservationAction.POLICY_DEVELOPMENT,
                    ConservationAction.INTERNATIONAL_COOPERATION
                ]
            }
        }
    
    def _initialize_habitat_protocols(self) -> Dict[str, Dict[str, Any]]:
        """Initialize habitat restoration protocols."""
        return {
            "rainforest_restoration": {
                "target_ecosystems": ["eastern_rainforest", "montane_forest"],
                "restoration_phases": [
                    {
                        "phase": "site_preparation",
                        "duration_months": 3,
                        "activities": ["invasive_removal", "soil_assessment", "water_management"]
                    },
                    {
                        "phase": "pioneer_planting",
                        "duration_months": 6,
                        "activities": ["fast_growing_natives", "nurse_plants", "erosion_control"]
                    },
                    {
                        "phase": "canopy_development",
                        "duration_months": 24,
                        "activities": ["climax_species_planting", "wildlife_corridors", "monitoring"]
                    }
                ],
                "native_species": [
                    "Dalbergia_baronii", "Diospyros_perrieri", "Adansonia_suarezensis",
                    "Pachypodium_baronii", "Aloe_suzannae"
                ],
                "success_metrics": [
                    "canopy_cover_percentage", "native_species_establishment",
                    "wildlife_return_rate", "soil_quality_improvement"
                ]
            },
            "dry_forest_restoration": {
                "target_ecosystems": ["western_dry_forest", "southern_spiny_forest"],
                "restoration_phases": [
                    {
                        "phase": "soil_rehabilitation",
                        "duration_months": 6,
                        "activities": ["erosion_control", "organic_matter_addition", "microclimate_creation"]
                    },
                    {
                        "phase": "drought_tolerant_planting",
                        "duration_months": 12,
                        "activities": ["succulent_establishment", "tree_planting", "water_conservation"]
                    }
                ],
                "native_species": [
                    "Adansonia_za", "Pachypodium_lamerei", "Alluaudia_procera",
                    "Operculicarya_decaryi", "Commiphora_lamii"
                ],
                "success_metrics": [
                    "vegetation_density", "water_retention_capacity",
                    "endemic_species_recovery", "ecosystem_resilience"
                ]
            }
        }
    
    def _initialize_community_models(self) -> Dict[str, Dict[str, Any]]:
        """Initialize community engagement models."""
        return {
            "participatory_forest_management": {
                "approach": "community_based_natural_resource_management",
                "key_components": [
                    "local_governance_strengthening",
                    "benefit_sharing_mechanisms",
                    "traditional_knowledge_integration",
                    "capacity_building"
                ],
                "implementation_steps": [
                    "community_mapping_and_assessment",
                    "stakeholder_engagement_workshops",
                    "management_plan_development",
                    "monitoring_system_establishment"
                ],
                "success_factors": [
                    "community_ownership", "economic_benefits",
                    "conflict_resolution_mechanisms", "external_support"
                ]
            },
            "ecotourism_development": {
                "approach": "sustainable_community_based_ecotourism",
                "key_components": [
                    "guide_training_programs",
                    "accommodation_development",
                    "cultural_experience_design",
                    "revenue_sharing_systems"
                ],
                "target_outcomes": [
                    "alternative_income_generation",
                    "conservation_awareness_increase",
                    "habitat_protection_incentives",
                    "cultural_preservation"
                ]
            }
        }
    
    def _initialize_success_cases(self) -> Dict[str, Dict[str, Any]]:
        """Initialize documented success cases for reference."""
        return {
            "andasibe_mantadia_lemur_recovery": {
                "location": "Andasibe-Mantadia National Park",
                "target_species": ["Indri_indri", "Propithecus_diadema"],
                "interventions": [
                    "habitat_corridor_establishment",
                    "community_ecotourism_development",
                    "research_station_establishment"
                ],
                "outcomes": {
                    "population_increase": 0.3,
                    "habitat_connectivity_improvement": 0.4,
                    "community_income_increase": 0.25
                },
                "lessons_learned": [
                    "community_engagement_critical",
                    "long_term_monitoring_essential",
                    "adaptive_management_needed"
                ]
            },
            "masoala_integrated_conservation": {
                "location": "Masoala National Park",
                "approach": "integrated_conservation_development",
                "interventions": [
                    "marine_protected_area_establishment",
                    "sustainable_fishing_programs",
                    "forest_restoration_projects"
                ],
                "outcomes": {
                    "forest_cover_stability": 0.9,
                    "marine_biodiversity_recovery": 0.35,
                    "community_livelihoods_improvement": 0.4
                }
            }
        }
    
    def get_species_conservation_plan(self, species_type: SpeciesType, 
                                    conservation_status: ConservationStatus) -> Dict[str, Any]:
        """Get conservation plan for specific species."""
        if species_type not in self.species_conservation_strategies:
            return {"error": f"No conservation plan available for {species_type.value}"}
        
        base_plan = self.species_conservation_strategies[species_type].copy()
        
        # Adjust based on conservation status
        status_multipliers = {
            ConservationStatus.CRITICALLY_ENDANGERED: 2.0,
            ConservationStatus.ENDANGERED: 1.5,
            ConservationStatus.VULNERABLE: 1.2,
            ConservationStatus.NEAR_THREATENED: 1.0,
            ConservationStatus.LEAST_CONCERN: 0.8
        }
        
        urgency_multiplier = status_multipliers.get(conservation_status, 1.0)
        base_plan["urgency_multiplier"] = urgency_multiplier
        
        return base_plan
    
    def get_threat_mitigation_plan(self, threat_type: ThreatType, 
                                 threat_severity: float) -> Dict[str, Any]:
        """Get mitigation plan for specific threat."""
        if threat_type not in self.threat_mitigation_strategies:
            return {"error": f"No mitigation plan available for {threat_type.value}"}
        
        base_plan = self.threat_mitigation_strategies[threat_type].copy()
        
        # Adjust urgency based on severity
        severity_urgency = min(2.0, threat_severity * 2)
        base_plan["adjusted_urgency"] = base_plan["urgency_multiplier"] * severity_urgency
        
        return base_plan

def test_conservation_knowledge_base():
    """Test Madagascar conservation knowledge base."""
    print("🧠 Testing Conservation Knowledge Base...")
    
    try:
        kb = MadagascarConservationKnowledgeBase()
        
        # Test species strategies
        species_plans = 0
        for species_type in SpeciesType:
            plan = kb.get_species_conservation_plan(species_type, ConservationStatus.ENDANGERED)
            if "key_strategies" in plan and "recommended_actions" in plan:
                species_plans += 1
                print(f"✅ {species_type.value}: {len(plan['key_strategies'])} strategies, "
                      f"{len(plan['recommended_actions'])} actions")
        
        print(f"✅ Species conservation plans: {species_plans}/{len(SpeciesType)} species")
        
        # Test threat mitigation strategies
        threat_plans = 0
        for threat_type in [ThreatType.DEFORESTATION, ThreatType.POACHING, ThreatType.ILLEGAL_LOGGING]:
            plan = kb.get_threat_mitigation_plan(threat_type, 0.8)
            if "primary_strategies" in plan and "immediate_actions" in plan:
                threat_plans += 1
                print(f"✅ {threat_type.value}: {len(plan['primary_strategies'])} strategies, "
                      f"{len(plan['immediate_actions'])} immediate actions")
        
        print(f"✅ Threat mitigation plans: {threat_plans}/3 major threats")
        
        # Test habitat restoration protocols
        habitat_protocols = len(kb.habitat_restoration_protocols)
        if habitat_protocols > 0:
            print(f"✅ Habitat restoration protocols: {habitat_protocols} ecosystems")
            for protocol_name, protocol in kb.habitat_restoration_protocols.items():
                phases = len(protocol["restoration_phases"])
                print(f"   • {protocol_name}: {phases} restoration phases")
        else:
            print("❌ No habitat restoration protocols found")
            return False
        
        # Test community engagement models
        community_models = len(kb.community_engagement_models)
        if community_models > 0:
            print(f"✅ Community engagement models: {community_models} approaches")
        else:
            print("❌ No community engagement models found")
            return False
        
        # Test success case studies
        success_cases = len(kb.success_case_studies)
        if success_cases > 0:
            print(f"✅ Success case studies: {success_cases} documented cases")
            for case_name, case in kb.success_case_studies.items():
                if "outcomes" in case:
                    print(f"   • {case_name}: documented conservation outcomes")
        else:
            print("❌ No success case studies found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Conservation knowledge base error: {e}")
        return False

def test_conservation_recommendation_structure():
    """Test conservation recommendation data structure."""
    print("\n📋 Testing Conservation Recommendation Structure...")
    
    try:
        # Test ConservationRecommendation creation
        test_recommendation = ConservationRecommendation(
            recommendation_id="test_rec_001",
            priority=ConservationPriority.HIGH,
            strategy=ConservationStrategy.HABITAT_PROTECTION,
            actions=[
                ConservationAction.DEPLOY_PATROL_TEAM,
                ConservationAction.ESTABLISH_BUFFER_ZONE,
                ConservationAction.INSTALL_MONITORING_EQUIPMENT
            ],
            target_species=["Lemur_catta", "Propithecus_diadema"],
            target_threats=[ThreatType.DEFORESTATION, ThreatType.POACHING],
            target_location=(-18.947, 48.458),
            estimated_cost=50000.0,
            confidence_score=0.85
        )
        
        print(f"✅ Recommendation created: {test_recommendation.recommendation_id}")
        print(f"   • Priority: {test_recommendation.priority.value}")
        print(f"   • Strategy: {test_recommendation.strategy.value}")
        print(f"   • Actions: {len(test_recommendation.actions)}")
        print(f"   • Target species: {len(test_recommendation.target_species)}")
        print(f"   • Target threats: {len(test_recommendation.target_threats)}")
        
        # Test default timeline generation
        if test_recommendation.implementation_timeline:
            timeline_phases = len(test_recommendation.implementation_timeline)
            print(f"✅ Implementation timeline: {timeline_phases} phases")
        else:
            print("❌ Implementation timeline not generated")
            return False
        
        # Test default metrics generation
        if test_recommendation.success_metrics:
            metrics_count = len(test_recommendation.success_metrics)
            print(f"✅ Success metrics: {metrics_count} indicators")
        else:
            print("❌ Success metrics not generated")
            return False
        
        # Test serialization
        recommendation_dict = asdict(test_recommendation)
        if "recommendation_id" in recommendation_dict:
            print("✅ Recommendation serialization successful")
        else:
            print("❌ Recommendation serialization failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Conservation recommendation structure error: {e}")
        return False

def test_conservation_resource_management():
    """Test conservation resource management system."""
    print("\n💰 Testing Conservation Resource Management...")
    
    try:
        # Create test resources
        test_resources = [
            ConservationResource(
                resource_type="field_personnel",
                availability=0.8,
                capacity=20,
                location=(-18.947, 48.458),
                cost_per_unit=100.0,  # daily cost per person
                constraints=["weather_dependent", "requires_training"]
            ),
            ConservationResource(
                resource_type="monitoring_equipment", 
                availability=0.6,
                capacity=15,
                cost_per_unit=500.0,  # cost per camera trap
                constraints=["battery_life", "theft_risk"]
            ),
            ConservationResource(
                resource_type="conservation_funding",
                availability=1.0,
                capacity=100000,  # USD
                cost_per_unit=1.0,
                constraints=["approval_required", "reporting_obligations"]
            ),
            ConservationResource(
                resource_type="vehicle_transport",
                availability=0.7,
                capacity=5,
                cost_per_unit=200.0,  # daily cost per vehicle
                constraints=["fuel_availability", "road_conditions"]
            )
        ]
        
        print(f"✅ Conservation resources created: {len(test_resources)} types")
        
        # Test resource availability calculation
        total_available = 0
        for resource in test_resources:
            available = resource.get_available_capacity()
            total_available += available
            print(f"   • {resource.resource_type}: {available}/{resource.capacity} available")
        
        print(f"✅ Total available capacity: {total_available} units")
        
        # Test resource allocation
        personnel_resource = test_resources[0]
        allocation_success = personnel_resource.allocate_resources(5)
        
        if allocation_success:
            print(f"✅ Resource allocation successful: {personnel_resource.current_allocation}/20 personnel")
        else:
            print("❌ Resource allocation failed")
            return False
        
        # Test over-allocation prevention
        over_allocation = personnel_resource.allocate_resources(20)  # Would exceed capacity
        
        if not over_allocation:
            print("✅ Over-allocation prevention working")
        else:
            print("❌ Over-allocation prevention failed")
            return False
        
        # Test cost calculation
        total_cost = 0
        for resource in test_resources:
            if resource.current_allocation > 0:
                resource_cost = resource.current_allocation * resource.cost_per_unit
                total_cost += resource_cost
                print(f"   • {resource.resource_type} cost: ${resource_cost:.2f}")
        
        print(f"✅ Total resource cost calculation: ${total_cost:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Conservation resource management error: {e}")
        return False

def test_conservation_enums_and_types():
    """Test conservation enumeration types and classifications."""
    print("\n🏷️  Testing Conservation Enums and Types...")
    
    try:
        # Test ConservationPriority enum
        priorities = list(ConservationPriority)
        print(f"✅ Conservation priorities: {len(priorities)} levels")
        for priority in priorities:
            print(f"   • {priority.value}")
        
        # Test ConservationStrategy enum
        strategies = list(ConservationStrategy)
        print(f"✅ Conservation strategies: {len(strategies)} types")
        
        # Verify strategy coverage
        expected_strategies = [
            "habitat_protection", "species_recovery", "community_engagement",
            "law_enforcement", "ecosystem_restoration"
        ]
        
        strategy_values = [s.value for s in strategies]
        coverage = sum(1 for expected in expected_strategies if expected in strategy_values)
        print(f"✅ Strategy coverage: {coverage}/{len(expected_strategies)} core strategies")
        
        # Test ConservationAction enum
        actions = list(ConservationAction)
        print(f"✅ Conservation actions: {len(actions)} specific actions")
        
        # Group actions by category
        action_categories = {
            "immediate": ["deploy_patrol_team", "emergency_species_relocation"],
            "habitat": ["reforestation", "habitat_corridor_creation"],
            "community": ["alternative_livelihood_program", "ecotourism_development"],
            "research": ["population_survey", "genetic_analysis"],
            "policy": ["policy_development", "law_enforcement_strengthening"]
        }
        
        action_values = [a.value for a in actions]
        category_coverage = {}
        
        for category, expected_actions in action_categories.items():
            coverage = sum(1 for action in expected_actions if action in action_values)
            category_coverage[category] = coverage
            print(f"   • {category} actions: {coverage}/{len(expected_actions)}")
        
        total_expected = sum(len(actions) for actions in action_categories.values())
        total_coverage = sum(category_coverage.values())
        
        if total_coverage >= total_expected * 0.8:  # 80% coverage acceptable
            print(f"✅ Action coverage sufficient: {total_coverage}/{total_expected}")
        else:
            print(f"❌ Action coverage insufficient: {total_coverage}/{total_expected}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Conservation enums and types error: {e}")
        return False

def test_madagascar_specific_adaptations():
    """Test Madagascar-specific conservation adaptations."""
    print("\n🏝️  Testing Madagascar-Specific Adaptations...")
    
    try:
        kb = MadagascarConservationKnowledgeBase()
        
        # Test endemic species coverage
        madagascar_endemics = [SpeciesType.LEMUR, SpeciesType.TENREC, SpeciesType.FOSSA, 
                              SpeciesType.CHAMELEON, SpeciesType.BAOBAB]
        
        endemic_coverage = 0
        for species in madagascar_endemics:
            if species in kb.species_conservation_strategies:
                endemic_coverage += 1
                strategy = kb.species_conservation_strategies[species]
                print(f"✅ {species.value}: {len(strategy['primary_threats'])} threats, "
                      f"{len(strategy['recommended_actions'])} actions")
        
        print(f"✅ Endemic species coverage: {endemic_coverage}/{len(madagascar_endemics)}")
        
        # Test Madagascar-specific threats
        madagascar_threats = [ThreatType.DEFORESTATION, ThreatType.SLASH_AND_BURN, 
                             ThreatType.POACHING, ThreatType.MINING]
        
        threat_coverage = 0
        for threat in madagascar_threats:
            if threat in kb.threat_mitigation_strategies:
                threat_coverage += 1
                strategy = kb.threat_mitigation_strategies[threat]
                print(f"✅ {threat.value}: urgency x{strategy['urgency_multiplier']}")
        
        print(f"✅ Madagascar threat coverage: {threat_coverage}/{len(madagascar_threats)}")
        
        # Test habitat-specific protocols
        madagascar_habitats = ["rainforest_restoration", "dry_forest_restoration"]
        
        habitat_coverage = 0
        for habitat in madagascar_habitats:
            if habitat in kb.habitat_restoration_protocols:
                habitat_coverage += 1
                protocol = kb.habitat_restoration_protocols[habitat]
                phases = len(protocol["restoration_phases"])
                native_species = len(protocol["native_species"])
                print(f"✅ {habitat}: {phases} phases, {native_species} native species")
        
        print(f"✅ Habitat protocol coverage: {habitat_coverage}/{len(madagascar_habitats)}")
        
        # Test community engagement models
        madagascar_approaches = ["participatory_forest_management", "ecotourism_development"]
        
        community_coverage = 0
        for approach in madagascar_approaches:
            if approach in kb.community_engagement_models:
                community_coverage += 1
                model = kb.community_engagement_models[approach]
                components = len(model["key_components"])
                print(f"✅ {approach}: {components} key components")
        
        print(f"✅ Community model coverage: {community_coverage}/{len(madagascar_approaches)}")
        
        # Test success case integration
        documented_cases = list(kb.success_case_studies.keys())
        if len(documented_cases) >= 2:
            print(f"✅ Success cases documented: {len(documented_cases)} cases")
            for case in documented_cases:
                case_data = kb.success_case_studies[case]
                if "outcomes" in case_data:
                    outcomes = len(case_data["outcomes"])
                    print(f"   • {case}: {outcomes} measured outcomes")
        else:
            print("❌ Insufficient success cases documented")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Madagascar-specific adaptations error: {e}")
        return False

def main():
    """Run Section 1 tests."""
    print("🧠 STEP 6 - SECTION 1: Conservation Strategy Foundation")
    print("=" * 55)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Conservation knowledge base
    if test_conservation_knowledge_base():
        tests_passed += 1
    
    # Test 2: Conservation recommendation structure
    if test_conservation_recommendation_structure():
        tests_passed += 1
    
    # Test 3: Conservation resource management
    if test_conservation_resource_management():
        tests_passed += 1
    
    # Test 4: Conservation enums and types
    if test_conservation_enums_and_types():
        tests_passed += 1
    
    # Test 5: Madagascar-specific adaptations
    if test_madagascar_specific_adaptations():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Section 1 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 1 PASSED - Ready for Section 2")
        print("\n🎯 Next: Implement recommendation generation algorithms")
        return True
    else:
        print("❌ Section 1 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
