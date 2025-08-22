"""
Step 2: Agent Communication Protocols
====================================
Implement sophisticated communication protocols for seamless agent coordination.
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

# Import ecosystem core and Phase 4A agents
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4b_ecosystem/ecosystem_core')

from step4_section1_test import MadagascarSpecies, SpeciesConfidence, SpeciesDetection
from step5_section1_test import ThreatType, ThreatSeverity, ThreatUrgency, ThreatDetection
from step5_section3_test import ThreatAlert, ThreatAlertManager
from step6_section1_test import (ConservationPriority, ConservationStrategy, ConservationAction,
                               ConservationResource, ConservationRecommendation, SpeciesType, 
                               ConservationStatus, MadagascarConservationKnowledgeBase)
from step1_ecosystem_core import (AgentType, AgentStatus, MessageType, AgentMessage, 
                                AgentRegistration, EcosystemMetrics, ConservationEcosystemOrchestrator)

class CommunicationProtocol(Enum):
    """Communication protocols for different interaction patterns."""
    SYNCHRONOUS_REQUEST_RESPONSE = "sync_req_resp"
    ASYNCHRONOUS_MESSAGING = "async_messaging"
    PUBLISH_SUBSCRIBE = "pub_sub"
    BROADCAST_NOTIFICATION = "broadcast"
    WORKFLOW_COORDINATION = "workflow_coord"
    REAL_TIME_STREAMING = "real_time_stream"

class DataFormat(Enum):
    """Standardized data formats for inter-agent communication."""
    SPECIES_DETECTION_FORMAT = "species_detection"
    THREAT_ANALYSIS_FORMAT = "threat_analysis"
    SATELLITE_DATA_FORMAT = "satellite_data"
    FIELD_DATA_FORMAT = "field_data"
    CONSERVATION_RECOMMENDATION_FORMAT = "conservation_rec"
    ALERT_FORMAT = "alert"
    WORKFLOW_INSTRUCTION_FORMAT = "workflow_instruction"

@dataclass
class CommunicationChannel:
    """Communication channel between agents."""
    channel_id: str
    protocol: CommunicationProtocol
    sender_agent: AgentType
    receiver_agent: Optional[AgentType] = None  # None for broadcast channels
    data_format: DataFormat = DataFormat.SPECIES_DETECTION_FORMAT
    reliability_mode: str = "at_least_once"  # "at_most_once", "at_least_once", "exactly_once"
    compression_enabled: bool = False
    encryption_enabled: bool = False
    message_ttl_seconds: int = 300
    max_message_size_bytes: int = 10485760  # 10MB
    throughput_limit_per_second: int = 100
    
    # Channel statistics
    messages_sent: int = 0
    messages_received: int = 0
    total_bytes_transferred: int = 0
    average_latency_ms: float = 0.0
    error_count: int = 0
    last_activity: Optional[datetime] = None
    
    def update_statistics(self, message_size: int, latency_ms: float, error: bool = False):
        """Update channel statistics."""
        self.messages_sent += 1
        self.total_bytes_transferred += message_size
        self.last_activity = datetime.utcnow()
        
        if error:
            self.error_count += 1
        else:
            # Update rolling average latency
            self.average_latency_ms = (self.average_latency_ms * 0.9 + latency_ms * 0.1)

@dataclass
class WorkflowStep:
    """Individual step in a conservation workflow."""
    step_id: str
    step_name: str
    responsible_agent: AgentType
    input_requirements: List[DataFormat]
    output_format: DataFormat
    dependencies: List[str] = field(default_factory=list)
    timeout_seconds: int = 300
    retry_count: int = 3
    parallel_execution: bool = False
    
    # Execution state
    status: str = "pending"  # "pending", "running", "completed", "failed"
    start_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    execution_count: int = 0
    error_message: Optional[str] = None

@dataclass
class ConservationWorkflow:
    """Complete conservation workflow definition."""
    workflow_id: str
    workflow_name: str
    description: str
    steps: List[WorkflowStep]
    trigger_conditions: Dict[str, Any]
    priority: int = 1
    
    # Workflow state
    status: str = "initialized"  # "initialized", "running", "completed", "failed", "paused"
    current_step: Optional[str] = None
    start_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    execution_context: Dict[str, Any] = field(default_factory=dict)
    
    def get_next_steps(self) -> List[WorkflowStep]:
        """Get next executable steps based on dependencies."""
        if self.status != "running":
            return []
        
        completed_steps = [step.step_id for step in self.steps if step.status == "completed"]
        
        next_steps = []
        for step in self.steps:
            if (step.status == "pending" and 
                all(dep in completed_steps for dep in step.dependencies)):
                next_steps.append(step)
        
        return next_steps

class ConservationDataTransformer:
    """Transform data between different agent formats."""
    
    @staticmethod
    def species_detection_to_threat_input(detection: SpeciesDetection) -> Dict[str, Any]:
        """Transform species detection for threat analysis."""
        return {
            "species_presence": {
                "species": detection.species.value,
                "confidence": detection.confidence,
                "timestamp": detection.timestamp.isoformat(),
                "location_context": "derived_from_detection",
                "conservation_status": ConservationDataTransformer._get_conservation_status(detection.species)
            },
            "ecosystem_indicators": {
                "biodiversity_signal": detection.confidence,
                "habitat_quality_indicator": detection.confidence * 0.8,
                "population_health": "unknown"
            }
        }
    
    @staticmethod
    def threat_detection_to_alert_input(threat: ThreatDetection) -> Dict[str, Any]:
        """Transform threat detection for alert management."""
        return {
            "threat_classification": {
                "type": threat.threat_type.value,
                "severity": threat.severity,
                "urgency": threat.urgency.value,
                "confidence": threat.confidence
            },
            "alert_metadata": {
                "detection_id": threat.detection_id,
                "timestamp": threat.timestamp.isoformat(),
                "source": "threat_detection_agent",
                "requires_immediate_action": threat.urgency in [ThreatUrgency.EMERGENCY, ThreatUrgency.CRISIS]
            },
            "escalation_criteria": {
                "severity_threshold": 0.7,
                "stakeholder_notification": threat.severity > 0.8,
                "emergency_response": threat.urgency == ThreatUrgency.CRISIS
            }
        }
    
    @staticmethod
    def satellite_data_to_analysis_input(satellite_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform satellite data for multiple agent analysis."""
        return {
            "imagery_metadata": satellite_data.get("metadata", {}),
            "analysis_parameters": {
                "deforestation_detection": True,
                "habitat_change_analysis": True,
                "species_habitat_mapping": True,
                "temporal_comparison": True
            },
            "processing_instructions": {
                "resolution": satellite_data.get("resolution", "high"),
                "spectral_bands": satellite_data.get("spectral_bands", []),
                "analysis_priority": "conservation_focused"
            }
        }
    
    @staticmethod
    def field_data_to_integration_format(field_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform field data for ecosystem integration."""
        return {
            "observation_data": field_data.get("observations", {}),
            "validation_context": {
                "field_verification": True,
                "ground_truth_confidence": field_data.get("confidence", 0.8),
                "observer_expertise": field_data.get("observer_type", "trained")
            },
            "integration_instructions": {
                "cross_validate_with": ["species_identification", "threat_detection"],
                "update_population_estimates": True,
                "calibrate_remote_sensing": True
            }
        }
    
    @staticmethod
    def _get_conservation_status(species: MadagascarSpecies) -> str:
        """Get conservation status for species."""
        status_mapping = {
            MadagascarSpecies.LEMUR_CATTA: "endangered",
            MadagascarSpecies.INDRI_INDRI: "critically_endangered",
            MadagascarSpecies.EULEMUR_FULVUS: "vulnerable",
            MadagascarSpecies.PROPITHECUS_DIADEMA: "critically_endangered",
            MadagascarSpecies.MICROCEBUS_MURINUS: "least_concern",
            MadagascarSpecies.BROOKESIA_MICRA: "near_threatened",
            MadagascarSpecies.FURCIFER_PARDALIS: "least_concern",
            MadagascarSpecies.UROPLATUS_PHANTASTICUS: "vulnerable"
        }
        return status_mapping.get(species, "data_deficient")

class CommunicationProtocolManager:
    """Manage communication protocols between agents."""
    
    def __init__(self, orchestrator: ConservationEcosystemOrchestrator):
        self.orchestrator = orchestrator
        self.communication_channels: Dict[str, CommunicationChannel] = {}
        self.active_workflows: Dict[str, ConservationWorkflow] = {}
        self.data_transformer = ConservationDataTransformer()
        
        # Protocol handlers
        self.protocol_handlers = {
            CommunicationProtocol.SYNCHRONOUS_REQUEST_RESPONSE: self._handle_sync_request_response,
            CommunicationProtocol.ASYNCHRONOUS_MESSAGING: self._handle_async_messaging,
            CommunicationProtocol.PUBLISH_SUBSCRIBE: self._handle_pub_sub,
            CommunicationProtocol.BROADCAST_NOTIFICATION: self._handle_broadcast,
            CommunicationProtocol.WORKFLOW_COORDINATION: self._handle_workflow_coordination,
            CommunicationProtocol.REAL_TIME_STREAMING: self._handle_real_time_streaming
        }
        
        # Message queues for different protocols
        self.request_response_queue: Dict[str, Dict[str, Any]] = {}
        self.subscription_registry: Dict[str, List[AgentType]] = {}
        self.streaming_connections: Dict[str, Dict[str, Any]] = {}
        
        # Initialize standard communication channels
        self._initialize_communication_channels()
        
        # Initialize conservation workflows
        self._initialize_conservation_workflows()
        
        print("📡 Communication Protocol Manager initialized")
    
    def _initialize_communication_channels(self):
        """Initialize standard communication channels between agents."""
        
        # Species identification -> Multiple agents
        self._create_channel(
            "species_to_threat",
            CommunicationProtocol.ASYNCHRONOUS_MESSAGING,
            AgentType.SPECIES_IDENTIFICATION,
            AgentType.THREAT_DETECTION,
            DataFormat.SPECIES_DETECTION_FORMAT
        )
        
        self._create_channel(
            "species_to_conservation",
            CommunicationProtocol.ASYNCHRONOUS_MESSAGING,
            AgentType.SPECIES_IDENTIFICATION,
            AgentType.CONSERVATION_RECOMMENDATION,
            DataFormat.SPECIES_DETECTION_FORMAT
        )
        
        # Threat detection -> Alert management
        self._create_channel(
            "threat_to_alert",
            CommunicationProtocol.SYNCHRONOUS_REQUEST_RESPONSE,
            AgentType.THREAT_DETECTION,
            AgentType.ALERT_MANAGEMENT,
            DataFormat.THREAT_ANALYSIS_FORMAT
        )
        
        # Satellite monitoring -> Multiple agents
        self._create_channel(
            "satellite_broadcast",
            CommunicationProtocol.PUBLISH_SUBSCRIBE,
            AgentType.SATELLITE_MONITORING,
            None,  # Broadcast
            DataFormat.SATELLITE_DATA_FORMAT
        )
        
        # Field data integration -> Validation network
        self._create_channel(
            "field_validation",
            CommunicationProtocol.WORKFLOW_COORDINATION,
            AgentType.FIELD_DATA_INTEGRATION,
            None,
            DataFormat.FIELD_DATA_FORMAT
        )
        
        # Conservation recommendations -> Stakeholder notifications
        self._create_channel(
            "conservation_alerts",
            CommunicationProtocol.BROADCAST_NOTIFICATION,
            AgentType.CONSERVATION_RECOMMENDATION,
            None,
            DataFormat.CONSERVATION_RECOMMENDATION_FORMAT
        )
        
        # Real-time monitoring streams
        self._create_channel(
            "real_time_monitoring",
            CommunicationProtocol.REAL_TIME_STREAMING,
            AgentType.SATELLITE_MONITORING,
            AgentType.THREAT_DETECTION,
            DataFormat.SATELLITE_DATA_FORMAT
        )
        
        print(f"   📊 {len(self.communication_channels)} communication channels initialized")
    
    def _create_channel(self, channel_id: str, protocol: CommunicationProtocol, 
                       sender: AgentType, receiver: Optional[AgentType], 
                       data_format: DataFormat):
        """Create a communication channel."""
        channel = CommunicationChannel(
            channel_id=channel_id,
            protocol=protocol,
            sender_agent=sender,
            receiver_agent=receiver,
            data_format=data_format
        )
        self.communication_channels[channel_id] = channel
    
    def _initialize_conservation_workflows(self):
        """Initialize standard conservation workflows."""
        
        # Emergency Response Workflow
        emergency_workflow = ConservationWorkflow(
            workflow_id="emergency_response",
            workflow_name="Emergency Conservation Response",
            description="Rapid response to critical conservation threats",
            steps=[
                WorkflowStep(
                    step_id="threat_assessment",
                    step_name="Critical Threat Assessment",
                    responsible_agent=AgentType.THREAT_DETECTION,
                    input_requirements=[DataFormat.SATELLITE_DATA_FORMAT, DataFormat.FIELD_DATA_FORMAT],
                    output_format=DataFormat.THREAT_ANALYSIS_FORMAT,
                    timeout_seconds=60
                ),
                WorkflowStep(
                    step_id="species_impact_analysis",
                    step_name="Species Impact Analysis",
                    responsible_agent=AgentType.SPECIES_IDENTIFICATION,
                    input_requirements=[DataFormat.THREAT_ANALYSIS_FORMAT],
                    output_format=DataFormat.SPECIES_DETECTION_FORMAT,
                    dependencies=["threat_assessment"],
                    timeout_seconds=120,
                    parallel_execution=True
                ),
                WorkflowStep(
                    step_id="alert_generation",
                    step_name="Generate Emergency Alert",
                    responsible_agent=AgentType.ALERT_MANAGEMENT,
                    input_requirements=[DataFormat.THREAT_ANALYSIS_FORMAT, DataFormat.SPECIES_DETECTION_FORMAT],
                    output_format=DataFormat.ALERT_FORMAT,
                    dependencies=["threat_assessment", "species_impact_analysis"],
                    timeout_seconds=30
                ),
                WorkflowStep(
                    step_id="emergency_recommendations",
                    step_name="Generate Emergency Recommendations",
                    responsible_agent=AgentType.CONSERVATION_RECOMMENDATION,
                    input_requirements=[DataFormat.THREAT_ANALYSIS_FORMAT, DataFormat.SPECIES_DETECTION_FORMAT],
                    output_format=DataFormat.CONSERVATION_RECOMMENDATION_FORMAT,
                    dependencies=["threat_assessment", "species_impact_analysis"],
                    timeout_seconds=180,
                    parallel_execution=True
                )
            ],
            trigger_conditions={
                "threat_severity": "> 0.8",
                "threat_urgency": ["emergency", "crisis"],
                "critical_species_involved": True
            },
            priority=4
        )
        
        # Routine Monitoring Workflow
        routine_workflow = ConservationWorkflow(
            workflow_id="routine_monitoring",
            workflow_name="Routine Conservation Monitoring",
            description="Regular monitoring and assessment workflow",
            steps=[
                WorkflowStep(
                    step_id="satellite_analysis",
                    step_name="Satellite Data Analysis",
                    responsible_agent=AgentType.SATELLITE_MONITORING,
                    input_requirements=[DataFormat.SATELLITE_DATA_FORMAT],
                    output_format=DataFormat.SATELLITE_DATA_FORMAT,
                    timeout_seconds=600
                ),
                WorkflowStep(
                    step_id="species_survey",
                    step_name="Species Population Survey",
                    responsible_agent=AgentType.SPECIES_IDENTIFICATION,
                    input_requirements=[DataFormat.SATELLITE_DATA_FORMAT, DataFormat.FIELD_DATA_FORMAT],
                    output_format=DataFormat.SPECIES_DETECTION_FORMAT,
                    dependencies=["satellite_analysis"],
                    timeout_seconds=1800
                ),
                WorkflowStep(
                    step_id="threat_monitoring",
                    step_name="Threat Monitoring Assessment",
                    responsible_agent=AgentType.THREAT_DETECTION,
                    input_requirements=[DataFormat.SATELLITE_DATA_FORMAT, DataFormat.SPECIES_DETECTION_FORMAT],
                    output_format=DataFormat.THREAT_ANALYSIS_FORMAT,
                    dependencies=["satellite_analysis", "species_survey"],
                    timeout_seconds=900
                ),
                WorkflowStep(
                    step_id="conservation_planning",
                    step_name="Conservation Strategy Planning",
                    responsible_agent=AgentType.CONSERVATION_RECOMMENDATION,
                    input_requirements=[DataFormat.SPECIES_DETECTION_FORMAT, DataFormat.THREAT_ANALYSIS_FORMAT],
                    output_format=DataFormat.CONSERVATION_RECOMMENDATION_FORMAT,
                    dependencies=["species_survey", "threat_monitoring"],
                    timeout_seconds=1200
                )
            ],
            trigger_conditions={
                "schedule": "daily",
                "data_availability": True
            },
            priority=1
        )
        
        self.active_workflows = {
            "emergency_response": emergency_workflow,
            "routine_monitoring": routine_workflow
        }
        
        print(f"   📊 {len(self.active_workflows)} conservation workflows initialized")
    
    async def send_message_via_protocol(self, channel_id: str, message_data: Dict[str, Any],
                                       correlation_id: str = None) -> Dict[str, Any]:
        """Send message using specified communication protocol."""
        
        if channel_id not in self.communication_channels:
            return {"success": False, "error": "Channel not found"}
        
        channel = self.communication_channels[channel_id]
        start_time = time.time()
        
        try:
            # Transform data if needed
            transformed_data = await self._transform_data_for_channel(message_data, channel)
            
            # Create protocol message
            protocol_message = AgentMessage(
                message_id=f"{channel_id}_{uuid.uuid4().hex[:8]}",
                message_type=self._get_message_type_for_protocol(channel.protocol),
                sender_agent=channel.sender_agent,
                recipient_agent=channel.receiver_agent,
                payload=transformed_data,
                correlation_id=correlation_id
            )
            
            # Route through protocol handler
            result = await self.protocol_handlers[channel.protocol](channel, protocol_message)
            
            # Update channel statistics
            latency_ms = (time.time() - start_time) * 1000
            message_size = len(json.dumps(transformed_data).encode('utf-8'))
            channel.update_statistics(message_size, latency_ms, error=not result.get("success", False))
            
            return result
            
        except Exception as e:
            # Update error statistics
            latency_ms = (time.time() - start_time) * 1000
            channel.update_statistics(0, latency_ms, error=True)
            
            return {"success": False, "error": str(e)}
    
    async def _transform_data_for_channel(self, data: Dict[str, Any], 
                                        channel: CommunicationChannel) -> Dict[str, Any]:
        """Transform data according to channel data format requirements."""
        
        if channel.data_format == DataFormat.SPECIES_DETECTION_FORMAT:
            # Ensure species detection format
            if "species" in data and "confidence" in data:
                return {
                    "species_detection": data,
                    "metadata": {
                        "format_version": "1.0",
                        "transformation_time": datetime.utcnow().isoformat()
                    }
                }
        
        elif channel.data_format == DataFormat.THREAT_ANALYSIS_FORMAT:
            # Ensure threat analysis format
            if "threat_type" in data or "threat_classification" in data:
                return {
                    "threat_analysis": data,
                    "metadata": {
                        "format_version": "1.0", 
                        "analysis_time": datetime.utcnow().isoformat()
                    }
                }
        
        # Return data as-is if no specific transformation needed
        return {
            "payload": data,
            "metadata": {
                "format": channel.data_format.value,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    def _get_message_type_for_protocol(self, protocol: CommunicationProtocol) -> MessageType:
        """Get appropriate message type for communication protocol."""
        protocol_message_mapping = {
            CommunicationProtocol.SYNCHRONOUS_REQUEST_RESPONSE: MessageType.ANALYSIS_REQUEST,
            CommunicationProtocol.ASYNCHRONOUS_MESSAGING: MessageType.DATA_FEED,
            CommunicationProtocol.PUBLISH_SUBSCRIBE: MessageType.DATA_FEED,
            CommunicationProtocol.BROADCAST_NOTIFICATION: MessageType.ALERT_NOTIFICATION,
            CommunicationProtocol.WORKFLOW_COORDINATION: MessageType.COORDINATION_REQUEST,
            CommunicationProtocol.REAL_TIME_STREAMING: MessageType.DATA_FEED
        }
        return protocol_message_mapping.get(protocol, MessageType.DATA_FEED)
    
    async def _handle_sync_request_response(self, channel: CommunicationChannel, 
                                          message: AgentMessage) -> Dict[str, Any]:
        """Handle synchronous request-response communication."""
        try:
            # Store request for response tracking
            request_id = message.correlation_id or message.message_id
            self.request_response_queue[request_id] = {
                "request": message,
                "timestamp": datetime.utcnow(),
                "timeout": datetime.utcnow() + timedelta(seconds=channel.message_ttl_seconds)
            }
            
            # Send message to recipient
            await self.orchestrator.send_message(message)
            
            # Wait for response (simplified for testing)
            await asyncio.sleep(0.1)  # Simulate processing time
            
            return {
                "success": True,
                "request_id": request_id,
                "protocol": "synchronous_request_response",
                "response_expected": True
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _handle_async_messaging(self, channel: CommunicationChannel,
                                    message: AgentMessage) -> Dict[str, Any]:
        """Handle asynchronous messaging communication."""
        try:
            # Queue message for asynchronous delivery
            await self.orchestrator.send_message(message)
            
            return {
                "success": True,
                "message_id": message.message_id,
                "protocol": "asynchronous_messaging",
                "delivery_mode": "queued"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _handle_pub_sub(self, channel: CommunicationChannel,
                            message: AgentMessage) -> Dict[str, Any]:
        """Handle publish-subscribe communication."""
        try:
            # Get subscribers for this topic
            topic = f"{channel.sender_agent.value}_{channel.data_format.value}"
            subscribers = self.subscription_registry.get(topic, [])
            
            # Publish to all subscribers
            delivery_count = 0
            for subscriber in subscribers:
                subscriber_message = AgentMessage(
                    message_id=f"{message.message_id}_{subscriber.value}",
                    message_type=message.message_type,
                    sender_agent=message.sender_agent,
                    recipient_agent=subscriber,
                    payload=message.payload,
                    correlation_id=message.correlation_id
                )
                
                await self.orchestrator.send_message(subscriber_message)
                delivery_count += 1
            
            return {
                "success": True,
                "message_id": message.message_id,
                "protocol": "publish_subscribe",
                "subscribers_notified": delivery_count,
                "topic": topic
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _handle_broadcast(self, channel: CommunicationChannel,
                              message: AgentMessage) -> Dict[str, Any]:
        """Handle broadcast notification communication."""
        try:
            # Broadcast to all agents except sender
            all_agents = list(AgentType)
            recipients = [agent for agent in all_agents if agent != channel.sender_agent]
            
            delivery_count = 0
            for recipient in recipients:
                broadcast_message = AgentMessage(
                    message_id=f"{message.message_id}_{recipient.value}",
                    message_type=MessageType.ALERT_NOTIFICATION,
                    sender_agent=message.sender_agent,
                    recipient_agent=recipient,
                    payload=message.payload,
                    priority=4  # High priority for broadcasts
                )
                
                await self.orchestrator.send_message(broadcast_message)
                delivery_count += 1
            
            return {
                "success": True,
                "message_id": message.message_id,
                "protocol": "broadcast_notification",
                "recipients_notified": delivery_count
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _handle_workflow_coordination(self, channel: CommunicationChannel,
                                          message: AgentMessage) -> Dict[str, Any]:
        """Handle workflow coordination communication."""
        try:
            # Extract workflow context
            workflow_id = message.payload.get("workflow_id")
            step_id = message.payload.get("step_id")
            
            if workflow_id and workflow_id in self.active_workflows:
                workflow = self.active_workflows[workflow_id]
                
                # Update workflow execution context
                workflow.execution_context.update(message.payload)
                
                # Coordinate next steps
                next_steps = workflow.get_next_steps()
                coordination_actions = []
                
                for step in next_steps:
                    coordination_message = AgentMessage(
                        message_id=f"workflow_{workflow_id}_{step.step_id}",
                        message_type=MessageType.COORDINATION_REQUEST,
                        sender_agent=channel.sender_agent,
                        recipient_agent=step.responsible_agent,
                        payload={
                            "workflow_id": workflow_id,
                            "step_id": step.step_id,
                            "step_instructions": {
                                "input_data": message.payload.get("output_data", {}),
                                "timeout": step.timeout_seconds,
                                "parallel_allowed": step.parallel_execution
                            }
                        }
                    )
                    
                    await self.orchestrator.send_message(coordination_message)
                    coordination_actions.append(step.step_id)
                
                return {
                    "success": True,
                    "message_id": message.message_id,
                    "protocol": "workflow_coordination",
                    "workflow_id": workflow_id,
                    "coordinated_steps": coordination_actions
                }
            else:
                return {"success": False, "error": "Workflow not found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _handle_real_time_streaming(self, channel: CommunicationChannel,
                                        message: AgentMessage) -> Dict[str, Any]:
        """Handle real-time streaming communication."""
        try:
            # Establish streaming connection if not exists
            stream_id = f"{channel.sender_agent.value}_{channel.receiver_agent.value}"
            
            if stream_id not in self.streaming_connections:
                self.streaming_connections[stream_id] = {
                    "established": datetime.utcnow(),
                    "messages_streamed": 0,
                    "last_activity": datetime.utcnow()
                }
            
            # Stream message with minimal latency
            await self.orchestrator.send_message(message)
            
            # Update streaming statistics
            stream_info = self.streaming_connections[stream_id]
            stream_info["messages_streamed"] += 1
            stream_info["last_activity"] = datetime.utcnow()
            
            return {
                "success": True,
                "message_id": message.message_id,
                "protocol": "real_time_streaming",
                "stream_id": stream_id,
                "stream_position": stream_info["messages_streamed"]
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def subscribe_to_topic(self, subscriber: AgentType, publisher: AgentType, 
                               data_format: DataFormat) -> bool:
        """Subscribe agent to a publication topic."""
        topic = f"{publisher.value}_{data_format.value}"
        
        if topic not in self.subscription_registry:
            self.subscription_registry[topic] = []
        
        if subscriber not in self.subscription_registry[topic]:
            self.subscription_registry[topic].append(subscriber)
            return True
        
        return False  # Already subscribed
    
    async def execute_workflow(self, workflow_id: str, trigger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a conservation workflow."""
        if workflow_id not in self.active_workflows:
            return {"success": False, "error": "Workflow not found"}
        
        workflow = self.active_workflows[workflow_id]
        workflow.status = "running"
        workflow.start_time = datetime.utcnow()
        workflow.execution_context = trigger_data
        
        try:
            # Get initial steps (those with no dependencies)
            initial_steps = [step for step in workflow.steps if not step.dependencies]
            
            execution_results = []
            for step in initial_steps:
                step.status = "running"
                step.start_time = datetime.utcnow()
                
                # Send workflow coordination message
                result = await self.send_message_via_protocol(
                    "field_validation",  # Use workflow coordination channel
                    {
                        "workflow_id": workflow_id,
                        "step_id": step.step_id,
                        "step_data": trigger_data
                    }
                )
                
                execution_results.append({
                    "step_id": step.step_id,
                    "result": result
                })
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "execution_id": f"{workflow_id}_{int(datetime.utcnow().timestamp())}",
                "initial_steps_triggered": len(initial_steps),
                "execution_results": execution_results
            }
            
        except Exception as e:
            workflow.status = "failed"
            return {"success": False, "error": str(e)}
    
    def get_communication_statistics(self) -> Dict[str, Any]:
        """Get comprehensive communication statistics."""
        channel_stats = {}
        for channel_id, channel in self.communication_channels.items():
            channel_stats[channel_id] = {
                "protocol": channel.protocol.value,
                "sender": channel.sender_agent.value,
                "receiver": channel.receiver_agent.value if channel.receiver_agent else "broadcast",
                "messages_sent": channel.messages_sent,
                "total_bytes": channel.total_bytes_transferred,
                "average_latency_ms": channel.average_latency_ms,
                "error_count": channel.error_count,
                "last_activity": channel.last_activity.isoformat() if channel.last_activity else None
            }
        
        workflow_stats = {}
        for workflow_id, workflow in self.active_workflows.items():
            workflow_stats[workflow_id] = {
                "status": workflow.status,
                "priority": workflow.priority,
                "steps_total": len(workflow.steps),
                "steps_completed": len([s for s in workflow.steps if s.status == "completed"]),
                "start_time": workflow.start_time.isoformat() if workflow.start_time else None,
                "current_step": workflow.current_step
            }
        
        return {
            "communication_channels": channel_stats,
            "active_workflows": workflow_stats,
            "subscription_registry": {
                topic: [agent.value for agent in subscribers]
                for topic, subscribers in self.subscription_registry.items()
            },
            "streaming_connections": len(self.streaming_connections),
            "request_response_queue_size": len(self.request_response_queue)
        }

