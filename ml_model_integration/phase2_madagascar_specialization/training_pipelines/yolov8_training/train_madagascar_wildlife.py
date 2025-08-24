#!/usr/bin/env python3
"""
YOLOv8 Madagascar Wildlife Specialization Training
==================================================

This script implements transfer learning to specialize YOLOv8 for Madagascar endemic wildlife.
Focuses on optimizing detection for lemurs, fossas, tenrecs, and other endemic species.

Author: Madagascar Conservation AI Team  
Date: August 2025
"""

import os
import sys
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml

import torch
import numpy as np
from ultralytics import YOLO
import albumentations as A
from albumentations.pytorch import ToTensorV2
import wandb
import optuna

# Import centralized model path configuration
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.append(str(project_root))
from src.utils.model_paths import get_yolo_path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MadagascarYOLOv8Trainer:
    """Specialized trainer for Madagascar wildlife YOLOv8 models."""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path
        self.config = self.load_config()
        self.project_dir = Path(__file__).parent.parent.parent
        self.models_dir = self.project_dir / "phase2_madagascar_specialization" / "models" / "yolov8_madagascar"
        self.datasets_dir = self.project_dir / "phase2_madagascar_specialization" / "datasets" / "madagascar_wildlife_images"
        
        # Madagascar species configuration
        self.madagascar_species = {
            0: {"name": "Indri indri", "common": "Indri", "status": "Critically Endangered"},
            1: {"name": "Propithecus diadema", "common": "Diademed Sifaka", "status": "Critically Endangered"},
            2: {"name": "Lemur catta", "common": "Ring-tailed Lemur", "status": "Endangered"},
            3: {"name": "Eulemur macaco", "common": "Black Lemur", "status": "Vulnerable"},
            4: {"name": "Microcebus murinus", "common": "Gray Mouse Lemur", "status": "Least Concern"},
            5: {"name": "Daubentonia madagascariensis", "common": "Aye-aye", "status": "Endangered"},
            6: {"name": "Cryptoprocta ferox", "common": "Fossa", "status": "Vulnerable"},
            7: {"name": "Fossa fossana", "common": "Spotted Fanaloka", "status": "Vulnerable"},
            8: {"name": "Tenrec ecaudatus", "common": "Tailless Tenrec", "status": "Least Concern"},
            9: {"name": "Setifer setosus", "common": "Greater Hedgehog Tenrec", "status": "Least Concern"},
            10: {"name": "Hemicentetes semispinosus", "common": "Lowland Streaked Tenrec", "status": "Least Concern"},
            11: {"name": "Brookesia micra", "common": "Leaf Chameleon", "status": "Near Threatened"},
            12: {"name": "Furcifer pardalis", "common": "Panther Chameleon", "status": "Least Concern"},
            13: {"name": "Uroplatus fimbriatus", "common": "Fringed Leaf-tail Gecko", "status": "Vulnerable"},
            14: {"name": "Centrogenia gregaria", "common": "Madagascar Hissing Cockroach", "status": "Not Evaluated"},
            15: {"name": "Anas melleri", "common": "Meller's Duck", "status": "Endangered"},
            16: {"name": "Tachybaptus pelzelnii", "common": "Madagascar Grebe", "status": "Vulnerable"},
            17: {"name": "Lophotibis cristata", "common": "Madagascar Crested Ibis", "status": "Near Threatened"},
            18: {"name": "Monias benschi", "common": "Subdesert Mesite", "status": "Vulnerable"},
            19: {"name": "Xenopirostris xenopirostris", "common": "Lafresnaye's Vanga", "status": "Vulnerable"}
        }
        
        # Initialize models directory
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
    def load_config(self) -> Dict:
        """Load training configuration."""
        default_config = {
            "model": get_yolo_path(),  # Use centralized model path
            "epochs": 100,
            "batch": 16,
            "imgsz": 640,
            "device": "mps" if torch.backends.mps.is_available() else "cpu",
            "workers": 4,
            "optimizer": "AdamW",
            "lr0": 0.01,
            "momentum": 0.937,
            "weight_decay": 0.0005,
            "warmup_epochs": 3,
            "patience": 20,
            "save_period": 10,
            "augment": True,
            "mixup": 0.1,
            "copy_paste": 0.3,
            "flipud": 0.0,
            "fliplr": 0.5,
            "mosaic": 1.0,
            "hsv_h": 0.015,
            "hsv_s": 0.7,
            "hsv_v": 0.4,
            "degrees": 0.0,
            "translate": 0.1,
            "scale": 0.5,
            "shear": 0.0,
            "perspective": 0.0,
            "close_mosaic": 10
        }
        
        if self.config_path and os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                user_config = json.load(f)
            default_config.update(user_config.get('yolov8', {}))
        
        return default_config
    
    def create_dataset_yaml(self) -> Path:
        """Create YOLO dataset configuration file."""
        logger.info("🗂️ Creating Madagascar wildlife dataset configuration...")
        
        # Create dataset structure
        train_dir = self.datasets_dir / "train"
        val_dir = self.datasets_dir / "val" 
        test_dir = self.datasets_dir / "test"
        
        for split_dir in [train_dir, val_dir, test_dir]:
            split_dir.mkdir(parents=True, exist_ok=True)
            (split_dir / "images").mkdir(exist_ok=True)
            (split_dir / "labels").mkdir(exist_ok=True)
        
        # Create YOLO dataset configuration
        dataset_config = {
            "path": str(self.datasets_dir),
            "train": "train/images",
            "val": "val/images", 
            "test": "test/images",
            "nc": len(self.madagascar_species),
            "names": [species["common"] for species in self.madagascar_species.values()]
        }
        
        yaml_path = self.datasets_dir / "madagascar_wildlife.yaml"
        with open(yaml_path, 'w') as f:
            yaml.dump(dataset_config, f, default_flow_style=False)
        
        logger.info(f"✅ Dataset configuration saved: {yaml_path}")
        return yaml_path
    
    def setup_augmentation_pipeline(self) -> A.Compose:
        """Setup advanced augmentation pipeline for Madagascar wildlife."""
        logger.info("🔄 Setting up Madagascar-specific augmentation pipeline...")
        
        # Conservation-focused augmentations
        augmentations = A.Compose([
            # Lighting variations (important for forest environments)
            A.RandomBrightnessContrast(
                brightness_limit=0.3, 
                contrast_limit=0.3, 
                p=0.8
            ),
            
            # Color variations (different forest lighting)
            A.HueSaturationValue(
                hue_shift_limit=20,
                sat_shift_limit=30, 
                val_shift_limit=20,
                p=0.7
            ),
            
            # Weather and atmospheric effects
            A.OneOf([
                A.Blur(blur_limit=3, p=1.0),
                A.GaussNoise(var_limit=10.0, p=1.0),
                A.ISONoise(color_shift=0.05, intensity=0.5, p=1.0),
            ], p=0.3),
            
            # Geometric transformations (camera trap angles)
            A.ShiftScaleRotate(
                shift_limit=0.1,
                scale_limit=0.2,
                rotate_limit=15,
                border_mode=0,
                p=0.7
            ),
            
            # Perspective changes (different camera positions)
            A.Perspective(scale=0.05, p=0.3),
            
            # Vegetation occlusion simulation
            A.CoarseDropout(
                max_holes=8,
                max_height=32,
                max_width=32,
                min_holes=1,
                min_height=8,
                min_width=8,
                fill_value=0,
                p=0.3
            ),
            
            # Motion blur (animal movement)
            A.MotionBlur(blur_limit=7, p=0.2),
            
        ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
        
        logger.info("✅ Augmentation pipeline configured for Madagascar environments")
        return augmentations
    
    def optimize_hyperparameters(self, n_trials: int = 20) -> Dict:
        """Optimize hyperparameters using Optuna for Madagascar wildlife."""
        logger.info(f"🔍 Starting hyperparameter optimization ({n_trials} trials)...")
        
        def objective(trial):
            # Suggest hyperparameters
            params = {
                'lr0': trial.suggest_float('lr0', 1e-4, 1e-1, log=True),
                'momentum': trial.suggest_float('momentum', 0.8, 0.99),
                'weight_decay': trial.suggest_float('weight_decay', 1e-5, 1e-2, log=True),
                'warmup_epochs': trial.suggest_int('warmup_epochs', 1, 5),
                'box': trial.suggest_float('box', 5.0, 15.0),
                'cls': trial.suggest_float('cls', 0.3, 1.5),
                'dfl': trial.suggest_float('dfl', 1.0, 2.0),
                'hsv_h': trial.suggest_float('hsv_h', 0.0, 0.05),
                'hsv_s': trial.suggest_float('hsv_s', 0.3, 0.9),
                'hsv_v': trial.suggest_float('hsv_v', 0.2, 0.6),
                'degrees': trial.suggest_float('degrees', 0.0, 20.0),
                'translate': trial.suggest_float('translate', 0.05, 0.2),
                'scale': trial.suggest_float('scale', 0.3, 0.7),
                'mixup': trial.suggest_float('mixup', 0.0, 0.3),
                'copy_paste': trial.suggest_float('copy_paste', 0.0, 0.5)
            }
            
            # Update config with suggested parameters
            trial_config = self.config.copy()
            trial_config.update(params)
            
            # Train model with suggested parameters
            model = YOLO(self.config["model"])
            
            # Short training for optimization
            results = model.train(
                data=self.create_dataset_yaml(),
                epochs=10,  # Reduced for optimization
                batch=trial_config["batch"],
                imgsz=trial_config["imgsz"],
                device=trial_config["device"],
                workers=trial_config["workers"],
                **params,
                verbose=False,
                save=False
            )
            
            # Return mAP50 as optimization target
            return results.results_dict['metrics/mAP50(B)']
        
        # Run optimization
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials)
        
        best_params = study.best_params
        logger.info(f"✅ Best hyperparameters found: {best_params}")
        logger.info(f"🎯 Best mAP50: {study.best_value:.4f}")
        
        return best_params
    
    def train_madagascar_specialist(self, 
                                   optimize_hyperparams: bool = False,
                                   use_wandb: bool = True) -> YOLO:
        """Train specialized YOLOv8 model for Madagascar wildlife."""
        logger.info("🚀 Starting Madagascar wildlife YOLOv8 specialization training...")
        
        # Initialize Weights & Biases if requested
        if use_wandb:
            wandb.init(
                project="madagascar-conservation-ai",
                name="yolov8-wildlife-specialization",
                config=self.config,
                tags=["yolov8", "madagascar", "wildlife", "conservation"]
            )
        
        # Optimize hyperparameters if requested
        if optimize_hyperparams:
            best_params = self.optimize_hyperparameters()
            self.config.update(best_params)
        
        # Create dataset configuration
        dataset_yaml = self.create_dataset_yaml()
        
        # Initialize model
        model = YOLO(self.config["model"])
        
        # Add conservation-specific callbacks
        def on_train_start(trainer):
            logger.info("🦎 Training Madagascar wildlife specialist...")
            logger.info(f"📊 Species count: {len(self.madagascar_species)}")
            logger.info(f"🖥️ Device: {trainer.device}")
        
        def on_train_epoch_end(trainer):
            if hasattr(trainer, 'epoch'):
                epoch = trainer.epoch
                if epoch % 10 == 0:
                    logger.info(f"🔄 Epoch {epoch}: Specializing for Madagascar endemic species...")
        
        def on_train_end(trainer):
            logger.info("✅ Madagascar wildlife specialization complete!")
            logger.info("🎯 Model ready for conservation deployment")
        
        # Register callbacks
        model.add_callback("on_train_start", on_train_start)
        model.add_callback("on_train_epoch_end", on_train_epoch_end) 
        model.add_callback("on_train_end", on_train_end)
        
        # Train model
        results = model.train(
            data=str(dataset_yaml),
            epochs=self.config["epochs"],
            batch=self.config["batch"],
            imgsz=self.config["imgsz"],
            device=self.config["device"],
            workers=self.config["workers"],
            optimizer=self.config["optimizer"],
            lr0=self.config["lr0"],
            momentum=self.config["momentum"],
            weight_decay=self.config["weight_decay"],
            warmup_epochs=self.config["warmup_epochs"],
            patience=self.config["patience"],
            save_period=self.config["save_period"],
            project=str(self.models_dir),
            name="madagascar_wildlife_specialist",
            exist_ok=True,
            augment=self.config["augment"],
            mixup=self.config["mixup"],
            copy_paste=self.config["copy_paste"],
            flipud=self.config["flipud"],
            fliplr=self.config["fliplr"],
            mosaic=self.config["mosaic"],
            hsv_h=self.config["hsv_h"],
            hsv_s=self.config["hsv_s"], 
            hsv_v=self.config["hsv_v"],
            degrees=self.config["degrees"],
            translate=self.config["translate"],
            scale=self.config["scale"],
            shear=self.config["shear"],
            perspective=self.config["perspective"],
            close_mosaic=self.config["close_mosaic"]
        )
        
        # Save specialized model
        model_path = self.models_dir / "madagascar_wildlife_specialist.pt"
        model.save(str(model_path))
        
        # Save species mapping
        species_path = self.models_dir / "madagascar_species_mapping.json"
        with open(species_path, 'w') as f:
            json.dump(self.madagascar_species, f, indent=2)
        
        logger.info(f"✅ Specialized model saved: {model_path}")
        logger.info(f"📋 Species mapping saved: {species_path}")
        
        if use_wandb:
            wandb.finish()
        
        return model
    
    def evaluate_model(self, model_path: str) -> Dict:
        """Evaluate specialized Madagascar wildlife model."""
        logger.info("📊 Evaluating Madagascar wildlife specialist...")
        
        model = YOLO(model_path)
        dataset_yaml = self.create_dataset_yaml()
        
        # Run validation
        results = model.val(
            data=str(dataset_yaml),
            batch=self.config["batch"],
            imgsz=self.config["imgsz"],
            device=self.config["device"],
            save_json=True,
            save_hybrid=True
        )
        
        # Extract key metrics
        metrics = {
            'mAP50': results.results_dict.get('metrics/mAP50(B)', 0),
            'mAP50-95': results.results_dict.get('metrics/mAP50-95(B)', 0),
            'precision': results.results_dict.get('metrics/precision(B)', 0),
            'recall': results.results_dict.get('metrics/recall(B)', 0),
            'species_count': len(self.madagascar_species)
        }
        
        logger.info(f"🎯 Madagascar Wildlife Specialist Performance:")
        logger.info(f"   mAP50: {metrics['mAP50']:.4f}")
        logger.info(f"   mAP50-95: {metrics['mAP50-95']:.4f}")
        logger.info(f"   Precision: {metrics['precision']:.4f}")
        logger.info(f"   Recall: {metrics['recall']:.4f}")
        logger.info(f"   Species Coverage: {metrics['species_count']} endemic species")
        
        return metrics
    
    def export_for_deployment(self, model_path: str) -> Dict[str, str]:
        """Export model in multiple formats for field deployment."""
        logger.info("📦 Exporting Madagascar wildlife specialist for deployment...")
        
        model = YOLO(model_path)
        exports = {}
        
        export_formats = [
            ('onnx', 'ONNX'),
            ('openvino', 'OpenVINO'),
            ('coreml', 'CoreML'),
            ('tflite', 'TensorFlow Lite')
        ]
        
        for format_name, description in export_formats:
            try:
                export_path = model.export(format=format_name, optimize=True)
                exports[format_name] = str(export_path)
                logger.info(f"✅ {description} export: {export_path}")
            except Exception as e:
                logger.warning(f"⚠️ {description} export failed: {e}")
        
        return exports

def main():
    """Main training execution."""
    logger.info("🌍 Madagascar Wildlife YOLOv8 Specialization")
    logger.info("=" * 50)
    
    # Initialize trainer
    trainer = MadagascarYOLOv8Trainer()
    
    # Train specialized model
    model = trainer.train_madagascar_specialist(
        optimize_hyperparams=False,  # Set to True for hyperparameter optimization
        use_wandb=False  # Set to True to use Weights & Biases tracking
    )
    
    # Evaluate model
    model_path = trainer.models_dir / "madagascar_wildlife_specialist.pt"
    if model_path.exists():
        metrics = trainer.evaluate_model(str(model_path))
        
        # Export for deployment if performance is good
        if metrics['mAP50'] > 0.7:  # Threshold for deployment
            exports = trainer.export_for_deployment(str(model_path))
            logger.info("🚀 Model ready for conservation field deployment!")
        else:
            logger.warning("⚠️ Model performance below deployment threshold")
    
    logger.info("✅ Madagascar wildlife specialization complete!")

if __name__ == "__main__":
    main()
