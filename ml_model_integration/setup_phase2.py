#!/usr/bin/env python3
"""
Phase 2 Setup: Madagascar Specialization & Transfer Learning
============================================================

This script initializes Phase 2 of the Conservation AI project, focusing on
Madagascar-specific model specialization and transfer learning.

Author: Madagascar Conservation AI Team
Date: August 2025
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Phase2Setup:
    """Setup and initialization for Phase 2 Madagascar specialization."""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.phase2_path = self.base_path / "ml_model_integration" / "phase2_madagascar_specialization"
        self.datasets_path = self.phase2_path / "datasets"
        self.models_path = self.phase2_path / "models"
        self.training_path = self.phase2_path / "training_pipelines"
        
    def create_directory_structure(self) -> None:
        """Create the Phase 2 directory structure."""
        logger.info("🏗️ Creating Phase 2 directory structure...")
        
        directories = [
            # Main phase2 directories
            self.phase2_path,
            self.datasets_path,
            self.models_path,
            self.training_path,
            
            # Dataset subdirectories
            self.datasets_path / "madagascar_wildlife_images",
            self.datasets_path / "endemic_bird_audio",
            self.datasets_path / "ecosystem_boundaries",
            self.datasets_path / "lemur_identification",
            self.datasets_path / "camera_trap_data",
            self.datasets_path / "satellite_imagery",
            
            # Model subdirectories
            self.models_path / "yolov8_madagascar",
            self.models_path / "birdnet_madagascar", 
            self.models_path / "sam_madagascar",
            self.models_path / "lemur_classifier",
            self.models_path / "checkpoints",
            self.models_path / "exports",
            
            # Training subdirectories
            self.training_path / "yolov8_training",
            self.training_path / "birdnet_training",
            self.training_path / "sam_training",
            self.training_path / "lemur_training",
            self.training_path / "configs",
            self.training_path / "logs",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"✅ Created: {directory}")
    
    def create_dataset_configs(self) -> None:
        """Create dataset configuration files."""
        logger.info("📊 Creating dataset configurations...")
        
        # Madagascar wildlife dataset config
        wildlife_config = {
            "name": "madagascar_wildlife",
            "description": "Camera trap images of Madagascar endemic wildlife",
            "species_count": 40,
            "target_species": [
                "Indri indri", "Propithecus diadema", "Lemur catta",
                "Eulemur macaco", "Microcebus murinus", "Daubentonia madagascariensis",
                "Cryptoprocta ferox", "Fossa fossana", "Tenrec ecaudatus"
            ],
            "image_size": [640, 640],
            "batch_size": 16,
            "augmentation": True,
            "split_ratio": {"train": 0.7, "val": 0.2, "test": 0.1}
        }
        
        # Madagascar bird audio config
        bird_config = {
            "name": "madagascar_birds",
            "description": "Audio recordings of Madagascar endemic birds",
            "species_count": 250,
            "endemic_families": [
                "Vangidae", "Bernieridae", "Mesitornithidae", 
                "Leptosomidae", "Brachypteraciidae"
            ],
            "audio_format": "wav",
            "sample_rate": 22050,
            "duration": 3.0,
            "overlap": 0.5,
            "augmentation": True
        }
        
        # Ecosystem boundaries config
        ecosystem_config = {
            "name": "madagascar_ecosystems",
            "description": "Satellite imagery for ecosystem segmentation",
            "ecosystem_types": [
                "Spiny Forest", "Dry Deciduous Forest", "Eastern Rainforest",
                "Central Highland", "Mangrove", "Coastal Dune",
                "Agricultural Land", "Urban Area", "Water Body",
                "Degraded Forest", "Grassland", "Rocky Outcrop"
            ],
            "image_resolution": "10m",
            "tile_size": [512, 512],
            "channels": ["RGB", "NIR", "SWIR"],
            "temporal_range": "2020-2025"
        }
        
        # Lemur species config
        lemur_config = {
            "name": "lemur_species_identification",
            "description": "Specialized dataset for 108 lemur species",
            "species_count": 108,
            "genera": [
                "Lemur", "Eulemur", "Varecia", "Propithecus", "Indri",
                "Avahi", "Microcebus", "Mirza", "Cheirogaleus", "Phaner",
                "Allocebus", "Daubentonia", "Lepilemur"
            ],
            "features": ["visual", "acoustic", "behavioral"],
            "image_size": [224, 224],
            "conservation_status": True
        }
        
        # Save configurations
        configs = {
            "wildlife": wildlife_config,
            "birds": bird_config,
            "ecosystems": ecosystem_config,
            "lemurs": lemur_config
        }
        
        config_file = self.datasets_path / "dataset_configs.json"
        with open(config_file, 'w') as f:
            json.dump(configs, f, indent=2)
        
        logger.info(f"✅ Dataset configurations saved to: {config_file}")
    
    def create_training_configs(self) -> None:
        """Create training configuration files."""
        logger.info("🏋️ Creating training configurations...")
        
        # YOLOv8 training config
        yolo_config = {
            "model": "yolov8n.pt",
            "data": "madagascar_wildlife.yaml",
            "epochs": 100,
            "batch": 16,
            "imgsz": 640,
            "device": "mps",
            "workers": 4,
            "optimizer": "AdamW",
            "lr0": 0.01,
            "momentum": 0.937,
            "weight_decay": 0.0005,
            "warmup_epochs": 3,
            "augment": True,
            "mixup": 0.1,
            "copy_paste": 0.3
        }
        
        # BirdNET training config
        birdnet_config = {
            "model_architecture": "efficientnet_b0",
            "input_shape": [150, 150, 1],
            "num_classes": 250,
            "batch_size": 32,
            "epochs": 50,
            "learning_rate": 0.001,
            "optimizer": "adam",
            "loss": "categorical_crossentropy",
            "metrics": ["accuracy", "top_5_accuracy"],
            "callbacks": ["early_stopping", "reduce_lr", "model_checkpoint"],
            "augmentation": {
                "time_stretch": [0.8, 1.2],
                "pitch_shift": [-2, 2],
                "noise_injection": 0.1,
                "mixup": 0.2
            }
        }
        
        # SAM training config
        sam_config = {
            "model_type": "vit_h",
            "input_size": [1024, 1024],
            "num_classes": 12,
            "batch_size": 4,
            "epochs": 30,
            "learning_rate": 1e-4,
            "optimizer": "adamw",
            "weight_decay": 0.01,
            "scheduler": "cosine",
            "prompt_engineering": True,
            "mask_threshold": 0.5
        }
        
        # Lemur classifier config
        lemur_config = {
            "backbone": "resnet50",
            "pretrained": True,
            "num_classes": 108,
            "input_size": [224, 224],
            "batch_size": 64,
            "epochs": 75,
            "learning_rate": 0.001,
            "optimizer": "sgd",
            "momentum": 0.9,
            "weight_decay": 1e-4,
            "scheduler": "step",
            "step_size": 25,
            "gamma": 0.1,
            "augmentation": {
                "rotation": 15,
                "brightness": 0.2,
                "contrast": 0.2,
                "saturation": 0.2,
                "hue": 0.1
            }
        }
        
        # Save training configurations
        training_configs = {
            "yolov8": yolo_config,
            "birdnet": birdnet_config,
            "sam": sam_config,
            "lemur": lemur_config
        }
        
        config_file = self.training_path / "training_configs.json"
        with open(config_file, 'w') as f:
            json.dump(training_configs, f, indent=2)
        
        logger.info(f"✅ Training configurations saved to: {config_file}")
    
    def create_evaluation_framework(self) -> None:
        """Create evaluation and benchmarking framework."""
        logger.info("📊 Creating evaluation framework...")
        
        eval_config = {
            "metrics": {
                "detection": ["mAP50", "mAP50-95", "precision", "recall", "F1"],
                "classification": ["accuracy", "top_5_accuracy", "precision", "recall", "F1"],
                "segmentation": ["IoU", "dice_coefficient", "pixel_accuracy"],
                "conservation": ["species_coverage", "threat_detection_rate", "false_positive_rate"]
            },
            "benchmarks": {
                "yolov8_madagascar": {"target_map50": 0.9, "target_speed": "30_fps"},
                "birdnet_madagascar": {"target_accuracy": 0.85, "target_latency": "1s"},
                "sam_madagascar": {"target_iou": 0.95, "target_speed": "5_fps"},
                "lemur_classifier": {"target_accuracy": 0.92, "target_inference": "100ms"}
            },
            "validation": {
                "cross_validation": 5,
                "test_split": 0.1,
                "stratified": True,
                "temporal_split": True
            }
        }
        
        eval_file = self.phase2_path / "evaluation_config.json"
        with open(eval_file, 'w') as f:
            json.dump(eval_config, f, indent=2)
        
        logger.info(f"✅ Evaluation framework saved to: {eval_file}")
    
    def create_phase2_requirements(self) -> None:
        """Create Phase 2 specific requirements."""
        logger.info("📦 Creating Phase 2 requirements...")
        
        phase2_requirements = """# Phase 2: Madagascar Specialization Requirements
