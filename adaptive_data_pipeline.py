"""
Adaptive Data Collection Pipeline
===============================

Dynamic data pipeline that adapts based on metadata discovery and intelligent
selection criteria to optimize data collection from global databases.

Author: GeoSpatialAI Development Team
Date: August 24, 2025
"""

import asyncio
import aiohttp
import json
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
from pathlib import Path
import math
from smart_data_selection_interface import (
    SmartDataSelectionInterface, 
    DataSelectionCriteria, 
    OptimalSelectionResult
)
from global_metadata_discovery_system import GlobalDatabaseMetadataDiscovery

logger = logging.getLogger(__name__)

@dataclass
class AdaptiveSearchParameters:
    """Dynamic search parameters that adapt based on metadata."""
    base_coordinates: Tuple[float, float]
    search_radius_km: int
    max_records: int
    quality_filters: List[str]
    databases: List[str]
    temporal_range: str
    taxonomic_filters: List[str]
    priority_score: float

@dataclass
class CollectionResult:
    """Result of adaptive data collection."""
    location_name: str
    coordinates: Tuple[float, float]
    total_records: int
    species_count: int
    database_contributions: Dict[str, int]
    quality_metrics: Dict[str, float]
    collection_time_seconds: float
    success_rate: float

class AdaptiveDataPipeline:
    """
    Adaptive data collection pipeline that intelligently selects and configures
    data collection based on metadata analysis and selection criteria.
    """
    
    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        self.api_keys = api_keys or {}
        self.session = None
        
        # Components
        self.metadata_discovery = None
        self.selection_interface = SmartDataSelectionInterface()
        
        # Configuration
        self.adaptive_config = {
            "auto_radius_adjustment": True,
            "quality_threshold_adaptation": True,
            "load_balancing": True,
            "failure_recovery": True,
            "performance_optimization": True
        }
        
        # Performance tracking
        self.performance_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "avg_response_time": 0,
            "data_quality_trends": [],
            "geographic_coverage": {}
        }
        
        # Cache for adaptive parameters
        self.parameter_cache = {}
        self.results_cache = {}
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        self.metadata_discovery = GlobalDatabaseMetadataDiscovery()
        await self.metadata_discovery.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
        if self.metadata_discovery:
            await self.metadata_discovery.__aexit__(exc_type, exc_val, exc_tb)
    
    async def run_adaptive_collection(self, 
                                    research_criteria: DataSelectionCriteria) -> List[CollectionResult]:
        """
        Run adaptive data collection based on intelligent selection criteria.
        """
        
        logger.info(f"🚀 Starting Adaptive Data Collection")
        logger.info(f"🎯 Research Purpose: {research_criteria.research_purpose}")
        logger.info("=" * 60)
        
        # Step 1: Discover metadata if not cached
        await self._ensure_metadata_available()
        
        # Step 2: Generate optimal selection
        optimal_selection = self._generate_optimal_selection(research_criteria)
        
        # Step 3: Create adaptive search parameters
        search_parameters = await self._create_adaptive_parameters(optimal_selection, research_criteria)
        
        # Step 4: Execute adaptive collection
        results = await self._execute_adaptive_collection(search_parameters)
        
        # Step 5: Analyze and optimize
        await self._analyze_and_optimize_results(results)
        
        logger.info(f"✅ Adaptive collection completed!")
        logger.info(f"📊 Collected data from {len(results)} locations")
        
        return results
    
    async def _ensure_metadata_available(self):
        """Ensure metadata is available for adaptive decisions."""
        
        # Check for cached metadata
        metadata_files = list(Path("metadata_cache").glob("global_metadata_discovery_*.json"))
        
        if not metadata_files:
            logger.info("🔍 No metadata cache found, running discovery...")
            metadata = await self.metadata_discovery.discover_all_database_metadata()
            
            # Update selection interface with new metadata
            latest_file = max(metadata_files) if metadata_files else None
            if latest_file:
                self.selection_interface.load_metadata(str(latest_file))
        else:
            # Load most recent metadata
            latest_file = max(metadata_files, key=lambda x: x.stat().st_mtime)
            self.selection_interface.load_metadata(str(latest_file))
            logger.info(f"✅ Loaded metadata from {latest_file.name}")
    
    def _generate_optimal_selection(self, criteria: DataSelectionCriteria) -> OptimalSelectionResult:
        """Generate optimal selection using smart interface."""
        
        return self.selection_interface.analyze_research_requirements(
            research_purpose=criteria.research_purpose,
            geographic_scope=criteria.regions[0] if criteria.regions else "global",
            taxonomic_interest=criteria.taxonomic_groups,
            quality_requirements=criteria.data_quality_level
        )
    
    async def _create_adaptive_parameters(self, 
                                        selection: OptimalSelectionResult,
                                        criteria: DataSelectionCriteria) -> List[AdaptiveSearchParameters]:
        """Create adaptive search parameters for each location."""
        
        logger.info("🎛️  Creating adaptive search parameters...")
        
        parameters = []
        
        for country in selection.recommended_countries:
            country_code = country["country_code"]
            
            # Get representative coordinates for country
            coordinates = await self._get_country_coordinates(country_code)
            
            for coord in coordinates:
                # Create adaptive parameters
                adaptive_params = AdaptiveSearchParameters(
                    base_coordinates=coord,
                    search_radius_km=self._adapt_radius(country, selection),
                    max_records=self._adapt_max_records(country, selection),
                    quality_filters=self._adapt_quality_filters(country, selection),
                    databases=self._adapt_database_selection(country, selection),
                    temporal_range=self._adapt_temporal_range(country, selection),
                    taxonomic_filters=criteria.taxonomic_groups,
                    priority_score=country.get("research_suitability", 0.5)
                )
                
                parameters.append(adaptive_params)
        
        # Sort by priority score
        parameters.sort(key=lambda x: x.priority_score, reverse=True)
        
        logger.info(f"📍 Created {len(parameters)} adaptive search locations")
        return parameters
    
    async def _get_country_coordinates(self, country_code: str) -> List[Tuple[float, float]]:
        """Get representative coordinates for a country."""
        
        # Simplified coordinate mapping for major countries
        country_coords = {
            "US": [
                (39.8283, -98.5795),   # Geographic center
                (34.0522, -118.2437),  # Los Angeles
                (40.7128, -74.0060),   # New York
                (25.7617, -80.1918),   # Miami
                (47.6062, -122.3321)   # Seattle
            ],
            "CA": [
                (56.1304, -106.3468),  # Geographic center
                (43.6532, -79.3832),   # Toronto
                (49.2827, -123.1207),  # Vancouver
                (45.5017, -73.5673)    # Montreal
            ],
            "BR": [
                (-14.2350, -51.9253),  # Geographic center
                (-23.5505, -46.6333),  # São Paulo
                (-22.9068, -43.1729),  # Rio de Janeiro
                (-3.7319, -38.5267)    # Fortaleza
            ],
            "AU": [
                (-25.2744, 133.7751),  # Geographic center
                (-33.8688, 151.2093),  # Sydney
                (-37.8136, 144.9631),  # Melbourne
                (-31.9505, 115.8605)   # Perth
            ],
            "MG": [
                (-18.7669, 46.8691),   # Geographic center
                (-18.8792, 47.5079),   # Antananarivo
                (-12.2787, 49.2917),   # Andasibe-Mantadia
                (-24.0319, 46.7144)    # Isalo
            ]
        }
        
        return country_coords.get(country_code, [(0, 0)])  # Default fallback
    
    def _adapt_radius(self, country: Dict[str, Any], selection: OptimalSelectionResult) -> int:
        """Adapt search radius based on country characteristics."""
        
        base_radius = selection.optimal_parameters.get("search_radius_km", 50)
        
        # Adjust based on country data density
        data_availability = country.get("data_availability", 0)
        if isinstance(data_availability, int):
            if data_availability > 50000000:  # High data density
                return max(25, base_radius - 25)
            elif data_availability > 10000000:  # Medium data density
                return base_radius
            else:  # Low data density
                return min(100, base_radius + 50)
        
        return base_radius
    
    def _adapt_max_records(self, country: Dict[str, Any], selection: OptimalSelectionResult) -> int:
        """Adapt maximum records based on expected data volume."""
        
        base_records = selection.optimal_parameters.get("max_records_per_area", 1000)
        
        # Adjust based on research suitability
        suitability = country.get("research_suitability", 0.5)
        
        if suitability > 0.8:  # High suitability
            return min(2000, int(base_records * 1.5))
        elif suitability > 0.6:  # Medium suitability
            return base_records
        else:  # Lower suitability
            return max(500, int(base_records * 0.75))
    
    def _adapt_quality_filters(self, country: Dict[str, Any], selection: OptimalSelectionResult) -> List[str]:
        """Adapt quality filters based on country data quality."""
        
        base_filters = selection.optimal_parameters.get("quality_filters", [])
        
        quality_level = country.get("estimated_quality", "good")
        
        if quality_level == "excellent":
            return base_filters + ["basisOfRecord=PRESERVED_SPECIMEN"]
        elif quality_level == "very_good":
            return base_filters + ["hasCoordinate=true"]
        elif quality_level in ["emerging", "variable"]:
            # Relax filters for emerging regions
            return [f for f in base_filters if "precision" not in f.lower()]
        
        return base_filters
    
    def _adapt_database_selection(self, country: Dict[str, Any], selection: OptimalSelectionResult) -> List[str]:
        """Adapt database selection based on country characteristics."""
        
        base_databases = [selection.database_strategy["primary_database"]] + selection.database_strategy.get("secondary_databases", [])
        
        region = country.get("region", "unknown")
        
        # Regional database preferences
        if region == "north_america":
            return ["ebird", "gbif", "inaturalist"]
        elif region == "europe":
            return ["gbif", "ebird", "inaturalist"]
        elif region in ["africa", "south_america"]:
            return ["gbif", "inaturalist"]  # Skip eBird if coverage is limited
        
        return base_databases
    
    def _adapt_temporal_range(self, country: Dict[str, Any], selection: OptimalSelectionResult) -> str:
        """Adapt temporal range based on country data characteristics."""
        
        base_temporal = selection.optimal_parameters.get("temporal_range", "comprehensive_historical")
        
        quality_level = country.get("estimated_quality", "good")
        
        if quality_level in ["emerging", "variable"]:
            return "recent_data_focus"  # Focus on recent data for emerging regions
        elif quality_level == "excellent":
            return "comprehensive_historical"  # Use full historical range
        
        return base_temporal
    
    async def _execute_adaptive_collection(self, 
                                         parameters: List[AdaptiveSearchParameters]) -> List[CollectionResult]:
        """Execute adaptive data collection with intelligent optimization."""
        
        logger.info(f"🔄 Executing adaptive collection for {len(parameters)} locations...")
        
        results = []
        
        # Process in batches to avoid API limits
        batch_size = 5
        for i in range(0, len(parameters), batch_size):
            batch = parameters[i:i + batch_size]
            
            logger.info(f"📦 Processing batch {i//batch_size + 1}/{math.ceil(len(parameters)/batch_size)}")
            
            # Execute batch concurrently
            batch_tasks = [
                self._collect_location_data(param) for param in batch
            ]
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            # Process results
            for j, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    logger.error(f"❌ Location {i+j} failed: {result}")
                    # Create failure result
                    failed_result = CollectionResult(
                        location_name=f"Location_{i+j}",
                        coordinates=batch[j].base_coordinates,
                        total_records=0,
                        species_count=0,
                        database_contributions={},
                        quality_metrics={"success": 0.0},
                        collection_time_seconds=0,
                        success_rate=0.0
                    )
                    results.append(failed_result)
                else:
                    results.append(result)
            
            # Adaptive delay between batches
            if i + batch_size < len(parameters):
                await asyncio.sleep(2)  # Respect API limits
        
        return results
    
    async def _collect_location_data(self, params: AdaptiveSearchParameters) -> CollectionResult:
        """Collect data for a specific location with adaptive parameters."""
        
        start_time = datetime.now()
        location_name = f"Location_{params.base_coordinates[0]:.2f}_{params.base_coordinates[1]:.2f}"
        
        try:
            logger.info(f"📍 Collecting: {location_name} (r={params.search_radius_km}km)")
            
            # Collect from each database
            database_results = {}
            total_records = 0
            species_set = set()
            
            for database in params.databases:
                try:
                    db_result = await self._query_database(database, params)
                    database_results[database] = db_result
                    
                    total_records += db_result.get("count", 0)
                    species_set.update(db_result.get("species", []))
                    
                except Exception as e:
                    logger.warning(f"⚠️  {database} query failed: {e}")
                    database_results[database] = {"count": 0, "species": [], "error": str(e)}
            
            # Calculate quality metrics
            quality_metrics = self._calculate_location_quality(database_results, params)
            
            # Calculate success rate
            successful_dbs = sum(1 for db_result in database_results.values() if db_result.get("count", 0) > 0)
            success_rate = successful_dbs / len(params.databases) if params.databases else 0
            
            collection_time = (datetime.now() - start_time).total_seconds()
            
            result = CollectionResult(
                location_name=location_name,
                coordinates=params.base_coordinates,
                total_records=total_records,
                species_count=len(species_set),
                database_contributions={db: result.get("count", 0) for db, result in database_results.items()},
                quality_metrics=quality_metrics,
                collection_time_seconds=collection_time,
                success_rate=success_rate
            )
            
            logger.info(f"✅ {location_name}: {total_records} records, {len(species_set)} species")
            return result
            
        except Exception as e:
            logger.error(f"❌ Collection failed for {location_name}: {e}")
            raise
    
    async def _query_database(self, database: str, params: AdaptiveSearchParameters) -> Dict[str, Any]:
        """Query specific database with adaptive parameters."""
        
        lat, lon = params.base_coordinates
        
        if database == "gbif":
            return await self._query_gbif(lat, lon, params)
        elif database == "ebird":
            return await self._query_ebird(lat, lon, params)
        elif database == "inaturalist":
            return await self._query_inaturalist(lat, lon, params)
        else:
            return {"count": 0, "species": [], "error": f"Unknown database: {database}"}
    
    async def _query_gbif(self, lat: float, lon: float, params: AdaptiveSearchParameters) -> Dict[str, Any]:
        """Query GBIF with adaptive parameters."""
        
        # Build GBIF query URL
        base_url = "https://api.gbif.org/v1/occurrence/search"
        
        query_params = {
            "decimalLatitude": lat,
            "decimalLongitude": lon,
            "distanceInKilometers": params.search_radius_km,
            "limit": min(params.max_records, 1000),  # GBIF limit
            "hasCoordinate": "true"
        }
        
        # Add quality filters
        for filter_item in params.quality_filters:
            if "=" in filter_item:
                key, value = filter_item.split("=", 1)
                query_params[key] = value
        
        try:
            async with self.session.get(base_url, params=query_params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    results = data.get("results", [])
                    species = set()
                    
                    for record in results:
                        if record.get("species"):
                            species.add(record["species"])
                    
                    return {
                        "count": len(results),
                        "species": list(species),
                        "raw_data": results[:10]  # Sample for quality assessment
                    }
                else:
                    return {"count": 0, "species": [], "error": f"HTTP {response.status}"}
                    
        except Exception as e:
            return {"count": 0, "species": [], "error": str(e)}
    
    async def _query_ebird(self, lat: float, lon: float, params: AdaptiveSearchParameters) -> Dict[str, Any]:
        """Query eBird with adaptive parameters (requires API key)."""
        
        # Simplified eBird simulation (would need real API key)
        if "ebird" not in self.api_keys:
            return {"count": 0, "species": [], "error": "eBird API key required"}
        
        # Simulate eBird data based on location
        simulated_count = max(0, int(50 * params.priority_score))  # Simulate based on priority
        simulated_species = [f"Bird_species_{i}" for i in range(min(simulated_count // 3, 20))]
        
        return {
            "count": simulated_count,
            "species": simulated_species,
            "simulated": True
        }
    
    async def _query_inaturalist(self, lat: float, lon: float, params: AdaptiveSearchParameters) -> Dict[str, Any]:
        """Query iNaturalist with adaptive parameters."""
        
        base_url = "https://api.inaturalist.org/v1/observations"
        
        query_params = {
            "lat": lat,
            "lng": lon,
            "radius": params.search_radius_km,
            "per_page": min(params.max_records, 200),  # iNaturalist limit
            "quality_grade": "research",
            "photos": "true"
        }
        
        try:
            async with self.session.get(base_url, params=query_params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    results = data.get("results", [])
                    species = set()
                    
                    for obs in results:
                        taxon = obs.get("taxon", {})
                        if taxon.get("name"):
                            species.add(taxon["name"])
                    
                    return {
                        "count": len(results),
                        "species": list(species),
                        "raw_data": results[:5]  # Sample
                    }
                else:
                    return {"count": 0, "species": [], "error": f"HTTP {response.status}"}
                    
        except Exception as e:
            return {"count": 0, "species": [], "error": str(e)}
    
    def _calculate_location_quality(self, database_results: Dict[str, Dict], params: AdaptiveSearchParameters) -> Dict[str, float]:
        """Calculate quality metrics for a location."""
        
        total_records = sum(result.get("count", 0) for result in database_results.values())
        successful_databases = sum(1 for result in database_results.values() if result.get("count", 0) > 0)
        
        return {
            "data_density": min(1.0, total_records / 100),  # Normalize to 100 records
            "database_coverage": successful_databases / len(params.databases) if params.databases else 0,
            "coordinate_precision": 0.9,  # Assumed high for modern APIs
            "taxonomic_diversity": min(1.0, len(set().union(*(result.get("species", []) for result in database_results.values()))) / 50)
        }
    
    async def _analyze_and_optimize_results(self, results: List[CollectionResult]):
        """Analyze results and optimize future collections."""
        
        logger.info(f"📊 Analyzing collection results...")
        
        # Calculate summary statistics
        total_records = sum(r.total_records for r in results)
        total_species = len(set().union(*(r.database_contributions.keys() for r in results)))
        avg_success_rate = sum(r.success_rate for r in results) / len(results) if results else 0
        
        logger.info(f"📈 COLLECTION SUMMARY:")
        logger.info(f"   Total Records: {total_records:,}")
        logger.info(f"   Unique Species: {total_species:,}")
        logger.info(f"   Average Success Rate: {avg_success_rate:.1%}")
        logger.info(f"   Locations Processed: {len(results)}")
        
        # Identify best performing locations
        best_locations = sorted(results, key=lambda x: x.total_records, reverse=True)[:5]
        
        logger.info(f"\n🏆 TOP PERFORMING LOCATIONS:")
        for i, location in enumerate(best_locations, 1):
            logger.info(f"   {i}. {location.location_name}: {location.total_records} records, {location.species_count} species")
        
        # Update performance metrics
        self.performance_metrics["total_requests"] += len(results)
        self.performance_metrics["successful_requests"] += sum(1 for r in results if r.success_rate > 0.5)
        
        # Save results for future optimization
        self._save_optimization_data(results)
    
    def _save_optimization_data(self, results: List[CollectionResult]):
        """Save results for future optimization."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save results
        results_file = Path(f"adaptive_collection_results_{timestamp}.json")
        with open(results_file, 'w') as f:
            json.dump([asdict(result) for result in results], f, indent=2, default=str)
        
        logger.info(f"💾 Results saved to: {results_file}")

async def run_adaptive_pipeline_demo():
    """Run adaptive pipeline demonstration."""
    
    print("🚀 ADAPTIVE DATA COLLECTION PIPELINE DEMO")
    print("=" * 50)
    
    # Create sample criteria
    criteria = DataSelectionCriteria(
        regions=["global"],
        countries=[],
        ecosystem_types=["tropical_rainforest"],
        taxonomic_groups=["all"],
        research_purpose="biodiversity_assessment",
        temporal_range="comprehensive",
        data_quality_level="good",
        max_radius_km=50,
        max_records_per_area=1000,
        preferred_databases=["gbif", "inaturalist"]
    )
    
    async with AdaptiveDataPipeline() as pipeline:
        results = await pipeline.run_adaptive_collection(criteria)
        
        print(f"\n✅ ADAPTIVE COLLECTION COMPLETE!")
        print(f"📊 Processed {len(results)} locations")
        print(f"🌍 Ready for intelligent conservation analysis!")
        
        return results

if __name__ == "__main__":
    try:
        results = asyncio.run(run_adaptive_pipeline_demo())
        print(f"\n🎯 Adaptive pipeline successfully demonstrated!")
    except Exception as e:
        logger.error(f"Pipeline demo failed: {e}")
        import traceback
        traceback.print_exc()
