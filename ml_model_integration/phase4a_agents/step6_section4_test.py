"""
Step 6 Section 4: Deployment Integration & System Coordination
============================================================
Complete conservation recommendation agent with full system integration.
"""

import sys
import os
import json
import time
import math
import asyncio
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
from step6_section3_test import (InterventionOutcome, AdaptiveLearningRule, LearningMemory, AdaptiveDecisionEngine)

@dataclass
class SystemIntegrationStatus:
    """Status of integration with other AI agents."""
    species_identification_agent: bool = False
    threat_detection_agent: bool = False
    alert_management_system: bool = False
    satellite_monitoring: bool = False
    field_data_collection: bool = False
    stakeholder_communication: bool = False
    resource_management: bool = False
    last_synchronization: Optional[datetime] = None
    integration_health_score: float = 0.0
    communication_latency: Dict[str, float] = field(default_factory=dict)
    data_freshness: Dict[str, datetime] = field(default_factory=dict)
    
    def calculate_integration_health(self) -> float:
        """Calculate overall integration health score."""
        # Count active integrations
        active_integrations = sum([
            self.species_identification_agent,
            self.threat_detection_agent,
            self.alert_management_system,
            self.satellite_monitoring,
            self.field_data_collection,
            self.stakeholder_communication,
            self.resource_management
        ])
        
        base_health = active_integrations / 7.0  # 7 total integrations
        
        # Adjust for communication latency
        if self.communication_latency:
            avg_latency = sum(self.communication_latency.values()) / len(self.communication_latency)
            latency_factor = max(0.0, 1.0 - (avg_latency / 1000.0))  # Assume 1000ms is poor
        else:
            latency_factor = 1.0
        
        # Adjust for data freshness
        if self.data_freshness:
            now = datetime.utcnow()
            freshness_scores = []
            for source, last_update in self.data_freshness.items():
                age_hours = (now - last_update).total_seconds() / 3600
                freshness_score = max(0.0, 1.0 - (age_hours / 24.0))  # 24 hours = stale
                freshness_scores.append(freshness_score)
            avg_freshness = sum(freshness_scores) / len(freshness_scores)
        else:
            avg_freshness = 1.0
        
        self.integration_health_score = base_health * 0.5 + latency_factor * 0.25 + avg_freshness * 0.25
        return self.integration_health_score

@dataclass
class DeploymentConfiguration:
    """Configuration for conservation recommendation deployment."""
    deployment_id: str
    environment: str  # "development", "staging", "production"
    geographic_scope: Tuple[Tuple[float, float], Tuple[float, float]]  # ((min_lat, min_lon), (max_lat, max_lon))
    operational_mode: str = "automatic"  # "automatic", "semi_automatic", "manual"
    response_time_target: float = 300.0  # seconds
    confidence_threshold: float = 0.7
    max_concurrent_recommendations: int = 10
    resource_allocation_limits: Dict[str, float] = field(default_factory=dict)
    stakeholder_notification_rules: Dict[str, bool] = field(default_factory=dict)
    data_sources: List[str] = field(default_factory=list)
    backup_systems: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.resource_allocation_limits:
            self.resource_allocation_limits = {
                "max_budget_per_recommendation": 100000.0,
                "max_personnel_per_recommendation": 10,
                "max_duration_days": 365
            }
        
        if not self.stakeholder_notification_rules:
            self.stakeholder_notification_rules = {
                "government_agencies": True,
                "conservation_organizations": True,
                "local_communities": True,
                "international_partners": False,
                "media_outlets": False
            }
        
        if not self.data_sources:
            self.data_sources = [
                "species_identification_agent",
                "threat_detection_agent",
                "satellite_imagery",
                "field_reports",
                "community_observations"
            ]

@dataclass
class OperationalMetrics:
    """Metrics for operational performance monitoring."""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    recommendations_generated: int = 0
    recommendations_deployed: int = 0
    average_response_time: float = 0.0
    system_uptime_percentage: float = 100.0
    data_processing_rate: float = 0.0  # items per hour
    user_satisfaction_score: float = 0.0
    resource_utilization: Dict[str, float] = field(default_factory=dict)
    error_rates: Dict[str, float] = field(default_factory=dict)
    integration_success_rate: float = 100.0
    adaptive_learning_activity: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.resource_utilization:
            self.resource_utilization = {
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "storage_usage": 0.0,
                "network_bandwidth": 0.0
            }
        
        if not self.error_rates:
            self.error_rates = {
                "data_ingestion_errors": 0.0,
                "recommendation_generation_errors": 0.0,
                "integration_errors": 0.0,
                "deployment_errors": 0.0
            }
        
        if not self.adaptive_learning_activity:
            self.adaptive_learning_activity = {
                "new_rules_generated": 0,
                "rules_applied": 0,
                "outcomes_processed": 0,
                "knowledge_updates": 0
            }

