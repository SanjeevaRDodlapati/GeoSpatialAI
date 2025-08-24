"""
Data Management Module

This module handles global satellite data sources and conservation areas
for Earth observation analysis.
"""

from .global_data import (
    GlobalDataManager,
    SatelliteSource,
    ConservationArea,
    global_data_manager
)

__all__ = [
    "GlobalDataManager",
    "SatelliteSource",
    "ConservationArea", 
    "global_data_manager"
]
