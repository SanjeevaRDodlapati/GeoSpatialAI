"""
Conservation Database Example Records Generator
==============================================

Generates realistic example records from each conservation database
to provide concrete understanding of data structures and field contents.

Author: GeoSpatialAI Development Team
Date: August 24, 2025
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random

class ConservationExampleRecordsGenerator:
    """
    Generates realistic example records from each conservation database
    to illustrate actual data structures and field contents.
    """
    
    def __init__(self):
        self.madagascar_coordinates = {
            "lat_range": (-25.6, -11.9),
            "lng_range": (43.2, 50.5)
        }
        
        self.sample_species = [
            {
                "scientific_name": "Lemur catta",
                "common_name": "Ring-tailed Lemur",
                "kingdom": "Animalia",
                "phylum": "Chordata",
                "class": "Mammalia",
                "order": "Primates",
                "family": "Lemuridae",
                "genus": "Lemur",
                "species": "catta",
                "iucn_status": "EN"
            },
            {
                "scientific_name": "Coua cristata",
                "common_name": "Crested Coua",
                "kingdom": "Animalia",
                "phylum": "Chordata",
                "class": "Aves",
                "order": "Cuculiformes",
                "family": "Cuculidae",
                "genus": "Coua",
                "species": "cristata",
                "iucn_status": "LC"
            },
            {
                "scientific_name": "Brookesia micra",
                "common_name": "Nosy Hara Leaf Chameleon",
                "kingdom": "Animalia",
                "phylum": "Chordata",
                "class": "Reptilia",
                "order": "Squamata",
                "family": "Chamaeleonidae",
                "genus": "Brookesia",
                "species": "micra",
                "iucn_status": "NT"
            },
            {
                "scientific_name": "Eulemur fulvus",
                "common_name": "Brown Lemur",
                "kingdom": "Animalia",
                "phylum": "Chordata",
                "class": "Mammalia",
                "order": "Primates",
                "family": "Lemuridae",
                "genus": "Eulemur",
                "species": "fulvus",
                "iucn_status": "NT"
            },
            {
                "scientific_name": "Vanga curvirostris",
                "common_name": "Hook-billed Vanga",
                "kingdom": "Animalia",
                "phylum": "Chordata",
                "class": "Aves",
                "order": "Passeriformes",
                "family": "Vangidae",
                "genus": "Vanga",
                "species": "curvirostris",
                "iucn_status": "LC"
            }
        ]
    
    def generate_gbif_examples(self) -> List[Dict]:
        """Generate realistic GBIF record examples."""
        
        examples = []
        
        for i, species in enumerate(self.sample_species[:3]):
            lat = random.uniform(*self.madagascar_coordinates["lat_range"])
            lng = random.uniform(*self.madagascar_coordinates["lng_range"])
            
            record = {
                "gbifID": 2542976549 + i,
                "datasetKey": f"50c9509d-22c7-4a22-a47d-8c48425ef4a{i}",
                "occurrenceID": f"urn:catalog:USNM:Mammals:{12345 + i}",
                "kingdom": species["kingdom"],
                "phylum": species["phylum"],
                "class": species["class"],
                "order": species["order"],
                "family": species["family"],
                "genus": species["genus"],
                "species": species["species"],
                "scientificName": f"{species['scientific_name']} (Linnaeus, 1758)",
                "vernacularName": species["common_name"],
                "taxonomicStatus": "ACCEPTED",
                "decimalLatitude": round(lat, 6),
                "decimalLongitude": round(lng, 6),
                "coordinateUncertaintyInMeters": random.choice([10, 25, 50, 100, 250]),
                "country": "MG",
                "stateProvince": random.choice(["Antananarivo", "Toamasina", "Mahajanga", "Fianarantsoa"]),
                "locality": f"Andasibe-Mantadia National Park, {random.choice(['Trail A', 'Trail B', 'Camping Area'])}",
                "elevation": random.randint(800, 1200),
                "depth": None,
                "eventDate": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                "year": 2024,
                "month": random.randint(1, 12),
                "day": random.randint(1, 28),
                "basisOfRecord": random.choice(["HUMAN_OBSERVATION", "PRESERVED_SPECIMEN", "MACHINE_OBSERVATION"]),
                "institutionCode": random.choice(["USNM", "MNHN", "BMNH", "FMNH"]),
                "collectionCode": random.choice(["Mammals", "Birds", "Reptiles"]),
                "recordedBy": random.choice(["Dr. Jane Smith", "Research Team Alpha", "Conservation Survey 2024"]),
                "identifiedBy": random.choice(["Dr. John Doe", "Species Expert", "Field Team Lead"]),
                "license": "CC_BY_4_0",
                "hasCoordinate": True,
                "hasGeospatialIssue": False,
                "multimedia": [
                    {
                        "type": "StillImage",
                        "format": "image/jpeg",
                        "identifier": f"https://api.gbif.org/v1/image/{1234567 + i}.jpg",
                        "references": f"https://www.gbif.org/occurrence/{2542976549 + i}",
                        "title": f"Photo of {species['common_name']}",
                        "description": f"Field photograph of {species['scientific_name']} in natural habitat",
                        "created": "2024-03-15T10:30:00Z",
                        "creator": "Dr. Jane Smith",
                        "publisher": "Madagascar Biodiversity Survey",
                        "license": "CC_BY_4_0"
                    }
                ]
            }
            examples.append(record)
        
        return examples
    
    def generate_ebird_examples(self) -> List[Dict]:
        """Generate realistic eBird record examples."""
        
        examples = []
        bird_species = [s for s in self.sample_species if s["class"] == "Aves"]
        
        for i, species in enumerate(bird_species):
            lat = random.uniform(*self.madagascar_coordinates["lat_range"])
            lng = random.uniform(*self.madagascar_coordinates["lng_range"])
            
            record = {
                "speciesCode": f"{species['genus'][:3].lower()}{species['species'][:3].lower()}",
                "comName": species["common_name"],
                "sciName": species["scientific_name"],
                "locId": f"L{7654321 + i}",
                "locName": random.choice([
                    "Andasibe-Mantadia National Park",
                    "Ankarafantsika National Park", 
                    "Isalo National Park",
                    "Masoala National Park"
                ]),
                "obsDt": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M"),
                "howMany": random.randint(1, 8),
                "lat": round(lat, 6),
                "lng": round(lng, 6),
                "obsValid": True,
                "obsReviewed": True,
                "locationPrivate": False,
                "subId": f"S{87654321 + i}",
                "subnational1Code": "MG-T",
                "subnational1Name": "Toamasina",
                "countryCode": "MG",
                "countryName": "Madagascar",
                "userDisplayName": random.choice(["BirdWatcher2024", "MadagascarBirder", "ConservationTeam"]),
                "numObservers": random.randint(1, 4),
                "obsDuration": random.randint(30, 180),  # minutes
                "obsDistance": round(random.uniform(0.5, 3.0), 1),  # km
                "obsProjectCode": "EBIRD",
                "obsAuxCode": random.choice(["traveling", "stationary", "area"]),
                "breeding": random.choice([None, "NY", "ON", "FL"]),  # breeding codes
                "atlasBlock": None,
                "checklistComments": f"Beautiful sighting of {species['common_name']} in pristine forest habitat",
                "speciesComments": f"Adult {species['common_name']}, actively foraging in canopy"
            }
            examples.append(record)
        
        return examples
    
    def generate_inaturalist_examples(self) -> List[Dict]:
        """Generate realistic iNaturalist record examples."""
        
        examples = []
        
        for i, species in enumerate(self.sample_species[:3]):
            lat = random.uniform(*self.madagascar_coordinates["lat_range"])
            lng = random.uniform(*self.madagascar_coordinates["lng_range"])
            
            record = {
                "id": 12345678 + i,
                "observed_on": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
                "time_observed_at": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
                "time_zone": "Indian/Antananarivo",
                "location": f"{lat},{lng}",
                "place_guess": f"Andasibe-Mantadia National Park, Madagascar",
                "latitude": str(round(lat, 6)),
                "longitude": str(round(lng, 6)),
                "positional_accuracy": random.randint(5, 50),
                "quality_grade": random.choice(["research", "needs_id", "casual"]),
                "user": {
                    "id": 54321 + i,
                    "login": f"naturalist{2024 + i}",
                    "name": f"Madagascar Explorer {i+1}",
                    "icon": f"https://static.inaturalist.org/attachments/users/icons/{54321 + i}/medium.jpg"
                },
                "taxon": {
                    "id": 98765 + i,
                    "name": species["scientific_name"],
                    "rank": "species",
                    "common_name": {
                        "name": species["common_name"]
                    },
                    "preferred_common_name": species["common_name"],
                    "wikipedia_url": f"https://en.wikipedia.org/wiki/{species['genus']}_{species['species']}",
                    "ancestry": f"{species['kingdom']}/{species['phylum']}/{species['class']}/{species['order']}/{species['family']}/{species['genus']}"
                },
                "photos": [
                    {
                        "id": 23456789 + i,
                        "url": f"https://inaturalist-open-data.s3.amazonaws.com/photos/{23456789 + i}/medium.jpg",
                        "attribution": f"(c) Madagascar Explorer {i+1}, some rights reserved (CC BY-NC)",
                        "license_code": "cc-by-nc",
                        "width": 2048,
                        "height": 1536
                    }
                ],
                "sounds": [],
                "identifications": [
                    {
                        "id": 34567890 + i,
                        "user": {
                            "id": 11111 + i,
                            "login": f"expert_identifier_{i}",
                            "name": f"Dr. Species Expert {i+1}"
                        },
                        "taxon": {
                            "id": 98765 + i,
                            "name": species["scientific_name"],
                            "common_name": species["common_name"]
                        },
                        "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                        "body": f"Great photo! This is definitely {species['scientific_name']}. Note the distinctive {random.choice(['coloration', 'markings', 'size', 'habitat preference'])}.",
                        "current": True
                    }
                ],
                "comments": [
                    {
                        "id": 45678901 + i,
                        "user": {
                            "login": "conservation_researcher",
                            "name": "Conservation Researcher"
                        },
                        "body": f"Fantastic find! {species['common_name']} is {species['iucn_status']} status according to IUCN. Important for conservation monitoring.",
                        "created_at": (datetime.now() - timedelta(days=random.randint(1, 20))).isoformat()
                    }
                ],
                "project_observations": [
                    {
                        "project": {
                            "id": 9999,
                            "title": "Madagascar Biodiversity Project",
                            "description": "Documenting Madagascar's unique biodiversity"
                        }
                    }
                ],
                "faves": [
                    {
                        "user": {
                            "login": "nature_lover_2024",
                            "name": "Nature Lover"
                        }
                    }
                ],
                "uri": f"https://www.inaturalist.org/observations/{12345678 + i}",
                "cached_votes_total": random.randint(3, 15),
                "identifications_most_agree": True,
                "identifications_most_disagree": False,
                "identifications_count": random.randint(2, 8)
            }
            examples.append(record)
        
        return examples
    
    def generate_iucn_examples(self) -> List[Dict]:
        """Generate realistic IUCN Red List record examples."""
        
        examples = []
        
        for i, species in enumerate(self.sample_species):
            record = {
                "taxonid": 98765432 + i,
                "scientific_name": species["scientific_name"],
                "kingdom": species["kingdom"],
                "phylum": species["phylum"],
                "class": species["class"],
                "order": species["order"],
                "family": species["family"],
                "genus": species["genus"],
                "main_common_name": species["common_name"],
                "authority": "(Linnaeus, 1758)" if i == 0 else f"(Author, {1800 + i*20})",
                "published_year": 2022,
                "assessment_date": "2022-03-15",
                "category": species["iucn_status"],
                "criteria": {
                    "EN": "A2acd",
                    "NT": "A3c",
                    "LC": None,
                    "VU": "A2bc",
                    "CR": "A1ac"
                }.get(species["iucn_status"]),
                "population_trend": random.choice(["Decreasing", "Stable", "Increasing", "Unknown"]),
                "marine_system": False,
                "freshwater_system": False,
                "terrestrial_system": True,
                "assessor": random.choice([
                    "Dr. Conservation Expert",
                    "IUCN Species Specialist Group",
                    "Madagascar Wildlife Assessment Team"
                ]),
                "reviewer": "IUCN Red List Review Board",
                "aoo_km2": random.choice([None, 1500, 2300, 890, 4500]),
                "eoo_km2": random.choice([None, 15000, 23000, 8900, 45000]),
                "elevation_upper": random.randint(1000, 2000),
                "elevation_lower": random.randint(0, 500),
                "depth_upper": None,
                "depth_lower": None,
                "errata_flag": False,
                "errata_reason": None,
                "amended_flag": False,
                "amended_reason": None,
                "threats": [
                    {
                        "code": "2.1.2",
                        "title": "Logging & wood harvesting - Small-holder farming",
                        "timing": "Ongoing",
                        "scope": "Majority (50-90%)",
                        "severity": "Slow, Significant Declines",
                        "score": "Medium Impact: 6",
                        "invasive": None
                    },
                    {
                        "code": "7.1.1", 
                        "title": "Fire & fire suppression - Increase in fire frequency/intensity",
                        "timing": "Ongoing",
                        "scope": "Minority (< 50%)",
                        "severity": "Slow, Significant Declines",
                        "score": "Low Impact: 4",
                        "invasive": None
                    }
                ],
                "conservation_measures": [
                    {
                        "code": "1.1",
                        "title": "In-place land/water protection - In-place land/water protection",
                        "text": "Present in several protected areas including Andasibe-Mantadia National Park"
                    },
                    {
                        "code": "4.3",
                        "title": "Education & awareness - Awareness & communications",
                        "text": "Local community education programs about species importance"
                    }
                ],
                "habitats": [
                    {
                        "code": "1.6",
                        "habitat": "Forest - Subtropical/Tropical Moist Lowland",
                        "suitability": "Suitable",
                        "season": "Resident",
                        "majorimportance": "Yes"
                    },
                    {
                        "code": "1.9",
                        "habitat": "Forest - Subtropical/Tropical Moist Montane",
                        "suitability": "Suitable", 
                        "season": "Resident",
                        "majorimportance": "No"
                    }
                ],
                "countries": [
                    {
                        "code": "MG",
                        "country": "Madagascar",
                        "presence": "Extant",
                        "origin": "Native",
                        "distribution_code": "Native"
                    }
                ]
            }
            examples.append(record)
        
        return examples
    
    def generate_nasa_firms_examples(self) -> List[Dict]:
        """Generate realistic NASA FIRMS fire detection examples."""
        
        examples = []
        
        # Generate fire detections around Madagascar
        for i in range(5):
            lat = random.uniform(*self.madagascar_coordinates["lat_range"])
            lng = random.uniform(*self.madagascar_coordinates["lng_range"])
            detection_date = datetime.now() - timedelta(days=random.randint(0, 30))
            
            record = {
                "latitude": round(lat, 4),
                "longitude": round(lng, 4),
                "brightness": round(random.uniform(300.0, 450.0), 1),
                "scan": round(random.uniform(0.5, 2.0), 1),
                "track": round(random.uniform(0.8, 1.5), 1),
                "acq_date": detection_date.strftime("%Y-%m-%d"),
                "acq_time": f"{random.randint(0, 23):02d}{random.randint(0, 59):02d}",
                "satellite": random.choice(["T", "A", "N"]),  # Terra, Aqua, NPP
                "instrument": {"T": "MODIS", "A": "MODIS", "N": "VIIRS"}[random.choice(["T", "A", "N"])],
                "confidence": random.choice([
                    # MODIS confidence levels
                    {"value": 85, "class": "high"} if random.choice(["T", "A"]) else 
                    # VIIRS confidence levels  
                    {"value": 95, "class": "high"}
                ]),
                "version": "6.1" if random.choice([True, False]) else "2.0",
                "bright_t31": round(random.uniform(280.0, 320.0), 1),
                "frp": round(random.uniform(5.0, 150.0), 1),  # Fire Radiative Power (MW)
                "daynight": random.choice(["D", "N"]),
                "type": 0,  # 0 = presumed vegetation fire
                "acquisition_datetime": detection_date.isoformat(),
                "granule_id": f"MOD14.A{detection_date.strftime('%Y%j')}.{random.randint(1000, 2359)}.061.{random.randint(2022000000000, 2022999999999)}",
                "geographic_context": {
                    "country": "Madagascar",
                    "region": random.choice([
                        "Toliara Province", 
                        "Mahajanga Province",
                        "Antananarivo Province", 
                        "Fianarantsoa Province"
                    ]),
                    "distance_to_protected_area_km": round(random.uniform(0.5, 45.0), 1),
                    "land_cover": random.choice([
                        "Tropical dry forest",
                        "Savanna grassland", 
                        "Agricultural land",
                        "Spiny forest",
                        "Wetland margin"
                    ]),
                    "elevation_m": random.randint(10, 1200)
                },
                "fire_characteristics": {
                    "estimated_size_hectares": round(random.uniform(0.1, 25.0), 1),
                    "fire_intensity": random.choice(["Low", "Moderate", "High"]),
                    "burn_severity": random.choice(["Surface fire", "Crown fire", "Mixed severity"]),
                    "fire_cause": random.choice([
                        "Agricultural burning", 
                        "Land clearing",
                        "Natural (lightning)",
                        "Charcoal production",
                        "Unknown"
                    ])
                },
                "conservation_impact": {
                    "threatened_species_nearby": random.choice([True, False]),
                    "protected_area_threat_level": random.choice(["None", "Low", "Moderate", "High"]),
                    "habitat_type_affected": random.choice([
                        "Primary forest",
                        "Secondary forest", 
                        "Grassland",
                        "Agricultural land",
                        "Wetland"
                    ])
                }
            }
            examples.append(record)
        
        return examples
    
    def generate_integrated_examples(self) -> Dict:
        """Generate comprehensive example dataset showing all database structures."""
        
        integrated_examples = {
            "generation_timestamp": datetime.now().isoformat(),
            "location_focus": "Madagascar Conservation Areas",
            "coordinate_bounds": self.madagascar_coordinates,
            "example_records": {
                "gbif": {
                    "description": "Global Biodiversity Information Facility records showing occurrence data with taxonomic hierarchy, coordinates, and metadata",
                    "total_examples": 3,
                    "key_features": [
                        "Complete taxonomic hierarchy",
                        "Precise coordinates with uncertainty",
                        "Institutional and collection information",
                        "Multimedia extensions",
                        "Quality flags and validation"
                    ],
                    "records": self.generate_gbif_examples()
                },
                "ebird": {
                    "description": "eBird bird observation records with abundance data, validation status, and survey effort information",
                    "total_examples": 2,
                    "key_features": [
                        "Species abundance counts",
                        "Community validation",
                        "Survey effort data (duration, distance, observers)",
                        "Breeding behavior codes",
                        "Location and temporal precision"
                    ],
                    "records": self.generate_ebird_examples()
                },
                "inaturalist": {
                    "description": "iNaturalist community observations with photos, identifications, and social engagement data",
                    "total_examples": 3,
                    "key_features": [
                        "High-quality photos and multimedia",
                        "Community-based identifications", 
                        "Research-grade quality filtering",
                        "User engagement (comments, faves)",
                        "Project-based data organization"
                    ],
                    "records": self.generate_inaturalist_examples()
                },
                "iucn_red_list": {
                    "description": "IUCN Red List conservation assessments with threat analysis, conservation measures, and habitat information",
                    "total_examples": 5,
                    "key_features": [
                        "Expert-reviewed conservation status",
                        "Detailed threat assessments",
                        "Conservation action recommendations",
                        "Habitat requirements and distribution",
                        "Population trend analysis"
                    ],
                    "records": self.generate_iucn_examples()
                },
                "nasa_firms": {
                    "description": "NASA FIRMS real-time fire detection data with satellite measurements and conservation impact analysis",
                    "total_examples": 5,
                    "key_features": [
                        "Real-time satellite fire detection",
                        "Fire intensity measurements (brightness, FRP)",
                        "Multiple satellite sensors (MODIS, VIIRS)",
                        "Geographic and conservation context",
                        "Fire characteristics and impact assessment"
                    ],
                    "records": self.generate_nasa_firms_examples()
                }
            },
            "integration_examples": {
                "spatial_correlation": {
                    "description": "Example of correlating species observations with fire detections",
                    "scenario": "Ring-tailed Lemur observations within 10km of fire detections",
                    "method": "Spatial proximity analysis using coordinate buffering"
                },
                "temporal_correlation": {
                    "description": "Example of tracking species observations before/after fire events",
                    "scenario": "Bird observation frequency changes following fire events",
                    "method": "Time-series analysis with before/after comparison"
                },
                "conservation_integration": {
                    "description": "Example of combining conservation status with occurrence data",
                    "scenario": "Mapping threatened species distributions using IUCN + GBIF + eBird",
                    "method": "Taxonomic matching with status-weighted occurrence mapping"
                }
            },
            "data_quality_examples": {
                "high_quality_indicators": {
                    "gbif": "hasCoordinate=true, coordinateUncertaintyInMeters<100, basisOfRecord=PRESERVED_SPECIMEN",
                    "ebird": "obsValid=true, obsReviewed=true, numObservers>1",
                    "inaturalist": "quality_grade=research, identifications_count>2",
                    "iucn": "published_year>2020, assessor=IUCN Specialist Group",
                    "nasa_firms": "confidence>80, satellite=multiple"
                },
                "filtering_recommendations": {
                    "research_grade": "Apply highest quality filters for scientific analysis",
                    "conservation_planning": "Balance quality with coverage for comprehensive assessment",
                    "rapid_assessment": "Use validated recent data for quick biodiversity snapshots",
                    "public_engagement": "Include visual-rich data from iNaturalist for education"
                }
            }
        }
        
        return integrated_examples

def main():
    """Generate comprehensive example records from all conservation databases."""
    
    print("📋 CONSERVATION DATABASE EXAMPLE RECORDS GENERATOR")
    print("=" * 70)
    
    generator = ConservationExampleRecordsGenerator()
    
    # Generate integrated examples
    examples = generator.generate_integrated_examples()
    
    # Save examples
    output_file = f"conservation_database_examples_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ EXAMPLE RECORDS GENERATED!")
    print(f"📄 Comprehensive examples saved to: {output_file}")
    
    # Print summary
    print(f"\n🎯 EXAMPLE RECORDS SUMMARY:")
    for db_name, db_data in examples["example_records"].items():
        record_count = db_data["total_examples"]
        description = db_data["description"]
        print(f"   • {db_name.upper()}: {record_count} examples")
        print(f"     {description[:80]}...")
    
    print(f"\n📊 KEY FEATURES DEMONSTRATED:")
    total_examples = sum(db_data["total_examples"] for db_data in examples["example_records"].values())
    print(f"   • {total_examples} realistic example records")
    print(f"   • Madagascar-focused geographic coordinates")
    print(f"   • Multiple species across taxonomic groups")
    print(f"   • Real-world data structures and field contents")
    print(f"   • Integration scenarios and quality indicators")
    
    print(f"\n🔗 INTEGRATION CAPABILITIES SHOWN:")
    for integration_type, integration_info in examples["integration_examples"].items():
        print(f"   • {integration_type.replace('_', ' ').title()}: {integration_info['description']}")
    
    print(f"\n🚀 Ready for hands-on data structure analysis!")

if __name__ == "__main__":
    main()
