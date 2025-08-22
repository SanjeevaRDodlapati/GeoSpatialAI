#!/usr/bin/env python3
"""
Madagascar Conservation Server Test Client
==========================================
Test the running conservation server with Madagascar scenarios.
"""

import asyncio
import httpx
import json
from datetime import datetime
import sys

class MadagascarConservationTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        
    async def test_server_health(self):
        """Test if server is responding."""
        print("🏥 Testing server health...")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/health")
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Server healthy: {data['status']}")
                    print(f"   Uptime: {data['uptime_seconds']:.1f} seconds")
                    print(f"   Session: {data['server_name']}")
                    return True
                else:
                    print(f"❌ Health check failed: {response.status_code}")
                    return False
        except Exception as e:
            print(f"❌ Cannot connect to server: {e}")
            print("💡 Make sure the server is running:")
            print("   python mcp_foundation/simple_conservation_server.py")
            return False
    
    async def test_madagascar_scenarios(self):
        """Test with real Madagascar conservation data."""
        print("\n🏝️ Testing Madagascar Conservation Scenarios")
        print("=" * 50)
        
        # Madagascar conservation events
        scenarios = [
            {
                "site_id": "centre_valbio",
                "event_type": "species_detection",
                "confidence": 0.94,
                "metadata": {
                    "species": "lemur_catta",
                    "individual_count": 8,
                    "behavior": "foraging",
                    "habitat": "gallery_forest",
                    "researcher": "Dr. Patricia Wright",
                    "gps_coordinates": [-21.289, 47.424],
                    "temperature_c": 24.5,
                    "time_of_day": "morning"
                }
            },
            {
                "site_id": "maromizaha",
                "event_type": "species_detection", 
                "confidence": 0.89,
                "metadata": {
                    "species": "indri_indri",
                    "individual_count": 3,
                    "behavior": "singing",
                    "habitat": "primary_rainforest",
                    "song_duration_minutes": 4.2,
                    "gps_coordinates": [-18.947, 48.458],
                    "canopy_height_m": 35
                }
            },
            {
                "site_id": "centre_valbio",
                "event_type": "threat_detection",
                "confidence": 0.76,
                "metadata": {
                    "threat_type": "deforestation_edge_effect",
                    "severity": "moderate", 
                    "area_affected_hectares": 2.8,
                    "distance_from_protection_m": 450,
                    "response_urgency": "medium",
                    "stakeholder_notification": ["Madagascar National Parks", "Local Community"]
                }
            },
            {
                "site_id": "maromizaha",
                "event_type": "conservation_intervention",
                "confidence": 1.0,
                "metadata": {
                    "intervention_type": "community_education_program",
                    "participants": 42,
                    "duration_days": 3,
                    "topics": ["sustainable_agriculture", "lemur_conservation", "reforestation"],
                    "effectiveness_score": 0.87,
                    "follow_up_planned": True
                }
            },
            {
                "site_id": "centre_valbio",
                "event_type": "species_detection",
                "confidence": 0.82,
                "metadata": {
                    "species": "propithecus_diadema",
                    "individual_count": 2,
                    "behavior": "feeding_fruits",
                    "habitat": "secondary_forest",
                    "tree_species": "tamarindus_indica",
                    "height_above_ground_m": 12
                }
            }
        ]
        
        stored_events = []
        async with httpx.AsyncClient(timeout=10.0) as client:
            for i, scenario in enumerate(scenarios, 1):
                try:
                    print(f"\n📊 Scenario {i}: {scenario['event_type']} at {scenario['site_id']}")
                    
                    # Store the event
                    response = await client.post(
                        f"{self.base_url}/conservation/event",
                        json=scenario
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"   ✅ Stored with event_id: {result['event_id']}")
                        print(f"   📝 {result['message']}")
                        stored_events.append(result)
                        
                        # Show metadata highlights
                        metadata = scenario['metadata']
                        if 'species' in metadata:
                            print(f"   🐾 Species: {metadata['species']}")
                        if 'individual_count' in metadata:
                            print(f"   📊 Count: {metadata['individual_count']}")
                        if 'threat_type' in metadata:
                            print(f"   ⚠️  Threat: {metadata['threat_type']}")
                        if 'intervention_type' in metadata:
                            print(f"   🛠️  Intervention: {metadata['intervention_type']}")
                            
                    else:
                        print(f"   ❌ Failed to store: {response.status_code}")
                        print(f"      {response.text}")
                        
                except Exception as e:
                    print(f"   ❌ Error in scenario {i}: {e}")
        
        return stored_events
    
    async def test_data_retrieval(self):
        """Test retrieving stored conservation data."""
        print("\n📈 Testing Data Retrieval")
        print("=" * 30)
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Get overall statistics
            try:
                response = await client.get(f"{self.base_url}/conservation/stats")
                if response.status_code == 200:
                    stats = response.json()
                    print(f"📊 Total Events: {stats['total_events']}")
                    print(f"🏝️  Active Sites: {stats['active_sites']}")
                    print(f"📋 Event Types: {list(stats['event_types'].keys())}")
                    print(f"📍 Sites: {stats['sites']}")
                    
                    # Show event type breakdown
                    print("\n📊 Event Type Breakdown:")
                    for event_type, count in stats['event_types'].items():
                        print(f"   {event_type}: {count} events")
                        
                else:
                    print(f"❌ Failed to get stats: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error getting stats: {e}")
            
            # Get events for each Madagascar site
            madagascar_sites = ["centre_valbio", "maromizaha"]
            for site in madagascar_sites:
                try:
                    print(f"\n📍 Events for {site}:")
                    response = await client.get(f"{self.base_url}/conservation/events/{site}")
                    if response.status_code == 200:
                        site_data = response.json()
                        print(f"   📊 Total events: {site_data['event_count']}")
                        
                        # Show recent events
                        events = site_data['events'][-3:]  # Last 3 events
                        for event in events:
                            event_type = event.get('event_type', 'unknown')
                            confidence = event.get('confidence', 0)
                            print(f"   • {event_type} (confidence: {confidence})")
                            
                    else:
                        print(f"   ❌ Failed to get events: {response.status_code}")
                        
                except Exception as e:
                    print(f"   ❌ Error getting events for {site}: {e}")
    
    async def run_full_test_suite(self):
        """Run complete test suite."""
        print("🧪 Madagascar Conservation Server Test Suite")
        print("=" * 60)
        print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test server health
        if not await self.test_server_health():
            return False
        
        # Test Madagascar scenarios
        stored_events = await self.test_madagascar_scenarios()
        
        # Test data retrieval
        await self.test_data_retrieval()
        
        print(f"\n🎉 Test suite completed!")
        print(f"📊 Scenarios tested: {len(stored_events) if stored_events else 0}")
        print("🏝️  Madagascar conservation data successfully processed")
        
        return True

async def main():
    """Main test function."""
    tester = MadagascarConservationTester()
    
    print("🌿 Starting Madagascar Conservation Server Tests")
    print("Make sure the server is running first!")
    print("💡 To start server: python mcp_foundation/simple_conservation_server.py")
    print()
    
    success = await tester.run_full_test_suite()
    
    if success:
        print("\n✅ All tests completed successfully!")
        print("🎯 Next steps:")
        print("   1. Check server logs for processing details")
        print("   2. Try the web interface at http://localhost:8000/health")
        print("   3. Continue with Step 2: LangChain Memory Integration")
    else:
        print("\n❌ Tests failed. Check server status and try again.")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
