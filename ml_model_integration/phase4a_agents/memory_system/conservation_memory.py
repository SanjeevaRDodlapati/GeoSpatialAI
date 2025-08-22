"""
Conservation Memory System
=========================
LangChain-based memory management for conservation AI agents.
Stores and retrieves conservation events, species data, and site information.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryBufferMemory
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.memory.chat_memory import BaseChatMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConservationMemorySystem:
    """
    Memory system for conservation AI agents.
    Manages different types of conservation-related memories.
    """
    
    def __init__(self, agent_id: str, memory_dir: str = "memory_data"):
        self.agent_id = agent_id
        self.memory_dir = memory_dir
        self.memory_file = os.path.join(memory_dir, f"{agent_id}_memory.json")
        
        # Create memory directory if it doesn't exist
        os.makedirs(memory_dir, exist_ok=True)
        
        # Initialize LangChain memory components
        self.conversation_memory = ConversationBufferWindowMemory(
            k=20,  # Keep last 20 conversations
            return_messages=True
        )
        
        # Conservation-specific memory stores
        self.species_memory = {}      # Species observations and data
        self.threat_memory = {}       # Threat detections and responses
        self.site_memory = {}         # Site-specific information
        self.intervention_memory = {} # Conservation interventions
        self.research_memory = {}     # Research activities and findings
        
        # Load existing memory if available
        self.load_persistent_memory()
        
        logger.info(f"Initialized ConservationMemorySystem for agent: {agent_id}")
    
    async def store_conservation_event(self, event: Dict[str, Any]) -> bool:
        """
        Store a conservation event in the appropriate memory store.
        
        Args:
            event: Conservation event data
            
        Returns:
            bool: Success status
        """
        try:
            event_type = event.get("event_type", "unknown")
            site_id = event.get("site_id", "unknown_site")
            timestamp = event.get("timestamp", datetime.utcnow().isoformat())
            
            # Add to conversation memory as a structured message
            human_msg = f"Conservation event: {event_type} at {site_id}"
            ai_msg = f"Processed {event_type} event with confidence {event.get('confidence', 0.0)}"
            
            self.conversation_memory.save_context(
                {"input": human_msg},
                {"output": ai_msg}
            )
            
            # Store in specific memory based on event type
            if event_type == "species_detection":
                await self._store_species_event(event, timestamp)
            elif event_type == "threat_detection":
                await self._store_threat_event(event, timestamp)
            elif event_type == "conservation_intervention":
                await self._store_intervention_event(event, timestamp)
            elif event_type == "research_activity":
                await self._store_research_event(event, timestamp)
            
            # Always update site memory
            await self._update_site_memory(site_id, event, timestamp)
            
            # Persist memory to disk
            await self.persist_memory()
            
            logger.info(f"Stored {event_type} event for site {site_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing conservation event: {e}")
            return False
    
    async def _store_species_event(self, event: Dict[str, Any], timestamp: str):
        """Store species-specific event data."""
        metadata = event.get("metadata", {})
        species_id = metadata.get("species", "unknown_species")
        
        if species_id not in self.species_memory:
            self.species_memory[species_id] = {
                "detections": [],
                "population_estimates": [],
                "habitat_preferences": {},
                "behavioral_observations": [],
                "threat_associations": [],
                "first_observed": timestamp,
                "last_observed": timestamp
            }
        
        # Add detection data
        detection_data = {
            "timestamp": timestamp,
            "site_id": event.get("site_id"),
            "confidence": event.get("confidence", 0.0),
            "individual_count": metadata.get("individual_count", 1),
            "behavior": metadata.get("behavior", "unknown"),
            "habitat_type": metadata.get("habitat", "unknown"),
            "coordinates": metadata.get("coordinates", {}),
            "researcher": metadata.get("researcher", "unknown"),
            "observation_quality": metadata.get("observation_quality", "standard")
        }
        
        self.species_memory[species_id]["detections"].append(detection_data)
        self.species_memory[species_id]["last_observed"] = timestamp
        
        # Update behavioral observations
        behavior = metadata.get("behavior")
        if behavior and behavior != "unknown":
            self.species_memory[species_id]["behavioral_observations"].append({
                "behavior": behavior,
                "timestamp": timestamp,
                "site_id": event.get("site_id"),
                "context": metadata.get("behavior_context", "")
            })
        
        # Update habitat preferences
        habitat = metadata.get("habitat")
        if habitat and habitat != "unknown":
            if habitat not in self.species_memory[species_id]["habitat_preferences"]:
                self.species_memory[species_id]["habitat_preferences"][habitat] = 0
            self.species_memory[species_id]["habitat_preferences"][habitat] += 1
    
    async def _store_threat_event(self, event: Dict[str, Any], timestamp: str):
        """Store threat-specific event data."""
        metadata = event.get("metadata", {})
        threat_type = metadata.get("threat_type", "unknown_threat")
        
        if threat_type not in self.threat_memory:
            self.threat_memory[threat_type] = {
                "incidents": [],
                "severity_trends": [],
                "response_effectiveness": [],
                "affected_species": set(),
                "affected_sites": set(),
                "first_detected": timestamp,
                "last_detected": timestamp
            }
        
        # Add incident data
        incident_data = {
            "timestamp": timestamp,
            "site_id": event.get("site_id"),
            "confidence": event.get("confidence", 0.0),
            "severity": metadata.get("severity", "unknown"),
            "area_affected": metadata.get("area_affected_hectares", 0),
            "cause": metadata.get("cause", "unknown"),
            "response_urgency": metadata.get("response_urgency", "medium"),
            "coordinates": metadata.get("coordinates", {})
        }
        
        self.threat_memory[threat_type]["incidents"].append(incident_data)
        self.threat_memory[threat_type]["last_detected"] = timestamp
        self.threat_memory[threat_type]["affected_sites"].add(event.get("site_id"))
        
        # Convert set to list for JSON serialization
        self.threat_memory[threat_type]["affected_sites"] = list(self.threat_memory[threat_type]["affected_sites"])
    
    async def _store_intervention_event(self, event: Dict[str, Any], timestamp: str):
        """Store conservation intervention data."""
        metadata = event.get("metadata", {})
        intervention_type = metadata.get("intervention_type", "unknown_intervention")
        
        if intervention_type not in self.intervention_memory:
            self.intervention_memory[intervention_type] = {
                "activities": [],
                "effectiveness_scores": [],
                "participant_counts": [],
                "duration_analysis": [],
                "site_coverage": set()
            }
        
        # Add intervention data
        activity_data = {
            "timestamp": timestamp,
            "site_id": event.get("site_id"),
            "confidence": event.get("confidence", 0.0),
            "participants": metadata.get("participants", 0),
            "duration_days": metadata.get("duration_days", 0),
            "effectiveness_score": metadata.get("effectiveness_score", 0.0),
            "topics": metadata.get("topics", []),
            "target_species": metadata.get("target_species", []),
            "coordinator": metadata.get("coordinator", "unknown")
        }
        
        self.intervention_memory[intervention_type]["activities"].append(activity_data)
        self.intervention_memory[intervention_type]["site_coverage"].add(event.get("site_id"))
        
        # Track effectiveness
        effectiveness = metadata.get("effectiveness_score", 0.0)
        if effectiveness > 0:
            self.intervention_memory[intervention_type]["effectiveness_scores"].append(effectiveness)
        
        # Convert set to list for JSON serialization
        self.intervention_memory[intervention_type]["site_coverage"] = list(self.intervention_memory[intervention_type]["site_coverage"])
    
    async def _store_research_event(self, event: Dict[str, Any], timestamp: str):
        """Store research activity data."""
        metadata = event.get("metadata", {})
        activity_type = metadata.get("activity_type", "unknown_research")
        
        if activity_type not in self.research_memory:
            self.research_memory[activity_type] = {
                "activities": [],
                "research_teams": set(),
                "target_species": set(),
                "equipment_deployments": [],
                "duration_tracking": []
            }
        
        # Add research data
        research_data = {
            "timestamp": timestamp,
            "site_id": event.get("site_id"),
            "confidence": event.get("confidence", 0.0),
            "research_team": metadata.get("research_team", "unknown"),
            "equipment_count": metadata.get("equipment_count", 0),
            "deployment_duration_months": metadata.get("deployment_duration_months", 0),
            "target_species": metadata.get("target_species", []),
            "methodology": metadata.get("methodology", "unknown")
        }
        
        self.research_memory[activity_type]["activities"].append(research_data)
        self.research_memory[activity_type]["research_teams"].add(metadata.get("research_team", "unknown"))
        
        # Track target species
        for species in metadata.get("target_species", []):
            self.research_memory[activity_type]["target_species"].add(species)
        
        # Convert sets to lists for JSON serialization
        self.research_memory[activity_type]["research_teams"] = list(self.research_memory[activity_type]["research_teams"])
        self.research_memory[activity_type]["target_species"] = list(self.research_memory[activity_type]["target_species"])
    
    async def _update_site_memory(self, site_id: str, event: Dict[str, Any], timestamp: str):
        """Update site-specific memory."""
        if site_id not in self.site_memory:
            self.site_memory[site_id] = {
                "events": [],
                "species_observed": set(),
                "threats_detected": set(),
                "interventions_conducted": set(),
                "research_activities": set(),
                "first_activity": timestamp,
                "last_activity": timestamp,
                "total_events": 0
            }
        
        # Add event summary
        event_summary = {
            "timestamp": timestamp,
            "type": event.get("event_type"),
            "confidence": event.get("confidence", 0.0),
            "summary": f"{event.get('event_type')} event"
        }
        
        self.site_memory[site_id]["events"].append(event_summary)
        self.site_memory[site_id]["last_activity"] = timestamp
        self.site_memory[site_id]["total_events"] += 1
        
        # Update category-specific tracking
        event_type = event.get("event_type")
        metadata = event.get("metadata", {})
        
        if event_type == "species_detection":
            species = metadata.get("species")
            if species:
                self.site_memory[site_id]["species_observed"].add(species)
        elif event_type == "threat_detection":
            threat = metadata.get("threat_type")
            if threat:
                self.site_memory[site_id]["threats_detected"].add(threat)
        elif event_type == "conservation_intervention":
            intervention = metadata.get("intervention_type")
            if intervention:
                self.site_memory[site_id]["interventions_conducted"].add(intervention)
        elif event_type == "research_activity":
            activity = metadata.get("activity_type")
            if activity:
                self.site_memory[site_id]["research_activities"].add(activity)
        
        # Convert sets to lists for JSON serialization
        for key in ["species_observed", "threats_detected", "interventions_conducted", "research_activities"]:
            if isinstance(self.site_memory[site_id][key], set):
                self.site_memory[site_id][key] = list(self.site_memory[site_id][key])
    
    async def recall_conservation_context(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve relevant conservation context based on query.
        
        Args:
            query: Query parameters (site_id, species_id, threat_type, etc.)
            
        Returns:
            dict: Relevant conservation context
        """
        context = {
            "conversation_history": self.conversation_memory.buffer,
            "relevant_species": {},
            "relevant_threats": {},
            "relevant_sites": {},
            "relevant_interventions": {},
            "relevant_research": {},
            "summary_statistics": {}
        }
        
        try:
            # Get specific context based on query
            if "species_id" in query:
                species_id = query["species_id"]
                if species_id in self.species_memory:
                    context["relevant_species"][species_id] = self.species_memory[species_id]
            
            if "site_id" in query:
                site_id = query["site_id"]
                if site_id in self.site_memory:
                    context["relevant_sites"][site_id] = self.site_memory[site_id]
            
            if "threat_type" in query:
                threat_type = query["threat_type"]
                if threat_type in self.threat_memory:
                    context["relevant_threats"][threat_type] = self.threat_memory[threat_type]
            
            # Generate summary statistics
            context["summary_statistics"] = {
                "total_species_tracked": len(self.species_memory),
                "total_threats_monitored": len(self.threat_memory),
                "total_sites_active": len(self.site_memory),
                "total_interventions": len(self.intervention_memory),
                "total_research_activities": len(self.research_memory),
                "memory_last_updated": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Retrieved conservation context for query: {query}")
            return context
            
        except Exception as e:
            logger.error(f"Error retrieving conservation context: {e}")
            return context
    
    async def persist_memory(self):
        """Persist memory to disk for recovery."""
        try:
            memory_data = {
                "agent_id": self.agent_id,
                "last_updated": datetime.utcnow().isoformat(),
                "species_memory": self.species_memory,
                "threat_memory": self.threat_memory,
                "site_memory": self.site_memory,
                "intervention_memory": self.intervention_memory,
                "research_memory": self.research_memory,
                "conversation_count": len(self.conversation_memory.buffer) if hasattr(self.conversation_memory, 'buffer') else 0
            }
            
            with open(self.memory_file, "w") as f:
                json.dump(memory_data, f, indent=2, default=str)
            
            logger.info(f"Memory persisted to {self.memory_file}")
            
        except Exception as e:
            logger.error(f"Error persisting memory: {e}")
    
    def load_persistent_memory(self):
        """Load memory from persistent storage."""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, "r") as f:
                    memory_data = json.load(f)
                
                self.species_memory = memory_data.get("species_memory", {})
                self.threat_memory = memory_data.get("threat_memory", {})
                self.site_memory = memory_data.get("site_memory", {})
                self.intervention_memory = memory_data.get("intervention_memory", {})
                self.research_memory = memory_data.get("research_memory", {})
                
                logger.info(f"Loaded persistent memory from {self.memory_file}")
            else:
                logger.info("No persistent memory found, starting with empty memory")
                
        except Exception as e:
            logger.error(f"Error loading persistent memory: {e}")
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics."""
        stats = {
            "agent_id": self.agent_id,
            "memory_categories": {
                "species": len(self.species_memory),
                "threats": len(self.threat_memory),
                "sites": len(self.site_memory),
                "interventions": len(self.intervention_memory),
                "research": len(self.research_memory)
            },
            "total_events": sum(len(site_data.get("events", [])) for site_data in self.site_memory.values()),
            "conversation_history_length": len(self.conversation_memory.buffer) if hasattr(self.conversation_memory, 'buffer') else 0,
            "memory_file_exists": os.path.exists(self.memory_file),
            "last_updated": datetime.utcnow().isoformat()
        }
        
        return stats
