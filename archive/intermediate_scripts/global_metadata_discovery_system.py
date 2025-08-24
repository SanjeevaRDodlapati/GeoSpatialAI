"""
Global Conservation Database Metadata Discovery System
=====================================================

This system discovers and catalogs available data across major conservation 
databases to enable intelligent data selection by country, region, ecosystem,
or taxonomic group.

Author: GeoSpatialAI Development Team  
Date: August 24, 2025
"""

import asyncio
import aiohttp
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Set
import logging
from pathlib import Path
from collections import defaultdict
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GlobalDatabaseMetadataDiscovery:
    """
    Discover and catalog metadata from major conservation databases to understand
    global data availability patterns.
    """
    
    def __init__(self):
        self.session = None
        
        # Database endpoints
        self.gbif_base_url = "https://api.gbif.org/v1"
        self.ebird_base_url = "https://ebird.org/ws2.0"
        self.inaturalist_base_url = "https://api.inaturalist.org/v1"
        self.iucn_base_url = "https://apiv3.iucnredlist.org/api/v3"
        
        # Metadata cache
        self.metadata_cache = {}
        self.cache_dir = Path("metadata_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        # Discovery results
        self.global_metadata = {
            "discovery_timestamp": None,
            "databases": {},
            "countries": {},
            "ecosystems": {},
            "taxonomic_groups": {},
            "data_availability_matrix": {},
            "recommendations": {}
        }
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def discover_all_database_metadata(self) -> Dict[str, Any]:
        """
        Comprehensive metadata discovery across all major conservation databases.
        """
        logger.info("🔍 Starting Global Conservation Database Metadata Discovery")
        logger.info("=" * 70)
        
        start_time = datetime.now()
        self.global_metadata["discovery_timestamp"] = start_time.isoformat()
        
        # Discover metadata for each database
        await self._discover_gbif_metadata()
        await self._discover_ebird_metadata()
        await self._discover_inaturalist_metadata()
        await self._discover_iucn_metadata()
        await self._discover_nasa_firms_metadata()
        
        # Analyze cross-database patterns
        await self._analyze_cross_database_patterns()
        
        # Generate recommendations
        self._generate_data_selection_recommendations()
        
        # Save comprehensive metadata
        self._save_metadata_results()
        
        discovery_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Metadata discovery completed in {discovery_time:.2f} seconds")
        
        return self.global_metadata
    
    async def _discover_gbif_metadata(self):
        """Discover GBIF global metadata and availability patterns."""
        logger.info("\n🌍 Discovering GBIF Metadata...")
        
        gbif_metadata = {
            "database_name": "Global Biodiversity Information Facility (GBIF)",
            "base_url": self.gbif_base_url,
            "access_type": "open",
            "global_statistics": {},
            "country_coverage": {},
            "taxonomic_coverage": {},
            "temporal_coverage": {},
            "data_quality_indicators": {},
            "recommended_parameters": {}
        }
        
        try:
            # Get global statistics
            logger.info("   📊 Fetching global statistics...")
            async with self.session.get(f"{self.gbif_base_url}/occurrence/count") as response:
                if response.status == 200:
                    total_occurrences = await response.text()
                    gbif_metadata["global_statistics"]["total_occurrences"] = int(total_occurrences)
                    logger.info(f"      Total GBIF occurrences: {int(total_occurrences):,}")
            
            # Get country-wise statistics
            logger.info("   🌍 Analyzing country coverage...")
            country_stats = await self._get_gbif_country_statistics()
            gbif_metadata["country_coverage"] = country_stats
            
            # Get taxonomic kingdom statistics
            logger.info("   🧬 Analyzing taxonomic coverage...")
            taxonomic_stats = await self._get_gbif_taxonomic_statistics()
            gbif_metadata["taxonomic_coverage"] = taxonomic_stats
            
            # Get temporal coverage
            logger.info("   📅 Analyzing temporal coverage...")
            temporal_stats = await self._get_gbif_temporal_statistics()
            gbif_metadata["temporal_coverage"] = temporal_stats
            
            # Analyze data quality patterns
            logger.info("   💯 Analyzing data quality indicators...")
            quality_stats = await self._get_gbif_quality_indicators()
            gbif_metadata["data_quality_indicators"] = quality_stats
            
            # Generate recommended parameters
            gbif_metadata["recommended_parameters"] = {
                "optimal_radius_km": 50,
                "max_records_per_query": 1000,
                "recommended_filters": ["hasCoordinate=true", "hasGeospatialIssue=false"],
                "best_coverage_countries": country_stats.get("top_countries", [])[:10] if country_stats else [],
                "high_quality_kingdoms": ["Animalia", "Plantae"],
                "temporal_range": "1990-present"
            }
            
        except Exception as e:
            logger.error(f"❌ GBIF metadata discovery failed: {e}")
            gbif_metadata["error"] = str(e)
        
        self.global_metadata["databases"]["gbif"] = gbif_metadata
    
    async def _get_gbif_country_statistics(self) -> Dict[str, Any]:
        """Get country-wise GBIF data availability."""
        country_stats = {
            "total_countries": 0,
            "top_countries": [],
            "coverage_by_region": {},
            "data_density_ranking": {}
        }
        
        try:
            # Get faceted country statistics
            facet_url = f"{self.gbif_base_url}/occurrence/search?facet=country&limit=0&facetLimit=300"
            async with self.session.get(facet_url) as response:
                if response.status == 200:
                    data = await response.json()
                    country_facets = data.get("facets", [])
                    
                    for facet in country_facets:
                        if facet.get("field") == "COUNTRY":
                            country_counts = facet.get("counts", [])
                            
                            country_stats["total_countries"] = len(country_counts)
                            country_stats["top_countries"] = [
                                {"country": item["name"], "occurrences": item["count"]}
                                for item in country_counts[:20]
                            ]
                            
                            # Group by regions (simplified)
                            region_totals = defaultdict(int)
                            for item in country_counts:
                                region = self._get_region_for_country(item["name"])
                                region_totals[region] += item["count"]
                            
                            country_stats["coverage_by_region"] = dict(region_totals)
                            break
        
        except Exception as e:
            logger.warning(f"Country statistics failed: {e}")
        
        return country_stats
    
    async def _get_gbif_taxonomic_statistics(self) -> Dict[str, Any]:
        """Get taxonomic coverage statistics from GBIF."""
        taxonomic_stats = {
            "kingdoms": {},
            "classes": {},
            "orders": {},
            "families": {},
            "species_count_estimate": 0
        }
        
        try:
            # Get kingdom-level statistics
            kingdom_url = f"{self.gbif_base_url}/occurrence/search?facet=kingdom&limit=0&facetLimit=20"
            async with self.session.get(kingdom_url) as response:
                if response.status == 200:
                    data = await response.json()
                    facets = data.get("facets", [])
                    
                    for facet in facets:
                        if facet.get("field") == "KINGDOM":
                            kingdom_counts = facet.get("counts", [])
                            taxonomic_stats["kingdoms"] = {
                                item["name"]: item["count"] for item in kingdom_counts
                            }
                            break
            
            # Get class-level statistics for animals
            class_url = f"{self.gbif_base_url}/occurrence/search?facet=class&kingdom=Animalia&limit=0&facetLimit=50"
            async with self.session.get(class_url) as response:
                if response.status == 200:
                    data = await response.json()
                    facets = data.get("facets", [])
                    
                    for facet in facets:
                        if facet.get("field") == "CLASS":
                            class_counts = facet.get("counts", [])
                            taxonomic_stats["classes"] = {
                                item["name"]: item["count"] for item in class_counts[:20]
                            }
                            break
            
            # Estimate species count
            species_url = f"{self.gbif_base_url}/species/search?q=*&limit=0"
            async with self.session.get(species_url) as response:
                if response.status == 200:
                    data = await response.json()
                    taxonomic_stats["species_count_estimate"] = data.get("count", 0)
        
        except Exception as e:
            logger.warning(f"Taxonomic statistics failed: {e}")
        
        return taxonomic_stats
    
    async def _get_gbif_temporal_statistics(self) -> Dict[str, Any]:
        """Get temporal coverage patterns from GBIF."""
        temporal_stats = {
            "year_range": {},
            "recent_data_percentage": 0,
            "historical_data_percentage": 0,
            "decade_distribution": {}
        }
        
        try:
            # Get year facets
            year_url = f"{self.gbif_base_url}/occurrence/search?facet=year&limit=0&facetLimit=50"
            async with self.session.get(year_url) as response:
                if response.status == 200:
                    data = await response.json()
                    facets = data.get("facets", [])
                    
                    for facet in facets:
                        if facet.get("field") == "YEAR":
                            year_counts = facet.get("counts", [])
                            
                            years = [int(item["name"]) for item in year_counts if item["name"].isdigit()]
                            if years:
                                temporal_stats["year_range"] = {
                                    "earliest": min(years),
                                    "latest": max(years),
                                    "span_years": max(years) - min(years)
                                }
                            
                            # Calculate recent vs historical
                            total_records = sum(item["count"] for item in year_counts)
                            recent_records = sum(item["count"] for item in year_counts 
                                               if item["name"].isdigit() and int(item["name"]) >= 2000)
                            
                            temporal_stats["recent_data_percentage"] = (recent_records / total_records * 100) if total_records > 0 else 0
                            temporal_stats["historical_data_percentage"] = 100 - temporal_stats["recent_data_percentage"]
                            
                            # Decade distribution
                            decade_counts = defaultdict(int)
                            for item in year_counts:
                                if item["name"].isdigit():
                                    decade = (int(item["name"]) // 10) * 10
                                    decade_counts[f"{decade}s"] += item["count"]
                            temporal_stats["decade_distribution"] = dict(decade_counts)
                            break
        
        except Exception as e:
            logger.warning(f"Temporal statistics failed: {e}")
        
        return temporal_stats
    
    async def _get_gbif_quality_indicators(self) -> Dict[str, Any]:
        """Analyze GBIF data quality indicators."""
        quality_stats = {
            "coordinate_quality": {},
            "identification_quality": {},
            "institution_diversity": {},
            "basis_of_record": {}
        }
        
        try:
            # Coordinate quality
            coord_url = f"{self.gbif_base_url}/occurrence/search?facet=hasCoordinate&limit=0"
            async with self.session.get(coord_url) as response:
                if response.status == 200:
                    data = await response.json()
                    facets = data.get("facets", [])
                    
                    for facet in facets:
                        if facet.get("field") == "HAS_COORDINATE":
                            coord_counts = facet.get("counts", [])
                            quality_stats["coordinate_quality"] = {
                                item["name"]: item["count"] for item in coord_counts
                            }
                            break
            
            # Basis of record
            basis_url = f"{self.gbif_base_url}/occurrence/search?facet=basisOfRecord&limit=0&facetLimit=20"
            async with self.session.get(basis_url) as response:
                if response.status == 200:
                    data = await response.json()
                    facets = data.get("facets", [])
                    
                    for facet in facets:
                        if facet.get("field") == "BASIS_OF_RECORD":
                            basis_counts = facet.get("counts", [])
                            quality_stats["basis_of_record"] = {
                                item["name"]: item["count"] for item in basis_counts
                            }
                            break
        
        except Exception as e:
            logger.warning(f"Quality indicators failed: {e}")
        
        return quality_stats
    
    async def _discover_ebird_metadata(self):
        """Discover eBird metadata and coverage patterns."""
        logger.info("\n🐦 Discovering eBird Metadata...")
        
        ebird_metadata = {
            "database_name": "eBird",
            "base_url": self.ebird_base_url,
            "access_type": "api_key_required",
            "global_coverage": {},
            "regional_coverage": {},
            "species_coverage": {},
            "temporal_coverage": {},
            "recommended_parameters": {}
        }
        
        try:
            # Get regional coverage (requires API key, so simulate based on known info)
            ebird_metadata["global_coverage"] = {
                "regions": "Worldwide",
                "countries": 195,
                "estimated_observations": "1+ billion",
                "species_covered": "10,000+",
                "real_time_updates": True
            }
            
            # Known high-coverage regions
            ebird_metadata["regional_coverage"] = {
                "highest_coverage": ["US", "CA", "IN", "MX", "CO"],
                "emerging_regions": ["BR", "AR", "AU", "ZA", "KE"],
                "coverage_density": "Urban > Suburban > Rural > Remote"
            }
            
            ebird_metadata["recommended_parameters"] = {
                "optimal_radius_km": 25,
                "max_records_per_query": 10000,
                "best_temporal_range": "recent_30_days",
                "data_quality": "citizen_science_validated"
            }
        
        except Exception as e:
            logger.error(f"❌ eBird metadata discovery failed: {e}")
        
        self.global_metadata["databases"]["ebird"] = ebird_metadata
    
    async def _discover_inaturalist_metadata(self):
        """Discover iNaturalist metadata and global patterns."""
        logger.info("\n📸 Discovering iNaturalist Metadata...")
        
        inaturalist_metadata = {
            "database_name": "iNaturalist",
            "base_url": self.inaturalist_base_url,
            "access_type": "open",
            "global_statistics": {},
            "taxonomic_coverage": {},
            "geographic_coverage": {},
            "community_engagement": {},
            "recommended_parameters": {}
        }
        
        try:
            # Get basic statistics
            stats_url = f"{self.inaturalist_base_url}/observations?verifiable=true&spam=false&per_page=0"
            async with self.session.get(stats_url) as response:
                if response.status == 200:
                    data = await response.json()
                    total_results = data.get("total_results", 0)
                    inaturalist_metadata["global_statistics"]["total_observations"] = total_results
                    logger.info(f"      Total iNaturalist observations: {total_results:,}")
            
            # Get species count
            species_url = f"{self.inaturalist_base_url}/taxa?rank=species&per_page=0"
            async with self.session.get(species_url) as response:
                if response.status == 200:
                    data = await response.json()
                    species_count = data.get("total_results", 0)
                    inaturalist_metadata["global_statistics"]["species_documented"] = species_count
                    logger.info(f"      Species documented: {species_count:,}")
            
            inaturalist_metadata["recommended_parameters"] = {
                "optimal_radius_km": 10,
                "photo_quality": "research_grade_preferred",
                "identification_quality": "community_verified",
                "temporal_focus": "2015_onwards"
            }
        
        except Exception as e:
            logger.error(f"❌ iNaturalist metadata discovery failed: {e}")
        
        self.global_metadata["databases"]["inaturalist"] = inaturalist_metadata
    
    async def _discover_iucn_metadata(self):
        """Discover IUCN Red List metadata."""
        logger.info("\n⚠️  Discovering IUCN Red List Metadata...")
        
        iucn_metadata = {
            "database_name": "IUCN Red List of Threatened Species",
            "base_url": self.iucn_base_url,
            "access_type": "api_key_required",
            "coverage": {
                "species_assessed": "150,000+",
                "conservation_categories": 9,
                "global_coverage": True,
                "taxonomic_focus": "vertebrates_plants_priority"
            },
            "conservation_categories": [
                "Least Concern", "Near Threatened", "Vulnerable",
                "Endangered", "Critically Endangered", "Extinct in the Wild",
                "Extinct", "Data Deficient", "Not Evaluated"
            ],
            "recommended_parameters": {
                "primary_use": "conservation_status_validation",
                "best_coverage": "mammals_birds_amphibians",
                "update_frequency": "annual"
            }
        }
        
        self.global_metadata["databases"]["iucn"] = iucn_metadata
    
    async def _discover_nasa_firms_metadata(self):
        """Discover NASA FIRMS metadata and capabilities."""
        logger.info("\n🔥 Discovering NASA FIRMS Metadata...")
        
        nasa_metadata = {
            "database_name": "NASA Fire Information for Resource Management System",
            "base_url": "https://firms.modaps.eosdis.nasa.gov/api",
            "access_type": "api_key_required",
            "global_coverage": {
                "geographic_scope": "global",
                "satellites": ["MODIS", "VIIRS", "GOES"],
                "temporal_coverage": "real_time",
                "spatial_resolution": "375m_1km",
                "detection_confidence": "percentage_based"
            },
            "data_products": [
                "Active Fire Detections", "Thermal Anomalies",
                "Fire Radiative Power", "Historical Fire Archives"
            ],
            "recommended_parameters": {
                "optimal_radius_km": 50,
                "temporal_range_days": 7,
                "confidence_threshold": 50,
                "sensor_preference": "VIIRS_SNPP_NRT"
            }
        }
        
        self.global_metadata["databases"]["nasa_firms"] = nasa_metadata
    
    async def _analyze_cross_database_patterns(self):
        """Analyze patterns across all databases to identify synergies."""
        logger.info("\n🔄 Analyzing Cross-Database Patterns...")
        
        cross_patterns = {
            "complementary_strengths": {},
            "geographic_synergies": {},
            "taxonomic_synergies": {},
            "temporal_synergies": {},
            "data_integration_opportunities": {}
        }
        
        # Complementary strengths
        cross_patterns["complementary_strengths"] = {
            "gbif": "Comprehensive historical specimen data",
            "ebird": "Real-time bird observations with high frequency",
            "inaturalist": "Community-driven photo documentation",
            "iucn": "Authoritative conservation status",
            "nasa_firms": "Real-time environmental threat monitoring"
        }
        
        # Geographic synergies
        cross_patterns["geographic_synergies"] = {
            "high_coverage_regions": ["North America", "Europe", "Australia"],
            "emerging_coverage": ["South America", "Africa", "Southeast Asia"],
            "data_gap_regions": ["Central Africa", "Central Asia", "Remote Islands"],
            "marine_coverage": "Limited across all databases"
        }
        
        # Integration opportunities
        cross_patterns["data_integration_opportunities"] = [
            "GBIF + iNaturalist: Historical + Modern observations",
            "eBird + GBIF: Real-time + Archived bird data",
            "NASA FIRMS + All: Environmental threat context",
            "IUCN + All: Conservation priority overlay",
            "Geographic clustering: Multi-database regional analysis"
        ]
        
        self.global_metadata["cross_database_analysis"] = cross_patterns
    
    def _generate_data_selection_recommendations(self):
        """Generate intelligent recommendations for data selection strategies."""
        logger.info("\n💡 Generating Data Selection Recommendations...")
        
        recommendations = {
            "optimal_search_strategies": {},
            "region_specific_advice": {},
            "taxonomic_strategies": {},
            "quality_optimization": {},
            "cost_benefit_analysis": {}
        }
        
        # Optimal search strategies
        recommendations["optimal_search_strategies"] = {
            "comprehensive_biodiversity": {
                "primary": "GBIF",
                "secondary": ["iNaturalist", "eBird"],
                "radius": "50km",
                "records": 1000,
                "filters": ["hasCoordinate=true", "year>=1990"]
            },
            "real_time_monitoring": {
                "primary": "eBird",
                "secondary": ["iNaturalist", "NASA FIRMS"],
                "radius": "25km",
                "temporal": "last_30_days",
                "frequency": "weekly_updates"
            },
            "conservation_assessment": {
                "primary": "IUCN",
                "secondary": ["GBIF", "iNaturalist"],
                "focus": "threatened_species",
                "validation": "cross_reference_required"
            },
            "threat_monitoring": {
                "primary": "NASA FIRMS",
                "secondary": ["GBIF for baseline"],
                "radius": "100km",
                "temporal": "real_time",
                "alerts": "automated"
            }
        }
        
        # Region-specific advice
        recommendations["region_specific_advice"] = {
            "north_america_europe": {
                "best_databases": ["eBird", "GBIF", "iNaturalist"],
                "data_quality": "excellent",
                "recommended_approach": "multi_database_integration"
            },
            "tropical_regions": {
                "best_databases": ["GBIF", "iNaturalist"],
                "challenges": "lower_coverage",
                "recommended_approach": "targeted_sampling_plus_citizen_science"
            },
            "marine_environments": {
                "best_databases": ["GBIF", "specialized_marine_databases"],
                "challenges": "limited_coverage",
                "recommended_approach": "supplement_with_regional_databases"
            },
            "remote_areas": {
                "best_databases": ["GBIF", "NASA FIRMS"],
                "challenges": "sparse_data",
                "recommended_approach": "large_radius_searches_historical_data"
            }
        }
        
        # Quality optimization
        recommendations["quality_optimization"] = {
            "data_validation_pipeline": [
                "Cross-reference between databases",
                "Coordinate validation",
                "Temporal consistency checks",
                "Taxonomic verification",
                "Institution credibility assessment"
            ],
            "quality_filters": {
                "gbif": ["hasCoordinate=true", "hasGeospatialIssue=false"],
                "ebird": ["research_grade=true"],
                "inaturalist": ["quality_grade=research"],
                "nasa_firms": ["confidence>=50"]
            }
        }
        
        self.global_metadata["recommendations"] = recommendations
    
    def _save_metadata_results(self):
        """Save comprehensive metadata results to files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save complete metadata
        metadata_file = self.cache_dir / f"global_metadata_discovery_{timestamp}.json"
        with open(metadata_file, 'w') as f:
            json.dump(self.global_metadata, f, indent=2, default=str)
        
        # Save country recommendations
        if "gbif" in self.global_metadata["databases"]:
            country_data = self.global_metadata["databases"]["gbif"].get("country_coverage", {})
            if country_data.get("top_countries"):
                country_file = self.cache_dir / f"recommended_countries_{timestamp}.json"
                with open(country_file, 'w') as f:
                    json.dump(country_data["top_countries"], f, indent=2)
        
        logger.info(f"💾 Metadata saved to: {metadata_file}")
    
    def _get_region_for_country(self, country_code: str) -> str:
        """Map country codes to regions (simplified)."""
        region_mapping = {
            "US": "North America", "CA": "North America", "MX": "North America",
            "BR": "South America", "AR": "South America", "CO": "South America",
            "GB": "Europe", "DE": "Europe", "FR": "Europe", "ES": "Europe",
            "CN": "Asia", "IN": "Asia", "JP": "Asia", "ID": "Southeast Asia",
            "AU": "Oceania", "NZ": "Oceania",
            "ZA": "Africa", "KE": "Africa", "NG": "Africa",
            "MG": "Africa"  # Madagascar
        }
        return region_mapping.get(country_code, "Other")
    
    async def generate_country_selection_interface(self) -> Dict[str, Any]:
        """Generate an interface for selecting countries/regions based on metadata."""
        logger.info("\n🌍 Generating Country/Region Selection Interface...")
        
        selection_interface = {
            "available_regions": {},
            "country_rankings": {},
            "ecosystem_coverage": {},
            "data_density_map": {},
            "selection_wizard": {}
        }
        
        # Create selection wizard
        selection_interface["selection_wizard"] = {
            "step_1_region": {
                "question": "Which region are you interested in?",
                "options": ["Global", "North America", "South America", "Europe", "Asia", "Africa", "Oceania"],
                "recommendations": {
                    "best_coverage": ["North America", "Europe"],
                    "emerging_data": ["South America", "Asia"],
                    "data_gaps": ["Central Africa", "Remote Islands"]
                }
            },
            "step_2_ecosystem": {
                "question": "Which ecosystem type?",
                "options": ["Tropical Rainforest", "Temperate Forest", "Grassland", "Desert", "Marine", "Urban"],
                "data_availability": {
                    "excellent": ["Temperate Forest", "Urban"],
                    "good": ["Tropical Rainforest", "Grassland"],
                    "limited": ["Desert", "Marine"]
                }
            },
            "step_3_taxonomic": {
                "question": "Primary taxonomic focus?",
                "options": ["All Species", "Birds", "Mammals", "Plants", "Insects", "Marine Life"],
                "database_recommendations": {
                    "Birds": ["eBird", "GBIF"],
                    "Mammals": ["GBIF", "IUCN"],
                    "Plants": ["GBIF", "iNaturalist"],
                    "All Species": ["GBIF", "iNaturalist", "eBird"]
                }
            },
            "step_4_purpose": {
                "question": "Primary research purpose?",
                "options": ["Conservation Assessment", "Biodiversity Survey", "Real-time Monitoring", "Threat Analysis"],
                "optimal_strategies": {
                    "Conservation Assessment": "IUCN + GBIF validation",
                    "Biodiversity Survey": "GBIF + iNaturalist comprehensive",
                    "Real-time Monitoring": "eBird + NASA FIRMS",
                    "Threat Analysis": "NASA FIRMS + baseline GBIF"
                }
            }
        }
        
        return selection_interface

async def run_comprehensive_metadata_discovery():
    """Run comprehensive metadata discovery across all databases."""
    
    print("🔍 GLOBAL CONSERVATION DATABASE METADATA DISCOVERY")
    print("=" * 65)
    
    async with GlobalDatabaseMetadataDiscovery() as discovery:
        
        # Run comprehensive discovery
        metadata_results = await discovery.discover_all_database_metadata()
        
        # Display summary results
        print(f"\n📊 DISCOVERY SUMMARY")
        print("-" * 30)
        
        databases = metadata_results.get("databases", {})
        print(f"Databases Analyzed: {len(databases)}")
        
        for db_name, db_info in databases.items():
            print(f"\n🗄️  {db_info.get('database_name', db_name).upper()}")
            
            if db_name == "gbif":
                stats = db_info.get("global_statistics", {})
                if stats:
                    total = stats.get("total_occurrences", 0)
                    print(f"   📊 Total Occurrences: {total:,}")
                
                country_stats = db_info.get("country_coverage", {})
                if country_stats.get("total_countries"):
                    print(f"   🌍 Countries Covered: {country_stats['total_countries']}")
                    
                    top_countries = country_stats.get("top_countries", [])[:5]
                    if top_countries:
                        print(f"   🔝 Top Countries:")
                        for country in top_countries:
                            name = country["country"]
                            count = country["occurrences"]
                            print(f"      • {name}: {count:,} records")
                
                taxonomic = db_info.get("taxonomic_coverage", {})
                kingdoms = taxonomic.get("kingdoms", {})
                if kingdoms:
                    print(f"   🧬 Taxonomic Coverage:")
                    for kingdom, count in list(kingdoms.items())[:3]:
                        print(f"      • {kingdom}: {count:,} records")
            
            elif db_name == "inaturalist":
                stats = db_info.get("global_statistics", {})
                if stats:
                    observations = stats.get("total_observations", 0)
                    species = stats.get("species_documented", 0)
                    print(f"   📊 Total Observations: {observations:,}")
                    print(f"   🦋 Species Documented: {species:,}")
        
        # Display recommendations
        print(f"\n💡 KEY RECOMMENDATIONS")
        print("-" * 30)
        
        recommendations = metadata_results.get("recommendations", {})
        strategies = recommendations.get("optimal_search_strategies", {})
        
        if strategies:
            print(f"Optimal Search Strategies:")
            for strategy, details in strategies.items():
                primary = details.get("primary", "Unknown")
                radius = details.get("radius", "Unknown")
                print(f"   • {strategy.replace('_', ' ').title()}: {primary} ({radius})")
        
        cross_analysis = metadata_results.get("cross_database_analysis", {})
        synergies = cross_analysis.get("geographic_synergies", {})
        if synergies:
            high_coverage = synergies.get("high_coverage_regions", [])
            print(f"\n🌍 Best Coverage Regions: {', '.join(high_coverage)}")
            
            data_gaps = synergies.get("data_gap_regions", [])
            if data_gaps:
                print(f"🔍 Data Gap Regions: {', '.join(data_gaps)}")
        
        # Generate country selection interface
        selection_interface = await discovery.generate_country_selection_interface()
        
        print(f"\n🎯 INTELLIGENT DATA SELECTION WIZARD")
        print("-" * 40)
        wizard = selection_interface.get("selection_wizard", {})
        
        for step, details in wizard.items():
            question = details.get("question", "")
            options = details.get("options", [])
            print(f"\n{step.replace('_', ' ').title()}: {question}")
            print(f"   Options: {', '.join(options[:4])}{'...' if len(options) > 4 else ''}")
        
        print(f"\n✅ METADATA DISCOVERY COMPLETE!")
        print(f"🎯 Use this metadata to intelligently select optimal countries,")
        print(f"   ecosystems, and database combinations for your research needs.")
        
        return metadata_results

if __name__ == "__main__":
    try:
        results = asyncio.run(run_comprehensive_metadata_discovery())
        print(f"\n🚀 Ready to implement intelligent data selection based on metadata!")
    except Exception as e:
        logger.error(f"Metadata discovery failed: {e}")
        import traceback
        traceback.print_exc()
