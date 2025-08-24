"""
Conservation Data Record Structure Analyzer
==========================================

Comprehensive analysis of data field types and structures available 
in each conservation database record.

Author: GeoSpatialAI Development Team
Date: August 24, 2025
"""

import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional
import requests
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

class ConservationDataStructureAnalyzer:
    """
    Analyzes the detailed structure and field types available in 
    conservation database records.
    """
    
    def __init__(self):
        self.data_structures = {}
        self.field_mappings = {}
        self.sample_records = {}
        
        # Load existing metadata
        self.metadata = self._load_existing_metadata()
    
    def _load_existing_metadata(self):
        """Load existing metadata files."""
        metadata_files = [
            "metadata_cache/global_metadata_discovery_20250824_043843.json",
            "real_world_data_analysis_report_20250824_042241.json"
        ]
        
        combined_metadata = {}
        for file_path in metadata_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    combined_metadata.update(data)
                    logger.info(f"✅ Loaded {file_path}")
            except FileNotFoundError:
                logger.warning(f"⚠️ File not found: {file_path}")
        
        return combined_metadata
    
    def analyze_gbif_record_structure(self) -> Dict:
        """Analyze GBIF record structure with field types and descriptions."""
        
        logger.info("🔍 Analyzing GBIF record structure...")
        
        gbif_structure = {
            "database": "GBIF (Global Biodiversity Information Facility)",
            "total_records": "3.2+ billion",
            "api_endpoint": "https://api.gbif.org/v1/occurrence",
            "core_fields": {
                # Occurrence Core Fields
                "gbifID": {
                    "type": "integer",
                    "description": "Unique GBIF identifier for the occurrence",
                    "example": 2542976549,
                    "required": True,
                    "use_case": "Record linking and deduplication"
                },
                "datasetKey": {
                    "type": "uuid",
                    "description": "UUID of the dataset containing this record",
                    "example": "50c9509d-22c7-4a22-a47d-8c48425ef4a7",
                    "required": True,
                    "use_case": "Data provenance and quality assessment"
                },
                "occurrenceID": {
                    "type": "string",
                    "description": "Original identifier from data provider",
                    "example": "urn:catalog:USNM:Mammals:12345",
                    "required": False,
                    "use_case": "Cross-referencing with source databases"
                },
                
                # Taxonomic Fields
                "kingdom": {
                    "type": "string",
                    "description": "Taxonomic kingdom",
                    "example": "Animalia",
                    "required": False,
                    "use_case": "High-level taxonomic filtering"
                },
                "phylum": {
                    "type": "string",
                    "description": "Taxonomic phylum",
                    "example": "Chordata",
                    "required": False,
                    "use_case": "Taxonomic classification"
                },
                "class": {
                    "type": "string",
                    "description": "Taxonomic class",
                    "example": "Aves",
                    "required": False,
                    "use_case": "Species group analysis (birds, mammals, etc.)"
                },
                "order": {
                    "type": "string",
                    "description": "Taxonomic order",
                    "example": "Passeriformes",
                    "required": False,
                    "use_case": "Detailed taxonomic analysis"
                },
                "family": {
                    "type": "string",
                    "description": "Taxonomic family",
                    "example": "Turdidae",
                    "required": False,
                    "use_case": "Family-level biodiversity studies"
                },
                "genus": {
                    "type": "string",
                    "description": "Taxonomic genus",
                    "example": "Turdus",
                    "required": False,
                    "use_case": "Genus-level distribution analysis"
                },
                "species": {
                    "type": "string",
                    "description": "Species epithet",
                    "example": "migratorius",
                    "required": False,
                    "use_case": "Species-specific studies"
                },
                "scientificName": {
                    "type": "string",
                    "description": "Complete scientific name with authorship",
                    "example": "Turdus migratorius Linnaeus, 1766",
                    "required": True,
                    "use_case": "Primary species identification"
                },
                "vernacularName": {
                    "type": "string",
                    "description": "Common name in local language",
                    "example": "American Robin",
                    "required": False,
                    "use_case": "Public communication and education"
                },
                "taxonomicStatus": {
                    "type": "string",
                    "description": "Nomenclatural status of the name",
                    "example": "ACCEPTED",
                    "required": False,
                    "use_case": "Taxonomic quality control"
                },
                
                # Geographic Fields
                "decimalLatitude": {
                    "type": "float",
                    "description": "Latitude in decimal degrees (WGS84)",
                    "example": 42.331429,
                    "required": False,
                    "use_case": "Spatial analysis and mapping"
                },
                "decimalLongitude": {
                    "type": "float",
                    "description": "Longitude in decimal degrees (WGS84)",
                    "example": -71.120611,
                    "required": False,
                    "use_case": "Spatial analysis and mapping"
                },
                "coordinateUncertaintyInMeters": {
                    "type": "float",
                    "description": "Uncertainty radius in meters",
                    "example": 100.0,
                    "required": False,
                    "use_case": "Spatial accuracy assessment"
                },
                "country": {
                    "type": "string",
                    "description": "ISO 3166-1 alpha-2 country code",
                    "example": "US",
                    "required": False,
                    "use_case": "Country-level analysis"
                },
                "stateProvince": {
                    "type": "string",
                    "description": "State or province name",
                    "example": "Massachusetts",
                    "required": False,
                    "use_case": "Regional distribution analysis"
                },
                "locality": {
                    "type": "string",
                    "description": "Specific locality description",
                    "example": "Harvard University, Cambridge",
                    "required": False,
                    "use_case": "Fine-scale habitat analysis"
                },
                "elevation": {
                    "type": "float",
                    "description": "Elevation above sea level in meters",
                    "example": 45.0,
                    "required": False,
                    "use_case": "Elevation range analysis"
                },
                "depth": {
                    "type": "float",
                    "description": "Depth below surface in meters",
                    "example": 10.5,
                    "required": False,
                    "use_case": "Marine/aquatic species analysis"
                },
                
                # Temporal Fields
                "eventDate": {
                    "type": "datetime",
                    "description": "Date/time of observation",
                    "example": "2023-05-15T08:30:00Z",
                    "required": False,
                    "use_case": "Temporal analysis and seasonality"
                },
                "year": {
                    "type": "integer",
                    "description": "Year of observation",
                    "example": 2023,
                    "required": False,
                    "use_case": "Annual trends analysis"
                },
                "month": {
                    "type": "integer",
                    "description": "Month of observation (1-12)",
                    "example": 5,
                    "required": False,
                    "use_case": "Seasonal pattern analysis"
                },
                "day": {
                    "type": "integer",
                    "description": "Day of month (1-31)",
                    "example": 15,
                    "required": False,
                    "use_case": "Daily activity patterns"
                },
                
                # Data Quality Fields
                "basisOfRecord": {
                    "type": "string",
                    "description": "Type of observation/record",
                    "example": "HUMAN_OBSERVATION",
                    "required": True,
                    "use_case": "Data quality filtering",
                    "values": [
                        "HUMAN_OBSERVATION",
                        "PRESERVED_SPECIMEN", 
                        "MACHINE_OBSERVATION",
                        "MATERIAL_SAMPLE",
                        "FOSSIL_SPECIMEN",
                        "LIVING_SPECIMEN"
                    ]
                },
                "institutionCode": {
                    "type": "string",
                    "description": "Institution holding the record",
                    "example": "MCZ",
                    "required": False,
                    "use_case": "Data provenance analysis"
                },
                "collectionCode": {
                    "type": "string",
                    "description": "Collection within institution",
                    "example": "Birds",
                    "required": False,
                    "use_case": "Collection-specific analysis"
                },
                "recordedBy": {
                    "type": "string",
                    "description": "Observer/collector name",
                    "example": "John Smith",
                    "required": False,
                    "use_case": "Observer effort analysis"
                },
                "identifiedBy": {
                    "type": "string",
                    "description": "Species identifier name",
                    "example": "Jane Doe",
                    "required": False,
                    "use_case": "Identification quality assessment"
                },
                "license": {
                    "type": "string",
                    "description": "Data usage license",
                    "example": "CC_BY_4_0",
                    "required": False,
                    "use_case": "Data usage rights"
                }
            },
            
            "quality_flags": {
                "hasCoordinate": {
                    "type": "boolean",
                    "description": "Record has valid coordinates",
                    "use_case": "Spatial analysis filtering"
                },
                "hasGeospatialIssue": {
                    "type": "boolean", 
                    "description": "Detected geospatial problems",
                    "use_case": "Quality control"
                },
                "coordinateUncertaintyInMeters": {
                    "type": "float",
                    "description": "Spatial precision indicator",
                    "use_case": "Precision-based filtering"
                }
            },
            
            "extensions": {
                "multimedia": {
                    "type": "array",
                    "description": "Images, sounds, videos",
                    "use_case": "Visual verification and analysis"
                },
                "measurements": {
                    "type": "array", 
                    "description": "Morphological measurements",
                    "use_case": "Trait-based ecology"
                },
                "identifications": {
                    "type": "array",
                    "description": "Identification history",
                    "use_case": "Taxonomic reliability assessment"
                }
            }
        }
        
        return gbif_structure
    
    def analyze_ebird_record_structure(self) -> Dict:
        """Analyze eBird record structure."""
        
        logger.info("🐦 Analyzing eBird record structure...")
        
        ebird_structure = {
            "database": "eBird",
            "total_records": "1+ billion observations",
            "api_endpoint": "https://ebird.org/ws2.0",
            "core_fields": {
                "speciesCode": {
                    "type": "string",
                    "description": "eBird species code",
                    "example": "amerob",
                    "required": True,
                    "use_case": "Species identification"
                },
                "comName": {
                    "type": "string",
                    "description": "Common name",
                    "example": "American Robin",
                    "required": True,
                    "use_case": "User-friendly species names"
                },
                "sciName": {
                    "type": "string",
                    "description": "Scientific name",
                    "example": "Turdus migratorius",
                    "required": True,
                    "use_case": "Scientific identification"
                },
                "locId": {
                    "type": "string",
                    "description": "Location identifier",
                    "example": "L123456",
                    "required": True,
                    "use_case": "Location-based analysis"
                },
                "locName": {
                    "type": "string",
                    "description": "Location name",
                    "example": "Central Park",
                    "required": True,
                    "use_case": "Site-specific studies"
                },
                "obsDt": {
                    "type": "datetime",
                    "description": "Observation date and time",
                    "example": "2023-05-15 08:30",
                    "required": True,
                    "use_case": "Temporal analysis"
                },
                "howMany": {
                    "type": "integer",
                    "description": "Number of individuals observed",
                    "example": 3,
                    "required": False,
                    "use_case": "Abundance analysis"
                },
                "lat": {
                    "type": "float",
                    "description": "Latitude in decimal degrees",
                    "example": 40.7829,
                    "required": True,
                    "use_case": "Spatial analysis"
                },
                "lng": {
                    "type": "float",
                    "description": "Longitude in decimal degrees", 
                    "example": -73.9654,
                    "required": True,
                    "use_case": "Spatial analysis"
                },
                "obsValid": {
                    "type": "boolean",
                    "description": "Observation validated by reviewers",
                    "example": True,
                    "required": True,
                    "use_case": "Quality filtering"
                },
                "obsReviewed": {
                    "type": "boolean",
                    "description": "Observation has been reviewed",
                    "example": True,
                    "required": True,
                    "use_case": "Quality assessment"
                },
                "locationPrivate": {
                    "type": "boolean",
                    "description": "Location coordinates are private",
                    "example": False,
                    "required": True,
                    "use_case": "Privacy consideration"
                },
                "subId": {
                    "type": "string",
                    "description": "Submission (checklist) identifier",
                    "example": "S12345678",
                    "required": True,
                    "use_case": "Checklist-based analysis"
                }
            },
            "specialized_fields": {
                "breeding_codes": {
                    "type": "string",
                    "description": "Breeding behavior indicators",
                    "use_case": "Breeding ecology studies"
                },
                "protocol_type": {
                    "type": "string",
                    "description": "Survey protocol used",
                    "use_case": "Effort standardization"
                },
                "duration_minutes": {
                    "type": "integer",
                    "description": "Survey duration",
                    "use_case": "Effort correction"
                },
                "distance_traveled_km": {
                    "type": "float",
                    "description": "Distance traveled during survey",
                    "use_case": "Effort standardization"
                },
                "number_observers": {
                    "type": "integer",
                    "description": "Number of observers",
                    "use_case": "Detection probability modeling"
                }
            }
        }
        
        return ebird_structure
    
    def analyze_inaturalist_record_structure(self) -> Dict:
        """Analyze iNaturalist record structure."""
        
        logger.info("📸 Analyzing iNaturalist record structure...")
        
        inaturalist_structure = {
            "database": "iNaturalist",
            "total_records": "268+ million observations",
            "api_endpoint": "https://api.inaturalist.org/v1",
            "core_fields": {
                "id": {
                    "type": "integer",
                    "description": "Unique observation identifier",
                    "example": 12345678,
                    "required": True,
                    "use_case": "Record identification"
                },
                "observed_on": {
                    "type": "date",
                    "description": "Date of observation",
                    "example": "2023-05-15",
                    "required": True,
                    "use_case": "Temporal analysis"
                },
                "time_observed_at": {
                    "type": "datetime",
                    "description": "Precise observation time",
                    "example": "2023-05-15T08:30:00Z",
                    "required": False,
                    "use_case": "Fine-scale temporal analysis"
                },
                "location": {
                    "type": "point",
                    "description": "Geographic coordinates",
                    "example": "40.7829,-73.9654",
                    "required": True,
                    "use_case": "Spatial analysis"
                },
                "place_guess": {
                    "type": "string",
                    "description": "Human-readable location",
                    "example": "Central Park, New York, NY, US",
                    "required": False,
                    "use_case": "Location context"
                },
                "quality_grade": {
                    "type": "string",
                    "description": "Data quality assessment",
                    "example": "research",
                    "required": True,
                    "use_case": "Quality filtering",
                    "values": ["casual", "needs_id", "research"]
                },
                "user": {
                    "type": "object",
                    "description": "Observer information",
                    "use_case": "Community analysis"
                },
                "taxon": {
                    "type": "object",
                    "description": "Taxonomic information",
                    "use_case": "Species identification",
                    "subfields": {
                        "id": "integer",
                        "name": "string",
                        "rank": "string",
                        "common_name": "string",
                        "preferred_common_name": "string"
                    }
                },
                "photos": {
                    "type": "array",
                    "description": "Observation photos",
                    "use_case": "Visual verification and AI analysis"
                },
                "sounds": {
                    "type": "array", 
                    "description": "Audio recordings",
                    "use_case": "Acoustic analysis"
                },
                "identifications": {
                    "type": "array",
                    "description": "Community identifications",
                    "use_case": "Identification confidence assessment"
                },
                "comments": {
                    "type": "array",
                    "description": "User comments",
                    "use_case": "Additional context and notes"
                },
                "faves": {
                    "type": "array",
                    "description": "User favorites/likes",
                    "use_case": "Community engagement metrics"
                }
            },
            "media_fields": {
                "photo_url": {
                    "type": "url",
                    "description": "Direct photo URL",
                    "use_case": "Image analysis and verification"
                },
                "photo_attribution": {
                    "type": "string",
                    "description": "Photo licensing information",
                    "use_case": "Usage rights"
                },
                "sound_url": {
                    "type": "url",
                    "description": "Audio file URL",
                    "use_case": "Acoustic species identification"
                }
            }
        }
        
        return inaturalist_structure
    
    def analyze_iucn_record_structure(self) -> Dict:
        """Analyze IUCN Red List record structure."""
        
        logger.info("🔴 Analyzing IUCN Red List record structure...")
        
        iucn_structure = {
            "database": "IUCN Red List of Threatened Species",
            "total_records": "150,000+ species assessments",
            "api_endpoint": "https://apiv3.iucnredlist.org/api/v3",
            "core_fields": {
                "taxonid": {
                    "type": "integer",
                    "description": "IUCN taxon identifier",
                    "example": 12345,
                    "required": True,
                    "use_case": "Species cross-referencing"
                },
                "scientific_name": {
                    "type": "string",
                    "description": "Full scientific name",
                    "example": "Panthera tigris",
                    "required": True,
                    "use_case": "Species identification"
                },
                "kingdom": {
                    "type": "string",
                    "description": "Taxonomic kingdom",
                    "example": "ANIMALIA",
                    "required": True,
                    "use_case": "High-level taxonomy"
                },
                "phylum": {
                    "type": "string",
                    "description": "Taxonomic phylum",
                    "example": "CHORDATA",
                    "required": True,
                    "use_case": "Taxonomic classification"
                },
                "class": {
                    "type": "string",
                    "description": "Taxonomic class", 
                    "example": "MAMMALIA",
                    "required": True,
                    "use_case": "Class-level analysis"
                },
                "order": {
                    "type": "string",
                    "description": "Taxonomic order",
                    "example": "CARNIVORA",
                    "required": True,
                    "use_case": "Order-level patterns"
                },
                "family": {
                    "type": "string",
                    "description": "Taxonomic family",
                    "example": "FELIDAE",
                    "required": True,
                    "use_case": "Family-level conservation"
                },
                "genus": {
                    "type": "string",
                    "description": "Taxonomic genus",
                    "example": "Panthera",
                    "required": True,
                    "use_case": "Genus-level analysis"
                },
                "main_common_name": {
                    "type": "string",
                    "description": "Primary common name",
                    "example": "Tiger",
                    "required": False,
                    "use_case": "Public communication"
                },
                "authority": {
                    "type": "string",
                    "description": "Taxonomic authority",
                    "example": "(Linnaeus, 1758)",
                    "required": False,
                    "use_case": "Nomenclatural reference"
                },
                "published_year": {
                    "type": "integer",
                    "description": "Assessment publication year",
                    "example": 2022,
                    "required": True,
                    "use_case": "Assessment currency"
                },
                "assessment_date": {
                    "type": "date",
                    "description": "Date of assessment",
                    "example": "2022-03-15",
                    "required": True,
                    "use_case": "Temporal analysis"
                },
                "category": {
                    "type": "string",
                    "description": "Conservation status category",
                    "example": "EN",
                    "required": True,
                    "use_case": "Conservation prioritization",
                    "values": ["EX", "EW", "CR", "EN", "VU", "NT", "LC", "DD", "NE"]
                },
                "criteria": {
                    "type": "string",
                    "description": "Assessment criteria used",
                    "example": "A2acd",
                    "required": False,
                    "use_case": "Assessment methodology"
                },
                "population_trend": {
                    "type": "string",
                    "description": "Population trend direction",
                    "example": "Decreasing",
                    "required": False,
                    "use_case": "Population dynamics",
                    "values": ["Increasing", "Stable", "Decreasing", "Unknown"]
                }
            },
            "conservation_fields": {
                "threats": {
                    "type": "array",
                    "description": "Threat categories and details",
                    "use_case": "Threat analysis and mitigation"
                },
                "conservation_measures": {
                    "type": "array",
                    "description": "Conservation actions",
                    "use_case": "Conservation planning"
                },
                "habitat": {
                    "type": "array",
                    "description": "Habitat requirements",
                    "use_case": "Habitat conservation"
                },
                "geographic_range": {
                    "type": "object",
                    "description": "Range information",
                    "use_case": "Spatial conservation planning"
                }
            }
        }
        
        return iucn_structure
    
    def analyze_nasa_firms_record_structure(self) -> Dict:
        """Analyze NASA FIRMS record structure."""
        
        logger.info("🔥 Analyzing NASA FIRMS record structure...")
        
        nasa_firms_structure = {
            "database": "NASA Fire Information for Resource Management System",
            "total_records": "Real-time fire detections",
            "api_endpoint": "https://firms.modaps.eosdis.nasa.gov/api",
            "core_fields": {
                "latitude": {
                    "type": "float",
                    "description": "Fire detection latitude",
                    "example": -18.95,
                    "required": True,
                    "use_case": "Spatial fire analysis"
                },
                "longitude": {
                    "type": "float",
                    "description": "Fire detection longitude",
                    "example": 47.52,
                    "required": True,
                    "use_case": "Spatial fire analysis"
                },
                "brightness": {
                    "type": "float",
                    "description": "Fire brightness temperature (Kelvin)",
                    "example": 325.4,
                    "required": True,
                    "use_case": "Fire intensity analysis"
                },
                "scan": {
                    "type": "float",
                    "description": "Scan angle",
                    "example": 1.1,
                    "required": True,
                    "use_case": "Detection quality assessment"
                },
                "track": {
                    "type": "float",
                    "description": "Track angle",
                    "example": 1.0,
                    "required": True,
                    "use_case": "Detection geometry"
                },
                "acq_date": {
                    "type": "date",
                    "description": "Acquisition date",
                    "example": "2023-05-15",
                    "required": True,
                    "use_case": "Temporal fire analysis"
                },
                "acq_time": {
                    "type": "time",
                    "description": "Acquisition time (HHMM)",
                    "example": "1423",
                    "required": True,
                    "use_case": "Diurnal fire patterns"
                },
                "satellite": {
                    "type": "string",
                    "description": "Satellite sensor",
                    "example": "T",
                    "required": True,
                    "use_case": "Data source tracking",
                    "values": ["T", "A", "N"]  # Terra, Aqua, NPP
                },
                "confidence": {
                    "type": "integer",
                    "description": "Detection confidence (0-100)",
                    "example": 85,
                    "required": True,
                    "use_case": "Quality filtering"
                },
                "version": {
                    "type": "string",
                    "description": "Data version",
                    "example": "6.0",
                    "required": True,
                    "use_case": "Version control"
                },
                "bright_t31": {
                    "type": "float",
                    "description": "Channel 31 brightness temperature",
                    "example": 295.8,
                    "required": True,
                    "use_case": "Fire detection algorithm"
                },
                "frp": {
                    "type": "float",
                    "description": "Fire Radiative Power (MW)",
                    "example": 15.7,
                    "required": True,
                    "use_case": "Fire intensity quantification"
                },
                "daynight": {
                    "type": "string",
                    "description": "Day or night detection",
                    "example": "D",
                    "required": True,
                    "use_case": "Diurnal analysis",
                    "values": ["D", "N"]
                },
                "type": {
                    "type": "integer",
                    "description": "Fire detection type",
                    "example": 0,
                    "required": True,
                    "use_case": "Fire classification"
                }
            }
        }
        
        return nasa_firms_structure
    
    def create_unified_data_structure_analysis(self) -> Dict:
        """Create comprehensive analysis of all database structures."""
        
        logger.info("🔧 Creating unified data structure analysis...")
        
        # Analyze each database
        structures = {
            "gbif": self.analyze_gbif_record_structure(),
            "ebird": self.analyze_ebird_record_structure(),
            "inaturalist": self.analyze_inaturalist_record_structure(),
            "iucn": self.analyze_iucn_record_structure(),
            "nasa_firms": self.analyze_nasa_firms_record_structure()
        }
        
        # Create unified analysis
        unified_analysis = {
            "analysis_timestamp": datetime.now().isoformat(),
            "database_structures": structures,
            "field_type_summary": self._analyze_field_types(structures),
            "common_fields": self._identify_common_fields(structures),
            "unique_capabilities": self._analyze_unique_capabilities(structures),
            "data_integration_mapping": self._create_integration_mapping(structures),
            "use_case_recommendations": self._generate_use_case_recommendations(structures)
        }
        
        return unified_analysis
    
    def _analyze_field_types(self, structures: Dict) -> Dict:
        """Analyze field types across databases."""
        
        field_types = defaultdict(list)
        
        for db_name, db_structure in structures.items():
            core_fields = db_structure.get("core_fields", {})
            for field_name, field_info in core_fields.items():
                field_type = field_info.get("type", "unknown")
                field_types[field_type].append(f"{db_name}.{field_name}")
        
        return dict(field_types)
    
    def _identify_common_fields(self, structures: Dict) -> Dict:
        """Identify common fields across databases."""
        
        # Common concepts that appear across databases
        common_concepts = {
            "spatial_coordinates": {
                "gbif": ["decimalLatitude", "decimalLongitude"],
                "ebird": ["lat", "lng"],
                "inaturalist": ["location"],
                "nasa_firms": ["latitude", "longitude"]
            },
            "temporal_information": {
                "gbif": ["eventDate", "year", "month", "day"],
                "ebird": ["obsDt"],
                "inaturalist": ["observed_on", "time_observed_at"],
                "iucn": ["assessment_date", "published_year"],
                "nasa_firms": ["acq_date", "acq_time"]
            },
            "taxonomic_identification": {
                "gbif": ["scientificName", "kingdom", "phylum", "class", "order", "family", "genus", "species"],
                "ebird": ["sciName", "comName", "speciesCode"],
                "inaturalist": ["taxon"],
                "iucn": ["scientific_name", "kingdom", "phylum", "class", "order", "family", "genus"]
            },
            "data_quality": {
                "gbif": ["basisOfRecord", "hasCoordinate", "hasGeospatialIssue"],
                "ebird": ["obsValid", "obsReviewed"],
                "inaturalist": ["quality_grade", "identifications"],
                "nasa_firms": ["confidence", "satellite"]
            },
            "unique_identifiers": {
                "gbif": ["gbifID", "occurrenceID"],
                "ebird": ["subId", "locId"],
                "inaturalist": ["id"],
                "iucn": ["taxonid"],
                "nasa_firms": ["latitude+longitude+acq_date+acq_time"]
            }
        }
        
        return common_concepts
    
    def _analyze_unique_capabilities(self, structures: Dict) -> Dict:
        """Analyze unique capabilities of each database."""
        
        unique_capabilities = {
            "gbif": {
                "strengths": [
                    "Massive specimen and observation data (3.2B+ records)",
                    "Comprehensive taxonomic coverage",
                    "Historical data going back to 1976",
                    "Institutional specimen collections",
                    "Global coordinate coverage",
                    "Rich metadata extensions"
                ],
                "unique_fields": [
                    "institutionCode",
                    "collectionCode", 
                    "basisOfRecord",
                    "coordinateUncertaintyInMeters",
                    "multimedia extensions"
                ],
                "best_for": [
                    "Historical biodiversity analysis",
                    "Museum specimen research",
                    "Large-scale biogeographic studies",
                    "Taxonomic distribution mapping"
                ]
            },
            "ebird": {
                "strengths": [
                    "Real-time bird observations",
                    "Standardized survey protocols",
                    "Abundance data (how many individuals)",
                    "Breeding behavior codes",
                    "Effort data (duration, distance, observers)",
                    "Community validation"
                ],
                "unique_fields": [
                    "howMany",
                    "breeding_codes",
                    "protocol_type",
                    "duration_minutes",
                    "distance_traveled_km",
                    "number_observers"
                ],
                "best_for": [
                    "Bird migration analysis",
                    "Real-time species monitoring",
                    "Abundance trend analysis",
                    "Citizen science studies"
                ]
            },
            "inaturalist": {
                "strengths": [
                    "Rich multimedia content (photos, sounds)",
                    "Community-based identification",
                    "Mobile app integration",
                    "Real-time observations",
                    "Broad taxonomic coverage",
                    "User engagement metrics"
                ],
                "unique_fields": [
                    "photos",
                    "sounds",
                    "identifications",
                    "comments",
                    "faves",
                    "quality_grade"
                ],
                "best_for": [
                    "Visual species verification",
                    "Community engagement analysis",
                    "Educational outreach",
                    "AI-assisted identification"
                ]
            },
            "iucn": {
                "strengths": [
                    "Authoritative conservation status",
                    "Threat assessments",
                    "Conservation action recommendations",
                    "Population trend data",
                    "Habitat requirements",
                    "Expert-reviewed assessments"
                ],
                "unique_fields": [
                    "category",
                    "criteria",
                    "population_trend",
                    "threats",
                    "conservation_measures",
                    "habitat"
                ],
                "best_for": [
                    "Conservation prioritization",
                    "Threat analysis",
                    "Policy development",
                    "Red List assessments"
                ]
            },
            "nasa_firms": {
                "strengths": [
                    "Real-time fire detection",
                    "Satellite-based monitoring",
                    "Fire intensity measurements",
                    "Global coverage",
                    "High temporal resolution",
                    "Multiple sensor integration"
                ],
                "unique_fields": [
                    "brightness",
                    "frp",
                    "confidence",
                    "satellite",
                    "scan",
                    "track"
                ],
                "best_for": [
                    "Fire impact assessment",
                    "Real-time threat monitoring",
                    "Conservation area protection",
                    "Climate change studies"
                ]
            }
        }
        
        return unique_capabilities
    
    def _create_integration_mapping(self, structures: Dict) -> Dict:
        """Create mapping for cross-database integration."""
        
        integration_mapping = {
            "spatial_join_fields": {
                "primary": "coordinates",
                "mapping": {
                    "gbif": "decimalLatitude, decimalLongitude",
                    "ebird": "lat, lng", 
                    "inaturalist": "location",
                    "nasa_firms": "latitude, longitude"
                },
                "precision": "coordinate_uncertainty_handling_required"
            },
            "temporal_join_fields": {
                "primary": "observation_date",
                "mapping": {
                    "gbif": "eventDate",
                    "ebird": "obsDt",
                    "inaturalist": "observed_on",
                    "nasa_firms": "acq_date"
                },
                "resolution": "daily_to_minute_precision"
            },
            "taxonomic_join_fields": {
                "primary": "scientific_name",
                "mapping": {
                    "gbif": "scientificName",
                    "ebird": "sciName",
                    "inaturalist": "taxon.name",
                    "iucn": "scientific_name"
                },
                "challenges": "name_standardization_required"
            },
            "cross_database_workflows": [
                {
                    "name": "comprehensive_species_assessment",
                    "description": "Combine GBIF occurrences, eBird abundance, iNat photos, IUCN status",
                    "databases": ["gbif", "ebird", "inaturalist", "iucn"],
                    "join_logic": "spatial_temporal_taxonomic"
                },
                {
                    "name": "fire_impact_on_biodiversity",
                    "description": "Analyze fire effects on species observations",
                    "databases": ["nasa_firms", "gbif", "ebird", "inaturalist"],
                    "join_logic": "spatial_temporal_proximity"
                },
                {
                    "name": "conservation_effectiveness",
                    "description": "Evaluate protected area performance",
                    "databases": ["gbif", "ebird", "inaturalist", "iucn"],
                    "join_logic": "spatial_within_protected_areas"
                }
            ]
        }
        
        return integration_mapping
    
    def _generate_use_case_recommendations(self, structures: Dict) -> Dict:
        """Generate recommendations for different use cases."""
        
        use_case_recommendations = {
            "research_scenarios": {
                "species_distribution_modeling": {
                    "primary_database": "gbif",
                    "secondary_databases": ["ebird", "inaturalist"],
                    "key_fields": [
                        "coordinates", "species_name", "observation_date", 
                        "data_quality_indicators"
                    ],
                    "filtering_strategy": "high_coordinate_precision + recent_data"
                },
                "real_time_biodiversity_monitoring": {
                    "primary_database": "ebird", 
                    "secondary_databases": ["inaturalist", "nasa_firms"],
                    "key_fields": [
                        "recent_observations", "abundance_data", "validation_status"
                    ],
                    "filtering_strategy": "last_30_days + validated_observations"
                },
                "conservation_status_assessment": {
                    "primary_database": "iucn",
                    "secondary_databases": ["gbif", "ebird", "inaturalist"],
                    "key_fields": [
                        "conservation_category", "population_trend", "threats",
                        "occurrence_data"
                    ],
                    "filtering_strategy": "threatened_species + occurrence_validation"
                },
                "habitat_threat_analysis": {
                    "primary_database": "nasa_firms",
                    "secondary_databases": ["gbif", "ebird", "inaturalist"],
                    "key_fields": [
                        "fire_detections", "species_occurrences", "temporal_overlap"
                    ],
                    "filtering_strategy": "high_confidence_fires + spatial_proximity"
                },
                "citizen_science_validation": {
                    "primary_database": "inaturalist",
                    "secondary_databases": ["gbif", "ebird"],
                    "key_fields": [
                        "photos", "community_identifications", "expert_observations"
                    ],
                    "filtering_strategy": "research_grade + photo_available"
                }
            },
            "data_collection_strategies": {
                "comprehensive_survey": {
                    "description": "Maximum species detection across all databases",
                    "databases": ["gbif", "ebird", "inaturalist"],
                    "search_radius": "50km",
                    "temporal_window": "all_available_data",
                    "expected_outcome": "highest_species_count"
                },
                "rapid_assessment": {
                    "description": "Quick biodiversity snapshot",
                    "databases": ["ebird", "inaturalist"],
                    "search_radius": "25km", 
                    "temporal_window": "last_12_months",
                    "expected_outcome": "recent_species_activity"
                },
                "conservation_focused": {
                    "description": "Threatened species prioritization",
                    "databases": ["iucn", "gbif", "ebird"],
                    "search_radius": "variable_by_species",
                    "temporal_window": "recent_validated_data",
                    "expected_outcome": "conservation_priority_species"
                },
                "threat_monitoring": {
                    "description": "Environmental threat assessment",
                    "databases": ["nasa_firms", "gbif", "ebird"],
                    "search_radius": "100km",
                    "temporal_window": "real_time_plus_historical",
                    "expected_outcome": "threat_impact_analysis"
                }
            }
        }
        
        return use_case_recommendations

