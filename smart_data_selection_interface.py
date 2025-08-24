"""
Smart Data Selection Interface
=============================

Interactive interface for selecting optimal countries, regions, and parameters
based on metadata discovery from global conservation databases.

Author: GeoSpatialAI Development Team
Date: August 24, 2025
"""

import json
from typing import Dict, List, Tuple, Optional, Any, Set
from pathlib import Path
import pandas as pd
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class DataSelectionCriteria:
    """Criteria for intelligent data selection."""
    regions: List[str]
    countries: List[str]
    ecosystem_types: List[str]
    taxonomic_groups: List[str]
    research_purpose: str
    temporal_range: str
    data_quality_level: str
    max_radius_km: int
    max_records_per_area: int
    preferred_databases: List[str]

@dataclass
class OptimalSelectionResult:
    """Result of optimal data selection analysis."""
    recommended_countries: List[Dict[str, Any]]
    optimal_parameters: Dict[str, Any]
    database_strategy: Dict[str, Any]
    expected_data_volume: Dict[str, int]
    quality_indicators: Dict[str, float]
    cost_benefit_score: float
    implementation_plan: List[str]

class SmartDataSelectionInterface:
    """
    Smart interface for selecting optimal data collection parameters
    based on comprehensive metadata analysis.
    """
    
    def __init__(self, metadata_file: Optional[str] = None):
        self.metadata = {}
        self.selection_history = []
        
        # Load metadata if available
        if metadata_file and Path(metadata_file).exists():
            self.load_metadata(metadata_file)
        else:
            self._load_default_metadata()
        
        # Initialize selection templates
        self.research_templates = self._create_research_templates()
        self.regional_expertise = self._create_regional_expertise()
        self.quality_benchmarks = self._create_quality_benchmarks()
    
    def load_metadata(self, metadata_file: str):
        """Load metadata from discovery results."""
        try:
            with open(metadata_file, 'r') as f:
                self.metadata = json.load(f)
            logger.info(f"✅ Loaded metadata from {metadata_file}")
        except Exception as e:
            logger.error(f"❌ Failed to load metadata: {e}")
            self._load_default_metadata()
    
    def _load_default_metadata(self):
        """Load default metadata structure."""
        self.metadata = {
            "databases": {
                "gbif": {
                    "global_statistics": {"total_occurrences": 1700000000},
                    "country_coverage": {
                        "top_countries": [
                            {"country": "US", "occurrences": 350000000},
                            {"country": "CA", "occurrences": 75000000},
                            {"country": "AU", "occurrences": 65000000},
                            {"country": "SE", "occurrences": 45000000},
                            {"country": "NO", "occurrences": 40000000},
                            {"country": "BR", "occurrences": 35000000},
                            {"country": "MX", "occurrences": 30000000},
                            {"country": "FR", "occurrences": 25000000},
                            {"country": "DE", "occurrences": 20000000},
                            {"country": "GB", "occurrences": 18000000}
                        ]
                    }
                }
            }
        }
    
    def _create_research_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create predefined templates for common research purposes."""
        return {
            "biodiversity_assessment": {
                "name": "Comprehensive Biodiversity Assessment",
                "description": "Complete species inventory for conservation planning",
                "optimal_databases": ["gbif", "inaturalist", "ebird"],
                "recommended_radius_km": 50,
                "min_records_per_area": 500,
                "quality_filters": ["hasCoordinate", "recent_data", "verified_identification"],
                "taxonomic_focus": "all_groups",
                "temporal_priority": "comprehensive_historical"
            },
            "real_time_monitoring": {
                "name": "Real-Time Conservation Monitoring",
                "description": "Current species activity and threat detection",
                "optimal_databases": ["ebird", "inaturalist", "nasa_firms"],
                "recommended_radius_km": 25,
                "min_records_per_area": 100,
                "quality_filters": ["recent_data", "citizen_science"],
                "taxonomic_focus": "indicator_species",
                "temporal_priority": "last_30_days"
            },
            "threat_assessment": {
                "name": "Environmental Threat Assessment",
                "description": "Identify and monitor conservation threats",
                "optimal_databases": ["nasa_firms", "gbif", "iucn"],
                "recommended_radius_km": 100,
                "min_records_per_area": 200,
                "quality_filters": ["threat_indicators", "conservation_status"],
                "taxonomic_focus": "threatened_species",
                "temporal_priority": "recent_trends"
            },
            "community_engagement": {
                "name": "Community-Based Conservation",
                "description": "Citizen science and community involvement",
                "optimal_databases": ["inaturalist", "ebird"],
                "recommended_radius_km": 15,
                "min_records_per_area": 150,
                "quality_filters": ["photo_verified", "community_engagement"],
                "taxonomic_focus": "charismatic_species",
                "temporal_priority": "recent_activity"
            },
            "scientific_research": {
                "name": "Academic Research Project",
                "description": "High-quality data for scientific publication",
                "optimal_databases": ["gbif", "iucn"],
                "recommended_radius_km": 75,
                "min_records_per_area": 1000,
                "quality_filters": ["museum_specimens", "peer_reviewed", "coordinate_precision"],
                "taxonomic_focus": "research_grade",
                "temporal_priority": "comprehensive_dataset"
            }
        }
    
    def _create_regional_expertise(self) -> Dict[str, Dict[str, Any]]:
        """Create regional expertise database for optimal data selection."""
        return {
            "north_america": {
                "countries": ["US", "CA", "MX"],
                "data_quality": "excellent",
                "best_databases": ["ebird", "gbif", "inaturalist"],
                "coverage_strength": "urban_suburban",
                "data_density": "very_high",
                "recommended_approach": "comprehensive_multi_database",
                "special_considerations": "excellent_citizen_science_coverage"
            },
            "europe": {
                "countries": ["GB", "DE", "FR", "ES", "IT", "SE", "NO"],
                "data_quality": "excellent", 
                "best_databases": ["gbif", "ebird", "inaturalist"],
                "coverage_strength": "comprehensive",
                "data_density": "very_high",
                "recommended_approach": "historical_plus_modern",
                "special_considerations": "long_term_monitoring_programs"
            },
            "australia_oceania": {
                "countries": ["AU", "NZ"],
                "data_quality": "very_good",
                "best_databases": ["gbif", "inaturalist"],
                "coverage_strength": "coastal_urban",
                "data_density": "high",
                "recommended_approach": "targeted_endemic_focus",
                "special_considerations": "unique_biodiversity_high_endemism"
            },
            "south_america": {
                "countries": ["BR", "AR", "CO", "PE", "EC", "CL"],
                "data_quality": "good_improving",
                "best_databases": ["gbif", "inaturalist"],
                "coverage_strength": "amazon_urban_areas",
                "data_density": "medium_high",
                "recommended_approach": "strategic_sampling_plus_community",
                "special_considerations": "biodiversity_hotspots_data_gaps"
            },
            "asia": {
                "countries": ["CN", "IN", "JP", "TH", "MY", "ID"],
                "data_quality": "variable",
                "best_databases": ["gbif", "inaturalist"],
                "coverage_strength": "urban_developed_areas",
                "data_density": "medium",
                "recommended_approach": "urban_focus_plus_targeted_surveys",
                "special_considerations": "rapidly_improving_infrastructure"
            },
            "africa": {
                "countries": ["ZA", "KE", "TZ", "BW", "NA", "MG"],
                "data_quality": "emerging",
                "best_databases": ["gbif", "inaturalist"],
                "coverage_strength": "protected_areas_urban",
                "data_density": "low_medium",
                "recommended_approach": "protected_area_focus_capacity_building",
                "special_considerations": "high_priority_conservation_areas"
            }
        }
    
    def _create_quality_benchmarks(self) -> Dict[str, Dict[str, Any]]:
        """Create quality benchmarks for different data types."""
        return {
            "excellent": {
                "min_records_per_km2": 50,
                "coordinate_precision_m": 100,
                "identification_confidence": 0.95,
                "temporal_coverage_years": 20,
                "institution_diversity": 10
            },
            "very_good": {
                "min_records_per_km2": 25,
                "coordinate_precision_m": 500,
                "identification_confidence": 0.85,
                "temporal_coverage_years": 10,
                "institution_diversity": 5
            },
            "good": {
                "min_records_per_km2": 10,
                "coordinate_precision_m": 1000,
                "identification_confidence": 0.75,
                "temporal_coverage_years": 5,
                "institution_diversity": 3
            },
            "acceptable": {
                "min_records_per_km2": 5,
                "coordinate_precision_m": 5000,
                "identification_confidence": 0.65,
                "temporal_coverage_years": 3,
                "institution_diversity": 2
            }
        }
    
    def analyze_research_requirements(self, 
                                   research_purpose: str,
                                   geographic_scope: str,
                                   taxonomic_interest: List[str],
                                   quality_requirements: str) -> OptimalSelectionResult:
        """
        Analyze research requirements and provide optimal data selection recommendations.
        """
        
        logger.info(f"🎯 Analyzing requirements for: {research_purpose}")
        
        # Get research template
        template = self.research_templates.get(research_purpose.lower().replace(" ", "_"), 
                                             self.research_templates["biodiversity_assessment"])
        
        # Analyze geographic scope
        optimal_countries = self._select_optimal_countries(geographic_scope, template)
        
        # Generate database strategy
        database_strategy = self._create_database_strategy(template, taxonomic_interest)
        
        # Calculate optimal parameters
        optimal_parameters = self._calculate_optimal_parameters(template, quality_requirements)
        
        # Estimate data volume
        expected_volume = self._estimate_data_volume(optimal_countries, optimal_parameters)
        
        # Calculate quality indicators
        quality_indicators = self._calculate_quality_indicators(optimal_countries, database_strategy)
        
        # Generate implementation plan
        implementation_plan = self._create_implementation_plan(
            template, optimal_countries, database_strategy
        )
        
        # Calculate cost-benefit score
        cost_benefit_score = self._calculate_cost_benefit_score(
            expected_volume, quality_indicators, len(optimal_countries)
        )
        
        return OptimalSelectionResult(
            recommended_countries=optimal_countries,
            optimal_parameters=optimal_parameters,
            database_strategy=database_strategy,
            expected_data_volume=expected_volume,
            quality_indicators=quality_indicators,
            cost_benefit_score=cost_benefit_score,
            implementation_plan=implementation_plan
        )
    
    def _select_optimal_countries(self, geographic_scope: str, template: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Select optimal countries based on geographic scope and research template."""
        
        if geographic_scope.lower() == "global":
            # Select top countries from each region
            optimal_countries = []
            
            # Get top countries from GBIF metadata
            gbif_countries = self.metadata.get("databases", {}).get("gbif", {}).get("country_coverage", {}).get("top_countries", [])
            
            # Add top global countries
            for country in gbif_countries[:15]:  # Top 15 globally
                country_info = {
                    "country_code": country["country"],
                    "data_availability": country["occurrences"],
                    "estimated_quality": self._estimate_country_quality(country["country"]),
                    "region": self._get_region_for_country(country["country"]),
                    "research_suitability": self._calculate_research_suitability(country["country"], template)
                }
                optimal_countries.append(country_info)
            
            # Sort by research suitability
            optimal_countries.sort(key=lambda x: x["research_suitability"], reverse=True)
            return optimal_countries[:10]  # Return top 10
        
        elif geographic_scope.lower() in self.regional_expertise:
            # Regional selection
            region_info = self.regional_expertise[geographic_scope.lower()]
            region_countries = region_info["countries"]
            
            optimal_countries = []
            gbif_countries = self.metadata.get("databases", {}).get("gbif", {}).get("country_coverage", {}).get("top_countries", [])
            
            for country_data in gbif_countries:
                if country_data["country"] in region_countries:
                    country_info = {
                        "country_code": country_data["country"],
                        "data_availability": country_data["occurrences"],
                        "estimated_quality": region_info["data_quality"],
                        "region": geographic_scope,
                        "research_suitability": self._calculate_research_suitability(country_data["country"], template),
                        "regional_strength": region_info["coverage_strength"]
                    }
                    optimal_countries.append(country_info)
            
            return optimal_countries
        
        else:
            # Single country or specific selection
            country_code = geographic_scope.upper()
            gbif_countries = self.metadata.get("databases", {}).get("gbif", {}).get("country_coverage", {}).get("top_countries", [])
            
            for country in gbif_countries:
                if country["country"] == country_code:
                    return [{
                        "country_code": country_code,
                        "data_availability": country["occurrences"],
                        "estimated_quality": self._estimate_country_quality(country_code),
                        "region": self._get_region_for_country(country_code),
                        "research_suitability": self._calculate_research_suitability(country_code, template)
                    }]
            
            # If not found in top countries, return basic info
            return [{
                "country_code": country_code,
                "data_availability": "unknown",
                "estimated_quality": "variable",
                "region": "unknown",
                "research_suitability": 0.5
            }]
    
    def _estimate_country_quality(self, country_code: str) -> str:
        """Estimate data quality for a country."""
        quality_map = {
            "US": "excellent", "CA": "excellent", "AU": "excellent",
            "GB": "excellent", "DE": "excellent", "FR": "excellent",
            "SE": "excellent", "NO": "excellent", "NL": "excellent",
            "BR": "very_good", "MX": "very_good", "AR": "very_good",
            "IN": "good", "CN": "good", "ZA": "good",
            "MG": "emerging", "KE": "emerging", "TZ": "emerging"
        }
        return quality_map.get(country_code, "variable")
    
    def _get_region_for_country(self, country_code: str) -> str:
        """Get region for country code."""
        region_map = {
            "US": "north_america", "CA": "north_america", "MX": "north_america",
            "BR": "south_america", "AR": "south_america", "CO": "south_america",
            "GB": "europe", "DE": "europe", "FR": "europe", "SE": "europe",
            "AU": "australia_oceania", "NZ": "australia_oceania",
            "CN": "asia", "IN": "asia", "JP": "asia",
            "ZA": "africa", "KE": "africa", "MG": "africa"
        }
        return region_map.get(country_code, "unknown")
    
    def _calculate_research_suitability(self, country_code: str, template: Dict[str, Any]) -> float:
        """Calculate research suitability score for a country."""
        base_score = 0.5
        
        # Quality bonus
        quality = self._estimate_country_quality(country_code)
        quality_bonus = {"excellent": 0.3, "very_good": 0.2, "good": 0.1, "emerging": 0.05}.get(quality, 0)
        
        # Database availability bonus
        region = self._get_region_for_country(country_code)
        if region in self.regional_expertise:
            region_info = self.regional_expertise[region]
            template_dbs = set(template.get("optimal_databases", []))
            region_dbs = set(region_info.get("best_databases", []))
            db_overlap = len(template_dbs.intersection(region_dbs)) / len(template_dbs) if template_dbs else 0
            db_bonus = db_overlap * 0.2
        else:
            db_bonus = 0
        
        return min(1.0, base_score + quality_bonus + db_bonus)
    
    def _create_database_strategy(self, template: Dict[str, Any], taxonomic_interest: List[str]) -> Dict[str, Any]:
        """Create optimal database usage strategy."""
        
        strategy = {
            "primary_database": template["optimal_databases"][0] if template["optimal_databases"] else "gbif",
            "secondary_databases": template["optimal_databases"][1:] if len(template["optimal_databases"]) > 1 else [],
            "query_sequence": [],
            "integration_approach": "",
            "validation_strategy": ""
        }
        
        # Create query sequence
        for i, db in enumerate(template["optimal_databases"]):
            query_info = {
                "database": db,
                "priority": i + 1,
                "purpose": self._get_database_purpose(db, taxonomic_interest),
                "expected_contribution": self._estimate_database_contribution(db, taxonomic_interest)
            }
            strategy["query_sequence"].append(query_info)
        
        # Integration approach
        if len(template["optimal_databases"]) > 1:
            strategy["integration_approach"] = "cross_reference_validation"
        else:
            strategy["integration_approach"] = "single_source_comprehensive"
        
        # Validation strategy
        strategy["validation_strategy"] = "coordinate_temporal_taxonomic_verification"
        
        return strategy
    
    def _get_database_purpose(self, database: str, taxonomic_interest: List[str]) -> str:
        """Get primary purpose for each database in the strategy."""
        purposes = {
            "gbif": "comprehensive_historical_specimens",
            "ebird": "real_time_bird_observations",
            "inaturalist": "community_photo_documentation",
            "iucn": "conservation_status_validation",
            "nasa_firms": "environmental_threat_monitoring"
        }
        return purposes.get(database, "general_biodiversity_data")
    
    def _estimate_database_contribution(self, database: str, taxonomic_interest: List[str]) -> float:
        """Estimate expected data contribution from each database."""
        contributions = {
            "gbif": 0.6,  # 60% of total data typically
            "ebird": 0.3,  # 30% for bird-focused
            "inaturalist": 0.25,  # 25% for photo-documented
            "iucn": 0.1,   # 10% conservation status
            "nasa_firms": 0.05  # 5% threat data
        }
        
        # Adjust based on taxonomic interest
        if "birds" in taxonomic_interest and database == "ebird":
            contributions[database] = 0.8
        
        return contributions.get(database, 0.1)
    
    def _calculate_optimal_parameters(self, template: Dict[str, Any], quality_requirements: str) -> Dict[str, Any]:
        """Calculate optimal search parameters."""
        
        quality_benchmark = self.quality_benchmarks.get(quality_requirements, self.quality_benchmarks["good"])
        
        return {
            "search_radius_km": template["recommended_radius_km"],
            "max_records_per_area": max(template["min_records_per_area"], quality_benchmark["min_records_per_km2"] * 100),
            "coordinate_precision_threshold_m": quality_benchmark["coordinate_precision_m"],
            "temporal_range": template["temporal_priority"],
            "quality_filters": template["quality_filters"],
            "batch_size": 1000,
            "concurrent_requests": 5,
            "cache_duration_hours": 24
        }
    
    def _estimate_data_volume(self, countries: List[Dict[str, Any]], parameters: Dict[str, Any]) -> Dict[str, int]:
        """Estimate expected data volume."""
        
        total_records = 0
        for country in countries:
            if isinstance(country["data_availability"], int):
                # Estimate based on search radius and country data density
                country_estimate = min(
                    parameters["max_records_per_area"],
                    int(country["data_availability"] * 0.001)  # 0.1% of country total
                )
                total_records += country_estimate
        
        return {
            "estimated_total_records": total_records,
            "estimated_species": int(total_records * 0.1),  # Rough estimate
            "estimated_locations": len(countries) * 5,  # ~5 locations per country
            "estimated_storage_mb": int(total_records * 0.002)  # ~2KB per record
        }
    
    def _calculate_quality_indicators(self, countries: List[Dict[str, Any]], strategy: Dict[str, Any]) -> Dict[str, float]:
        """Calculate expected quality indicators."""
        
        avg_quality = sum(
            {"excellent": 0.95, "very_good": 0.85, "good": 0.75, "emerging": 0.6, "variable": 0.65}
            .get(country.get("estimated_quality", "variable"), 0.65)
            for country in countries
        ) / len(countries) if countries else 0.65
        
        return {
            "overall_quality_score": avg_quality,
            "coordinate_accuracy": avg_quality,
            "taxonomic_reliability": avg_quality * 0.9,
            "temporal_coverage": avg_quality * 0.8,
            "cross_database_validation": len(strategy["secondary_databases"]) / 4.0  # Max 4 databases
        }
    
    def _create_implementation_plan(self, template: Dict[str, Any], countries: List[Dict[str, Any]], strategy: Dict[str, Any]) -> List[str]:
        """Create step-by-step implementation plan."""
        
        plan = [
            "🔧 Configure API credentials for selected databases",
            f"🌍 Set up geographic search areas for {len(countries)} countries",
            f"📊 Initialize data collection with {strategy['primary_database']} as primary source"
        ]
        
        if strategy["secondary_databases"]:
            plan.append(f"🔄 Configure secondary data sources: {', '.join(strategy['secondary_databases'])}")
        
        plan.extend([
            "📝 Implement data validation and quality filtering",
            "💾 Set up local caching and storage system",
            "🔍 Execute initial data collection and validation",
            "📈 Monitor data quality and coverage metrics",
            "🔄 Implement regular data updates and synchronization"
        ])
        
        return plan
    
    def _calculate_cost_benefit_score(self, data_volume: Dict[str, int], quality: Dict[str, float], num_countries: int) -> float:
        """Calculate cost-benefit score for the selection."""
        
        # Benefits: data volume, quality, geographic coverage
        data_benefit = min(1.0, data_volume["estimated_total_records"] / 100000)  # Normalize to 100k records
        quality_benefit = quality["overall_quality_score"]
        coverage_benefit = min(1.0, num_countries / 10)  # Normalize to 10 countries
        
        # Costs: API calls, storage, processing time
        api_cost = data_volume["estimated_total_records"] / 1000000  # Cost per million records
        storage_cost = data_volume["estimated_storage_mb"] / 10000   # Cost per 10GB
        processing_cost = num_countries / 50  # Processing complexity
        
        total_benefit = (data_benefit + quality_benefit + coverage_benefit) / 3
        total_cost = (api_cost + storage_cost + processing_cost) / 3
        
        return total_benefit / (total_cost + 0.1)  # Avoid division by zero
    
    def generate_selection_report(self, result: OptimalSelectionResult, criteria: DataSelectionCriteria) -> str:
        """Generate comprehensive selection report."""
        
        report = f"""
🎯 SMART DATA SELECTION REPORT
{'=' * 50}

📋 SELECTION CRITERIA
Research Purpose: {criteria.research_purpose}
Geographic Scope: {', '.join(criteria.regions) if criteria.regions else 'Global'}
Quality Level: {criteria.data_quality_level}
Max Radius: {criteria.max_radius_km} km
Max Records: {criteria.max_records_per_area}

🌍 RECOMMENDED COUNTRIES ({len(result.recommended_countries)})
{'-' * 30}"""

        for i, country in enumerate(result.recommended_countries[:5], 1):
            report += f"""
{i}. {country['country_code']} ({country.get('region', 'Unknown').title()})
   📊 Data Availability: {country['data_availability']:,} records
   💯 Quality Level: {country['estimated_quality'].title()}
   🎯 Research Suitability: {country['research_suitability']:.1%}"""

        report += f"""

💾 EXPECTED DATA VOLUME
{'-' * 25}
Total Records: {result.expected_data_volume['estimated_total_records']:,}
Estimated Species: {result.expected_data_volume['estimated_species']:,}
Storage Required: {result.expected_data_volume['estimated_storage_mb']} MB

🗄️  DATABASE STRATEGY
{'-' * 20}
Primary: {result.database_strategy['primary_database'].upper()}
Secondary: {', '.join(result.database_strategy['secondary_databases']).upper()}
Integration: {result.database_strategy['integration_approach'].replace('_', ' ').title()}

💯 QUALITY INDICATORS
{'-' * 20}
Overall Quality: {result.quality_indicators['overall_quality_score']:.1%}
Coordinate Accuracy: {result.quality_indicators['coordinate_accuracy']:.1%}
Cross-validation: {result.quality_indicators['cross_database_validation']:.1%}

💰 COST-BENEFIT SCORE: {result.cost_benefit_score:.2f}/10

📋 IMPLEMENTATION PLAN
{'-' * 22}"""

        for i, step in enumerate(result.implementation_plan, 1):
            report += f"\n{i}. {step}"

        report += f"""

✅ RECOMMENDATION SUMMARY
{'-' * 25}
This selection provides optimal balance of data quality, geographic coverage,
and implementation feasibility for your research objectives.

🚀 Ready to implement with high confidence of success!
"""
        
        return report

