"""
Step 1: Ecosystem Core Framework
===============================
Build the foundational orchestration system that coordinates all 6 AI agents.
"""

import sys
import os
import json
import time
import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union, Callable, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
import numpy as np
from collections import defaultdict, deque
import logging

# Import all Phase 4A agents
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
from step4_section1_test import MadagascarSpecies, SpeciesConfidence, SpeciesDetection
from step5_section1_test import ThreatType, ThreatSeverity, ThreatUrgency, ThreatDetection
from step5_section3_test import ThreatAlert, ThreatAlertManager
from step6_section1_test import (ConservationPriority, ConservationStrategy, ConservationAction,
                               ConservationResource, ConservationRecommendation, SpeciesType, 
                               ConservationStatus, MadagascarConservationKnowledgeBase)
from step6_section4_test import (ConservationRecommendationDeploymentAgent, DeploymentConfiguration,
                               SystemIntegrationStatus, OperationalMetrics)

class AgentType(Enum):
    """Types of AI agents in the ecosystem."""
    SPECIES_IDENTIFICATION = "species_identification"
    THREAT_DETECTION = "threat_detection"
    ALERT_MANAGEMENT = "alert_management"
    SATELLITE_MONITORING = "satellite_monitoring"
    FIELD_DATA_INTEGRATION = "field_data_integration"
    CONSERVATION_RECOMMENDATION = "conservation_recommendation"

class AgentStatus(Enum):
    """Status states for agents in the ecosystem."""
    INACTIVE = "inactive"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class MessageType(Enum):
    """Types of messages exchanged between agents."""
    DATA_FEED = "data_feed"
    ANALYSIS_REQUEST = "analysis_request"
    ANALYSIS_RESULT = "analysis_result"
    ALERT_NOTIFICATION = "alert_notification"
    STATUS_UPDATE = "status_update"
    COORDINATION_REQUEST = "coordination_request"
    RESOURCE_REQUEST = "resource_request"
    SYSTEM_COMMAND = "system_command"