class ConservationRecommendationDeploymentAgent:
    """Complete conservation recommendation agent with full deployment capabilities."""
    
    def __init__(self, config: DeploymentConfiguration):
        self.config = config
        self.adaptive_engine = AdaptiveDecisionEngine()
        self.integration_status = SystemIntegrationStatus()
        self.operational_metrics = OperationalMetrics()
        
        # Deployment state
        self.is_active = False
        self.active_recommendations: Dict[str, ConservationRecommendation] = {}
        self.deployment_history: List[Dict[str, Any]] = []
        self.system_health_alerts: List[Dict[str, Any]] = []
        
        # Performance monitoring
        self.performance_window = deque(maxlen=100)  # Last 100 operations
        self.last_health_check = datetime.utcnow()
        self.health_check_interval = 300  # 5 minutes
        
        # Initialize deployment
        self._initialize_deployment()
    
    def _initialize_deployment(self):
        """Initialize deployment systems and integrations."""
        print(f"🚀 Initializing Conservation Recommendation Agent (Environment: {self.config.environment})")
        
        # Simulate system integration checks
        self._check_system_integrations()
        
        # Initialize operational metrics
        self._initialize_operational_metrics()
        
        # Set up monitoring
        self._setup_monitoring()
        
        print(f"✅ Agent initialized with {self.integration_status.calculate_integration_health():.1%} integration health")
    
    def _check_system_integrations(self):
        """Check and establish integrations with other system components."""
        integrations_to_check = [
            ("species_identification_agent", "Species Identification"),
            ("threat_detection_agent", "Threat Detection"),
            ("alert_management_system", "Alert Management"),
            ("satellite_monitoring", "Satellite Monitoring"),
            ("field_data_collection", "Field Data Collection"),
            ("stakeholder_communication", "Stakeholder Communication"),
            ("resource_management", "Resource Management")
        ]
        
        for attr_name, display_name in integrations_to_check:
            # Simulate integration check (in real deployment, this would be actual system checks)
            integration_success = self._simulate_integration_check(attr_name)
            setattr(self.integration_status, attr_name, integration_success)
            
            if integration_success:
                print(f"   ✅ {display_name} integration active")
                # Simulate communication latency
                self.integration_status.communication_latency[attr_name] = np.random.uniform(50, 200)  # ms
                # Simulate data freshness
                self.integration_status.data_freshness[attr_name] = datetime.utcnow() - timedelta(minutes=np.random.randint(1, 30))
            else:
                print(f"   ⚠️  {display_name} integration unavailable")
        
        self.integration_status.last_synchronization = datetime.utcnow()
    
    def _simulate_integration_check(self, integration_name: str) -> bool:
        """Simulate integration health check."""
        # For testing, we'll make most integrations successful
        success_probability = {
            "species_identification_agent": 0.95,
            "threat_detection_agent": 0.9,
            "alert_management_system": 0.85,
            "satellite_monitoring": 0.8,
            "field_data_collection": 0.75,
            "stakeholder_communication": 0.9,
            "resource_management": 0.85
        }
        
        return np.random.random() < success_probability.get(integration_name, 0.8)
    
    def _initialize_operational_metrics(self):
        """Initialize operational performance metrics."""
        self.operational_metrics.timestamp = datetime.utcnow()
        
        # Set baseline metrics
        self.operational_metrics.system_uptime_percentage = 100.0
        self.operational_metrics.user_satisfaction_score = 0.8
        self.operational_metrics.integration_success_rate = self.integration_status.calculate_integration_health() * 100
    
    def _setup_monitoring(self):
        """Setup performance and health monitoring."""
        self.last_health_check = datetime.utcnow()
        print("   📊 Performance monitoring enabled")
        print("   🏥 Health check system active")
    
    def activate_deployment(self) -> bool:
        """Activate the conservation recommendation agent."""
        print("🟢 Activating Conservation Recommendation Agent...")
        
        try:
            # Pre-activation checks
            if not self._pre_activation_checks():
                print("❌ Pre-activation checks failed")
                return False
            
            # Activate system
            self.is_active = True
            
            # Update operational metrics
            self.operational_metrics.timestamp = datetime.utcnow()
            
            print("✅ Conservation Recommendation Agent ACTIVE")
            print(f"   🎯 Geographic scope: {self.config.geographic_scope}")
            print(f"   ⚡ Response target: {self.config.response_time_target}s")
            print(f"   🎚️  Confidence threshold: {self.config.confidence_threshold}")
            
            return True
            
        except Exception as e:
            print(f"❌ Activation failed: {e}")
            return False
    
    def _pre_activation_checks(self) -> bool:
        """Perform pre-activation system checks."""
        checks = []
        
        # Check integration health
        integration_health = self.integration_status.calculate_integration_health()
        checks.append(("Integration Health", integration_health >= 0.6, f"{integration_health:.1%}"))
        
        # Check adaptive engine
        engine_status = len(self.adaptive_engine.adaptive_rules) > 0
        checks.append(("Adaptive Engine", engine_status, f"{len(self.adaptive_engine.adaptive_rules)} rules"))
        
        # Check configuration
        config_valid = (self.config.deployment_id and 
                       self.config.environment and 
                       self.config.geographic_scope)
        checks.append(("Configuration", config_valid, "Valid"))
        
        # Check resource limits
        resource_limits_set = len(self.config.resource_allocation_limits) > 0
        checks.append(("Resource Limits", resource_limits_set, f"{len(self.config.resource_allocation_limits)} limits"))
        
        # Report check results
        all_passed = True
        for check_name, passed, status in checks:
            status_symbol = "✅" if passed else "❌"
            print(f"   {status_symbol} {check_name}: {status}")
            if not passed:
                all_passed = False
        
        return all_passed
    
    async def process_conservation_request(self, 
                                         threats: List[ThreatDetection],
                                         species_detections: List[SpeciesDetection],
                                         context: ConservationContext,
                                         available_resources: List[ConservationResource],
                                         request_id: str = None) -> Dict[str, Any]:
        """Process a conservation recommendation request."""
        
        if not self.is_active:
            return {"error": "Agent not active", "status": "inactive"}
        
        request_id = request_id or f"req_{int(datetime.utcnow().timestamp())}"
        start_time = datetime.utcnow()
        
        print(f"🔄 Processing conservation request {request_id}...")
        
        try:
            # Step 1: Validate and preprocess input data
            validation_result = await self._validate_input_data(threats, species_detections, context)
            if not validation_result["valid"]:
                return {"error": "Input validation failed", "details": validation_result}
            
            # Step 2: Check system resources and capacity
            capacity_check = await self._check_system_capacity()
            if not capacity_check["available"]:
                return {"error": "System at capacity", "details": capacity_check}
            
            # Step 3: Generate adaptive recommendations
            recommendations, insights = self.adaptive_engine.make_adaptive_recommendation(
                threats=threats,
                species_detections=species_detections,
                context=context,
                available_resources=available_resources,
                max_recommendations=self.config.max_concurrent_recommendations
            )
            
            # Step 4: Filter recommendations by confidence threshold
            filtered_recommendations = [
                rec for rec in recommendations 
                if rec.confidence_score >= self.config.confidence_threshold
            ]
            
            # Step 5: Prepare deployment packages
            deployment_packages = await self._prepare_deployment_packages(
                filtered_recommendations, context, insights
            )
            
            # Step 6: Update operational metrics
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            await self._update_operational_metrics(processing_time, len(filtered_recommendations))
            
            # Step 7: Log deployment decision
            deployment_record = {
                "request_id": request_id,
                "timestamp": start_time,
                "processing_time": processing_time,
                "recommendations_generated": len(recommendations),
                "recommendations_deployed": len(filtered_recommendations),
                "context_summary": self._summarize_context(context, threats, species_detections),
                "adaptive_insights": insights
            }
            
            self.deployment_history.append(deployment_record)
            
            # Step 8: Initiate stakeholder notifications if configured
            if self.config.stakeholder_notification_rules.get("conservation_organizations", False):
                await self._notify_stakeholders(filtered_recommendations, context, request_id)
            
            print(f"✅ Request {request_id} processed: {len(filtered_recommendations)} recommendations deployed")
            
            return {
                "status": "success",
                "request_id": request_id,
                "recommendations": filtered_recommendations,
                "deployment_packages": deployment_packages,
                "processing_time": processing_time,
                "adaptive_insights": insights,
                "system_health": self.integration_status.integration_health_score
            }
            
        except Exception as e:
            error_record = {
                "request_id": request_id,
                "timestamp": start_time,
                "error": str(e),
                "error_type": type(e).__name__
            }
            
            # Update error metrics
            self.operational_metrics.error_rates["recommendation_generation_errors"] += 1
            
            print(f"❌ Request {request_id} failed: {e}")
            
            return {
                "status": "error",
                "request_id": request_id,
                "error": str(e),
                "timestamp": start_time
            }
    
    async def _validate_input_data(self, threats: List[ThreatDetection],
                                 species_detections: List[SpeciesDetection],
                                 context: ConservationContext) -> Dict[str, Any]:
        """Validate input data for processing."""
        validation_issues = []
        
        # Check threats data
        if not threats:
            validation_issues.append("No threat detections provided")
        else:
            for threat in threats:
                if not (0.0 <= threat.confidence <= 1.0):
                    validation_issues.append(f"Invalid threat confidence: {threat.confidence}")
        
        # Check species data  
        if not species_detections:
            validation_issues.append("No species detections provided")
        else:
            for detection in species_detections:
                if not (0.0 <= detection.confidence <= 1.0):
                    validation_issues.append(f"Invalid species confidence: {detection.confidence}")
        
        # Check context
        if not context.location or len(context.location) != 2:
            validation_issues.append("Invalid location coordinates")
        
        # Check geographic scope
        lat, lon = context.location
        min_coords, max_coords = self.config.geographic_scope
        min_lat, min_lon = min_coords
        max_lat, max_lon = max_coords
        
        if not (min_lat <= lat <= max_lat and min_lon <= lon <= max_lon):
            validation_issues.append(f"Location outside operational scope: {context.location}")
        
        return {
            "valid": len(validation_issues) == 0,
            "issues": validation_issues,
            "data_quality_score": max(0.0, 1.0 - len(validation_issues) * 0.2)
        }
    
    async def _check_system_capacity(self) -> Dict[str, Any]:
        """Check if system has capacity to process new requests."""
        current_load = len(self.active_recommendations)
        max_load = self.config.max_concurrent_recommendations
        
        capacity_available = current_load < max_load
        
        return {
            "available": capacity_available,
            "current_load": current_load,
            "max_capacity": max_load,
            "utilization_percentage": (current_load / max_load) * 100 if max_load > 0 else 0
        }
    
    async def _prepare_deployment_packages(self, recommendations: List[ConservationRecommendation],
                                         context: ConservationContext,
                                         insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prepare deployment packages for recommendations."""
        packages = []
        
        for rec in recommendations:
            package = {
                "recommendation_id": rec.recommendation_id,
                "deployment_priority": rec.priority.value,
                "implementation_timeline": self._calculate_implementation_timeline(rec),
                "resource_requirements": self._calculate_resource_requirements(rec),
                "stakeholder_coordination": self._identify_stakeholders(rec, context),
                "monitoring_plan": self._create_monitoring_plan(rec),
                "success_metrics": self._define_success_metrics(rec),
                "risk_assessment": self._assess_implementation_risks(rec, context),
                "adaptive_triggers": self._define_adaptive_triggers(rec, insights)
            }
            
            packages.append(package)
            
            # Add to active recommendations
            self.active_recommendations[rec.recommendation_id] = rec
        
        return packages
    
    def _calculate_implementation_timeline(self, recommendation: ConservationRecommendation) -> Dict[str, Any]:
        """Calculate implementation timeline for recommendation."""
        # Simplified timeline calculation
        base_duration = {
            ConservationAction.DEPLOY_PATROL_TEAM: 7,
            ConservationAction.COMMUNITY_CONSERVATION_TRAINING: 21,
            ConservationAction.REFORESTATION: 90,
            ConservationAction.POPULATION_SURVEY: 45,
            ConservationAction.LAW_ENFORCEMENT_STRENGTHENING: 60,
            ConservationAction.HABITAT_CORRIDOR_CREATION: 180
        }
        
        total_duration = max(base_duration.get(action, 30) for action in recommendation.actions)
        
        start_date = datetime.utcnow() + timedelta(days=3)  # 3-day preparation
        end_date = start_date + timedelta(days=total_duration)
        
        return {
            "preparation_phase": 3,
            "implementation_duration": total_duration,
            "estimated_start": start_date.isoformat(),
            "estimated_completion": end_date.isoformat(),
            "critical_milestones": self._identify_milestones(recommendation.actions)
        }
    
    def _calculate_resource_requirements(self, recommendation: ConservationRecommendation) -> Dict[str, Any]:
        """Calculate detailed resource requirements."""
        return {
            "personnel_needed": recommendation.required_resources.get("field_personnel", 5),
            "equipment_list": self._generate_equipment_list(recommendation.actions),
            "budget_breakdown": self._create_budget_breakdown(recommendation),
            "expertise_requirements": recommendation.required_resources.get("expertise_required", []),
            "logistical_support": self._assess_logistical_needs(recommendation)
        }
    
    def _identify_stakeholders(self, recommendation: ConservationRecommendation, 
                             context: ConservationContext) -> Dict[str, Any]:
        """Identify stakeholders for coordination."""
        stakeholders = {
            "primary": ["Madagascar National Parks", "Local Conservation Organizations"],
            "secondary": ["Community Leaders", "Government Agencies"],
            "international": [] if not context.protected_area_status else ["International Conservation NGOs"],
            "coordination_plan": {
                "initial_meeting": "Within 7 days",
                "regular_updates": "Weekly",
                "decision_authority": "Local Conservation Authority"
            }
        }
        
        # Add community stakeholders for community-focused actions
        community_actions = [ConservationAction.COMMUNITY_CONSERVATION_TRAINING, 
                           ConservationAction.ALTERNATIVE_LIVELIHOOD_PROGRAM]
        if any(action in recommendation.actions for action in community_actions):
            stakeholders["primary"].append("Community Representatives")
        
        return stakeholders
    
    def _create_monitoring_plan(self, recommendation: ConservationRecommendation) -> Dict[str, Any]:
        """Create monitoring plan for recommendation implementation."""
        return {
            "monitoring_frequency": "Weekly progress updates",
            "key_indicators": [
                "Implementation progress percentage",
                "Resource utilization",
                "Stakeholder satisfaction",
                "Environmental impact indicators"
            ],
            "reporting_schedule": {
                "progress_reports": "Weekly",
                "milestone_reports": "At each milestone",
                "final_report": "30 days post-completion"
            },
            "adaptive_checkpoints": [
                "25% implementation",
                "50% implementation", 
                "75% implementation"
            ]
        }
    
    def _define_success_metrics(self, recommendation: ConservationRecommendation) -> Dict[str, Any]:
        """Define success metrics for recommendation."""
        base_metrics = {
            "implementation_completion": {"target": "100%", "weight": 0.25},
            "budget_adherence": {"target": "Within 110%", "weight": 0.20},
            "stakeholder_satisfaction": {"target": ">80%", "weight": 0.20},
            "environmental_impact": {"target": "Positive impact", "weight": 0.35}
        }
        
        # Add strategy-specific metrics
        if recommendation.strategy == ConservationStrategy.SPECIES_RECOVERY:
            base_metrics["species_population_change"] = {"target": ">5% increase", "weight": 0.15}
        elif recommendation.strategy == ConservationStrategy.HABITAT_PROTECTION:
            base_metrics["habitat_area_protected"] = {"target": "100% target area", "weight": 0.15}
        
        return base_metrics
    
    def _assess_implementation_risks(self, recommendation: ConservationRecommendation,
                                   context: ConservationContext) -> Dict[str, Any]:
        """Assess risks for recommendation implementation."""
        risks = {
            "high_risk_factors": [],
            "medium_risk_factors": [],
            "low_risk_factors": [],
            "mitigation_strategies": {},
            "overall_risk_level": "medium"
        }
        
        # Assess context-based risks
        if context.accessibility < 0.5:
            risks["high_risk_factors"].append("Low accessibility")
            risks["mitigation_strategies"]["accessibility"] = "Arrange specialized transport"
        
        if context.local_governance_strength < 0.5:
            risks["medium_risk_factors"].append("Weak governance")
            risks["mitigation_strategies"]["governance"] = "Increase stakeholder engagement"
        
        if not context.community_presence:
            risks["medium_risk_factors"].append("Limited community support")
            risks["mitigation_strategies"]["community"] = "Develop community outreach program"
        
        # Calculate overall risk level
        high_risks = len(risks["high_risk_factors"])
        medium_risks = len(risks["medium_risk_factors"])
        
        if high_risks >= 2:
            risks["overall_risk_level"] = "high"
        elif high_risks == 1 or medium_risks >= 3:
            risks["overall_risk_level"] = "medium"
        else:
            risks["overall_risk_level"] = "low"
        
        return risks
    
    def _define_adaptive_triggers(self, recommendation: ConservationRecommendation,
                                insights: Dict[str, Any]) -> Dict[str, Any]:
        """Define triggers for adaptive modifications."""
        return {
            "performance_triggers": {
                "below_50_percent_progress": "Review and adapt implementation approach",
                "budget_overrun_20_percent": "Reassess resource allocation",
                "stakeholder_resistance": "Increase engagement and modify approach"
            },
            "environmental_triggers": {
                "unexpected_ecological_impact": "Immediate assessment and adaptation",
                "species_behavior_change": "Modify intervention methods",
                "habitat_degradation_acceleration": "Intensify protection measures"
            },
            "adaptive_thresholds": {
                "confidence_threshold": 0.6,
                "success_threshold": 0.7,
                "modification_threshold": 0.3
            },
            "learning_integration": {
                "outcome_recording": "Continuous",
                "rule_updates": "Monthly",
                "knowledge_integration": "Quarterly"
            }
        }
    
    def _identify_milestones(self, actions: List[ConservationAction]) -> List[str]:
        """Identify key milestones for actions."""
        milestones = []
        
        if ConservationAction.DEPLOY_PATROL_TEAM in actions:
            milestones.append("Patrol team deployment complete")
        
        if ConservationAction.COMMUNITY_CONSERVATION_TRAINING in actions:
            milestones.append("Community training program launched")
            milestones.append("First cohort training completed")
        
        if ConservationAction.REFORESTATION in actions:
            milestones.append("Site preparation completed")
            milestones.append("Seedling planting phase complete")
            milestones.append("First growth monitoring cycle")
        
        return milestones
    
    def _generate_equipment_list(self, actions: List[ConservationAction]) -> List[str]:
        """Generate equipment list for actions."""
        equipment = set()
        
        action_equipment = {
            ConservationAction.DEPLOY_PATROL_TEAM: ["GPS devices", "Communication radios", "Camping gear"],
            ConservationAction.POPULATION_SURVEY: ["Binoculars", "Camera traps", "Data recording tablets"],
            ConservationAction.REFORESTATION: ["Seedlings", "Planting tools", "Irrigation equipment"],
            ConservationAction.COMMUNITY_CONSERVATION_TRAINING: ["Training materials", "Projector", "Flipcharts"]
        }
        
        for action in actions:
            equipment.update(action_equipment.get(action, []))
        
        return list(equipment)
    
    def _create_budget_breakdown(self, recommendation: ConservationRecommendation) -> Dict[str, float]:
        """Create detailed budget breakdown."""
        total_cost = recommendation.estimated_cost
        
        return {
            "personnel_costs": total_cost * 0.4,
            "equipment_costs": total_cost * 0.25,
            "operational_costs": total_cost * 0.2,
            "administrative_costs": total_cost * 0.1,
            "contingency": total_cost * 0.05,
            "total": total_cost
        }
    
    def _assess_logistical_needs(self, recommendation: ConservationRecommendation) -> Dict[str, Any]:
        """Assess logistical support needs."""
        return {
            "transportation": "4WD vehicles for remote access",
            "accommodation": "Field stations or camping arrangements",
            "communication": "Satellite phones for remote areas",
            "supply_chain": "Regular supply runs for extended operations",
            "emergency_support": "Medical evacuation capability"
        }
    
    async def _notify_stakeholders(self, recommendations: List[ConservationRecommendation],
                                 context: ConservationContext, request_id: str):
        """Notify relevant stakeholders about new recommendations."""
        # Simulate stakeholder notification
        notification_summary = {
            "request_id": request_id,
            "location": context.location,
            "recommendations_count": len(recommendations),
            "priority_levels": [rec.priority.value for rec in recommendations],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        print(f"   📢 Stakeholder notifications sent for request {request_id}")
        print(f"      • {len(recommendations)} recommendations")
        print(f"      • Location: {context.location}")
    
    async def _update_operational_metrics(self, processing_time: float, 
                                        recommendations_count: int):
        """Update operational performance metrics."""
        self.operational_metrics.recommendations_generated += recommendations_count
        self.operational_metrics.recommendations_deployed += recommendations_count
        
        # Update average response time
        if self.operational_metrics.average_response_time == 0:
            self.operational_metrics.average_response_time = processing_time
        else:
            # Rolling average
            self.operational_metrics.average_response_time = (
                self.operational_metrics.average_response_time * 0.8 + processing_time * 0.2
            )
        
        # Add to performance window
        self.performance_window.append({
            "timestamp": datetime.utcnow(),
            "processing_time": processing_time,
            "recommendations": recommendations_count
        })
        
        # Update data processing rate
        if len(self.performance_window) > 1:
            time_span = (self.performance_window[-1]["timestamp"] - 
                        self.performance_window[0]["timestamp"]).total_seconds() / 3600
            if time_span > 0:
                total_items = sum(item["recommendations"] for item in self.performance_window)
                self.operational_metrics.data_processing_rate = total_items / time_span
    
    def _summarize_context(self, context: ConservationContext,
                          threats: List[ThreatDetection],
                          species_detections: List[SpeciesDetection]) -> Dict[str, Any]:
        """Summarize request context for logging."""
        return {
            "ecosystem_type": context.ecosystem_type,
            "protected_area": context.protected_area_status,
            "accessibility": context.accessibility,
            "threat_types": [threat.threat_type.value for threat in threats],
            "threat_severities": [threat.severity for threat in threats],
            "species_detected": [detection.species.value for detection in species_detections],
            "species_confidence": [detection.confidence for detection in species_detections]
        }
    
    def get_deployment_status(self) -> Dict[str, Any]:
        """Get comprehensive deployment status report."""
        return {
            "agent_status": {
                "active": self.is_active,
                "deployment_id": self.config.deployment_id,
                "environment": self.config.environment,
                "uptime": self._calculate_uptime()
            },
            "integration_status": {
                "health_score": self.integration_status.calculate_integration_health(),
                "active_integrations": self._count_active_integrations(),
                "last_sync": self.integration_status.last_synchronization,
                "communication_latency": self.integration_status.communication_latency
            },
            "operational_metrics": asdict(self.operational_metrics),
            "active_workload": {
                "active_recommendations": len(self.active_recommendations),
                "max_capacity": self.config.max_concurrent_recommendations,
                "utilization": len(self.active_recommendations) / self.config.max_concurrent_recommendations * 100
            },
            "learning_status": self.adaptive_engine.get_learning_status(),
            "recent_activity": {
                "deployments_last_24h": self._count_recent_deployments(24),
                "average_response_time": self.operational_metrics.average_response_time,
                "error_rate": sum(self.operational_metrics.error_rates.values())
            }
        }
    
    def _calculate_uptime(self) -> float:
        """Calculate system uptime in hours."""
        if hasattr(self, '_activation_time'):
            return (datetime.utcnow() - self._activation_time).total_seconds() / 3600
        return 0.0
    
    def _count_active_integrations(self) -> int:
        """Count number of active integrations."""
        return sum([
            self.integration_status.species_identification_agent,
            self.integration_status.threat_detection_agent,
            self.integration_status.alert_management_system,
            self.integration_status.satellite_monitoring,
            self.integration_status.field_data_collection,
            self.integration_status.stakeholder_communication,
            self.integration_status.resource_management
        ])
    
    def _count_recent_deployments(self, hours: int) -> int:
        """Count deployments in the last N hours."""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        return len([
            deployment for deployment in self.deployment_history
            if deployment["timestamp"] > cutoff
        ])
    
    def deactivate_deployment(self) -> bool:
        """Safely deactivate the conservation recommendation agent."""
        print("🔴 Deactivating Conservation Recommendation Agent...")
        
        try:
            # Complete any ongoing recommendations
            if self.active_recommendations:
                print(f"   ⏳ Completing {len(self.active_recommendations)} active recommendations...")
                # In real deployment, this would wait for or safely stop active work
            
            # Save state and learning data
            self._save_deployment_state()
            
            # Clean shutdown
            self.is_active = False
            
            print("✅ Conservation Recommendation Agent deactivated safely")
            return True
            
        except Exception as e:
            print(f"❌ Deactivation error: {e}")
            return False
    
    def _save_deployment_state(self):
        """Save deployment state for future restoration."""
        state = {
            "deployment_config": asdict(self.config),
            "learning_statistics": self.adaptive_engine.get_learning_status(),
            "operational_metrics": asdict(self.operational_metrics),
            "deployment_history_summary": {
                "total_deployments": len(self.deployment_history),
                "successful_deployments": len([d for d in self.deployment_history if "error" not in d]),
                "last_deployment": self.deployment_history[-1] if self.deployment_history else None
            }
        }
        
        print("   💾 Deployment state saved")
        # In real deployment, this would save to persistent storage

def test_system_integration_status():
    """Test system integration status tracking."""
    print("🔗 Testing System Integration Status...")
    
    try:
        status = SystemIntegrationStatus()
        
        # Test initial state
        if status.integration_health_score == 0.0:
            print("✅ Initial integration health score")
        else:
            print("❌ Unexpected initial health score")
            return False
        
        # Simulate integrations
        status.species_identification_agent = True
        status.threat_detection_agent = True
        status.alert_management_system = True
        status.communication_latency = {
            "species_identification_agent": 150.0,
            "threat_detection_agent": 200.0,
            "alert_management_system": 100.0
        }
        status.data_freshness = {
            "species_identification_agent": datetime.utcnow() - timedelta(hours=2),
            "threat_detection_agent": datetime.utcnow() - timedelta(hours=1),
            "alert_management_system": datetime.utcnow() - timedelta(minutes=30)
        }
        
        # Test health calculation
        health_score = status.calculate_integration_health()
        if 0.0 <= health_score <= 1.0:
            print(f"✅ Integration health calculated: {health_score:.2f}")
        else:
            print(f"❌ Invalid health score: {health_score}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ System integration status error: {e}")
        return False

def test_deployment_configuration():
    """Test deployment configuration setup."""
    print("\n⚙️  Testing Deployment Configuration...")
    
    try:
        config = DeploymentConfiguration(
            deployment_id="test_deployment_001",
            environment="development",
            geographic_scope=((-25.0, 43.0), (-12.0, 51.0)),  # Madagascar bounds
            operational_mode="automatic",
            response_time_target=300.0,
            confidence_threshold=0.7
        )
        
        # Test configuration initialization
        if config.deployment_id == "test_deployment_001":
            print("✅ Deployment ID set correctly")
        else:
            print("❌ Deployment ID mismatch")
            return False
        
        # Test default values
        if len(config.resource_allocation_limits) >= 3:
            print(f"✅ Resource allocation limits: {len(config.resource_allocation_limits)}")
        else:
            print("❌ Resource allocation limits incomplete")
            return False
        
        # Test geographic scope
        min_coords, max_coords = config.geographic_scope
        if len(min_coords) == 2 and len(max_coords) == 2:
            print("✅ Geographic scope properly defined")
        else:
            print("❌ Geographic scope format invalid")
            return False
        
        # Test stakeholder rules
        if len(config.stakeholder_notification_rules) >= 3:
            print(f"✅ Stakeholder notification rules: {len(config.stakeholder_notification_rules)}")
        else:
            print("❌ Stakeholder notification rules incomplete")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment configuration error: {e}")
        return False

def test_operational_metrics():
    """Test operational metrics tracking."""
    print("\n📊 Testing Operational Metrics...")
    
    try:
        metrics = OperationalMetrics()
        
        # Test initialization
        if metrics.recommendations_generated == 0:
            print("✅ Initial metrics state")
        else:
            print("❌ Unexpected initial metrics")
            return False
        
        # Test metrics update
        metrics.recommendations_generated = 5
        metrics.recommendations_deployed = 4
        metrics.average_response_time = 245.5
        metrics.system_uptime_percentage = 99.8
        
        # Test resource utilization
        if len(metrics.resource_utilization) >= 4:
            print(f"✅ Resource utilization tracking: {len(metrics.resource_utilization)} metrics")
        else:
            print("❌ Resource utilization incomplete")
            return False
        
        # Test error rates
        if len(metrics.error_rates) >= 4:
            print(f"✅ Error rate tracking: {len(metrics.error_rates)} types")
        else:
            print("❌ Error rate tracking incomplete")
            return False
        
        # Test adaptive learning activity
        if len(metrics.adaptive_learning_activity) >= 4:
            print(f"✅ Adaptive learning activity: {len(metrics.adaptive_learning_activity)} metrics")
        else:
            print("❌ Adaptive learning activity incomplete")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Operational metrics error: {e}")
        return False

async def test_deployment_agent_initialization():
    """Test deployment agent initialization."""
    print("\n🚀 Testing Deployment Agent Initialization...")
    
    try:
        config = DeploymentConfiguration(
            deployment_id="test_init_001",
            environment="development",
            geographic_scope=((-25.0, 43.0), (-12.0, 51.0))
        )
        
        # Initialize agent
        agent = ConservationRecommendationDeploymentAgent(config)
        
        # Test agent components
        if agent.adaptive_engine:
            print("✅ Adaptive engine initialized")
        else:
            print("❌ Adaptive engine missing")
            return False
        
        if agent.integration_status:
            print("✅ Integration status initialized")
        else:
            print("❌ Integration status missing")
            return False
        
        if agent.operational_metrics:
            print("✅ Operational metrics initialized")
        else:
            print("❌ Operational metrics missing")
            return False
        
        # Test initial state
        if not agent.is_active:
            print("✅ Agent starts in inactive state")
        else:
            print("❌ Agent should start inactive")
            return False
        
        # Test activation
        activation_success = agent.activate_deployment()
        if activation_success and agent.is_active:
            print("✅ Agent activation successful")
        else:
            print("❌ Agent activation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment agent initialization error: {e}")
        return False

async def test_conservation_request_processing():
    """Test complete conservation request processing."""
    print("\n🔄 Testing Conservation Request Processing...")
    
    try:
        # Setup agent
        config = DeploymentConfiguration(
            deployment_id="test_processing_001",
            environment="development",
            geographic_scope=((-25.0, 43.0), (-12.0, 51.0)),
            confidence_threshold=0.5  # Lower threshold for testing
        )
        
        agent = ConservationRecommendationDeploymentAgent(config)
        agent.activate_deployment()
        
        # Create test request data
        test_threats = [
            ThreatDetection(
                detection_id="proc_threat_1",
                threat_type=ThreatType.DEFORESTATION,
                severity=0.8,
                severity_level=ThreatSeverity.HIGH,
                urgency=ThreatUrgency.URGENT,
                confidence=0.9
            )
        ]
        
        test_species = [
            SpeciesDetection(
                detection_id="proc_species_1",
                species=MadagascarSpecies.LEMUR_CATTA,
                confidence=0.9,
                confidence_level=SpeciesConfidence.VERY_HIGH,
                timestamp=datetime.utcnow(),
                source="test_processing"
            )
        ]
        
        test_context = ConservationContext(
            location=(-18.947, 48.458),  # Within Madagascar bounds
            ecosystem_type="rainforest",
            protected_area_status=True,
            accessibility=0.7
        )
        
        test_resources = [
            ConservationResource(
                resource_type="field_personnel",
                availability=0.8,
                capacity=15,
                cost_per_unit=100.0
            )
        ]
        
        # Process request
        result = await agent.process_conservation_request(
            threats=test_threats,
            species_detections=test_species,
            context=test_context,
            available_resources=test_resources,
            request_id="test_request_001"
        )
        
        # Validate result
        if result["status"] == "success":
            print("✅ Request processing successful")
        else:
            print(f"❌ Request processing failed: {result.get('error', 'Unknown error')}")
            return False
        
        if "recommendations" in result and len(result["recommendations"]) > 0:
            print(f"✅ Recommendations generated: {len(result['recommendations'])}")
        else:
            print("❌ No recommendations generated")
            return False
        
        if "deployment_packages" in result:
            print(f"✅ Deployment packages created: {len(result['deployment_packages'])}")
        else:
            print("❌ Deployment packages missing")
            return False
        
        if "adaptive_insights" in result:
            print("✅ Adaptive insights included")
        else:
            print("❌ Adaptive insights missing")
            return False
        
        # Check if recommendation was added to active recommendations
        if len(agent.active_recommendations) > 0:
            print(f"✅ Active recommendations updated: {len(agent.active_recommendations)}")
        else:
            print("❌ Active recommendations not updated")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Conservation request processing error: {e}")
        return False

def test_deployment_status_reporting():
    """Test deployment status reporting."""
    print("\n📊 Testing Deployment Status Reporting...")
    
    try:
        config = DeploymentConfiguration(
            deployment_id="test_status_001",
            environment="development",
            geographic_scope=((-25.0, 43.0), (-12.0, 51.0))
        )
        
        agent = ConservationRecommendationDeploymentAgent(config)
        agent.activate_deployment()
        
        # Get status report
        status = agent.get_deployment_status()
        
        # Validate status structure
        required_sections = [
            "agent_status",
            "integration_status", 
            "operational_metrics",
            "active_workload",
            "learning_status",
            "recent_activity"
        ]
        
        missing_sections = [section for section in required_sections if section not in status]
        if not missing_sections:
            print(f"✅ Status report complete: {len(required_sections)} sections")
        else:
            print(f"❌ Missing status sections: {missing_sections}")
            return False
        
        # Validate agent status
        agent_status = status["agent_status"]
        if agent_status["active"] and agent_status["deployment_id"] == "test_status_001":
            print("✅ Agent status accurate")
        else:
            print("❌ Agent status inaccurate")
            return False
        
        # Validate integration status
        integration_status = status["integration_status"]
        if "health_score" in integration_status and 0.0 <= integration_status["health_score"] <= 1.0:
            print(f"✅ Integration health score: {integration_status['health_score']:.2f}")
        else:
            print("❌ Invalid integration health score")
            return False
        
        # Validate operational metrics
        operational_metrics = status["operational_metrics"]
        if "recommendations_generated" in operational_metrics:
            print("✅ Operational metrics included")
        else:
            print("❌ Operational metrics incomplete")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment status reporting error: {e}")
        return False

async def main():
    """Run Section 4 tests."""
    print("🚀 STEP 6 - SECTION 4: Deployment Integration & System Coordination")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: System integration status
    if test_system_integration_status():
        tests_passed += 1
    
    # Test 2: Deployment configuration
    if test_deployment_configuration():
        tests_passed += 1
    
    # Test 3: Operational metrics
    if test_operational_metrics():
        tests_passed += 1
    
    # Test 4: Deployment agent initialization
    if await test_deployment_agent_initialization():
        tests_passed += 1
    
    # Test 5: Conservation request processing
    if await test_conservation_request_processing():
        tests_passed += 1
    
    # Test 6: Deployment status reporting
    if test_deployment_status_reporting():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Section 4 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 4 PASSED - Conservation Recommendation Agent COMPLETE!")
        print("\n🎉 STEP 6 COMPLETE: Conservation Recommendation Agent")
        print("🌟 PHASE 4A COMPLETE: AI Agent Development (6/6 Agents)")
        print("\n🎯 Achievement Summary:")
        print("   • ✅ Species Identification Agent")
        print("   • ✅ Threat Detection Agent") 
        print("   • ✅ Alert Management System")
        print("   • ✅ Satellite Monitoring Agent")
        print("   • ✅ Field Data Integration Agent")
        print("   • ✅ Conservation Recommendation Agent")
        print("\n🚀 Ready for Phase 4B: Full Ecosystem Integration!")
        return True
    else:
        print("❌ Section 4 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