# Additional packages for transfer learning and specialization

# Training and optimization
albumentations==1.3.0          # Advanced data augmentation
wandb==0.15.0                   # Experiment tracking and visualization
optuna==3.2.0                   # Hyperparameter optimization
pytorch-lightning==2.0.0        # Training framework
timm==0.9.0                     # Vision model library
audiomentations==0.30.0         # Audio data augmentation

# Data processing
roboflow==1.1.0                 # Dataset management
fiftyone==0.21.0                # Dataset visualization
albumentations==1.3.0           # Image augmentation
librosa==0.10.0                 # Audio processing (already installed)

# Model optimization
onnx==1.14.0                    # Model export format
tensorrt==8.6.0                 # NVIDIA optimization (if available)
openvino==2023.0.0              # Intel optimization

# Evaluation and monitoring
tensorboard==2.13.0             # Training visualization
mlflow==2.5.0                   # Model lifecycle management
evidently==0.4.0                # Model monitoring

# Conservation-specific
inat-tools==0.1.0               # iNaturalist data integration
gbif-api==0.6.0                 # GBIF biodiversity data
ebird-api==2.0.0                # eBird data integration
"""
        
        req_file = self.phase2_path / "requirements_phase2.txt"
        with open(req_file, 'w') as f:
            f.write(phase2_requirements)
        
        logger.info(f"✅ Phase 2 requirements saved to: {req_file}")
    
    def create_readme(self) -> None:
        """Create Phase 2 README documentation."""
        logger.info("📚 Creating Phase 2 documentation...")
        
        readme_content = """# Phase 2: Madagascar Specialization & Transfer Learning

