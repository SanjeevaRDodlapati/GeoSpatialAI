"""
Step 2 Section 1: Basic Memory System Test
==========================================
Simple test to verify LangChain memory imports and basic functionality.
"""

import sys
import os
from datetime import datetime

def test_basic_imports():
    """Test basic imports before building complex system."""
    print("🧪 Testing Basic Imports...")
    
    try:
        # Test LangChain imports
        from langchain.memory import ConversationBufferWindowMemory
        print("✅ LangChain ConversationBufferWindowMemory imported")
        
        from langchain.schema import HumanMessage, AIMessage  
        print("✅ LangChain message schemas imported")
        
        # Test basic memory creation
        memory = ConversationBufferWindowMemory(k=5, return_messages=True)
        print("✅ Basic LangChain memory created")
        
        # Test memory functionality
        memory.save_context(
            {"input": "Test conservation event at Centre ValBio"},
            {"output": "Processed species detection with 0.9 confidence"}
        )
        print("✅ Memory save_context working")
        
        # Test memory retrieval
        buffer = memory.buffer
        print(f"✅ Memory buffer contains {len(buffer)} messages")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Memory test error: {e}")
        return False

def test_json_persistence():
    """Test basic JSON file operations for memory persistence."""
    print("\n🗃️  Testing JSON Persistence...")
    
    try:
        import json
        
        # Test data
        test_memory_data = {
            "agent_id": "test_agent",
            "timestamp": datetime.utcnow().isoformat(),
            "test_data": {
                "species": "lemur_catta",
                "site": "centre_valbio",
                "confidence": 0.9
            }
        }
        
        # Test write
        test_file = "test_memory.json"
        with open(test_file, "w") as f:
            json.dump(test_memory_data, f, indent=2)
        print("✅ JSON write successful")
        
        # Test read
        with open(test_file, "r") as f:
            loaded_data = json.load(f)
        print("✅ JSON read successful")
        
        # Verify data
        if loaded_data["agent_id"] == "test_agent":
            print("✅ JSON data integrity verified")
        
        # Cleanup
        os.remove(test_file)
        print("✅ Test file cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"❌ JSON persistence error: {e}")
        return False

def test_directory_creation():
    """Test directory creation for memory storage."""
    print("\n📁 Testing Directory Creation...")
    
    try:
        memory_dir = "test_memory_data"
        
        # Create directory
        os.makedirs(memory_dir, exist_ok=True)
        print(f"✅ Directory created: {memory_dir}")
        
        # Verify directory exists
        if os.path.exists(memory_dir):
            print("✅ Directory existence verified")
        
        # Cleanup
        os.rmdir(memory_dir)
        print("✅ Test directory cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Directory creation error: {e}")
        return False

def main():
    """Run Section 1 tests."""
    print("🧠 STEP 2 - SECTION 1: Basic Memory System Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Run tests
    if test_basic_imports():
        tests_passed += 1
    
    if test_json_persistence():
        tests_passed += 1
        
    if test_directory_creation():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Section 1 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 1 PASSED - Ready for Section 2")
        return True
    else:
        print("❌ Section 1 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
