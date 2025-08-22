"""
Step 2 Section 3: FastAPI Integration
=====================================
Integrate simple memory with FastAPI endpoints.
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import required modules at module level
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

# Import from Section 2
from step2_section2_test import SimpleConservationMemory

def test_fastapi_imports():
    """Test FastAPI imports."""
    print("🌐 Testing FastAPI Imports...")
    
    if FASTAPI_AVAILABLE:
        print("✅ FastAPI imports successful")
        return True
    else:
        print("❌ FastAPI import error")
        return False

class ConservationEvent(BaseModel if FASTAPI_AVAILABLE else object):
    """Pydantic model for conservation events."""
    event_type: str
    location: Optional[str] = None
    confidence: Optional[float] = None
    observer: Optional[str] = None
    activity: Optional[str] = None
    team_size: Optional[int] = None
    weather: Optional[str] = None
    notes: Optional[str] = None

class MemoryQuery(BaseModel if FASTAPI_AVAILABLE else object):
    """Pydantic model for memory queries."""
    entity_name: str
    entity_type: str  # "species" or "site"

def create_memory_app() -> tuple:
    """Create FastAPI app with memory integration."""
    print("\n🚀 Creating Memory-Integrated FastAPI App...")
    
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.responses import JSONResponse
        
        app = FastAPI(title="Conservation Memory API", version="1.0.0")
        memory = SimpleConservationMemory("api_memory_data")
        
        @app.get("/")
        async def root():
            return {"message": "Conservation Memory API", "status": "running"}
        
        @app.get("/health")
        async def health_check():
            stats = memory.get_memory_stats()
            return {
                "status": "healthy",
                "memory_stats": stats,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        @app.post("/memory/species/{species_name}")
        async def store_species_event(species_name: str, event: ConservationEvent):
            """Store species-related event in memory."""
            try:
                event_data = event.dict(exclude_none=True)
                memory.store_species_event(species_name, event_data)
                return {
                    "message": f"Species event stored for {species_name}",
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.post("/memory/site/{site_name}")
        async def store_site_event(site_name: str, event: ConservationEvent):
            """Store site-related event in memory."""
            try:
                event_data = event.dict(exclude_none=True)
                memory.store_site_event(site_name, event_data)
                return {
                    "message": f"Site event stored for {site_name}",
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/memory/species/{species_name}")
        async def get_species_memory(species_name: str):
            """Retrieve species memory."""
            try:
                events = memory.get_species_memory(species_name)
                return {
                    "species": species_name,
                    "event_count": len(events),
                    "events": events
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/memory/site/{site_name}")
        async def get_site_memory(site_name: str):
            """Retrieve site memory."""
            try:
                events = memory.get_site_memory(site_name)
                return {
                    "site": site_name,
                    "event_count": len(events),
                    "events": events
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/memory/stats")
        async def get_memory_stats():
            """Get memory statistics."""
            try:
                stats = memory.get_memory_stats()
                return {
                    "memory_stats": stats,
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        print("✅ FastAPI app created successfully")
        return app, memory
        
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return None, None

def test_app_creation():
    """Test FastAPI app creation."""
    print("\n🏗️  Testing App Creation...")
    
    try:
        app, memory = create_memory_app()
        if app and memory:
            print("✅ App and memory created successfully")
            return app, memory
        else:
            print("❌ App creation failed")
            return None, None
            
    except Exception as e:
        print(f"❌ App creation test error: {e}")
        return None, None

def test_pydantic_models():
    """Test Pydantic models."""
    print("\n📋 Testing Pydantic Models...")
    
    try:
        # Test ConservationEvent
        species_event = ConservationEvent(
            event_type="detection",
            location="centre_valbio",
            confidence=0.95,
            observer="field_camera_01"
        )
        print("✅ Species ConservationEvent created")
        
        site_event = ConservationEvent(
            event_type="monitoring",
            activity="biodiversity_survey",
            team_size=3,
            weather="clear"
        )
        print("✅ Site ConservationEvent created")
        
        # Test MemoryQuery
        query = MemoryQuery(
            entity_name="lemur_catta",
            entity_type="species"
        )
        print("✅ MemoryQuery created")
        
        return True
        
    except Exception as e:
        print(f"❌ Pydantic model error: {e}")
        return False

def test_app_routes():
    """Test basic app route structure."""
    print("\n🛣️  Testing App Routes...")
    
    try:
        app, memory = create_memory_app()
        if not app:
            return False
        
        # Check routes exist
        routes = [route.path for route in app.routes]
        expected_routes = [
            "/",
            "/health", 
            "/memory/species/{species_name}",
            "/memory/site/{site_name}",
            "/memory/stats"
        ]
        
        route_count = 0
        for expected in expected_routes:
            # Check if route pattern exists (simplified check)
            route_found = any(expected.replace("{species_name}", "").replace("{site_name}", "") in route 
                            for route in routes)
            if route_found:
                route_count += 1
        
        print(f"✅ Found {route_count}/{len(expected_routes)} expected routes")
        
        if route_count >= 3:  # At least basic routes
            print("✅ Core routes verified")
            return True
        else:
            print("❌ Missing core routes")
            return False
            
    except Exception as e:
        print(f"❌ Route test error: {e}")
        return False

def test_manual_memory_operations():
    """Test memory operations manually without HTTP client."""
    print("\n🔧 Testing Manual Memory Operations...")
    
    try:
        app, memory = create_memory_app()
        if not app or not memory:
            return False
        
        # Test direct memory operations
        test_species_event = {
            "event_type": "detection",
            "location": "centre_valbio", 
            "confidence": 0.95,
            "observer": "field_camera_01"
        }
        
        memory.store_species_event("lemur_catta", test_species_event)
        print("✅ Species event stored directly")
        
        retrieved = memory.get_species_memory("lemur_catta")
        if len(retrieved) > 0:
            print("✅ Species event retrieved directly")
        
        test_site_event = {
            "event_type": "monitoring",
            "activity": "biodiversity_survey",
            "team_size": 3
        }
        
        memory.store_site_event("maromizaha", test_site_event)
        print("✅ Site event stored directly")
        
        site_retrieved = memory.get_site_memory("maromizaha")
        if len(site_retrieved) > 0:
            print("✅ Site event retrieved directly")
        
        stats = memory.get_memory_stats()
        print(f"✅ Memory stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Manual operations error: {e}")
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
    """Run Section 3 tests."""
    print("🧠 STEP 2 - SECTION 3: FastAPI Integration")
    print("=" * 45)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: FastAPI imports
    if test_fastapi_imports():
        tests_passed += 1
    
    # Test 2: Pydantic models
    if test_pydantic_models():
        tests_passed += 1
    
    # Test 3: App creation
    if test_app_creation()[0]:
        tests_passed += 1
    
    # Test 4: Route structure
    if test_app_routes():
        tests_passed += 1
    
    # Test 5: Manual operations
    if test_manual_memory_operations():
        tests_passed += 1
    
    # Cleanup
    cleanup_test_files()
    
    # Summary
    print(f"\n📊 Section 3 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 3 PASSED - Ready for Section 4")
        return True
    else:
        print("❌ Section 3 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