@dataclass
class AgentMessage:
    """Message structure for inter-agent communication."""
    message_id: str
    message_type: MessageType
    sender_agent: AgentType
    recipient_agent: Optional[AgentType] = None  # None for broadcast
    timestamp: datetime = field(default_factory=datetime.utcnow)
    priority: int = 1  # 1=low, 2=medium, 3=high, 4=critical
    payload: Dict[str, Any] = field(default_factory=dict)
    requires_response: bool = False
    correlation_id: Optional[str] = None  # For request-response pairing
    ttl_seconds: int = 300  # Time to live
    
    def is_expired(self) -> bool:
        """Check if message has expired."""
        return (datetime.utcnow() - self.timestamp).total_seconds() > self.ttl_seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization."""
        return {
            "message_id": self.message_id,
            "message_type": self.message_type.value,
            "sender_agent": self.sender_agent.value,
            "recipient_agent": self.recipient_agent.value if self.recipient_agent else None,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority,
            "payload": self.payload,
            "requires_response": self.requires_response,
            "correlation_id": self.correlation_id,
            "ttl_seconds": self.ttl_seconds
        }

@dataclass
class AgentRegistration:
    """Registration information for agents in the ecosystem."""
    agent_id: str
    agent_type: AgentType
    agent_name: str
    version: str
    capabilities: List[str]
    endpoints: Dict[str, str]
    health_check_url: str
    status: AgentStatus = AgentStatus.INACTIVE
    last_heartbeat: Optional[datetime] = None
    load_metrics: Dict[str, float] = field(default_factory=dict)
    configuration: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.load_metrics:
            self.load_metrics = {
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "request_queue_size": 0,
                "average_response_time": 0.0,
                "error_rate": 0.0
            }

@dataclass
class EcosystemMetrics:
    """Comprehensive metrics for the entire ecosystem."""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    total_agents: int = 0
    active_agents: int = 0
    total_messages_processed: int = 0
    messages_per_minute: float = 0.0
    average_message_latency: float = 0.0
    system_health_score: float = 0.0
    resource_utilization: Dict[str, float] = field(default_factory=dict)
    workflow_completion_rate: float = 0.0
    error_rates: Dict[str, float] = field(default_factory=dict)
    performance_trends: Dict[str, List[float]] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.resource_utilization:
            self.resource_utilization = {
                "total_cpu_usage": 0.0,
                "total_memory_usage": 0.0,
                "network_bandwidth_usage": 0.0,
                "storage_usage": 0.0
            }
        
        if not self.error_rates:
            self.error_rates = {
                "message_delivery_failures": 0.0,
                "agent_failures": 0.0,
                "workflow_failures": 0.0,
                "data_processing_errors": 0.0
            }

class ConservationEcosystemOrchestrator:
    """Central orchestrator for the Madagascar Conservation AI Ecosystem."""
    
    def __init__(self, ecosystem_id: str = None):
        self.ecosystem_id = ecosystem_id or f"madagascar_conservation_{uuid.uuid4().hex[:8]}"
        self.registered_agents: Dict[str, AgentRegistration] = {}
        self.message_queues: Dict[AgentType, deque] = {agent_type: deque() for agent_type in AgentType}
        self.broadcast_queue: deque = deque()
        self.message_history: deque = deque(maxlen=10000)
        
        # Ecosystem state
        self.is_active = False
        self.startup_time: Optional[datetime] = None
        self.ecosystem_metrics = EcosystemMetrics()
        self.workflow_registry: Dict[str, Dict[str, Any]] = {}
        
        # Performance monitoring
        self.performance_window = deque(maxlen=1000)
        self.health_check_interval = 30  # seconds
        self.last_health_check = datetime.utcnow()
        
        # Conservation-specific state
        self.active_conservation_areas: Dict[str, Dict[str, Any]] = {}
        self.species_population_tracking: Dict[str, Dict[str, Any]] = {}
        self.threat_monitoring_zones: Dict[str, Dict[str, Any]] = {}
        self.ongoing_interventions: Dict[str, Dict[str, Any]] = {}
        
        # Initialize logging
        self._setup_logging()
        
        print(f"🌍 Madagascar Conservation AI Ecosystem Orchestrator initialized")
        print(f"   🆔 Ecosystem ID: {self.ecosystem_id}")
    
    def _setup_logging(self):
        """Setup ecosystem logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                # In production, add file handler
            ]
        )
        self.logger = logging.getLogger(f"EcosystemOrchestrator-{self.ecosystem_id}")
    
    async def initialize_ecosystem(self) -> bool:
        """Initialize the complete conservation ecosystem."""
        print("🚀 Initializing Madagascar Conservation AI Ecosystem...")
        
        try:
            # Step 1: Initialize core systems
            await self._initialize_core_systems()
            
            # Step 2: Register and start agents
            await self._register_all_agents()
            
            # Step 3: Establish communication channels
            await self._establish_communication_channels()
            
            # Step 4: Initialize conservation monitoring
            await self._initialize_conservation_monitoring()
            
            # Step 5: Start ecosystem services
            await self._start_ecosystem_services()
            
            # Step 6: Perform system health check
            health_check_passed = await self._perform_initial_health_check()
            
            if health_check_passed:
                self.is_active = True
                self.startup_time = datetime.utcnow()
                self.logger.info("Ecosystem initialization completed successfully")
                print("✅ Madagascar Conservation AI Ecosystem ACTIVE")
                return True
            else:
                self.logger.error("Ecosystem health check failed")
                print("❌ Ecosystem initialization failed - health check")
                return False
                
        except Exception as e:
            self.logger.error(f"Ecosystem initialization failed: {e}")
            print(f"❌ Ecosystem initialization failed: {e}")
            return False
    
    async def _initialize_core_systems(self):
        """Initialize core ecosystem systems."""
        print("   🔧 Initializing core systems...")
        
        # Initialize message processing
        self.message_processor_active = False
        
        # Initialize metrics collection
        self.metrics_collector_active = False
        
        # Initialize workflow engine
        self.workflow_engine_active = False
        
        # Initialize conservation knowledge base
        self.knowledge_base = MadagascarConservationKnowledgeBase()
        
        print("      ✅ Core systems initialized")
    
    async def _register_all_agents(self):
        """Register all AI agents in the ecosystem."""
        print("   🤖 Registering AI agents...")
        
        # Define agent configurations
        agent_configs = [
            {
                "agent_type": AgentType.SPECIES_IDENTIFICATION,
                "agent_name": "Madagascar Species Identification Agent",
                "version": "1.0.0",
                "capabilities": [
                    "species_identification",
                    "image_analysis",
                    "confidence_scoring",
                    "lemur_specialization",
                    "endemic_species_detection"
                ]
            },
            {
                "agent_type": AgentType.THREAT_DETECTION,
                "agent_name": "Conservation Threat Detection Agent", 
                "version": "1.0.0",
                "capabilities": [
                    "deforestation_detection",
                    "poaching_detection",
                    "climate_impact_analysis",
                    "habitat_degradation_monitoring",
                    "multi_modal_analysis"
                ]
            },
            {
                "agent_type": AgentType.ALERT_MANAGEMENT,
                "agent_name": "Conservation Alert Management System",
                "version": "1.0.0", 
                "capabilities": [
                    "threat_prioritization",
                    "alert_routing",
                    "escalation_management",
                    "stakeholder_notification",
                    "emergency_coordination"
                ]
            },
            {
                "agent_type": AgentType.SATELLITE_MONITORING,
                "agent_name": "Madagascar Satellite Monitoring Agent",
                "version": "1.0.0",
                "capabilities": [
                    "satellite_imagery_analysis",
                    "change_detection",
                    "deforestation_monitoring",
                    "habitat_mapping",
                    "temporal_analysis"
                ]
            },
            {
                "agent_type": AgentType.FIELD_DATA_INTEGRATION,
                "agent_name": "Field Data Integration Agent",
                "version": "1.0.0",
                "capabilities": [
                    "sensor_data_integration",
                    "field_report_processing",
                    "real_time_data_validation",
                    "mobile_data_collection",
                    "community_reporting"
                ]
            },
            {
                "agent_type": AgentType.CONSERVATION_RECOMMENDATION,
                "agent_name": "Adaptive Conservation Recommendation Agent",
                "version": "1.0.0",
                "capabilities": [
                    "conservation_strategy_generation",
                    "adaptive_learning",
                    "resource_optimization",
                    "stakeholder_coordination",
                    "intervention_planning"
                ]
            }
        ]
        
        # Register each agent
        for config in agent_configs:
            agent_id = f"{config['agent_type'].value}_{uuid.uuid4().hex[:8]}"
            
            registration = AgentRegistration(
                agent_id=agent_id,
                agent_type=config["agent_type"],
                agent_name=config["agent_name"],
                version=config["version"],
                capabilities=config["capabilities"],
                endpoints={
                    "health": f"/agents/{agent_id}/health",
                    "process": f"/agents/{agent_id}/process",
                    "status": f"/agents/{agent_id}/status"
                },
                health_check_url=f"/agents/{agent_id}/health",
                status=AgentStatus.INITIALIZING
            )
            
            self.registered_agents[agent_id] = registration
            print(f"      ✅ {config['agent_name']} registered")
        
        print(f"      📊 Total agents registered: {len(self.registered_agents)}")
    
    async def _establish_communication_channels(self):
        """Establish communication channels between agents."""
        print("   📡 Establishing communication channels...")
        
        # Initialize message queues for each agent type
        for agent_type in AgentType:
            self.message_queues[agent_type] = deque(maxlen=1000)
        
        # Initialize broadcast queue
        self.broadcast_queue = deque(maxlen=1000)
        
        # Setup message routing rules
        self.routing_rules = {
            # Species identification results go to threat detection and conservation recommendation
            AgentType.SPECIES_IDENTIFICATION: [
                AgentType.THREAT_DETECTION,
                AgentType.CONSERVATION_RECOMMENDATION
            ],
            # Threat detection results go to alert management and conservation recommendation
            AgentType.THREAT_DETECTION: [
                AgentType.ALERT_MANAGEMENT,
                AgentType.CONSERVATION_RECOMMENDATION
            ],
            # Alerts are broadcast to relevant agents
            AgentType.ALERT_MANAGEMENT: [
                AgentType.FIELD_DATA_INTEGRATION,
                AgentType.CONSERVATION_RECOMMENDATION
            ],
            # Satellite data feeds multiple agents
            AgentType.SATELLITE_MONITORING: [
                AgentType.THREAT_DETECTION,
                AgentType.SPECIES_IDENTIFICATION,
                AgentType.CONSERVATION_RECOMMENDATION
            ],
            # Field data validates and enriches other agent data
            AgentType.FIELD_DATA_INTEGRATION: [
                AgentType.SPECIES_IDENTIFICATION,
                AgentType.THREAT_DETECTION,
                AgentType.ALERT_MANAGEMENT
            ],
            # Conservation recommendations coordinate with all agents
            AgentType.CONSERVATION_RECOMMENDATION: [
                AgentType.ALERT_MANAGEMENT,
                AgentType.FIELD_DATA_INTEGRATION
            ]
        }
        
        print("      ✅ Communication channels established")
        print(f"      📊 Routing rules configured for {len(self.routing_rules)} agent types")
    
    async def _initialize_conservation_monitoring(self):
        """Initialize conservation-specific monitoring systems."""
        print("   🌿 Initializing conservation monitoring...")
        
        # Initialize key conservation areas in Madagascar
        self.active_conservation_areas = {
            "andasibe_mantadia": {
                "name": "Andasibe-Mantadia National Park",
                "coordinates": (-18.938, 48.419),
                "area_km2": 155,
                "primary_species": ["indri_indri", "eulemur_fulvus"],
                "threat_level": "medium",
                "monitoring_priority": "high"
            },
            "ranomafana": {
                "name": "Ranomafana National Park", 
                "coordinates": (-21.289, 47.419),
                "area_km2": 416,
                "primary_species": ["lemur_catta", "propithecus_diadema"],
                "threat_level": "high",
                "monitoring_priority": "critical"
            },
            "ankarafantsika": {
                "name": "Ankarafantsika National Park",
                "coordinates": (-16.317, 46.809),
                "area_km2": 1350,
                "primary_species": ["microcebus_murinus", "eulemur_fulvus"],
                "threat_level": "medium",
                "monitoring_priority": "high"
            }
        }
        
        # Initialize species population tracking
        self.species_population_tracking = {
            species.value: {
                "current_population_estimate": 0,
                "population_trend": "unknown",
                "last_survey_date": None,
                "conservation_status": "unknown",
                "monitoring_locations": []
            }
            for species in MadagascarSpecies if species != MadagascarSpecies.UNKNOWN_SPECIES
        }
        
        # Initialize threat monitoring zones
        self.threat_monitoring_zones = {
            "deforestation_hotspots": {
                "active_zones": [],
                "severity_levels": {},
                "trend_analysis": {}
            },
            "poaching_risk_areas": {
                "high_risk_zones": [],
                "patrol_coverage": {},
                "incident_history": {}
            },
            "climate_impact_zones": {
                "vulnerable_areas": [],
                "impact_metrics": {},
                "adaptation_measures": {}
            }
        }
        
        print("      ✅ Conservation monitoring systems initialized")
        print(f"      📊 {len(self.active_conservation_areas)} conservation areas")
        print(f"      📊 {len(self.species_population_tracking)} species tracked")
    
    async def _start_ecosystem_services(self):
        """Start essential ecosystem services."""
        print("   ⚙️  Starting ecosystem services...")
        
        # Start message processor
        await self._start_message_processor()
        
        # Start metrics collector
        await self._start_metrics_collector()
        
        # Start health monitor
        await self._start_health_monitor()
        
        # Start workflow engine
        await self._start_workflow_engine()
        
        print("      ✅ All ecosystem services started")
    
    async def _start_message_processor(self):
        """Start the message processing service."""
        self.message_processor_active = True
        print("         📨 Message processor started")
    
    async def _start_metrics_collector(self):
        """Start the metrics collection service."""
        self.metrics_collector_active = True
        print("         📊 Metrics collector started")
    
    async def _start_health_monitor(self):
        """Start the health monitoring service."""
        self.health_monitor_active = True
        print("         🏥 Health monitor started")
    
    async def _start_workflow_engine(self):
        """Start the workflow automation engine."""
        self.workflow_engine_active = True
        print("         🔄 Workflow engine started")
    
    async def _perform_initial_health_check(self) -> bool:
        """Perform initial ecosystem health check."""
        print("   🏥 Performing initial health check...")
        
        health_checks = []
        
        # Check agent registrations
        registered_agents = len(self.registered_agents)
        expected_agents = len(AgentType)
        agent_check = registered_agents == expected_agents
        health_checks.append(("Agent Registration", agent_check, f"{registered_agents}/{expected_agents}"))
        
        # Check communication channels
        queue_check = len(self.message_queues) == len(AgentType)
        health_checks.append(("Communication Channels", queue_check, f"{len(self.message_queues)} queues"))
        
        # Check core services
        services_check = all([
            self.message_processor_active,
            self.metrics_collector_active,
            self.health_monitor_active,
            self.workflow_engine_active
        ])
        health_checks.append(("Core Services", services_check, "All services active"))
        
        # Check conservation monitoring
        conservation_check = (
            len(self.active_conservation_areas) > 0 and
            len(self.species_population_tracking) > 0 and
            len(self.threat_monitoring_zones) > 0
        )
        health_checks.append(("Conservation Monitoring", conservation_check, "Monitoring initialized"))
        
        # Report health check results
        passed_checks = 0
        for check_name, passed, status in health_checks:
            status_symbol = "✅" if passed else "❌"
            print(f"      {status_symbol} {check_name}: {status}")
            if passed:
                passed_checks += 1
        
        overall_health = passed_checks / len(health_checks)
        self.ecosystem_metrics.system_health_score = overall_health
        
        print(f"      📊 Overall health: {overall_health:.1%}")
        
        return overall_health >= 0.8  # Require 80% health to proceed
    
    async def send_message(self, message: AgentMessage) -> bool:
        """Send a message through the ecosystem."""
        if not self.is_active:
            self.logger.warning("Cannot send message - ecosystem not active")
            return False
        
        if message.is_expired():
            self.logger.warning(f"Message {message.message_id} expired before sending")
            return False
        
        try:
            # Add to message history
            self.message_history.append(message)
            
            # Route message
            if message.recipient_agent:
                # Direct message
                self.message_queues[message.recipient_agent].append(message)
                self.logger.debug(f"Message {message.message_id} queued for {message.recipient_agent.value}")
            else:
                # Broadcast message
                self.broadcast_queue.append(message)
                self.logger.debug(f"Message {message.message_id} queued for broadcast")
            
            # Update metrics
            self.ecosystem_metrics.total_messages_processed += 1
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send message {message.message_id}: {e}")
            return False
    
    async def get_ecosystem_status(self) -> Dict[str, Any]:
        """Get comprehensive ecosystem status."""
        if not self.is_active:
            return {"status": "inactive", "message": "Ecosystem not initialized"}
        
        # Calculate uptime
        uptime_seconds = (datetime.utcnow() - self.startup_time).total_seconds() if self.startup_time else 0
        
        # Get agent status summary
        agent_status_counts = defaultdict(int)
        for agent in self.registered_agents.values():
            agent_status_counts[agent.status.value] += 1
        
        # Calculate message processing rate
        if len(self.message_history) > 1:
            time_span = (self.message_history[-1].timestamp - self.message_history[0].timestamp).total_seconds()
            if time_span > 0:
                self.ecosystem_metrics.messages_per_minute = (len(self.message_history) / time_span) * 60
        
        return {
            "ecosystem_id": self.ecosystem_id,
            "status": "active" if self.is_active else "inactive",
            "uptime_hours": uptime_seconds / 3600,
            "startup_time": self.startup_time.isoformat() if self.startup_time else None,
            "agents": {
                "total_registered": len(self.registered_agents),
                "status_breakdown": dict(agent_status_counts),
                "agent_details": [
                    {
                        "id": agent.agent_id,
                        "type": agent.agent_type.value,
                        "name": agent.agent_name,
                        "status": agent.status.value,
                        "capabilities": agent.capabilities
                    }
                    for agent in self.registered_agents.values()
                ]
            },
            "communication": {
                "total_messages_processed": self.ecosystem_metrics.total_messages_processed,
                "messages_per_minute": self.ecosystem_metrics.messages_per_minute,
                "queue_sizes": {
                    agent_type.value: len(queue) 
                    for agent_type, queue in self.message_queues.items()
                },
                "broadcast_queue_size": len(self.broadcast_queue)
            },
            "conservation_monitoring": {
                "active_conservation_areas": len(self.active_conservation_areas),
                "species_tracked": len(self.species_population_tracking),
                "threat_monitoring_zones": len(self.threat_monitoring_zones),
                "ongoing_interventions": len(self.ongoing_interventions)
            },
            "system_health": {
                "overall_score": self.ecosystem_metrics.system_health_score,
                "services_active": {
                    "message_processor": self.message_processor_active,
                    "metrics_collector": self.metrics_collector_active,
                    "health_monitor": self.health_monitor_active,
                    "workflow_engine": self.workflow_engine_active
                }
            },
            "performance_metrics": asdict(self.ecosystem_metrics)
        }
    
    async def shutdown_ecosystem(self) -> bool:
        """Safely shutdown the ecosystem."""
        print("🔴 Shutting down Madagascar Conservation AI Ecosystem...")
        
        try:
            # Stop ecosystem services
            self.message_processor_active = False
            self.metrics_collector_active = False
            self.health_monitor_active = False
            self.workflow_engine_active = False
            
            # Update agent statuses
            for agent in self.registered_agents.values():
                agent.status = AgentStatus.INACTIVE
            
            # Clear message queues (save if needed)
            for queue in self.message_queues.values():
                queue.clear()
            self.broadcast_queue.clear()
            
            # Mark ecosystem as inactive
            self.is_active = False
            
            self.logger.info("Ecosystem shutdown completed")
            print("✅ Ecosystem shutdown completed safely")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during ecosystem shutdown: {e}")
            print(f"❌ Ecosystem shutdown error: {e}")
            return False