def test_communication_channel_creation():
    """Test communication channel creation and configuration."""
    print("📡 Testing Communication Channel Creation...")
    
    try:
        # Test channel creation
        channel = CommunicationChannel(
            channel_id="test_channel_001",
            protocol=CommunicationProtocol.ASYNCHRONOUS_MESSAGING,
            sender_agent=AgentType.SPECIES_IDENTIFICATION,
            receiver_agent=AgentType.THREAT_DETECTION,
            data_format=DataFormat.SPECIES_DETECTION_FORMAT
        )
        
        # Test channel properties
        if channel.protocol == CommunicationProtocol.ASYNCHRONOUS_MESSAGING:
            print("✅ Channel protocol set correctly")
        else:
            print("❌ Channel protocol mismatch")
            return False
        
        # Test statistics initialization
        if channel.messages_sent == 0 and channel.average_latency_ms == 0.0:
            print("✅ Channel statistics initialized")
        else:
            print("❌ Channel statistics initialization failed")
            return False
        
        # Test statistics update
        channel.update_statistics(1024, 150.0, error=False)
        
        if channel.messages_sent == 1 and channel.total_bytes_transferred == 1024:
            print("✅ Channel statistics update successful")
        else:
            print("❌ Channel statistics update failed")
            return False
        
        # Test broadcast channel
        broadcast_channel = CommunicationChannel(
            channel_id="broadcast_test",
            protocol=CommunicationProtocol.BROADCAST_NOTIFICATION,
            sender_agent=AgentType.ALERT_MANAGEMENT,
            receiver_agent=None,  # Broadcast
            data_format=DataFormat.ALERT_FORMAT
        )
        
        if broadcast_channel.receiver_agent is None:
            print("✅ Broadcast channel created correctly")
        else:
            print("❌ Broadcast channel configuration failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Communication channel creation error: {e}")
        return False

