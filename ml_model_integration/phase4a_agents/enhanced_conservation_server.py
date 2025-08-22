"""
Enhanced Conservation Server with Memory Integration
=================================================
Integrates LangChain memory system with our simple conservation server.
Adds persistent memory for species, threats, sites, and conservation activities.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Import our memory system
from memory_system.conservation_memory import ConservationMemorySystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConservationEvent(BaseModel):
    """Enhanced conservation event model."""
    site_id: str
    event_type: str
    timestamp: Optional[str] = None
    confidence: float = 0.0
    metadata: Dict[str, Any] = {}

class MemoryQuery(BaseModel):
    """Model for memory query requests."""
    site_id: Optional[str] = None
    species_id: Optional[str] = None
    threat_type: Optional[str] = None
    intervention_type: Optional[str] = None
    time_range_days: Optional[int] = None

class HealthResponse(BaseModel):
    """Enhanced health check response with memory status."""
    status: str
    server_name: str
    uptime_seconds: float
    timestamp: str
    memory_status: Dict[str, Any]

class EnhancedConservationServer:
    """Enhanced conservation server with memory integration."""
    
    def __init__(self, server_name: str = "enhanced-conservation-server"):
        self.server_name = server_name
        self.start_time = datetime.utcnow()
        self.session_id = str(uuid.uuid4())[:8]
        
        # Initialize memory system
        self.memory_system = ConservationMemorySystem(
            agent_id=f"server_{self.session_id}",
            memory_dir="memory_data"
        )
        
        # Initialize FastAPI app
        self.app = FastAPI(title=server_name)
        self._setup_routes()
        
        logger.info(f"Initialized {server_name} with memory integration (session: {self.session_id})")
    
    def _setup_routes(self):
        """Setup enhanced HTTP routes with memory integration."""
        
        @self.app.get("/health", response_model=HealthResponse)
        async def health_check():
            """Enhanced health check with memory status."""
            uptime = (datetime.utcnow() - self.start_time).total_seconds()
            memory_stats = self.memory_system.get_memory_statistics()
            
            return HealthResponse(
                status="healthy",
                server_name=self.server_name,
                uptime_seconds=uptime,
                timestamp=datetime.utcnow().isoformat(),
                memory_status=memory_stats
            )
        
        @self.app.post("/conservation/event")
        async def store_conservation_event(event: ConservationEvent):
            """Store conservation event with memory integration."""
            try:
                # Add timestamp if not provided
                if not event.timestamp:
                    event.timestamp = datetime.utcnow().isoformat()
                
                # Validate required fields
                if not event.site_id or not event.event_type:
                    raise HTTPException(status_code=400, detail="site_id and event_type required")
                
                # Convert to dict for memory system
                event_dict = event.model_dump()
                
                # Store in memory system
                success = await self.memory_system.store_conservation_event(event_dict)
                
                if success:
                    logger.info(f"Stored {event.event_type} event for site {event.site_id} in memory")
                    
                    return {
                        "status": "success",
                        "message": f"Stored {event.event_type} event for site {event.site_id}",
                        "timestamp": event.timestamp,
                        "session_id": self.session_id,
                        "memory_updated": True
                    }
                else:
                    raise HTTPException(status_code=500, detail="Failed to store event in memory")
                
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error storing conservation event: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/conservation/memory/query")
        async def query_conservation_memory(query: MemoryQuery):
            """Query conservation memory for relevant context."""
            try:
                # Convert query to dict
                query_dict = {k: v for k, v in query.model_dump().items() if v is not None}
                
                # Get context from memory system
                context = await self.memory_system.recall_conservation_context(query_dict)
                
                return {
                    "status": "success",
                    "query": query_dict,
                    "context": context,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
            except Exception as e:
                logger.error(f"Error querying conservation memory: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/conservation/memory/species/{species_id}")
        async def get_species_memory(species_id: str):
            """Get detailed memory for a specific species."""
            try:
                context = await self.memory_system.recall_conservation_context({"species_id": species_id})
                
                if species_id in context["relevant_species"]:
                    species_data = context["relevant_species"][species_id]
                    
                    # Calculate summary statistics
                    detections = species_data.get("detections", [])
                    summary = {
                        "species_id": species_id,
                        "total_detections": len(detections),
                        "first_observed": species_data.get("first_observed"),
                        "last_observed": species_data.get("last_observed"),
                        "habitats": list(species_data.get("habitat_preferences", {}).keys()),
                        "sites_observed": list(set(d.get("site_id") for d in detections)),
                        "behaviors_observed": list(set(b.get("behavior") for b in species_data.get("behavioral_observations", []))),
                        "data": species_data
                    }
                    
                    return {
                        "status": "success",
                        "species_summary": summary,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                else:
                    return {
                        "status": "not_found",
                        "message": f"No memory data found for species: {species_id}",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                
            except Exception as e:
                logger.error(f"Error retrieving species memory: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/conservation/memory/site/{site_id}")
        async def get_site_memory(site_id: str):
            """Get detailed memory for a specific site."""
            try:
                context = await self.memory_system.recall_conservation_context({"site_id": site_id})
                
                if site_id in context["relevant_sites"]:
                    site_data = context["relevant_sites"][site_id]
                    
                    # Calculate summary statistics
                    summary = {
                        "site_id": site_id,
                        "total_events": site_data.get("total_events", 0),
                        "first_activity": site_data.get("first_activity"),
                        "last_activity": site_data.get("last_activity"),
                        "species_count": len(site_data.get("species_observed", [])),
                        "threat_types": len(site_data.get("threats_detected", [])),
                        "intervention_types": len(site_data.get("interventions_conducted", [])),
                        "research_activities": len(site_data.get("research_activities", [])),
                        "data": site_data
                    }
                    
                    return {
                        "status": "success",
                        "site_summary": summary,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                else:
                    return {
                        "status": "not_found", 
                        "message": f"No memory data found for site: {site_id}",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                
            except Exception as e:
                logger.error(f"Error retrieving site memory: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/conservation/memory/statistics")
        async def get_memory_statistics():
            """Get comprehensive memory system statistics."""
            try:
                stats = self.memory_system.get_memory_statistics()
                
                # Add server-specific information
                enhanced_stats = {
                    "server_info": {
                        "server_name": self.server_name,
                        "session_id": self.session_id,
                        "uptime_seconds": (datetime.utcnow() - self.start_time).total_seconds()
                    },
                    "memory_statistics": stats,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                return {
                    "status": "success",
                    "statistics": enhanced_stats
                }
                
            except Exception as e:
                logger.error(f"Error retrieving memory statistics: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/conservation/memory/backup")
        async def backup_memory():
            """Create a backup of the current memory state."""
            try:
                await self.memory_system.persist_memory()
                
                return {
                    "status": "success",
                    "message": "Memory backup completed successfully",
                    "timestamp": datetime.utcnow().isoformat(),
                    "session_id": self.session_id
                }
                
            except Exception as e:
                logger.error(f"Error backing up memory: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def start_server(self, host: str = "localhost", port: int = 8000):
        """Start the enhanced conservation server."""
        logger.info(f"Starting Enhanced Conservation Server with Memory on {host}:{port}")
        config = uvicorn.Config(self.app, host=host, port=port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

# Test data for Madagascar with enhanced metadata
def create_enhanced_madagascar_events():
    """Create enhanced test events for Madagascar conservation sites."""
    return [
        ConservationEvent(
            site_id="centre_valbio",
            event_type="species_detection",
            confidence=0.94,
            metadata={
                "species": "lemur_catta",
                "individual_count": 8,
                "behavior": "foraging",
                "habitat": "gallery_forest",
                "researcher": "Dr. Patricia Wright",
                "coordinates": {"lat": -21.289, "lon": 47.958},
                "observation_quality": "excellent",
                "weather_conditions": "clear_morning",
                "group_composition": "mixed_age",
                "feeding_behavior": "fruit_foraging"
            }
        ),
        ConservationEvent(
            site_id="maromizaha",
            event_type="species_detection",
            confidence=0.91,
            metadata={
                "species": "indri_indri",
                "individual_count": 4,
                "behavior": "territorial_calling",
                "habitat": "primary_rainforest",
                "audio_duration_seconds": 240,
                "coordinates": {"lat": -18.947, "lon": 48.458},
                "call_type": "territorial_song",
                "family_group": True,
                "canopy_height_meters": 25
            }
        ),
        ConservationEvent(
            site_id="centre_valbio",
            event_type="threat_detection",
            confidence=0.82,
            metadata={
                "threat_type": "habitat_fragmentation",
                "severity": "moderate",
                "area_affected_hectares": 5.7,
                "cause": "agricultural_expansion",
                "response_urgency": "high",
                "mitigation_required": True,
                "affected_species": ["lemur_catta", "microcebus_rufus"],
                "human_activity_intensity": "moderate"
            }
        ),
        ConservationEvent(
            site_id="maromizaha",
            event_type="conservation_intervention",
            confidence=1.0,
            metadata={
                "intervention_type": "community_education",
                "participants": 89,
                "duration_days": 7,
                "topics": ["lemur_conservation", "sustainable_agriculture", "ecotourism"],
                "effectiveness_score": 0.93,
                "coordinator": "Madagascar_National_Parks",
                "local_leaders_involved": True,
                "follow_up_planned": True
            }
        ),
        ConservationEvent(
            site_id="centre_valbio",
            event_type="research_activity",
            confidence=1.0,
            metadata={
                "activity_type": "long_term_monitoring",
                "research_team": "Duke_Lemur_Center",
                "equipment_count": 15,
                "deployment_duration_months": 12,
                "target_species": ["lemur_catta", "propithecus_diadema", "varecia_variegata"],
                "methodology": "camera_trap_and_behavioral_observation",
                "data_collection_frequency": "daily"
            }
        )
    ]

if __name__ == "__main__":
    # Create and run the enhanced server
    server = EnhancedConservationServer("madagascar-conservation-memory-server")
    
    print("🧠 Enhanced Conservation Server with Memory Integration")
    print("=" * 55)
    print("🌐 Server: http://localhost:8000")
    print("📊 Health: http://localhost:8000/health")
    print("🧠 Memory Stats: http://localhost:8000/conservation/memory/statistics")
    print("🏝️  Madagascar conservation events with persistent memory!")
    print()
    
    asyncio.run(server.start_server(host="localhost", port=8000))
