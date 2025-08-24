"""
Model Research Package Initialization

This package provides a comprehensive framework for Earth observation analysis
using the PRITHVI foundation model from NASA-IBM collaboration.

Modules:
- models: PRITHVI model implementation and variants
- data: Global satellite data and conservation area management
- analysis: High-performance inference and analysis engines
- visualization: Plotting and visualization utilities
"""

__version__ = "1.0.0"
__author__ = "Earth Observation Research Team"

# Core imports for easy access
from .models.prithvi import (
    SimplifiedPRITHVI,
    PRITHVIConfig,
    create_change_detection_model,
    create_land_cover_model,
    create_prithvi_model
)

from .analysis.inference import (
    InferenceEngine,
    create_inference_engine,
    quick_analysis
)

from .data.global_data import (
    GlobalDataManager,
    global_data_manager,
    SatelliteSource,
    ConservationArea
)

# Package-level convenience functions
def quick_start():
    """Quick start guide for the package."""
    print("🌍 PRITHVI Earth Observation Framework")
    print("=" * 40)
    print("Quick start:")
    print("1. from model_research import create_inference_engine")
    print("2. engine = create_inference_engine()")
    print("3. results = engine.analyze_conservation_area('masoala_np')")
    print()
    print("Available conservation areas:")
    areas = list(global_data_manager.conservation_areas.keys())[:5]
    for area in areas:
        area_info = global_data_manager.get_conservation_area(area)
        print(f"  • {area}: {area_info.name}")
    print(f"  ... and {len(global_data_manager.conservation_areas) - 5} more")

def get_model_info():
    """Get information about available models."""
    model = create_change_detection_model()
    return model.get_model_info()

def get_data_summary():
    """Get summary of available data sources."""
    return global_data_manager.get_summary_statistics()

# Module exports
__all__ = [
    # Core classes
    "SimplifiedPRITHVI",
    "PRITHVIConfig", 
    "InferenceEngine",
    "GlobalDataManager",
    "SatelliteSource",
    "ConservationArea",
    
    # Factory functions
    "create_change_detection_model",
    "create_land_cover_model",
    "create_prithvi_model",
    "create_inference_engine",
    
    # Convenience functions
    "quick_analysis",
    "quick_start",
    "get_model_info",
    "get_data_summary",
    
    # Global instances
    "global_data_manager"
]
