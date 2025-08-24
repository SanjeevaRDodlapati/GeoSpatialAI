"""
Global Data Management for Earth Observation
Satellite data sources and conservation area definitions for PRITHVI analysis.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@dataclass
class SatelliteSource:
    """Configuration for satellite data sources."""
    name: str
    bands: List[str]
    resolution_m: float
    temporal_resolution_days: int
    coverage: str
    description: str

@dataclass
class ConservationArea:
    """Conservation area definition."""
    name: str
    country: str
    coordinates: Tuple[float, float, float, float]  # (min_lat, min_lon, max_lat, max_lon)
    area_km2: float
    ecosystem_type: str
    protection_status: str
    key_species: List[str]
    threats: List[str]

class GlobalDataManager:
    """
    Manages global satellite data sources and conservation areas for Earth observation analysis.
    """
    
    def __init__(self):
        self.satellite_sources = self._initialize_satellite_sources()
        self.conservation_areas = self._initialize_conservation_areas()
        
    def _initialize_satellite_sources(self) -> Dict[str, SatelliteSource]:
        """Initialize satellite data source configurations."""
        sources = {
            "sentinel2": SatelliteSource(
                name="Sentinel-2",
                bands=["B02", "B03", "B04", "B08", "B11", "B12"],  # Blue, Green, Red, NIR, SWIR1, SWIR2
                resolution_m=10.0,
                temporal_resolution_days=5,
                coverage="Global",
                description="ESA optical satellite constellation for land monitoring"
            ),
            "landsat8": SatelliteSource(
                name="Landsat-8",
                bands=["B2", "B3", "B4", "B5", "B6", "B7"],  # Blue, Green, Red, NIR, SWIR1, SWIR2
                resolution_m=30.0,
                temporal_resolution_days=16,
                coverage="Global",
                description="NASA/USGS satellite for Earth observation since 2013"
            ),
            "landsat9": SatelliteSource(
                name="Landsat-9",
                bands=["B2", "B3", "B4", "B5", "B6", "B7"],
                resolution_m=30.0,
                temporal_resolution_days=16,
                coverage="Global",
                description="NASA/USGS satellite for Earth observation since 2021"
            ),
            "modis": SatelliteSource(
                name="MODIS",
                bands=["Band1", "Band2", "Band3", "Band4", "Band5", "Band6"],
                resolution_m=250.0,
                temporal_resolution_days=1,
                coverage="Global",
                description="NASA Terra/Aqua moderate resolution imaging"
            ),
            "planet_labs": SatelliteSource(
                name="Planet Labs",
                bands=["Blue", "Green", "Red", "NIR"],
                resolution_m=3.0,
                temporal_resolution_days=1,
                coverage="Global (commercial)",
                description="High-resolution commercial satellite constellation"
            )
        }
        return sources
    
    def _initialize_conservation_areas(self) -> Dict[str, ConservationArea]:
        """Initialize priority conservation areas for analysis."""
        areas = {
            "masoala_np": ConservationArea(
                name="Masoala National Park",
                country="Madagascar",
                coordinates=(-15.8, 49.9, -15.3, 50.5),
                area_km2=2300.0,
                ecosystem_type="Tropical Rainforest",
                protection_status="National Park",
                key_species=["Red-ruffed Lemur", "Aye-aye", "Madagascar Serpent Eagle"],
                threats=["Deforestation", "Illegal logging", "Slash-and-burn agriculture"]
            ),
            "andasibe_mantadia": ConservationArea(
                name="Andasibe-Mantadia National Park",
                country="Madagascar",
                coordinates=(-18.9, 48.4, -18.7, 48.6),
                area_km2=155.0,
                ecosystem_type="Montane Rainforest",
                protection_status="National Park",
                key_species=["Indri", "Diademed Sifaka", "Madagascar Tree Boa"],
                threats=["Habitat fragmentation", "Human encroachment", "Climate change"]
            ),
            "amazon_core": ConservationArea(
                name="Amazon Core Region",
                country="Brazil",
                coordinates=(-10.0, -70.0, -2.0, -60.0),
                area_km2=500000.0,
                ecosystem_type="Tropical Rainforest",
                protection_status="Multiple Protected Areas",
                key_species=["Jaguar", "Giant Otter", "Harpy Eagle", "Brazil Nut Tree"],
                threats=["Deforestation", "Mining", "Cattle ranching", "Infrastructure development"]
            ),
            "borneo_heart": ConservationArea(
                name="Heart of Borneo",
                country="Malaysia/Indonesia/Brunei",
                coordinates=(0.0, 110.0, 7.0, 119.0),
                area_km2=220000.0,
                ecosystem_type="Tropical Rainforest",
                protection_status="Transboundary Conservation Initiative",
                key_species=["Bornean Orangutan", "Pygmy Elephant", "Clouded Leopard"],
                threats=["Palm oil plantations", "Logging", "Mining", "Forest fires"]
            ),
            "congo_basin": ConservationArea(
                name="Congo Basin Core",
                country="Democratic Republic of Congo",
                coordinates=(-5.0, 15.0, 5.0, 30.0),
                area_km2=200000.0,
                ecosystem_type="Tropical Rainforest",
                protection_status="Multiple National Parks",
                key_species=["Mountain Gorilla", "Forest Elephant", "Okapi", "Chimpanzee"],
                threats=["Illegal logging", "Mining", "Bushmeat hunting", "Political instability"]
            ),
            "yellowstone": ConservationArea(
                name="Greater Yellowstone Ecosystem",
                country="United States",
                coordinates=(44.0, -111.0, 45.0, -109.5),
                area_km2=20000.0,
                ecosystem_type="Temperate Forest/Grassland",
                protection_status="National Park + Surrounding Areas",
                key_species=["Grizzly Bear", "Gray Wolf", "Bison", "Elk"],
                threats=["Climate change", "Human development", "Disease", "Tourism pressure"]
            ),
            "serengeti": ConservationArea(
                name="Serengeti Ecosystem",
                country="Tanzania/Kenya",
                coordinates=(-3.0, 34.0, -1.0, 36.0),
                area_km2=30000.0,
                ecosystem_type="Savanna",
                protection_status="National Park + Conservancies",
                key_species=["African Lion", "African Elephant", "Wildebeest", "Cheetah"],
                threats=["Human-wildlife conflict", "Poaching", "Habitat fragmentation", "Climate change"]
            ),
            "great_barrier_reef": ConservationArea(
                name="Great Barrier Reef",
                country="Australia",
                coordinates=(-24.0, 145.0, -10.0, 155.0),
                area_km2=35000.0,
                ecosystem_type="Marine Coral Reef",
                protection_status="World Heritage Marine Park",
                key_species=["Coral species", "Green Sea Turtle", "Dugong", "Reef Sharks"],
                threats=["Ocean warming", "Ocean acidification", "Pollution", "Crown-of-thorns starfish"]
            ),
            "antarctic_peninsula": ConservationArea(
                name="Antarctic Peninsula",
                country="Antarctica",
                coordinates=(-70.0, -80.0, -60.0, -50.0),
                area_km2=100000.0,
                ecosystem_type="Polar/Marine",
                protection_status="Antarctic Treaty Protected",
                key_species=["Emperor Penguin", "Adelie Penguin", "Weddell Seal", "Antarctic Krill"],
                threats=["Climate change", "Ice sheet melting", "Ocean warming", "Tourism"]
            ),
            "sahel_corridor": ConservationArea(
                name="Sahel Conservation Corridor",
                country="Multiple (West Africa)",
                coordinates=(10.0, -15.0, 18.0, 15.0),
                area_km2=300000.0,
                ecosystem_type="Savanna/Dry Forest",
                protection_status="Multiple Protected Areas",
                key_species=["West African Giraffe", "African Wild Dog", "Cheetah", "Desert Elephant"],
                threats=["Desertification", "Overgrazing", "Human migration", "Climate change"]
            )
        }
        return areas
    
    def get_satellite_source(self, source_name: str) -> Optional[SatelliteSource]:
        """Get satellite source configuration by name."""
        return self.satellite_sources.get(source_name.lower())
    
    def get_conservation_area(self, area_name: str) -> Optional[ConservationArea]:
        """Get conservation area by name."""
        return self.conservation_areas.get(area_name.lower())
    
    def list_satellite_sources(self) -> List[str]:
        """List available satellite data sources."""
        return list(self.satellite_sources.keys())
    
    def list_conservation_areas(self) -> List[str]:
        """List available conservation areas."""
        return list(self.conservation_areas.keys())
    
    def get_areas_by_ecosystem(self, ecosystem_type: str) -> List[ConservationArea]:
        """Get conservation areas by ecosystem type."""
        return [area for area in self.conservation_areas.values() 
                if ecosystem_type.lower() in area.ecosystem_type.lower()]
    
    def get_areas_by_country(self, country: str) -> List[ConservationArea]:
        """Get conservation areas by country."""
        return [area for area in self.conservation_areas.values() 
                if country.lower() in area.country.lower()]
    
    def generate_sample_data(self, area_name: str, source_name: str, 
                           num_samples: int = 100) -> np.ndarray:
        """
        Generate synthetic satellite data for a conservation area.
        
        Args:
            area_name: Name of conservation area
            source_name: Name of satellite source
            num_samples: Number of synthetic samples to generate
            
        Returns:
            Synthetic satellite data array
        """
        area = self.get_conservation_area(area_name)
        source = self.get_satellite_source(source_name)
        
        if not area or not source:
            raise ValueError(f"Invalid area ({area_name}) or source ({source_name})")
        
        # Generate synthetic data based on ecosystem type
        if "forest" in area.ecosystem_type.lower():
            # Forest areas: higher NIR, lower red (healthy vegetation)
            base_values = [0.1, 0.15, 0.12, 0.4, 0.2, 0.15]  # Typical forest reflectance
        elif "savanna" in area.ecosystem_type.lower():
            # Savanna: mixed vegetation
            base_values = [0.15, 0.18, 0.2, 0.35, 0.25, 0.2]
        elif "marine" in area.ecosystem_type.lower():
            # Marine areas: higher blue/green, very low NIR
            base_values = [0.08, 0.12, 0.15, 0.05, 0.03, 0.02]
        else:
            # Default values
            base_values = [0.12, 0.15, 0.18, 0.25, 0.2, 0.15]
        
        # Add realistic noise and variation
        num_bands = len(source.bands)
        data = np.random.normal(
            loc=base_values[:num_bands], 
            scale=0.05, 
            size=(num_samples, 224, 224, num_bands)
        )
        
        # Ensure values are within valid range [0, 1]
        data = np.clip(data, 0, 1)
        
        logger.info(f"Generated {num_samples} synthetic samples for {area.name} using {source.name}")
        
        return data
    
    def get_priority_analysis_queue(self) -> List[Tuple[str, str, str]]:
        """
        Get priority conservation areas for analysis.
        
        Returns:
            List of (area_name, satellite_source, analysis_type) tuples
        """
        priority_queue = [
            ("masoala_np", "sentinel2", "deforestation_monitoring"),
            ("amazon_core", "landsat8", "change_detection"),
            ("borneo_heart", "planet_labs", "palm_oil_expansion"),
            ("congo_basin", "sentinel2", "illegal_logging_detection"),
            ("great_barrier_reef", "modis", "coral_bleaching_monitoring"),
            ("antarctic_peninsula", "landsat9", "ice_loss_tracking"),
            ("serengeti", "sentinel2", "habitat_fragmentation"),
            ("yellowstone", "landsat8", "wildfire_recovery"),
            ("andasibe_mantadia", "planet_labs", "forest_degradation"),
            ("sahel_corridor", "modis", "desertification_monitoring")
        ]
        
        return priority_queue
    
    def get_summary_statistics(self) -> Dict:
        """Get summary statistics for the global data repository."""
        total_area = sum(area.area_km2 for area in self.conservation_areas.values())
        
        ecosystem_counts = {}
        for area in self.conservation_areas.values():
            ecosystem = area.ecosystem_type
            ecosystem_counts[ecosystem] = ecosystem_counts.get(ecosystem, 0) + 1
        
        country_counts = {}
        for area in self.conservation_areas.values():
            countries = area.country.split("/")
            for country in countries:
                country = country.strip()
                country_counts[country] = country_counts.get(country, 0) + 1
        
        return {
            "total_conservation_areas": len(self.conservation_areas),
            "total_protected_area_km2": total_area,
            "satellite_sources": len(self.satellite_sources),
            "ecosystem_distribution": ecosystem_counts,
            "country_distribution": country_counts,
            "priority_analysis_tasks": len(self.get_priority_analysis_queue())
        }

# Global instance
global_data_manager = GlobalDataManager()

if __name__ == "__main__":
    # Example usage
    manager = GlobalDataManager()
    
    print("Global Data Manager Summary:")
    stats = manager.get_summary_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\nPriority Analysis Queue:")
    for i, (area, source, analysis) in enumerate(manager.get_priority_analysis_queue()[:5]):
        print(f"  {i+1}. {area} ({source}) - {analysis}")