def main():
    """Generate comprehensive data structure analysis."""
    
    print("🔍 CONSERVATION DATA STRUCTURE ANALYZER")
    print("=" * 60)
    
    analyzer = ConservationDataStructureAnalyzer()
    
    # Generate comprehensive analysis
    analysis = analyzer.create_unified_data_structure_analysis()
    
    # Save analysis
    output_file = f"conservation_data_structure_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ ANALYSIS COMPLETE!")
    print(f"📊 Detailed structure analysis saved to: {output_file}")
    
    # Print summary
    print(f"\n🎯 SUMMARY:")
    for db_name, db_data in analysis["database_structures"].items():
        core_fields_count = len(db_data.get("core_fields", {}))
        total_records = db_data.get("total_records", "unknown")
        print(f"   • {db_name.upper()}: {core_fields_count} core fields, {total_records}")
    
    print(f"\n📋 FIELD TYPES IDENTIFIED:")
    for field_type, fields in analysis["field_type_summary"].items():
        print(f"   • {field_type}: {len(fields)} fields")
    
    print(f"\n🔗 INTEGRATION CAPABILITIES:")
    common_concepts = analysis["common_fields"]
    print(f"   • {len(common_concepts)} common concept mappings")
    print(f"   • Cross-database joins supported")
    print(f"   • Multi-source analysis workflows available")
    
    print(f"\n🚀 Ready for advanced conservation data analysis!")

if __name__ == "__main__":
    main()