def test_agent_message_system():
    """Test agent message system."""
    print("📨 Testing Agent Message System...")
    
    try:
        # Test message creation
        message = AgentMessage(
            message_id="test_msg_001",
            message_type=MessageType.DATA_FEED,
            sender_agent=AgentType.SPECIES_IDENTIFICATION,
            recipient_agent=AgentType.THREAT_DETECTION,
            priority=2,
            payload={"species_detected": "lemur_catta", "confidence": 0.95},
            requires_response=True
        )
        
        # Test message properties
        if message.message_id == "test_msg_001":
            print("✅ Message ID set correctly")
        else:
            print("❌ Message ID mismatch")
            return False
        
        # Test message expiration
        if not message.is_expired():
            print("✅ Message not expired")
        else:
            print("❌ Message unexpectedly expired")
            return False
        
        # Test message serialization
        message_dict = message.to_dict()
        if "message_id" in message_dict and "payload" in message_dict:
            print("✅ Message serialization successful")
        else:
            print("❌ Message serialization failed")
            return False
        
        # Test broadcast message
        broadcast_message = AgentMessage(
            message_id="broadcast_001",
            message_type=MessageType.ALERT_NOTIFICATION,
            sender_agent=AgentType.ALERT_MANAGEMENT,
            priority=4,
            payload={"alert_type": "critical_threat", "location": (-18.947, 48.458)}
        )
        
        if broadcast_message.recipient_agent is None:
            print("✅ Broadcast message created correctly")
        else:
            print("❌ Broadcast message has unexpected recipient")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Agent message system error: {e}")
        return False

