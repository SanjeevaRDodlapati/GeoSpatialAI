"""
GBIF Data Validation and Debugging Script
=========================================

This script validates our GBIF data collection to ensure we're getting comprehensive
real-world data and not missing important species records.

Author: GeoSpatialAI Development Team  
Date: August 24, 2025
"""

import asyncio
import aiohttp
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GBIFValidationTester:
    """Test and validate GBIF API responses to ensure comprehensive data collection."""
    
    def __init__(self):
        self.base_url = "https://api.gbif.org/v1"
        
    async def test_gbif_comprehensive_search(self, lat: float, lon: float, area_name: str):
        """Test comprehensive GBIF search with multiple parameters."""
        
        logger.info(f"🔍 Testing comprehensive GBIF search for {area_name}")
        logger.info(f"📍 Coordinates: ({lat}, {lon})")
        
        async with aiohttp.ClientSession() as session:
            
            # Test 1: Basic species occurrence search (our current method)
            logger.info("\n1️⃣ Testing basic species occurrence search...")
            basic_url = f"{self.base_url}/occurrence/search"
            basic_params = {
                'decimalLatitude': lat,
                'decimalLongitude': lon,
                'radius': 10000,  # 10km radius in meters
                'limit': 300,
                'hasCoordinate': 'true',
                'hasGeospatialIssue': 'false'
            }
            
            async with session.get(basic_url, params=basic_params) as response:
                if response.status == 200:
                    basic_data = await response.json()
                    basic_count = basic_data.get('count', 0)
                    basic_results = basic_data.get('results', [])
                    logger.info(f"   📊 Basic search: {basic_count} total occurrences available")
                    logger.info(f"   📦 Retrieved: {len(basic_results)} records")
                    
                    # Analyze taxonomic diversity
                    kingdoms = set()
                    classes = set()
                    families = set()
                    species = set()
                    
                    for record in basic_results:
                        if record.get('kingdom'):
                            kingdoms.add(record['kingdom'])
                        if record.get('class'):
                            classes.add(record['class'])
                        if record.get('family'):
                            families.add(record['family'])
                        if record.get('species'):
                            species.add(record['species'])
                    
                    logger.info(f"   🧬 Taxonomic diversity:")
                    logger.info(f"      Kingdoms: {len(kingdoms)} ({list(kingdoms)})")
                    logger.info(f"      Classes: {len(classes)}")
                    logger.info(f"      Families: {len(families)}")
                    logger.info(f"      Unique species: {len(species)}")
                    
                    # Show sample species
                    logger.info(f"   🦋 Sample species found:")
                    for i, record in enumerate(basic_results[:10]):
                        species_name = record.get('species', 'Unknown')
                        kingdom = record.get('kingdom', 'Unknown')
                        class_name = record.get('class', 'Unknown')
                        year = record.get('year', 'Unknown')
                        logger.info(f"      {i+1}. {species_name} ({class_name}, {kingdom}) - {year}")
                else:
                    logger.error(f"❌ Basic search failed: {response.status}")
            
            # Test 2: Animal-only search
            logger.info(f"\n2️⃣ Testing animal-only search...")
            animal_params = {
                **basic_params,
                'kingdom': 'Animalia'
            }
            
            async with session.get(basic_url, params=animal_params) as response:
                if response.status == 200:
                    animal_data = await response.json()
                    animal_count = animal_data.get('count', 0)
                    animal_results = animal_data.get('results', [])
                    logger.info(f"   📊 Animal-only search: {animal_count} total animal occurrences")
                    logger.info(f"   📦 Retrieved: {len(animal_results)} animal records")
                    
                    # Analyze animal classes
                    animal_classes = set()
                    for record in animal_results:
                        if record.get('class'):
                            animal_classes.add(record['class'])
                    
                    logger.info(f"   🐾 Animal classes: {list(animal_classes)}")
                else:
                    logger.error(f"❌ Animal search failed: {response.status}")
            
            # Test 3: Plant-only search
            logger.info(f"\n3️⃣ Testing plant-only search...")
            plant_params = {
                **basic_params,
                'kingdom': 'Plantae'
            }
            
            async with session.get(basic_url, params=plant_params) as response:
                if response.status == 200:
                    plant_data = await response.json()
                    plant_count = plant_data.get('count', 0)
                    plant_results = plant_data.get('results', [])
                    logger.info(f"   📊 Plant-only search: {plant_count} total plant occurrences")
                    logger.info(f"   📦 Retrieved: {len(plant_results)} plant records")
                else:
                    logger.error(f"❌ Plant search failed: {response.status}")
            
            # Test 4: Specific taxonomic groups
            logger.info(f"\n4️⃣ Testing specific Madagascar fauna...")
            
            # Birds
            bird_params = {
                **basic_params,
                'class': 'Aves'
            }
            async with session.get(basic_url, params=bird_params) as response:
                if response.status == 200:
                    bird_data = await response.json()
                    bird_count = bird_data.get('count', 0)
                    logger.info(f"   🐦 Birds: {bird_count} occurrences")
                    
            # Reptiles
            reptile_params = {
                **basic_params,
                'class': 'Reptilia'
            }
            async with session.get(basic_url, params=reptile_params) as response:
                if response.status == 200:
                    reptile_data = await response.json()
                    reptile_count = reptile_data.get('count', 0)
                    logger.info(f"   🦎 Reptiles: {reptile_count} occurrences")
            
            # Amphibians
            amphibian_params = {
                **basic_params,
                'class': 'Amphibia'
            }
            async with session.get(basic_url, params=amphibian_params) as response:
                if response.status == 200:
                    amphibian_data = await response.json()
                    amphibian_count = amphibian_data.get('count', 0)
                    logger.info(f"   🐸 Amphibians: {amphibian_count} occurrences")
            
            # Mammals
            mammal_params = {
                **basic_params,
                'class': 'Mammalia'
            }
            async with session.get(basic_url, params=mammal_params) as response:
                if response.status == 200:
                    mammal_data = await response.json()
                    mammal_count = mammal_data.get('count', 0)
                    logger.info(f"   🐾 Mammals: {mammal_count} occurrences")
            
            # Test 5: Larger radius search
            logger.info(f"\n5️⃣ Testing larger radius search (50km)...")
            large_radius_params = {
                'decimalLatitude': lat,
                'decimalLongitude': lon,
                'radius': 50000,  # 50km radius
                'limit': 300,
                'hasCoordinate': 'true',
                'hasGeospatialIssue': 'false'
            }
            
            async with session.get(basic_url, params=large_radius_params) as response:
                if response.status == 200:
                    large_data = await response.json()
                    large_count = large_data.get('count', 0)
                    large_results = large_data.get('results', [])
                    logger.info(f"   📊 Large radius (50km): {large_count} total occurrences")
                    logger.info(f"   📦 Retrieved: {len(large_results)} records")
                    
                    # Count unique species in larger radius
                    large_species = set()
                    for record in large_results:
                        if record.get('species'):
                            large_species.add(record['species'])
                    logger.info(f"   🔬 Unique species in 50km: {len(large_species)}")
                else:
                    logger.error(f"❌ Large radius search failed: {response.status}")
            
            # Test 6: Check data quality and basis of record
            logger.info(f"\n6️⃣ Analyzing data quality...")
            if 'basic_results' in locals():
                basis_counts = {}
                years = []
                institutions = set()
                
                for record in basic_results:
                    basis = record.get('basisOfRecord', 'Unknown')
                    basis_counts[basis] = basis_counts.get(basis, 0) + 1
                    
                    if record.get('year'):
                        years.append(record['year'])
                    
                    if record.get('institutionCode'):
                        institutions.add(record['institutionCode'])
                
                logger.info(f"   📋 Basis of record distribution:")
                for basis, count in basis_counts.items():
                    logger.info(f"      {basis}: {count} records")
                
                if years:
                    logger.info(f"   📅 Year range: {min(years)} - {max(years)}")
                    logger.info(f"   📈 Total years covered: {len(set(years))}")
                
                logger.info(f"   🏛️ Contributing institutions: {len(institutions)}")
                logger.info(f"      Sample institutions: {list(institutions)[:10]}")

async def validate_all_conservation_areas():
    """Validate GBIF data for all our conservation areas."""
    
    print("🔍 GBIF DATA VALIDATION AND DEBUGGING")
    print("=" * 60)
    
    validator = GBIFValidationTester()
    
    # Test all our conservation areas
    test_areas = [
        ("Andasibe-Mantadia National Park", -18.9333, 48.4167),
        ("Ranomafana National Park", -21.25, 47.4167),
        ("Masoala National Park", -15.7, 50.2333),
        ("Isalo National Park", -22.55, 45.3167)
    ]
    
    for area_name, lat, lon in test_areas:
        print(f"\n{'='*60}")
        print(f"TESTING: {area_name}")
        print(f"{'='*60}")
        
        await validator.test_gbif_comprehensive_search(lat, lon, area_name)
        
        print(f"\n" + "─" * 60)
    
    print(f"\n✅ VALIDATION COMPLETE")
    print(f"🔬 This test shows actual GBIF API responses vs our cached data")
    print(f"📊 Helps identify if we're missing data or if GBIF has limited records")

if __name__ == "__main__":
    try:
        asyncio.run(validate_all_conservation_areas())
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        import traceback
        traceback.print_exc()
