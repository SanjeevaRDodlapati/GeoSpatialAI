"""
Simple Conservation Server Tests
===============================
Direct testing approach without complex async fixtures.
"""

import pytest
import asyncio
import httpx
import time
import subprocess
import signal
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

@pytest.mark.asyncio
async def test_direct_server_health():
    """Test server health check by starting server directly."""
    from mcp_foundation.simple_conservation_server import SimpleConservationServer
    
    # Create server
    server = SimpleConservationServer("direct-test-server")
    
    # Start server task
    server_task = asyncio.create_task(
        server.start_server(host="localhost", port=8002)
    )
    
    # Wait for server to start
    await asyncio.sleep(1)
    
    try:
        # Test health check
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8002/health")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["status"] == "healthy"
            assert "uptime_seconds" in data
            assert data["server_name"] == "direct-test-server"
            
            print(f"✅ Direct health check passed: {data['status']}")
            
    finally:
        # Cleanup
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass

@pytest.mark.asyncio
async def test_direct_conservation_event():
    """Test storing and retrieving conservation events."""
    from mcp_foundation.simple_conservation_server import SimpleConservationServer
    
    # Create server
    server = SimpleConservationServer("event-test-server")
    
    # Start server task
    server_task = asyncio.create_task(
        server.start_server(host="localhost", port=8003)
    )
    
    # Wait for server to start
    await asyncio.sleep(1)
    
    try:
        async with httpx.AsyncClient() as client:
            # Store a Madagascar conservation event
            test_event = {
                "site_id": "centre_valbio",
                "event_type": "species_detection",
                "confidence": 0.92,
                "metadata": {
                    "species": "lemur_catta",
                    "individual_count": 5,
                    "researcher": "Dr. Patricia Wright"
                }
            }
            
            # Store event
            response = await client.post(
                "http://localhost:8003/conservation/event",
                json=test_event
            )
            
            assert response.status_code == 200
            store_result = response.json()
            assert store_result["status"] == "success"
            
            # Retrieve events for site
            response = await client.get("http://localhost:8003/conservation/events/centre_valbio")
            
            assert response.status_code == 200
            site_data = response.json()
            assert site_data["site_id"] == "centre_valbio"
            assert site_data["event_count"] >= 1
            
            # Check statistics
            response = await client.get("http://localhost:8003/conservation/stats")
            
            assert response.status_code == 200
            stats = response.json()
            assert stats["total_events"] >= 1
            assert "centre_valbio" in stats["sites"]
            
            print(f"✅ Conservation event test passed: {stats['total_events']} events stored")
            
    finally:
        # Cleanup
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass

@pytest.mark.asyncio
async def test_madagascar_conservation_scenarios():
    """Test Madagascar-specific conservation scenarios."""
    from mcp_foundation.simple_conservation_server import SimpleConservationServer, create_test_events
    
    # Create server
    server = SimpleConservationServer("madagascar-test-server")
    
    # Start server task
    server_task = asyncio.create_task(
        server.start_server(host="localhost", port=8004)
    )
    
    # Wait for server to start
    await asyncio.sleep(1)
    
    try:
        async with httpx.AsyncClient() as client:
            # Get test events
            test_events = create_test_events()
            
            # Store all test events
            for event in test_events:
                response = await client.post(
                    "http://localhost:8004/conservation/event",
                    json=event.dict()
                )
                assert response.status_code == 200
            
            # Check final statistics
            response = await client.get("http://localhost:8004/conservation/stats")
            
            assert response.status_code == 200
            stats = response.json()
            
            # Verify Madagascar sites are present
            assert "centre_valbio" in stats["sites"]
            assert "maromizaha" in stats["sites"]
            
            # Verify event types
            assert "species_detection" in stats["event_types"]
            assert "threat_detection" in stats["event_types"]
            assert "conservation_intervention" in stats["event_types"]
            
            print(f"✅ Madagascar scenario test passed:")
            print(f"   📊 Total events: {stats['total_events']}")
            print(f"   🏝️  Sites: {len(stats['sites'])}")
            print(f"   📋 Event types: {len(stats['event_types'])}")
            
    finally:
        # Cleanup
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass

def test_server_import():
    """Simple import test to verify module loading."""
    try:
        from mcp_foundation.simple_conservation_server import SimpleConservationServer, ConservationEvent
        
        # Test creating server instance
        server = SimpleConservationServer("import-test")
        assert server.server_name == "import-test"
        
        # Test creating event
        event = ConservationEvent(
            site_id="test_site",
            event_type="test_event",
            confidence=0.8
        )
        assert event.site_id == "test_site"
        assert event.confidence == 0.8
        
        print("✅ Server import test passed")
        
    except ImportError as e:
        pytest.fail(f"Failed to import server modules: {e}")

if __name__ == "__main__":
    # Run tests directly
    print("🧪 Running Direct Conservation Server Tests")
    print("=" * 45)
    
    # Run import test
    test_server_import()
    
    # Run async tests
    asyncio.run(test_direct_server_health())
    asyncio.run(test_direct_conservation_event())
    asyncio.run(test_madagascar_conservation_scenarios())
    
    print("\n🎉 All direct tests passed!")