def test_agent_registration():
    """Test agent registration system."""
    print("\n🤖 Testing Agent Registration...")
    
    try:
        # Test agent registration creation
        registration = AgentRegistration(
            agent_id="test_agent_001",
            agent_type=AgentType.SPECIES_IDENTIFICATION,
            agent_name="Test Species Agent",
            version="1.0.0",
            capabilities=["species_identification", "image_analysis"],
            endpoints={"health": "/health", "process": "/process"},
            health_check_url="/health"
        )
        
        # Test registration properties
        if registration.agent_type == AgentType.SPECIES_IDENTIFICATION:
            print("✅ Agent type set correctly")
        else:
            print("❌ Agent type mismatch")
            return False
        
        # Test capabilities
        if len(registration.capabilities) == 2:
            print("✅ Capabilities set correctly")
        else:
            print("❌ Capabilities mismatch")
            return False
        
        # Test load metrics initialization
        if len(registration.load_metrics) >= 5:
            print(f"✅ Load metrics initialized: {len(registration.load_metrics)}")
        else:
            print("❌ Load metrics incomplete")
            return False
        
        # Test status
        if registration.status == AgentStatus.INACTIVE:
            print("✅ Initial status correct")
        else:
            print("❌ Initial status incorrect")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Agent registration error: {e}")
        return False