def test_workflow_definition():
    """Test conservation workflow definition and management."""
    print("\n🔄 Testing Workflow Definition...")
    
    try:
        # Test workflow step creation
        step1 = WorkflowStep(
            step_id="test_step_1",
            step_name="Test Analysis Step",
            responsible_agent=AgentType.THREAT_DETECTION,
            input_requirements=[DataFormat.SATELLITE_DATA_FORMAT],
            output_format=DataFormat.THREAT_ANALYSIS_FORMAT,
            timeout_seconds=300
        )
        
        step2 = WorkflowStep(
            step_id="test_step_2", 
            step_name="Test Recommendation Step",
            responsible_agent=AgentType.CONSERVATION_RECOMMENDATION,
            input_requirements=[DataFormat.THREAT_ANALYSIS_FORMAT],
            output_format=DataFormat.CONSERVATION_RECOMMENDATION_FORMAT,
            dependencies=["test_step_1"],
            timeout_seconds=600
        )
        
        # Test workflow creation
        workflow = ConservationWorkflow(
            workflow_id="test_workflow",
            workflow_name="Test Conservation Workflow",
            description="Test workflow for validation",
            steps=[step1, step2],
            trigger_conditions={"test": True},
            priority=2
        )
        
        # Test workflow properties
        if len(workflow.steps) == 2:
            print("✅ Workflow steps added correctly")
        else:
            print("❌ Workflow steps mismatch")
            return False
        
        # Test dependency resolution
        workflow.status = "running"
        step1.status = "completed"  # Mark first step as completed
        
        next_steps = workflow.get_next_steps()
        
        if len(next_steps) == 1 and next_steps[0].step_id == "test_step_2":
            print("✅ Workflow dependency resolution successful")
        else:
            print("❌ Workflow dependency resolution failed")
            return False
        
        # Test workflow with no dependencies
        step3 = WorkflowStep(
            step_id="test_step_3",
            step_name="Independent Step",
            responsible_agent=AgentType.SATELLITE_MONITORING,
            input_requirements=[DataFormat.SATELLITE_DATA_FORMAT],
            output_format=DataFormat.SATELLITE_DATA_FORMAT
        )
        
        # Reset step1 status for parallel test
        step1.status = "pending"
        
        parallel_workflow = ConservationWorkflow(
            workflow_id="parallel_test",
            workflow_name="Parallel Test Workflow", 
            description="Test parallel execution",
            steps=[step1, step3],  # Both steps have no dependencies
            trigger_conditions={},
            priority=1
        )
        
        parallel_workflow.status = "running"
        parallel_next_steps = parallel_workflow.get_next_steps()
        
        if len(parallel_next_steps) == 2:
            print("✅ Parallel workflow execution supported")
        else:
            print("❌ Parallel workflow execution failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow definition error: {e}")
        return False