def interactive_selection_wizard():
    """Run interactive selection wizard."""
    
    print("🧙‍♂️ SMART DATA SELECTION WIZARD")
    print("=" * 40)
    
    interface = SmartDataSelectionInterface()
    
    # Step 1: Research Purpose
    print("\n1️⃣  What is your research purpose?")
    purposes = list(interface.research_templates.keys())
    for i, purpose in enumerate(purposes, 1):
        template = interface.research_templates[purpose]
        print(f"   {i}. {template['name']}")
        print(f"      {template['description']}")
    
    purpose_choice = input(f"\nSelect purpose (1-{len(purposes)}): ").strip()
    try:
        selected_purpose = purposes[int(purpose_choice) - 1]
    except (ValueError, IndexError):
        selected_purpose = "biodiversity_assessment"
    
    # Step 2: Geographic Scope
    print("\n2️⃣  Geographic scope?")
    regions = ["global", "north_america", "europe", "south_america", "asia", "africa", "australia_oceania"]
    for i, region in enumerate(regions, 1):
        print(f"   {i}. {region.replace('_', ' ').title()}")
    
    geo_choice = input(f"\nSelect scope (1-{len(regions)}): ").strip()
    try:
        selected_scope = regions[int(geo_choice) - 1]
    except (ValueError, IndexError):
        selected_scope = "global"
    
    # Step 3: Quality Requirements
    print("\n3️⃣  Data quality requirements?")
    qualities = ["excellent", "very_good", "good", "acceptable"]
    for i, quality in enumerate(qualities, 1):
        print(f"   {i}. {quality.replace('_', ' ').title()}")
    
    quality_choice = input(f"\nSelect quality (1-{len(qualities)}): ").strip()
    try:
        selected_quality = qualities[int(quality_choice) - 1]
    except (ValueError, IndexError):
        selected_quality = "good"
    
    # Generate recommendations
    print(f"\n🔍 Analyzing optimal selection...")
    
    result = interface.analyze_research_requirements(
        research_purpose=selected_purpose,
        geographic_scope=selected_scope,
        taxonomic_interest=["all"],
        quality_requirements=selected_quality
    )
    
    # Create criteria object
    criteria = DataSelectionCriteria(
        regions=[selected_scope],
        countries=[],
        ecosystem_types=[],
        taxonomic_groups=["all"],
        research_purpose=selected_purpose,
        temporal_range="comprehensive",
        data_quality_level=selected_quality,
        max_radius_km=50,
        max_records_per_area=1000,
        preferred_databases=[]
    )
    
    # Generate and display report
    report = interface.generate_selection_report(result, criteria)
    print(report)
    
    return result

if __name__ == "__main__":
    try:
        result = interactive_selection_wizard()
        print(f"\n🎯 Selection complete! Use these recommendations to configure your data collection.")
    except Exception as e:
        logger.error(f"Selection wizard failed: {e}")
        import traceback
        traceback.print_exc()