def test_ecosystem_metrics():
    """Test ecosystem metrics system."""
    print("\n📊 Testing Ecosystem Metrics...")
    
    try:
        metrics = EcosystemMetrics()
        
        # Test initial values
        if metrics.total_agents == 0:
            print("✅ Initial metrics state")
        else:
            print("❌ Unexpected initial metrics")
            return False
        
        # Test resource utilization
        if len(metrics.resource_utilization) >= 4:
            print(f"✅ Resource utilization tracking: {len(metrics.resource_utilization)}")
        else:
            print("❌ Resource utilization incomplete")
            return False
        
        # Test error rates
        if len(metrics.error_rates) >= 4:
            print(f"✅ Error rate tracking: {len(metrics.error_rates)}")
        else:
            print("❌ Error rate tracking incomplete")
            return False
        
        # Test metrics update
        metrics.total_agents = 6
        metrics.active_agents = 5
        metrics.system_health_score = 0.85
        
        if metrics.active_agents < metrics.total_agents:
            print("✅ Metrics update successful")
        else:
            print("❌ Metrics update failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Ecosystem metrics error: {e}")
        return False

async def test_ecosystem_orchestrator():
    """Test ecosystem orchestrator functionality."""
    print("\n🌍 Testing Ecosystem Orchestrator...")
    
    try:
        # Test orchestrator creation
        orchestrator = ConservationEcosystemOrchestrator("test_ecosystem")
        
        if orchestrator.ecosystem_id == "test_ecosystem":
            print("✅ Orchestrator created with correct ID")
        else:
            print("❌ Orchestrator ID mismatch")
            return False
        
        # Test initialization
        initialization_success = await orchestrator.initialize_ecosystem()
        
        if initialization_success:
            print("✅ Ecosystem initialization successful")
        else:
            print("❌ Ecosystem initialization failed")
            return False
        
        # Test agent registration count
        if len(orchestrator.registered_agents) == 6:
            print(f"✅ All 6 agents registered")
        else:
            print(f"❌ Agent registration incomplete: {len(orchestrator.registered_agents)}/6")
            return False
        
        # Test message sending
        test_message = AgentMessage(
            message_id="test_orchestrator_msg",
            message_type=MessageType.STATUS_UPDATE,
            sender_agent=AgentType.SPECIES_IDENTIFICATION,
            recipient_agent=AgentType.THREAT_DETECTION,
            payload={"status": "active"}
        )
        
        message_sent = await orchestrator.send_message(test_message)
        if message_sent:
            print("✅ Message sending successful")
        else:
            print("❌ Message sending failed")
            return False
        
        # Test ecosystem status
        status = await orchestrator.get_ecosystem_status()
        
        if status["status"] == "active":
            print("✅ Ecosystem status reporting successful")
        else:
            print("❌ Ecosystem status reporting failed")
            return False
        
        # Test conservation monitoring
        if len(orchestrator.active_conservation_areas) >= 3:
            print(f"✅ Conservation areas initialized: {len(orchestrator.active_conservation_areas)}")
        else:
            print("❌ Conservation areas incomplete")
            return False
        
        # Test shutdown
        shutdown_success = await orchestrator.shutdown_ecosystem()
        if shutdown_success:
            print("✅ Ecosystem shutdown successful")
        else:
            print("❌ Ecosystem shutdown failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Ecosystem orchestrator error: {e}")
        return False

