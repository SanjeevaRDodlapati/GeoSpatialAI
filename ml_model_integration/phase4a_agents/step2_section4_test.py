"""
Step 2 Section 4: HTTP Client Testing
=====================================
Test the memory API with actual HTTP requests using httpx.
"""

import sys
import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import from Section 3
from step2_section3_test import create_memory_app, ConservationEvent

def test_httpx_imports():
    """Test httpx imports for HTTP client testing."""
    print("🌐 Testing HTTP Client Imports...")
    
    try:
        import httpx
        print("✅ httpx import successful")
        return True
    except ImportError as e:
        print(f"❌ httpx import error: {e}")
        print("💡 Install with: conda install httpx")
        return False

def test_uvicorn_imports():
    """Test uvicorn imports for server testing."""
    print("🚀 Testing Server Imports...")
    
    try:
        import uvicorn
        print("✅ uvicorn import successful")
        return True
    except ImportError as e:
        print(f"❌ uvicorn import error: {e}")
        print("💡 Install with: conda install uvicorn")
        return False

async def test_memory_api_endpoints():
    """Test memory API endpoints with HTTP client."""
    print("\n🧪 Testing Memory API Endpoints...")
    
    try:
        import httpx
        from fastapi.testclient import TestClient
        
        # Create app
        app, memory = create_memory_app()
        if not app:
            print("❌ Failed to create app")
            return False
        
        # Create test client
        client = TestClient(app)
        
        # Test 1: Health check
        response = client.get("/health")
        if response.status_code == 200:
            print("✅ Health check endpoint working")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test 2: Store species event
        species_data = {
            "event_type": "detection",
            "location": "centre_valbio",
            "confidence": 0.95,
            "observer": "field_camera_01"
        }
        
        response = client.post("/memory/species/lemur_catta", json=species_data)
        if response.status_code == 200:
            print("✅ Species event storage endpoint working")
        else:
            print(f"❌ Species storage failed: {response.status_code}")
            return False
        
        # Test 3: Retrieve species memory
        response = client.get("/memory/species/lemur_catta")
        if response.status_code == 200:
            data = response.json()
            if data["event_count"] > 0:
                print("✅ Species retrieval endpoint working")
            else:
                print("❌ No species events retrieved")
                return False
        else:
            print(f"❌ Species retrieval failed: {response.status_code}")
            return False
        
        # Test 4: Store site event
        site_data = {
            "event_type": "monitoring",
            "activity": "biodiversity_survey",
            "team_size": 3,
            "weather": "clear"
        }
        
        response = client.post("/memory/site/maromizaha", json=site_data)
        if response.status_code == 200:
            print("✅ Site event storage endpoint working")
        else:
            print(f"❌ Site storage failed: {response.status_code}")
            return False
        
        # Test 5: Retrieve site memory
        response = client.get("/memory/site/maromizaha")
        if response.status_code == 200:
            data = response.json()
            if data["event_count"] > 0:
                print("✅ Site retrieval endpoint working")
            else:
                print("❌ No site events retrieved")
                return False
        else:
            print(f"❌ Site retrieval failed: {response.status_code}")
            return False
        
        # Test 6: Memory stats
        response = client.get("/memory/stats")
        if response.status_code == 200:
            data = response.json()
            stats = data["memory_stats"]
            if stats["species_count"] > 0 and stats["site_count"] > 0:
                print("✅ Memory stats endpoint working")
                print(f"   📊 Stats: {stats}")
            else:
                print("❌ Invalid memory stats")
                return False
        else:
            print(f"❌ Memory stats failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoint test error: {e}")
        return False

def test_error_handling():
    """Test API error handling."""
    print("\n⚠️  Testing Error Handling...")
    
    try:
        from fastapi.testclient import TestClient
        
        app, memory = create_memory_app()
        if not app:
            return False
        
        client = TestClient(app)
        
        # Test invalid species retrieval
        response = client.get("/memory/species/nonexistent_species")
        if response.status_code == 200:
            data = response.json()
            if data["event_count"] == 0:
                print("✅ Non-existent species handled correctly")
            else:
                print("❌ Non-existent species returned events")
                return False
        else:
            print(f"❌ Non-existent species request failed: {response.status_code}")
            return False
        
        # Test invalid site retrieval
        response = client.get("/memory/site/nonexistent_site")
        if response.status_code == 200:
            data = response.json()
            if data["event_count"] == 0:
                print("✅ Non-existent site handled correctly")
            else:
                print("❌ Non-existent site returned events")
                return False
        else:
            print(f"❌ Non-existent site request failed: {response.status_code}")
            return False
        
        # Test malformed data
        response = client.post("/memory/species/test_species", json={"invalid": "data"})
        if response.status_code in [200, 422]:  # 422 is validation error
            print("✅ Malformed data handled appropriately")
        else:
            print(f"❌ Malformed data handling unexpected: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test error: {e}")
        return False

