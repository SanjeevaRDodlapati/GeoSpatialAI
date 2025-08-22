"""
Simple Test Suite for Conservation Server
========================================
Basic tests with minimal complexity and clear validation.
"""

import pytest
import asyncio
import httpx
from datetime import datetime
import time

# Import our simple server
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from mcp_foundation.simple_conservation_server import SimpleConservationServer, ConservationEvent

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def server_setup():
    """Setup test server."""
    server = SimpleConservationServer("test-conservation-server")
    
    # Start server in background
    server_task = asyncio.create_task(
        server.start_server(host="localhost", port=8001)
    )
    
    # Wait for server to start
    await asyncio.sleep(2)
    
    # Provide server info to tests
    server_info = {
        "base_url": "http://localhost:8001",
        "server": server,
        "task": server_task
    }
    
    yield server_info
    
    # Cleanup
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass
    
@pytest.mark.asyncio
async def test_server_health_check(server_setup):
    """Test basic server health check."""
    base_url = server_setup["base_url"]
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "uptime_seconds" in data
        assert "timestamp" in data
        assert data["server_name"] == "test-conservation-server"
        
        print(f"✅ Health check passed: {data['status']}")

@pytest.mark.asyncio
async def test_store_conservation_event(server_setup):
    """Test storing a conservation event."""
    base_url = server_setup["base_url"]
    
    # Create test event
    test_event = {
        "site_id": "centre_valbio",
        "event_type": "species_detection",
        "confidence": 0.85,
        "metadata": {
            "species": "lemur_catta",
            "individual_count": 3
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/conservation/event",
            json=test_event
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert "event_id" in data
        assert "centre_valbio" in data["message"]
        
        print(f"✅ Event stored successfully: {data['message']}")

@pytest.mark.asyncio
async def test_retrieve_site_events(server_setup):
    """Test retrieving events for a site."""
    base_url = server_setup["base_url"]
    
    # First, store some test events
    test_events = [
        {
            "site_id": "centre_valbio",
            "event_type": "species_detection",
            "confidence": 0.85
        },
        {
            "site_id": "centre_valbio",
            "event_type": "threat_detection",
            "confidence": 0.72
        }
    ]
    
    async with httpx.AsyncClient() as client:
        # Store events
        for event in test_events:
            await client.post(f"{base_url}/conservation/event", json=event)
        
        # Retrieve events for site
        response = await client.get(f"{base_url}/conservation/events/centre_valbio")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["site_id"] == "centre_valbio"
        assert data["event_count"] >= 2  # At least our 2 test events
        assert len(data["events"]) >= 2
        
        print(f"✅ Retrieved {data['event_count']} events for Centre ValBio")

@pytest.mark.asyncio
async def test_conservation_statistics(server_setup):
    """Test getting conservation statistics."""
    base_url = server_setup["base_url"]
    
    # Store a variety of test events
    test_events = [
        {
            "site_id": "centre_valbio",
            "event_type": "species_detection",
            "confidence": 0.85
        },
        {
            "site_id": "maromizaha",
            "event_type": "threat_detection",
            "confidence": 0.72
        },
        {
            "site_id": "centre_valbio",
            "event_type": "conservation_intervention",
            "confidence": 1.0
        }
    ]
    
    async with httpx.AsyncClient() as client:
        # Store events
        for event in test_events:
            await client.post(f"{base_url}/conservation/event", json=event)
        
        # Get statistics
        response = await client.get(f"{base_url}/conservation/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_events"] >= 3
        assert data["active_sites"] >= 2
        assert "event_types" in data
        assert "sites" in data
        
        # Check specific sites are included
        assert "centre_valbio" in data["sites"]
        assert "maromizaha" in data["sites"]
        
        print(f"✅ Statistics: {data['total_events']} events across {data['active_sites']} sites")

@pytest.mark.asyncio
async def test_error_handling(server_setup):
    """Test error handling for invalid data."""
    base_url = server_setup["base_url"]
    
    # Test with missing required fields
    invalid_event = {
        "confidence": 0.5
        # Missing site_id and event_type
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/conservation/event",
            json=invalid_event
        )
        
        assert response.status_code == 400
        error_data = response.json()
        assert "site_id and event_type required" in error_data["detail"]
        
        print("✅ Error handling working correctly")

# Simple performance test
@pytest.mark.asyncio
async def test_response_time(server_setup):
    """Test that responses are reasonably fast."""
    base_url = server_setup["base_url"]
    
    async with httpx.AsyncClient() as client:
        # Measure health check response time
        start_time = time.time()
        response = await client.get(f"{base_url}/health")
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # Should respond within 1 second
        
        print(f"✅ Health check response time: {response_time:.3f} seconds")

@pytest.mark.asyncio
async def test_multiple_requests(server_setup):
    """Test handling multiple simultaneous requests."""
    base_url = server_setup["base_url"]
    
    async def make_request(client, request_id):
        """Make a single request."""
        test_event = {
            "site_id": f"test_site_{request_id}",
            "event_type": "test_event",
            "confidence": 0.5
        }
        
        response = await client.post(
            f"{base_url}/conservation/event",
            json=test_event
        )
        return response.status_code == 200
    
    # Make 5 concurrent requests
    async with httpx.AsyncClient() as client:
        tasks = [make_request(client, i) for i in range(5)]
        results = await asyncio.gather(*tasks)
        
        # All requests should succeed
        assert all(results), "Not all concurrent requests succeeded"
        
        print("✅ Multiple concurrent requests handled successfully")

# Simple test runner function
def run_simple_tests():
    """Run tests with simple output."""
    print("🧪 Running Simple Conservation Server Tests...")
    print("=" * 50)
    
    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short"])

if __name__ == "__main__":
    # Direct test execution
    run_simple_tests()