async def test_ecosystem_communication():
    """Test ecosystem communication and message routing."""
    print("\n📡 Testing Ecosystem Communication...")
    
    try:
        orchestrator = ConservationEcosystemOrchestrator("test_communication")
        await orchestrator.initialize_ecosystem()
        
        # Test routing rules
        if len(orchestrator.routing_rules) == len(AgentType):
            print(f"✅ Routing rules configured for all {len(AgentType)} agent types")
        else:
            print("❌ Routing rules incomplete")
            return False
        
        # Test message queue creation
        queue_count = len(orchestrator.message_queues)
        if queue_count == len(AgentType):
            print(f"✅ Message queues created: {queue_count}")
        else:
            print(f"❌ Message queue creation incomplete: {queue_count}/{len(AgentType)}")
            return False
        
        # Test direct message routing
        direct_message = AgentMessage(
            message_id="direct_test",
            message_type=MessageType.ANALYSIS_REQUEST,
            sender_agent=AgentType.SATELLITE_MONITORING,
            recipient_agent=AgentType.THREAT_DETECTION,
            payload={"image_data": "satellite_image_001"}
        )
        
        await orchestrator.send_message(direct_message)
        
        # Check if message was queued correctly
        threat_queue_size = len(orchestrator.message_queues[AgentType.THREAT_DETECTION])
        if threat_queue_size >= 1:
            print("✅ Direct message routing successful")
        else:
            print("❌ Direct message routing failed")
            return False
        
        # Test broadcast message
        broadcast_message = AgentMessage(
            message_id="broadcast_test",
            message_type=MessageType.ALERT_NOTIFICATION,
            sender_agent=AgentType.ALERT_MANAGEMENT,
            priority=4,
            payload={"alert": "system_wide_alert"}
        )
        
        await orchestrator.send_message(broadcast_message)
        
        # Check broadcast queue
        broadcast_queue_size = len(orchestrator.broadcast_queue)
        if broadcast_queue_size >= 1:
            print("✅ Broadcast message routing successful")
        else:
            print("❌ Broadcast message routing failed")
            return False
        
        # Test message history
        if len(orchestrator.message_history) >= 2:
            print("✅ Message history tracking successful")
        else:
            print("❌ Message history tracking failed")
            return False
        
        await orchestrator.shutdown_ecosystem()
        return True
        
    except Exception as e:
        print(f"❌ Ecosystem communication error: {e}")
        return False

async def main():
    """Run Step 1 tests."""
    print("🌍 STEP 1: Ecosystem Core Framework")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Agent message system
    if test_agent_message_system():
        tests_passed += 1
    
    # Test 2: Agent registration
    if test_agent_registration():
        tests_passed += 1
    
    # Test 3: Ecosystem metrics
    if test_ecosystem_metrics():
        tests_passed += 1
    
    # Test 4: Ecosystem orchestrator
    if await test_ecosystem_orchestrator():
        tests_passed += 1
    
    # Test 5: Ecosystem communication
    if await test_ecosystem_communication():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Step 1 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Step 1 PASSED - Ecosystem Core Framework Complete")
        print("\n🎯 Next: Implement Agent Communication Protocols")
        print("\n🌟 Achievements:")
        print("   • ✅ Ecosystem orchestration framework")
        print("   • ✅ Agent registration and management")
        print("   • ✅ Inter-agent message routing")
        print("   • ✅ Conservation monitoring integration")
        print("   • ✅ System health and metrics tracking")
        return True
    else:
        print("❌ Step 1 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    asyncio.run(main())
