"""
Model Path Configuration
========================
Centralized configuration for all model file paths.
This allows easy updating when model locations change.
"""

import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

class ModelPaths:
    """Centralized model path configuration."""
    
    # Base directories
    MODELS_DIR = PROJECT_ROOT / "models"
    
    # Specific model files
    YOLOV8_NANO = MODELS_DIR / "yolov8n.pt"
    
    # Legacy paths for backward compatibility
    YOLOV8_NANO_LEGACY = PROJECT_ROOT / "yolov8n.pt"
    
    @classmethod
    def get_yolo_model_path(cls):
        """Get YOLOv8 model path, checking new location first, then legacy."""
        if cls.YOLOV8_NANO.exists():
            return str(cls.YOLOV8_NANO)
        elif cls.YOLOV8_NANO_LEGACY.exists():
            return str(cls.YOLOV8_NANO_LEGACY)
        else:
            # Return new path - YOLO will download if needed
            return str(cls.YOLOV8_NANO)
    
    @classmethod
    def ensure_models_dir(cls):
        """Ensure models directory exists."""
        cls.MODELS_DIR.mkdir(exist_ok=True)
        return cls.MODELS_DIR

# Convenience function for easy import
def get_yolo_path():
    """Get the YOLOv8 model path."""
    return ModelPaths.get_yolo_model_path()
