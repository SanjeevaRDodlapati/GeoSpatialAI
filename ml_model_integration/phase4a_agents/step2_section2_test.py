"""
Step 2 Section 2: Simple Conservation Memory Store
==================================================
Build basic conservation memory with updated LangChain patterns.
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

def test_updated_memory_imports():
    """Test updated LangChain memory imports to avoid deprecation warnings."""
    print("🧪 Testing Updated Memory Imports...")
    
    try:
        # Updated LangChain imports
        from langchain_core.memory import BaseMemory
        from langchain_core.messages import HumanMessage, AIMessage
        print("✅ Updated LangChain core imports successful")
        
        # Test pydantic for data models
        from pydantic import BaseModel, Field
        print("✅ Pydantic imports successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

class SimpleConservationMemory:
    """Simple conservation memory store with basic functionality."""
    
    def __init__(self, storage_dir: str = "memory_data"):
        self.storage_dir = storage_dir
        self.species_memory = {}
        self.site_memory = {}
        
        # Create storage directory
        os.makedirs(storage_dir, exist_ok=True)
        
        # Load existing memory if available
        self._load_memory()
    
    def store_species_event(self, species_name: str, event_data: Dict[str, Any]):
        """Store species-related event."""
        if species_name not in self.species_memory:
            self.species_memory[species_name] = []
        
        event_data["timestamp"] = datetime.utcnow().isoformat()
        self.species_memory[species_name].append(event_data)
        
        # Persist to disk
        self._save_memory()
    
    def store_site_event(self, site_name: str, event_data: Dict[str, Any]):
        """Store site-related event."""
        if site_name not in self.site_memory:
            self.site_memory[site_name] = []
        
        event_data["timestamp"] = datetime.utcnow().isoformat()
        self.site_memory[site_name].append(event_data)
        
        # Persist to disk
        self._save_memory()
    
    def get_species_memory(self, species_name: str) -> List[Dict[str, Any]]:
        """Retrieve species memory."""
        return self.species_memory.get(species_name, [])
    
    def get_site_memory(self, site_name: str) -> List[Dict[str, Any]]:
        """Retrieve site memory."""
        return self.site_memory.get(site_name, [])
    
    def get_memory_stats(self) -> Dict[str, int]:
        """Get memory statistics."""
        return {
            "species_count": len(self.species_memory),
            "site_count": len(self.site_memory),
            "total_species_events": sum(len(events) for events in self.species_memory.values()),
            "total_site_events": sum(len(events) for events in self.site_memory.values())
        }
    
    def _load_memory(self):
        """Load memory from disk."""
        species_file = os.path.join(self.storage_dir, "species_memory.json")
        site_file = os.path.join(self.storage_dir, "site_memory.json")
        
        if os.path.exists(species_file):
            with open(species_file, "r") as f:
                self.species_memory = json.load(f)
        
        if os.path.exists(site_file):
            with open(site_file, "r") as f:
                self.site_memory = json.load(f)
    
    def _save_memory(self):
        """Save memory to disk."""
        species_file = os.path.join(self.storage_dir, "species_memory.json")
        site_file = os.path.join(self.storage_dir, "site_memory.json")
        
        with open(species_file, "w") as f:
            json.dump(self.species_memory, f, indent=2)
        
        with open(site_file, "w") as f:
            json.dump(self.site_memory, f, indent=2)

def test_simple_memory_creation():
    """Test creating simple conservation memory."""
    print("\n🧠 Testing Simple Memory Creation...")
    
    try:
        memory = SimpleConservationMemory("test_simple_memory")
        print("✅ Simple conservation memory created")
        
        # Test memory stats
        stats = memory.get_memory_stats()
        print(f"✅ Memory stats: {stats}")
        
        return memory
        
    except Exception as e:
        print(f"❌ Memory creation error: {e}")
        return None

def test_species_memory_storage(memory: SimpleConservationMemory):
    """Test species memory storage and retrieval."""
    print("\n🐾 Testing Species Memory Storage...")
    
    try:
        # Store species event
        species_event = {
            "event_type": "detection",
            "location": "centre_valbio",
            "confidence": 0.95,
            "observer": "field_camera_01"
        }
        
        memory.store_species_event("lemur_catta", species_event)
        print("✅ Species event stored")
        
        # Retrieve species memory
        retrieved = memory.get_species_memory("lemur_catta")
        print(f"✅ Species memory retrieved: {len(retrieved)} events")
        
        # Verify data
        if len(retrieved) > 0 and retrieved[0]["confidence"] == 0.95:
            print("✅ Species data integrity verified")
            return True
        else:
            print("❌ Species data integrity failed")
            return False
            
    except Exception as e:
        print(f"❌ Species memory error: {e}")
        return False

def test_site_memory_storage(memory: SimpleConservationMemory):
    """Test site memory storage and retrieval."""
    print("\n🏞️  Testing Site Memory Storage...")
    
    try:
        # Store site event
        site_event = {
            "event_type": "monitoring",
            "activity": "biodiversity_survey",
            "team_size": 3,
            "weather": "clear"
        }
        
        memory.store_site_event("maromizaha", site_event)
        print("✅ Site event stored")
        
        # Retrieve site memory
        retrieved = memory.get_site_memory("maromizaha")
        print(f"✅ Site memory retrieved: {len(retrieved)} events")
        
        # Verify data
        if len(retrieved) > 0 and retrieved[0]["team_size"] == 3:
            print("✅ Site data integrity verified")
            return True
        else:
            print("❌ Site data integrity failed")
            return False
            
    except Exception as e:
        print(f"❌ Site memory error: {e}")
        return False

def test_memory_persistence(memory: SimpleConservationMemory):
    """Test memory persistence across instances."""
    print("\n💾 Testing Memory Persistence...")
    
    try:
        # Get current stats
        stats_before = memory.get_memory_stats()
        print(f"✅ Stats before: {stats_before}")
        
        # Create new memory instance (should load from disk)
        new_memory = SimpleConservationMemory("test_simple_memory")
        stats_after = new_memory.get_memory_stats()
        print(f"✅ Stats after reload: {stats_after}")
        
        # Verify persistence
        if (stats_before["species_count"] == stats_after["species_count"] and 
            stats_before["site_count"] == stats_after["site_count"]):
            print("✅ Memory persistence verified")
            return True
        else:
            print("❌ Memory persistence failed")
            return False
            
    except Exception as e:
        print(f"❌ Persistence test error: {e}")
        return False

def cleanup_test_files():
    """Clean up test files."""
    try:
        import shutil
        if os.path.exists("test_simple_memory"):
            shutil.rmtree("test_simple_memory")
        print("✅ Test files cleaned up")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

def main():
    """Run Section 2 tests."""
    print("🧠 STEP 2 - SECTION 2: Simple Conservation Memory Store")
    print("=" * 55)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Updated imports
    if test_updated_memory_imports():
        tests_passed += 1
    
    # Test 2: Memory creation
    memory = test_simple_memory_creation()
    if memory:
        tests_passed += 1
        
        # Test 3: Species memory
        if test_species_memory_storage(memory):
            tests_passed += 1
        
        # Test 4: Site memory
        if test_site_memory_storage(memory):
            tests_passed += 1
        
        # Test 5: Persistence
        if test_memory_persistence(memory):
            tests_passed += 1
    
    # Cleanup
    cleanup_test_files()
    
    # Summary
    print(f"\n📊 Section 2 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 2 PASSED - Ready for Section 3")
        return True
    else:
        print("❌ Section 2 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
