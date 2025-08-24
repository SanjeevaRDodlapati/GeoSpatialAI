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
    CHECKPOINTS_DIR = MODELS_DIR / "checkpoints"
    IMPLEMENTATIONS_DIR = MODELS_DIR / "implementations"
    CONFIGS_DIR = MODELS_DIR / "configs"
    
    # Specific model files (updated paths)
    YOLOV8_NANO = CHECKPOINTS_DIR / "yolov8n.pt"
    SAM_VIT_H = CHECKPOINTS_DIR / "sam" / "sam_vit_h.pth"
    
    # Legacy paths for backward compatibility
    YOLOV8_NANO_LEGACY = PROJECT_ROOT / "yolov8n.pt"
    SAM_LEGACY = PROJECT_ROOT / "models" / "sam" / "sam_vit_h.pth"
    
    @classmethod
    def get_yolo_model_path(cls):
        """Get YOLOv8 model path, checking new location first, then legacy."""
        if cls.YOLOV8_NANO.exists():
            return str(cls.YOLOV8_NANO)
        elif cls.YOLOV8_NANO_LEGACY.exists():
            return str(cls.YOLOV8_NANO_LEGACY)
        else:
            # Return new path - YOLO will download if needed
            cls.ensure_models_dir()
            return str(cls.YOLOV8_NANO)
    
    @classmethod
    def get_sam_model_path(cls, model_type: str = "vit_h"):
        """Get SAM model path."""
        if model_type == "vit_h":
            if cls.SAM_VIT_H.exists():
                return str(cls.SAM_VIT_H)
            elif cls.SAM_LEGACY.exists():
                return str(cls.SAM_LEGACY)
        return str(cls.CHECKPOINTS_DIR / "sam" / f"sam_{model_type}.pth")
    
    @classmethod
    def ensure_models_dir(cls):
        """Ensure all model directories exist."""
        cls.MODELS_DIR.mkdir(exist_ok=True)
        cls.CHECKPOINTS_DIR.mkdir(exist_ok=True)
        cls.IMPLEMENTATIONS_DIR.mkdir(exist_ok=True)
        cls.CONFIGS_DIR.mkdir(exist_ok=True)
        return cls.MODELS_DIR

# Convenience functions for easy import
def get_yolo_path():
    """Get the YOLOv8 model path."""
    return ModelPaths.get_yolo_model_path()

def get_sam_path(model_type: str = "vit_h"):
    """Get the SAM model path."""
    return ModelPaths.get_sam_model_path(model_type)

def get_models_info():
    """Get information about available models."""
    return {
        "checkpoints_dir": str(ModelPaths.CHECKPOINTS_DIR),
        "implementations_dir": str(ModelPaths.IMPLEMENTATIONS_DIR),
        "configs_dir": str(ModelPaths.CONFIGS_DIR),
        "yolo_path": ModelPaths.get_yolo_model_path(),
        "sam_path": ModelPaths.get_sam_model_path()
    }
