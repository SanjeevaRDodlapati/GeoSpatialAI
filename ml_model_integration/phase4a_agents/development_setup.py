#!/usr/bin/env python3
"""
Simple Development Environment Setup
===================================
Easy setup and testing for Phase 4A development.
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path

def setup_development_environment():
    """Setup the development environment with minimal complexity."""
    print("🚀 Setting up Phase 4A Development Environment")
    print("=" * 50)
    
    # Get current directory
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent.parent
    
    print(f"📁 Project root: {project_root}")
    print(f"📁 Phase 4A directory: {current_dir}")
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8+ required for Phase 4A development")
        return False
    
    # Install requirements
    print("\n📦 Installing requirements...")
    requirements_file = current_dir / "requirements_phase4a.txt"
    
    if requirements_file.exists():
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True, cwd=str(current_dir))
            print("✅ Requirements installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install requirements: {e}")
            return False
    else:
        print("❌ Requirements file not found")
        return False
    
    print("\n✅ Development environment setup complete!")
    return True

def test_simple_server():
    """Test the simple conservation server."""
    print("\n🧪 Testing Simple Conservation Server")
    print("=" * 40)
    
    try:
        # Run the tests
        current_dir = Path(__file__).parent
        test_file = current_dir / "tests" / "test_simple_server.py"
        
        if test_file.exists():
            result = subprocess.run([
                sys.executable, "-m", "pytest", str(test_file), "-v"
            ], cwd=str(current_dir))
            
            if result.returncode == 0:
                print("✅ All tests passed!")
                return True
            else:
                print("❌ Some tests failed")
                return False
        else:
            print("❌ Test file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def start_development_server():
    """Start the development server for manual testing."""
    print("\n🌐 Starting Development Server")
    print("=" * 35)
    
    try:
        current_dir = Path(__file__).parent
        server_file = current_dir / "mcp_foundation" / "simple_conservation_server.py"
        
        if server_file.exists():
            print("🚀 Starting server on http://localhost:8000")
            print("📊 Health check: http://localhost:8000/health")
            print("📈 Statistics: http://localhost:8000/conservation/stats")
            print("\n⏹️  Press Ctrl+C to stop the server")
            
            subprocess.run([
                sys.executable, str(server_file)
            ], cwd=str(current_dir))
            
        else:
            print("❌ Server file not found")
            return False
            
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def run_madagascar_test_scenarios():
    """Run test scenarios with Madagascar conservation data."""
    print("\n🏝️  Running Madagascar Conservation Test Scenarios")
    print("=" * 50)
    
    import httpx
    import json
    
    # Test data for Madagascar sites
    madagascar_events = [
        {
            "site_id": "centre_valbio",
            "event_type": "species_detection",
            "confidence": 0.92,
            "metadata": {
                "species": "lemur_catta",
                "individual_count": 5,
                "behavior": "feeding",
                "habitat": "gallery_forest",
                "researcher": "Dr. Patricia Wright"
            }
        },
        {
            "site_id": "maromizaha",
            "event_type": "species_detection",
            "confidence": 0.87,
            "metadata": {
                "species": "indri_indri",
                "individual_count": 2,
                "behavior": "singing",
                "habitat": "primary_rainforest"
            }
        },
        {
            "site_id": "centre_valbio",
            "event_type": "threat_detection",
            "confidence": 0.74,
            "metadata": {
                "threat_type": "edge_effect",
                "severity": "moderate",
                "area_affected_hectares": 3.2,
                "response_needed": True
            }
        },
        {
            "site_id": "maromizaha",
            "event_type": "conservation_intervention",
            "confidence": 1.0,
            "metadata": {
                "intervention_type": "community_education",
                "participants": 45,
                "duration_days": 3,
                "effectiveness_score": 0.88
            }
        }
    ]
    
    async def test_madagascar_scenarios():
        base_url = "http://localhost:8000"
        
        async with httpx.AsyncClient() as client:
            try:
                # Test server health
                health_response = await client.get(f"{base_url}/health")
                if health_response.status_code != 200:
                    print("❌ Server not responding")
                    return False
                
                print("✅ Server is healthy")
                
                # Store Madagascar events
                print("\n📊 Storing Madagascar conservation events...")
                for i, event in enumerate(madagascar_events, 1):
                    response = await client.post(f"{base_url}/conservation/event", json=event)
                    if response.status_code == 200:
                        print(f"  ✅ Event {i}: {event['event_type']} at {event['site_id']}")
                    else:
                        print(f"  ❌ Failed to store event {i}")
                
                # Get statistics
                print("\n📈 Getting conservation statistics...")
                stats_response = await client.get(f"{base_url}/conservation/stats")
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                    print(f"  📊 Total events: {stats['total_events']}")
                    print(f"  🏝️  Active sites: {stats['active_sites']}")
                    print(f"  📋 Event types: {list(stats['event_types'].keys())}")
                
                # Get events for specific sites
                print("\n📍 Getting events for Madagascar sites...")
                for site in ["centre_valbio", "maromizaha"]:
                    events_response = await client.get(f"{base_url}/conservation/events/{site}")
                    if events_response.status_code == 200:
                        site_data = events_response.json()
                        print(f"  🌿 {site}: {site_data['event_count']} events")
                
                print("\n✅ Madagascar test scenarios completed successfully!")
                return True
                
            except Exception as e:
                print(f"❌ Error in Madagascar scenarios: {e}")
                return False
    
    # Run the async test
    try:
        result = asyncio.run(test_madagascar_scenarios())
        return result
    except Exception as e:
        print(f"❌ Failed to run Madagascar scenarios: {e}")
        print("💡 Make sure the server is running first!")
        return False

def main():
    """Main development setup and testing function."""
    print("🌿 Phase 4A AI Agent Development Setup")
    print("🏝️  Madagascar Conservation AI Agents")
    print("=" * 60)
    
    # Setup environment
    if not setup_development_environment():
        print("❌ Environment setup failed")
        return
    
    # Ask user what they want to do
    print("\n🎯 Choose development action:")
    print("1. Run automated tests")
    print("2. Start development server")
    print("3. Run Madagascar test scenarios")
    print("4. Run all (tests + server)")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            test_simple_server()
        elif choice == "2":
            start_development_server()
        elif choice == "3":
            print("💡 Make sure to start the server first (choice 2)")
            run_madagascar_test_scenarios()
        elif choice == "4":
            if test_simple_server():
                print("\n🎉 Tests passed! Starting server...")
                start_development_server()
        else:
            print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
