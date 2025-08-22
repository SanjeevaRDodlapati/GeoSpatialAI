"""
Simple Conservation MCP Server
=============================
Minimal complexity MCP implementation for conservation agents.
Built for reliability and ease of understanding.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import uuid

# Simple HTTP server instead of complex MCP protocol initially
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Configure simple logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConservationEvent(BaseModel):
    """Simple data model for conservation events."""
    site_id: str
    event_type: str
    timestamp: Optional[str] = None
    confidence: float = 0.0
    metadata: Dict[str, Any] = {}

class HealthResponse(BaseModel):
    """Simple health check response."""
    status: str
    server_name: str
    uptime_seconds: float
    timestamp: str

class SimpleConservationServer:
    """Simple conservation server with minimal complexity."""
    
    def __init__(self, server_name: str = "simple-conservation-server"):
        self.server_name = server_name
        self.start_time = datetime.utcnow()
        self.session_id = str(uuid.uuid4())[:8]  # Short session ID
        
        # Simple in-memory storage (no complex databases initially)
        self.events_store = []
        self.active_sites = set()
        
        # Create FastAPI app
        self.app = FastAPI(title=server_name)
        self._setup_routes()
        
        logger.info(f"Initialized {server_name} with session {self.session_id}")
    
    def _setup_routes(self):
        """Setup simple HTTP routes."""
        
        @self.app.get("/health", response_model=HealthResponse)
        async def health_check():
            """Simple health check endpoint."""
            uptime = (datetime.utcnow() - self.start_time).total_seconds()
            return HealthResponse(
                status="healthy",
                server_name=self.server_name,
                uptime_seconds=uptime,
                timestamp=datetime.utcnow().isoformat()
            )
        
        @self.app.post("/conservation/event")
        async def store_event(event: ConservationEvent):
            """Store a conservation event."""
            try:
                # Add timestamp if not provided
                if not event.timestamp:
                    event.timestamp = datetime.utcnow().isoformat()
                
                # Simple validation
                if not event.site_id or not event.event_type:
                    raise HTTPException(status_code=400, detail="site_id and event_type required")
                
                # Store event
                event_dict = event.dict()
                self.events_store.append(event_dict)
                self.active_sites.add(event.site_id)
                
                logger.info(f"Stored event: {event.event_type} at {event.site_id}")
                
                return {
                    "status": "success",
                    "event_id": len(self.events_store) - 1,
                    "message": f"Stored {event.event_type} event for site {event.site_id}"
                }
                
            except Exception as e:
                logger.error(f"Error storing event: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/conservation/events/{site_id}")
        async def get_events_for_site(site_id: str):
            """Get events for a specific site."""
            try:
                site_events = [
                    event for event in self.events_store 
                    if event.get("site_id") == site_id
                ]
                
                return {
                    "site_id": site_id,
                    "event_count": len(site_events),
                    "events": site_events
                }
                
            except Exception as e:
                logger.error(f"Error retrieving events for site {site_id}: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/conservation/stats")
        async def get_conservation_stats():
            """Get simple conservation statistics."""
            try:
                event_types = {}
                for event in self.events_store:
                    event_type = event.get("event_type", "unknown")
                    event_types[event_type] = event_types.get(event_type, 0) + 1
                
                return {
                    "total_events": len(self.events_store),
                    "active_sites": len(self.active_sites),
                    "event_types": event_types,
                    "sites": list(self.active_sites)
                }
                
            except Exception as e:
                logger.error(f"Error getting stats: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def start_server(self, host: str = "localhost", port: int = 8000):
        """Start the simple conservation server."""
        logger.info(f"Starting {self.server_name} on {host}:{port}")
        config = uvicorn.Config(self.app, host=host, port=port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

# Simple test function
def create_test_events():
    """Create test events for Madagascar conservation sites."""
    return [
        ConservationEvent(
            site_id="centre_valbio",
            event_type="species_detection",
            confidence=0.85,
            metadata={
                "species": "lemur_catta",
                "individual_count": 3,
                "behavior": "foraging"
            }
        ),
        ConservationEvent(
            site_id="maromizaha",
            event_type="threat_detection",
            confidence=0.72,
            metadata={
                "threat_type": "deforestation",
                "severity": "medium",
                "area_affected_hectares": 2.5
            }
        ),
        ConservationEvent(
            site_id="centre_valbio",
            event_type="conservation_intervention",
            confidence=1.0,
            metadata={
                "intervention_type": "habitat_restoration",
                "area_restored_hectares": 5.0,
                "species_benefited": ["lemur_catta", "propithecus_diadema"]
            }
        )
    ]

if __name__ == "__main__":
    # Simple direct execution for testing
    server = SimpleConservationServer("madagascar-conservation-server")
    
    # Run with basic configuration
    asyncio.run(server.start_server(host="localhost", port=8000))