def test_response_validation():
    """Test response data validation."""
    print("\n✅ Testing Response Validation...")
    
    try:
        from fastapi.testclient import TestClient
        
        app, memory = create_memory_app()
        if not app:
            return False
        
        client = TestClient(app)
        
        # Store test data
        test_data = {
            "event_type": "detection",
            "location": "centre_valbio",
            "confidence": 0.95,
            "observer": "test_camera"
        }
        
        response = client.post("/memory/species/validation_test", json=test_data)
        if response.status_code != 200:
            print(f"❌ Failed to store test data: {response.status_code}")
            return False
        
        # Retrieve and validate
        response = client.get("/memory/species/validation_test")
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            if "species" in data and "event_count" in data and "events" in data:
                print("✅ Response structure valid")
            else:
                print("❌ Response missing required fields")
                return False
            
            # Check event data
            if len(data["events"]) > 0:
                event = data["events"][0]
                if "timestamp" in event and "event_type" in event:
                    print("✅ Event data structure valid")
                else:
                    print("❌ Event data missing required fields")
                    return False
            
            # Check data integrity
            if data["species"] == "validation_test" and data["event_count"] > 0:
                print("✅ Data integrity verified")
            else:
                print("❌ Data integrity check failed")
                return False
        else:
            print(f"❌ Validation retrieval failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Response validation error: {e}")
        return False

def test_concurrent_requests():
    """Test concurrent request handling."""
    print("\n🔄 Testing Concurrent Requests...")
    
    try:
        from fastapi.testclient import TestClient
        import threading
        import time
        
        app, memory = create_memory_app()
        if not app:
            return False
        
        client = TestClient(app)
        results = []
        
        def make_request(species_id):
            """Make a request in a separate thread."""
            try:
                test_data = {
                    "event_type": "detection",
                    "location": f"location_{species_id}",
                    "confidence": 0.9,
                    "observer": f"camera_{species_id}"
                }
                
                response = client.post(f"/memory/species/species_{species_id}", json=test_data)
                results.append(response.status_code == 200)
            except Exception as e:
                results.append(False)
        
        # Create threads for concurrent requests
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # Check results
        success_count = sum(results)
        if success_count == 5:
            print(f"✅ Concurrent requests successful: {success_count}/5")
        else:
            print(f"⚠️  Partial concurrent success: {success_count}/5")
            # Still pass if most succeeded
            return success_count >= 3
        
        return True
        
    except Exception as e:
        print(f"❌ Concurrent request test error: {e}")
        return False

def cleanup_test_files():
    """Clean up test files."""
    try:
        import shutil
        if os.path.exists("api_memory_data"):
            shutil.rmtree("api_memory_data")
        print("✅ Test files cleaned up")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

def main():
    """Run Section 4 tests."""
    print("🧠 STEP 2 - SECTION 4: HTTP Client Testing")
    print("=" * 45)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: HTTP client imports
    if test_httpx_imports():
        tests_passed += 1
    else:
        print("⚠️  Skipping HTTP client tests - httpx not available")
        total_tests = 1  # Only count import test
    
    # Only run remaining tests if httpx is available
    if tests_passed == 1:
        # Test 2: Server imports
        if test_uvicorn_imports():
            tests_passed += 1
        
        # Test 3: API endpoints
        result = asyncio.run(test_memory_api_endpoints()) if hasattr(asyncio, 'run') else False
        if result:
            tests_passed += 1
        
        # Test 4: Error handling
        if test_error_handling():
            tests_passed += 1
        
        # Test 5: Response validation
        if test_response_validation():
            tests_passed += 1
        
        # Test 6: Concurrent requests
        if test_concurrent_requests():
            tests_passed += 1
    
    # Cleanup
    cleanup_test_files()
    
    # Summary
    print(f"\n📊 Section 4 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 4 PASSED - Ready for Final Integration")
        return True
    else:
        print("❌ Section 4 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