## 🎯 Overview
Phase 2 focuses on specializing the foundation models for Madagascar's unique biodiversity and conservation challenges.

## 🗂️ Directory Structure
```
phase2_madagascar_specialization/
├── datasets/                   # Specialized datasets
│   ├── madagascar_wildlife_images/
│   ├── endemic_bird_audio/
│   ├── ecosystem_boundaries/
│   └── lemur_identification/
├── models/                     # Specialized models
│   ├── yolov8_madagascar/
│   ├── birdnet_madagascar/
│   ├── sam_madagascar/
│   └── lemur_classifier/
├── training_pipelines/         # Training scripts
│   ├── yolov8_training/
│   ├── birdnet_training/
│   ├── sam_training/
│   └── lemur_training/
├── dataset_configs.json        # Dataset configurations
├── training_configs.json       # Training configurations
├── evaluation_config.json      # Evaluation framework
└── requirements_phase2.txt     # Additional dependencies
```

## 🚀 Getting Started

### 1. Install Phase 2 Dependencies
```bash
conda run -n base pip install -r requirements_phase2.txt
```

### 2. Data Preparation
```bash
python prepare_madagascar_datasets.py
```

### 3. Model Training
```bash
# YOLOv8 Madagascar Wildlife
python training_pipelines/yolov8_training/train_madagascar_wildlife.py

# BirdNET Madagascar Enhancement  
python training_pipelines/birdnet_training/train_madagascar_birds.py

# SAM Ecosystem Specialization
python training_pipelines/sam_training/train_madagascar_ecosystems.py

# Lemur Species Classifier
python training_pipelines/lemur_training/train_lemur_classifier.py
```

### 4. Evaluation and Benchmarking
```bash
python evaluate_specialized_models.py
```

## 📊 Expected Outcomes
- **YOLOv8 Madagascar**: >90% mAP on endemic species
- **BirdNET Enhancement**: >85% accuracy on Madagascar birds  
- **SAM Ecosystem**: >95% IoU on habitat segmentation
- **Lemur Classifier**: >92% accuracy on 108 species

## 🌟 Conservation Impact
- Real-time anti-poaching monitoring
- Automated biodiversity surveys
- Habitat change detection
- Species population tracking

Ready to begin Madagascar conservation AI specialization! 🦎🌿
"""
        
        readme_file = self.phase2_path / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        logger.info(f"✅ Phase 2 README created: {readme_file}")
    
    def setup_phase2(self) -> None:
        """Execute complete Phase 2 setup."""
        logger.info("🌍 Starting Phase 2: Madagascar Specialization Setup")
        logger.info("=" * 60)
        
        try:
            self.create_directory_structure()
            self.create_dataset_configs()
            self.create_training_configs()
            self.create_evaluation_framework()
            self.create_phase2_requirements()
            self.create_readme()
            
            logger.info("\n🎉 Phase 2 Setup Complete!")
            logger.info("=" * 40)
            logger.info("🔬 Madagascar Specialization Ready")
            logger.info("🦎 Lemur Species Identification")
            logger.info("🎵 Endemic Bird Classification")
            logger.info("🗺️ Ecosystem Segmentation")
            logger.info("🌿 Conservation AI Workflows")
            logger.info("\n🚀 Ready to begin specialized model training!")
            
        except Exception as e:
            logger.error(f"❌ Phase 2 setup failed: {e}")
            raise

def main():
    """Main execution function."""
    setup = Phase2Setup()
    setup.setup_phase2()

if __name__ == "__main__":
    main()