def test_data_transformation():
    """Test data transformation between agent formats."""
    print("\n🔄 Testing Data Transformation...")
    
    try:
        transformer = ConservationDataTransformer()
        
        # Test species detection transformation
        species_detection = SpeciesDetection(
            detection_id="test_species_001",
            species=MadagascarSpecies.LEMUR_CATTA,
            confidence=0.9,
            confidence_level=SpeciesConfidence.VERY_HIGH,
            timestamp=datetime.utcnow(),
            source="test_transform"
        )
        
        threat_input = transformer.species_detection_to_threat_input(species_detection)
        
        if "species_presence" in threat_input and "ecosystem_indicators" in threat_input:
            print("✅ Species to threat transformation successful")
        else:
            print("❌ Species to threat transformation failed")
            return False
        
        # Test threat detection transformation
        threat_detection = ThreatDetection(
            detection_id="test_threat_001",
            threat_type=ThreatType.DEFORESTATION,
            severity=0.8,
            severity_level=ThreatSeverity.HIGH,
            urgency=ThreatUrgency.URGENT,
            confidence=0.85,
            timestamp=datetime.utcnow()
        )
        
        alert_input = transformer.threat_detection_to_alert_input(threat_detection)
        
        if "threat_classification" in alert_input and "alert_metadata" in alert_input:
            print("✅ Threat to alert transformation successful")
        else:
            print("❌ Threat to alert transformation failed")
            return False
        
        # Test satellite data transformation
        satellite_data = {
            "metadata": {"resolution": "high", "timestamp": datetime.utcnow().isoformat()},
            "spectral_bands": ["red", "green", "blue", "nir"],
            "coverage_area": {"lat": -18.947, "lon": 48.458}
        }
        
        analysis_input = transformer.satellite_data_to_analysis_input(satellite_data)
        
        if "imagery_metadata" in analysis_input and "analysis_parameters" in analysis_input:
            print("✅ Satellite data transformation successful")
        else:
            print("❌ Satellite data transformation failed")
            return False
        
        # Test field data transformation
        field_data = {
            "observations": {"species_count": 15, "habitat_quality": "good"},
            "confidence": 0.85,
            "observer_type": "trained_biologist"
        }
        
        integration_format = transformer.field_data_to_integration_format(field_data)
        
        if "observation_data" in integration_format and "validation_context" in integration_format:
            print("✅ Field data transformation successful")
        else:
            print("❌ Field data transformation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Data transformation error: {e}")
        return False

async def test_protocol_manager():
    """Test communication protocol manager functionality."""
    print("\n📡 Testing Protocol Manager...")
    
    try:
        # Initialize ecosystem and protocol manager
        orchestrator = ConservationEcosystemOrchestrator("test_protocol_manager")
        await orchestrator.initialize_ecosystem()
        
        protocol_manager = CommunicationProtocolManager(orchestrator)
        
        # Test channel initialization
        if len(protocol_manager.communication_channels) >= 6:
            print(f"✅ Communication channels initialized: {len(protocol_manager.communication_channels)}")
        else:
            print("❌ Communication channels initialization failed")
            return False
        
        # Test workflow initialization
        if len(protocol_manager.active_workflows) >= 2:
            print(f"✅ Conservation workflows initialized: {len(protocol_manager.active_workflows)}")
        else:
            print("❌ Conservation workflows initialization failed")
            return False
        
        # Test message sending via protocol
        test_data = {
            "species": "lemur_catta",
            "confidence": 0.9,
            "location": {"lat": -18.947, "lon": 48.458}
        }
        
        result = await protocol_manager.send_message_via_protocol("species_to_threat", test_data)
        
        if result.get("success", False):
            print("✅ Message sending via protocol successful")
        else:
            print(f"❌ Message sending via protocol failed: {result.get('error', 'Unknown error')}")
            return False
        
        # Test subscription
        subscription_success = await protocol_manager.subscribe_to_topic(
            AgentType.THREAT_DETECTION,
            AgentType.SATELLITE_MONITORING,
            DataFormat.SATELLITE_DATA_FORMAT
        )
        
        if subscription_success:
            print("✅ Topic subscription successful")
        else:
            print("❌ Topic subscription failed")
            return False
        
        # Test workflow execution
        workflow_result = await protocol_manager.execute_workflow(
            "routine_monitoring",
            {"trigger": "test_execution", "priority": 1}
        )
        
        if workflow_result.get("success", False):
            print("✅ Workflow execution successful")
        else:
            print(f"❌ Workflow execution failed: {workflow_result.get('error', 'Unknown error')}")
            return False
        
        # Test statistics
        stats = protocol_manager.get_communication_statistics()
        
        if "communication_channels" in stats and "active_workflows" in stats:
            print("✅ Communication statistics generated")
        else:
            print("❌ Communication statistics generation failed")
            return False
        
        await orchestrator.shutdown_ecosystem()
        return True
        
    except Exception as e:
        print(f"❌ Protocol manager error: {e}")
        return False

async def test_protocol_handlers():
    """Test different communication protocol handlers."""
    print("\n🔗 Testing Protocol Handlers...")
    
    try:
        # Initialize system
        orchestrator = ConservationEcosystemOrchestrator("test_protocols")
        await orchestrator.initialize_ecosystem()
        
        protocol_manager = CommunicationProtocolManager(orchestrator)
        
        # Test synchronous request-response
        sync_channel = protocol_manager.communication_channels["threat_to_alert"]
        test_message = AgentMessage(
            message_id="sync_test",
            message_type=MessageType.ANALYSIS_REQUEST,
            sender_agent=AgentType.THREAT_DETECTION,
            recipient_agent=AgentType.ALERT_MANAGEMENT,
            payload={"test": "sync_data"},
            requires_response=True
        )
        
        sync_result = await protocol_manager._handle_sync_request_response(sync_channel, test_message)
        
        if sync_result.get("success", False) and sync_result.get("response_expected", False):
            print("✅ Synchronous request-response protocol working")
        else:
            print("❌ Synchronous request-response protocol failed")
            return False
        
        # Test asynchronous messaging
        async_channel = protocol_manager.communication_channels["species_to_threat"]
        async_message = AgentMessage(
            message_id="async_test",
            message_type=MessageType.DATA_FEED,
            sender_agent=AgentType.SPECIES_IDENTIFICATION,
            recipient_agent=AgentType.THREAT_DETECTION,
            payload={"test": "async_data"}
        )
        
        async_result = await protocol_manager._handle_async_messaging(async_channel, async_message)
        
        if async_result.get("success", False) and async_result.get("delivery_mode") == "queued":
            print("✅ Asynchronous messaging protocol working")
        else:
            print("❌ Asynchronous messaging protocol failed")
            return False
        
        # Test publish-subscribe
        pub_sub_channel = protocol_manager.communication_channels["satellite_broadcast"]
        
        # Add subscribers
        await protocol_manager.subscribe_to_topic(
            AgentType.THREAT_DETECTION,
            AgentType.SATELLITE_MONITORING,
            DataFormat.SATELLITE_DATA_FORMAT
        )
        await protocol_manager.subscribe_to_topic(
            AgentType.SPECIES_IDENTIFICATION,
            AgentType.SATELLITE_MONITORING,
            DataFormat.SATELLITE_DATA_FORMAT
        )
        
        pub_message = AgentMessage(
            message_id="pub_test",
            message_type=MessageType.DATA_FEED,
            sender_agent=AgentType.SATELLITE_MONITORING,
            payload={"test": "published_data"}
        )
        
        pub_result = await protocol_manager._handle_pub_sub(pub_sub_channel, pub_message)
        
        if (pub_result.get("success", False) and 
            pub_result.get("subscribers_notified", 0) >= 2):
            print("✅ Publish-subscribe protocol working")
        else:
            print("❌ Publish-subscribe protocol failed")
            return False
        
        # Test broadcast notification
        broadcast_channel = protocol_manager.communication_channels["conservation_alerts"]
        broadcast_message = AgentMessage(
            message_id="broadcast_test",
            message_type=MessageType.ALERT_NOTIFICATION,
            sender_agent=AgentType.CONSERVATION_RECOMMENDATION,
            payload={"test": "broadcast_alert"}
        )
        
        broadcast_result = await protocol_manager._handle_broadcast(broadcast_channel, broadcast_message)
        
        if (broadcast_result.get("success", False) and 
            broadcast_result.get("recipients_notified", 0) >= 5):  # All agents except sender
            print("✅ Broadcast notification protocol working")
        else:
            print("❌ Broadcast notification protocol failed")
            return False
        
        await orchestrator.shutdown_ecosystem()
        return True
        
    except Exception as e:
        print(f"❌ Protocol handlers error: {e}")
        return False

async def main():
    """Run Step 2 tests."""
    print("📡 STEP 2: Agent Communication Protocols")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Communication channel creation
    if test_communication_channel_creation():
        tests_passed += 1
    
    # Test 2: Workflow definition
    if test_workflow_definition():
        tests_passed += 1
    
    # Test 3: Data transformation
    if test_data_transformation():
        tests_passed += 1
    
    # Test 4: Protocol manager
    if await test_protocol_manager():
        tests_passed += 1
    
    # Test 5: Protocol handlers
    if await test_protocol_handlers():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Step 2 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Step 2 PASSED - Agent Communication Protocols Complete")
        print("\n🎯 Next: Implement Unified Conservation Dashboard")
        print("\n🌟 Achievements:")
        print("   • ✅ Multi-protocol communication system")
        print("   • ✅ Conservation workflow orchestration")
        print("   • ✅ Cross-agent data transformation")
        print("   • ✅ Publish-subscribe messaging")
        print("   • ✅ Real-time coordination protocols")
        return True
    else:
        print("❌ Step 2 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    asyncio.run(main())
