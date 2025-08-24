#!/usr/bin/env python3
"""
Advanced Madagascar Training Pipeline Setup
===========================================

Step 2 of Phase 2: Set up comprehensive training pipelines with advanced
features for Madagascar conservation AI models.

Author: Madagascar Conservation AI Team
Date: August 2025
"""

import os
import sys
import logging
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import wandb
import optuna
from ultralytics import YOLO
import timm
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MadagascarTrainingPipelineSetup:
    """Set up advanced training pipelines for Madagascar conservation AI."""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.phase2_path = self.base_path / "ml_model_integration" / "phase2_madagascar_specialization"
        self.training_path = self.phase2_path / "training_pipelines"
        
        # Training configurations
        self.training_configs = self.setup_training_configurations()
        
        # Hardware detection
        self.device = self.detect_hardware()
        
    def detect_hardware(self) -> str:
        """Detect available hardware for training."""
        if torch.cuda.is_available():
            device = "cuda"
            logger.info(f"🚀 CUDA detected: {torch.cuda.get_device_name(0)}")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            device = "mps"
            logger.info("🍎 Apple Silicon MPS detected")
        else:
            device = "cpu"
            logger.info("💻 Using CPU")
        
        return device
    
    def setup_training_configurations(self) -> Dict[str, Any]:
        """Set up comprehensive training configurations."""
        configs = {
            "yolov8_madagascar_wildlife": {
                "model_type": "detection",
                "base_model": get_yolo_path(),  # Use centralized model path
                "target_species": 20,
                "image_size": 640,
                "batch_size": 16,
                "epochs": 100,
                "patience": 10,
                "learning_rate": 0.01,
                "momentum": 0.937,
                "weight_decay": 0.0005,
                "warmup_epochs": 3,
                "augmentation": {
                    "hsv_h": 0.015,
                    "hsv_s": 0.7,
                    "hsv_v": 0.4,
                    "degrees": 0.0,
                    "translate": 0.1,
                    "scale": 0.5,
                    "shear": 0.0,
                    "perspective": 0.0,
                    "flipud": 0.0,
                    "fliplr": 0.5,
                    "mosaic": 1.0,
                    "mixup": 0.1,
                    "copy_paste": 0.1
                },
                "conservation_metrics": [
                    "species_detection_accuracy",
                    "anti_poaching_precision", 
                    "camera_trap_recall",
                    "field_deployment_fps"
                ]
            },
            "lemur_species_classifier": {
                "model_type": "classification",
                "architecture": "efficientnet_b3",
                "num_classes": 108,
                "image_size": 224,
                "batch_size": 32,
                "epochs": 50,
                "patience": 7,
                "learning_rate": 0.001,
                "scheduler": "cosine",
                "label_smoothing": 0.1,
                "mixup_alpha": 0.2,
                "cutmix_alpha": 1.0,
                "augmentation": {
                    "random_crop": True,
                    "horizontal_flip": 0.5,
                    "color_jitter": 0.3,
                    "rotation": 15,
                    "gaussian_blur": 0.1
                },
                "conservation_features": {
                    "conservation_status_prediction": True,
                    "habitat_association": True,
                    "behavioral_classification": True,
                    "morphometric_estimation": True
                }
            },
            "ecosystem_segmentation": {
                "model_type": "segmentation",
                "architecture": "unet_resnet50",
                "num_classes": 12,
                "image_size": 512,
                "batch_size": 8,
                "epochs": 75,
                "patience": 10,
                "learning_rate": 0.0003,
                "loss_function": "focal_loss",
                "class_weights": True,
                "augmentation": {
                    "random_crop": True,
                    "horizontal_flip": 0.5,
                    "vertical_flip": 0.2,
                    "rotation": 30,
                    "brightness": 0.2,
                    "contrast": 0.2
                },
                "conservation_applications": [
                    "deforestation_monitoring",
                    "habitat_connectivity_analysis",
                    "protected_area_management",
                    "climate_change_impact_assessment"
                ]
            },
            "bird_audio_classifier": {
                "model_type": "audio_classification",
                "architecture": "resnet18_1d",
                "num_classes": 250,
                "sample_rate": 22050,
                "duration": 3.0,
                "batch_size": 64,
                "epochs": 40,
                "patience": 8,
                "learning_rate": 0.001,
                "augmentation": {
                    "time_stretch": 0.2,
                    "pitch_shift": 2,
                    "gaussian_noise": 0.005,
                    "time_mask": 0.1,
                    "frequency_mask": 0.1
                },
                "acoustic_features": [
                    "mfcc_coefficients",
                    "spectral_centroid",
                    "spectral_rolloff",
                    "zero_crossing_rate",
                    "chroma_features"
                ]
            }
        }
        
        logger.info(f"📋 Training configurations loaded for {len(configs)} model types")
        return configs
    
    def create_training_directories(self) -> None:
        """Create comprehensive training directory structure."""
        logger.info("🏗️ Creating advanced training directory structure...")
        
        directories = [
            # Main training directories
            self.training_path / "yolov8_madagascar_wildlife",
            self.training_path / "lemur_species_classifier", 
            self.training_path / "ecosystem_segmentation",
            self.training_path / "bird_audio_classifier",
            
            # Experiment tracking
            self.training_path / "experiments" / "wandb_logs",
            self.training_path / "experiments" / "optuna_studies",
            self.training_path / "experiments" / "tensorboard_logs",
            
            # Model outputs
            self.training_path / "trained_models" / "yolov8_variants",
            self.training_path / "trained_models" / "lemur_classifiers",
            self.training_path / "trained_models" / "ecosystem_models",
            self.training_path / "trained_models" / "audio_models",
            
            # Evaluation results
            self.training_path / "evaluation" / "performance_metrics",
            self.training_path / "evaluation" / "conservation_impact",
            self.training_path / "evaluation" / "field_validation",
            
            # Configuration files
            self.training_path / "configs" / "hyperparameters",
            self.training_path / "configs" / "augmentation",
            self.training_path / "configs" / "deployment",
            
            # Training utilities
            self.training_path / "utils" / "data_processing",
            self.training_path / "utils" / "model_optimization", 
            self.training_path / "utils" / "conservation_metrics",
            
            # Checkpoints and logs
            self.training_path / "checkpoints" / "best_models",
            self.training_path / "checkpoints" / "intermediate",
            self.training_path / "logs" / "training_logs",
            self.training_path / "logs" / "error_logs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"✅ Created: {directory}")
    
    def create_hyperparameter_optimization_configs(self) -> None:
        """Create hyperparameter optimization configurations using Optuna."""
        logger.info("🔬 Creating hyperparameter optimization configurations...")
        
        configs_dir = self.training_path / "configs" / "hyperparameters"
        
        # YOLOv8 hyperparameter optimization
        yolo_optuna_config = {
            "study_name": "yolov8_madagascar_wildlife_optimization",
            "direction": "maximize",
            "metric": "mAP50-95",
            "n_trials": 50,
            "parameters": {
                "learning_rate": {
                    "type": "loguniform",
                    "low": 1e-4,
                    "high": 1e-1
                },
                "batch_size": {
                    "type": "categorical",
                    "choices": [8, 16, 24, 32]
                },
                "weight_decay": {
                    "type": "loguniform", 
                    "low": 1e-6,
                    "high": 1e-3
                },
                "momentum": {
                    "type": "uniform",
                    "low": 0.8,
                    "high": 0.99
                },
                "warmup_epochs": {
                    "type": "int",
                    "low": 1,
                    "high": 5
                },
                "augmentation": {
                    "mosaic": {
                        "type": "uniform",
                        "low": 0.5,
                        "high": 1.0
                    },
                    "mixup": {
                        "type": "uniform",
                        "low": 0.0,
                        "high": 0.3
                    },
                    "copy_paste": {
                        "type": "uniform",
                        "low": 0.0,
                        "high": 0.3
                    }
                }
            },
            "conservation_constraints": {
                "min_anti_poaching_precision": 0.95,
                "min_field_deployment_fps": 10,
                "max_model_size_mb": 50
            }
        }
        
        # Lemur classifier hyperparameter optimization
        lemur_optuna_config = {
            "study_name": "lemur_species_classifier_optimization",
            "direction": "maximize",
            "metric": "conservation_weighted_accuracy",
            "n_trials": 30,
            "parameters": {
                "architecture": {
                    "type": "categorical",
                    "choices": ["efficientnet_b0", "efficientnet_b3", "resnet50", "vit_base_patch16_224"]
                },
                "learning_rate": {
                    "type": "loguniform",
                    "low": 1e-5,
                    "high": 1e-2
                },
                "batch_size": {
                    "type": "categorical",
                    "choices": [16, 32, 48, 64]
                },
                "label_smoothing": {
                    "type": "uniform",
                    "low": 0.0,
                    "high": 0.2
                },
                "mixup_alpha": {
                    "type": "uniform",
                    "low": 0.0,
                    "high": 0.5
                },
                "dropout_rate": {
                    "type": "uniform",
                    "low": 0.1,
                    "high": 0.5
                }
            },
            "conservation_priorities": {
                "critically_endangered_weight": 5.0,
                "endangered_weight": 3.0,
                "vulnerable_weight": 2.0,
                "endemic_bonus": 1.5
            }
        }
        
        # Save configurations
        with open(configs_dir / "yolov8_optuna_config.yaml", 'w') as f:
            yaml.dump(yolo_optuna_config, f, default_flow_style=False)
        
        with open(configs_dir / "lemur_classifier_optuna_config.yaml", 'w') as f:
            yaml.dump(lemur_optuna_config, f, default_flow_style=False)
        
        logger.info("✅ Hyperparameter optimization configurations created")
    
    def create_wandb_integration(self) -> None:
        """Create Weights & Biases integration for experiment tracking."""
        logger.info("📊 Setting up Weights & Biases integration...")
        
        wandb_dir = self.training_path / "experiments" / "wandb_logs"
        
        # W&B configuration template
        wandb_config = {
            "project_name": "madagascar_conservation_ai",
            "entity": "conservation_ai_team",
            "experiment_groups": {
                "wildlife_detection": {
                    "description": "YOLOv8 Madagascar wildlife detection experiments",
                    "tags": ["yolov8", "wildlife", "detection", "madagascar"],
                    "metrics_to_track": [
                        "mAP50",
                        "mAP50-95", 
                        "precision",
                        "recall",
                        "f1_score",
                        "training_loss",
                        "validation_loss",
                        "learning_rate",
                        "conservation_impact_score"
                    ]
                },
                "lemur_classification": {
                    "description": "Lemur species classification experiments",
                    "tags": ["classification", "lemur", "species", "conservation"],
                    "metrics_to_track": [
                        "accuracy",
                        "top5_accuracy", 
                        "conservation_weighted_accuracy",
                        "per_species_precision",
                        "per_species_recall",
                        "confusion_matrix",
                        "training_loss",
                        "validation_loss",
                        "endemic_species_performance"
                    ]
                },
                "ecosystem_segmentation": {
                    "description": "Madagascar ecosystem segmentation experiments",
                    "tags": ["segmentation", "ecosystem", "satellite", "habitat"],
                    "metrics_to_track": [
                        "iou",
                        "dice_coefficient",
                        "pixel_accuracy",
                        "mean_iou",
                        "class_iou",
                        "deforestation_detection_rate",
                        "habitat_connectivity_score"
                    ]
                }
            },
            "custom_metrics": {
                "conservation_impact_score": {
                    "description": "Weighted score based on conservation priority",
                    "formula": "CR_weight * CR_accuracy + EN_weight * EN_accuracy + VU_weight * VU_accuracy"
                },
                "anti_poaching_effectiveness": {
                    "description": "Model effectiveness for anti-poaching applications", 
                    "components": ["detection_speed", "accuracy", "false_positive_rate"]
                },
                "field_deployment_readiness": {
                    "description": "Readiness score for field deployment",
                    "factors": ["model_size", "inference_speed", "power_consumption", "accuracy"]
                }
            }
        }
        
        # Create W&B setup script
        wandb_setup_script = f'''#!/usr/bin/env python3
"""
Weights & Biases Setup for Madagascar Conservation AI
"""

import wandb
import os
from pathlib import Path

def setup_wandb_for_madagascar_conservation():
    """Initialize W&B for Madagascar conservation experiments."""
    
    # Initialize wandb (will prompt for login if needed)
    print("🔐 Setting up Weights & Biases...")
    print("Please ensure you have a W&B account and run 'wandb login' if needed")
    
    # Test configuration
    config = {{
        "project": "madagascar_conservation_ai",
        "experiment_type": "setup_test",
        "hardware": "{self.device}",
        "phase": "phase2_setup"
    }}
    
    try:
        # Initialize a test run
        run = wandb.init(
            project="madagascar_conservation_ai",
            name="setup_test",
            config=config,
            tags=["setup", "test"]
        )
        
        # Log a test metric
        wandb.log({{"setup_success": 1}})
        
        # Finish the run
        wandb.finish()
        
        print("✅ W&B setup successful!")
        return True
        
    except Exception as e:
        print(f"❌ W&B setup failed: {{e}}")
        print("Please run 'wandb login' and try again")
        return False

if __name__ == "__main__":
    setup_wandb_for_madagascar_conservation()
'''
        
        # Save W&B configuration and setup script
        with open(wandb_dir / "wandb_config.yaml", 'w') as f:
            yaml.dump(wandb_config, f, default_flow_style=False)
        
        with open(wandb_dir / "setup_wandb.py", 'w') as f:
            f.write(wandb_setup_script)
        
        logger.info("✅ W&B integration configuration created")
    
    def create_conservation_metrics_framework(self) -> None:
        """Create framework for conservation-specific metrics and evaluation."""
        logger.info("🌿 Creating conservation metrics framework...")
        
        metrics_dir = self.training_path / "utils" / "conservation_metrics"
        
        conservation_metrics_code = '''#!/usr/bin/env python3
"""
Conservation-Specific Metrics for Madagascar AI Models
======================================================

Custom metrics that prioritize conservation impact and real-world effectiveness.
"""

import numpy as np
import torch
import torch.nn.functional as F
from typing import Dict, List, Tuple, Optional
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
import pandas as pd

class ConservationMetrics:
    """Conservation-focused metrics for Madagascar AI models."""
    
    def __init__(self):
        # IUCN Red List status weights
        self.conservation_weights = {
            'CR': 5.0,  # Critically Endangered
            'EN': 3.0,  # Endangered  
            'VU': 2.0,  # Vulnerable
            'NT': 1.5,  # Near Threatened
            'LC': 1.0   # Least Concern
        }
        
        # Madagascar endemic species bonus
        self.endemic_bonus = 1.5
        
        # Species information database
        self.species_info = self.load_species_conservation_status()
    
    def load_species_conservation_status(self) -> Dict:
        """Load conservation status for Madagascar species."""
        return {
            'Indri_indri': {'status': 'CR', 'endemic': True, 'priority': 'highest'},
            'Propithecus_diadema': {'status': 'CR', 'endemic': True, 'priority': 'highest'},
            'Lemur_catta': {'status': 'EN', 'endemic': True, 'priority': 'high'},
            'Eulemur_macaco': {'status': 'VU', 'endemic': True, 'priority': 'high'},
            'Daubentonia_madagascariensis': {'status': 'EN', 'endemic': True, 'priority': 'highest'},
            'Cryptoprocta_ferox': {'status': 'VU', 'endemic': True, 'priority': 'high'},
            # Add more species as needed
        }
    
    def conservation_weighted_accuracy(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                     species_names: List[str]) -> float:
        """Calculate accuracy weighted by conservation priority."""
        total_weight = 0
        weighted_correct = 0
        
        for i, species in enumerate(species_names):
            mask = y_true == i
            if not mask.any():
                continue
            
            species_accuracy = (y_pred[mask] == y_true[mask]).mean()
            
            # Get conservation weight
            if species in self.species_info:
                status = self.species_info[species]['status']
                weight = self.conservation_weights.get(status, 1.0)
                
                # Apply endemic bonus
                if self.species_info[species].get('endemic', False):
                    weight *= self.endemic_bonus
            else:
                weight = 1.0
            
            weighted_correct += species_accuracy * weight * mask.sum()
            total_weight += weight * mask.sum()
        
        return weighted_correct / total_weight if total_weight > 0 else 0.0
    
    def anti_poaching_precision(self, y_true: np.ndarray, y_pred: np.ndarray,
                               target_species: List[str]) -> float:
        """Calculate precision for high-priority anti-poaching species."""
        target_indices = [i for i, species in enumerate(target_species) 
                         if species in ['Indri_indri', 'Propithecus_diadema', 
                                       'Lemur_catta', 'Cryptoprocta_ferox']]
        
        if not target_indices:
            return 0.0
        
        # Calculate precision for target species
        target_mask = np.isin(y_true, target_indices)
        if not target_mask.any():
            return 0.0
        
        target_true = y_true[target_mask]
        target_pred = y_pred[target_mask]
        
        precision_scores = []
        for idx in target_indices:
            tp = ((target_true == idx) & (target_pred == idx)).sum()
            fp = ((target_true != idx) & (target_pred == idx)).sum()
            
            if tp + fp > 0:
                precision_scores.append(tp / (tp + fp))
        
        return np.mean(precision_scores) if precision_scores else 0.0
    
    def ecosystem_connectivity_score(self, predicted_masks: np.ndarray,
                                   true_masks: np.ndarray) -> float:
        """Calculate habitat connectivity preservation score."""
        # Simplified connectivity metric based on preserved habitat patches
        connectivity_scores = []
        
        for i in range(len(predicted_masks)):
            pred_mask = predicted_masks[i]
            true_mask = true_masks[i]
            
            # Calculate preserved habitat area
            preserved_ratio = np.logical_and(pred_mask > 0, true_mask > 0).sum() / max(true_mask.sum(), 1)
            
            # Calculate fragmentation (simplified)
            # In practice, this would use more sophisticated connectivity algorithms
            fragmentation_penalty = self.calculate_fragmentation_penalty(pred_mask)
            
            connectivity_score = preserved_ratio * (1 - fragmentation_penalty)
            connectivity_scores.append(connectivity_score)
        
        return np.mean(connectivity_scores)
    
    def calculate_fragmentation_penalty(self, mask: np.ndarray) -> float:
        """Calculate habitat fragmentation penalty."""
        # Simplified fragmentation calculation
        # Count number of separate habitat patches
        from scipy import ndimage
        
        labeled_array, num_features = ndimage.label(mask > 0)
        
        if num_features == 0:
            return 1.0  # Complete fragmentation
        
        # Penalty based on number of fragments vs ideal (fewer is better)
        ideal_fragments = 1
        fragmentation_penalty = min(1.0, (num_features - ideal_fragments) / 10.0)
        
        return max(0.0, fragmentation_penalty)
    
    def field_deployment_score(self, model_size_mb: float, inference_fps: float,
                              accuracy: float) -> float:
        """Calculate readiness score for field deployment."""
        # Normalize components (0-1 scale)
        size_score = max(0, 1 - model_size_mb / 100)  # Penalty for models > 100MB
        speed_score = min(1.0, inference_fps / 30)     # Target 30 FPS
        accuracy_score = accuracy
        
        # Weighted combination
        deployment_score = (
            0.3 * size_score +
            0.3 * speed_score + 
            0.4 * accuracy_score
        )
        
        return deployment_score
    
    def generate_conservation_report(self, results: Dict) -> Dict:
        """Generate comprehensive conservation impact report."""
        report = {
            'conservation_summary': {
                'overall_conservation_score': 0.0,
                'species_performance': {},
                'habitat_preservation': {},
                'anti_poaching_readiness': {},
                'field_deployment_status': {}
            },
            'recommendations': [],
            'priority_actions': []
        }
        
        # Add detailed analysis based on results
        # This would be expanded based on specific model outputs
        
        return report

def calculate_model_conservation_impact(model_results: Dict, 
                                      conservation_priorities: Dict) -> Dict:
    """Calculate overall conservation impact of the model."""
    metrics = ConservationMetrics()
    
    impact_score = {
        'species_protection': 0.0,
        'habitat_preservation': 0.0, 
        'anti_poaching_effectiveness': 0.0,
        'research_advancement': 0.0,
        'overall_impact': 0.0
    }
    
    # Calculate impact components
    # Implementation would depend on specific model outputs
    
    return impact_score
'''
        
        with open(metrics_dir / "conservation_metrics.py", 'w') as f:
            f.write(conservation_metrics_code)
        
        logger.info("✅ Conservation metrics framework created")
    
    def create_training_orchestrator(self) -> None:
        """Create main training orchestrator script."""
        logger.info("🎼 Creating training orchestrator...")
        
        orchestrator_code = f'''#!/usr/bin/env python3
"""
Madagascar Conservation AI Training Orchestrator
===============================================

Main script to orchestrate training of all Madagascar conservation models.
"""

import os
import sys
import logging
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
import torch
import wandb
import optuna
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from training_pipelines.yolov8_madagascar_wildlife.train_madagascar_wildlife import MadagascarYOLOv8Trainer
from training_pipelines.lemur_species_classifier.train_lemur_classifier import LemurSpeciesClassifier
from utils.conservation_metrics.conservation_metrics import ConservationMetrics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MadagascarTrainingOrchestrator:
    """Orchestrate training of all Madagascar conservation models."""
    
    def __init__(self, config_path: str = None):
        self.base_path = Path(__file__).parent
        self.config_path = config_path or self.base_path / "configs"
        self.device = "{self.device}"
        
        # Initialize experiment tracking
        self.setup_experiment_tracking()
        
        # Load training configurations
        self.configs = self.load_training_configurations()
        
        # Initialize conservation metrics
        self.conservation_metrics = ConservationMetrics()
    
    def setup_experiment_tracking(self):
        """Set up experiment tracking systems."""
        logger.info("📊 Setting up experiment tracking...")
        
        # Initialize W&B project
        try:
            wandb.init(
                project="madagascar_conservation_ai",
                name=f"training_session_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}",
                tags=["orchestrated_training", "phase2", "madagascar"]
            )
            logger.info("✅ W&B initialized")
        except Exception as e:
            logger.warning(f"⚠️ W&B initialization failed: {{e}}")
    
    def load_training_configurations(self) -> Dict:
        """Load all training configurations."""
        configs = {{}}
        
        config_files = [
            "yolov8_optuna_config.yaml",
            "lemur_classifier_optuna_config.yaml"
        ]
        
        for config_file in config_files:
            config_path = self.config_path / "hyperparameters" / config_file
            if config_path.exists():
                with open(config_path, 'r') as f:
                    configs[config_file.split('_')[0]] = yaml.safe_load(f)
        
        return configs
    
    def run_yolov8_training(self, optimize_hyperparameters: bool = True) -> Dict:
        """Run YOLOv8 Madagascar wildlife detection training."""
        logger.info("🦅 Starting YOLOv8 Madagascar wildlife training...")
        
        if optimize_hyperparameters and 'yolov8' in self.configs:
            # Run hyperparameter optimization
            study = optuna.create_study(direction="maximize")
            study.optimize(self.yolov8_objective, n_trials=10)
            
            best_params = study.best_params
            logger.info(f"🏆 Best YOLOv8 parameters: {{best_params}}")
        else:
            # Use default parameters
            best_params = {{}}
        
        # Train with best parameters
        trainer = MadagascarYOLOv8Trainer()
        results = trainer.train_model(
            data_path=self.base_path.parent / "datasets" / "madagascar_wildlife_images",
            **best_params
        )
        
        return results
    
    def yolov8_objective(self, trial):
        """Optuna objective function for YOLOv8 optimization."""
        # Define hyperparameter search space
        params = {{
            'learning_rate': trial.suggest_loguniform('learning_rate', 1e-4, 1e-1),
            'batch_size': trial.suggest_categorical('batch_size', [8, 16, 24, 32]),
            'epochs': 20  # Reduced for optimization
        }}
        
        # Train model with suggested parameters
        trainer = MadagascarYOLOv8Trainer()
        results = trainer.train_model(
            data_path=self.base_path.parent / "datasets" / "madagascar_wildlife_images",
            **params
        )
        
        # Return metric to optimize (mAP50-95)
        return results.get('mAP50-95', 0.0)
    
    def run_lemur_classification_training(self, optimize_hyperparameters: bool = True) -> Dict:
        """Run lemur species classification training."""
        logger.info("🦎 Starting lemur species classification training...")
        
        # Similar implementation for lemur classifier
        classifier = LemurSpeciesClassifier()
        results = classifier.train_model(
            data_path=self.base_path.parent / "datasets" / "lemur_identification"
        )
        
        return results
    
    def run_full_training_pipeline(self) -> Dict:
        """Run complete training pipeline for all models."""
        logger.info("🚀 Starting full Madagascar conservation AI training pipeline...")
        
        pipeline_results = {{
            'training_session': {{
                'start_time': datetime.now().isoformat(),
                'device': self.device,
                'models_trained': []
            }},
            'model_results': {{}},
            'conservation_impact': {{}}
        }}
        
        try:
            # 1. YOLOv8 Wildlife Detection
            logger.info("=" * 50)
            logger.info("🦅 PHASE 1: Wildlife Detection Training")
            yolo_results = self.run_yolov8_training()
            pipeline_results['model_results']['yolov8_wildlife'] = yolo_results
            pipeline_results['training_session']['models_trained'].append('yolov8_wildlife')
            
            # 2. Lemur Species Classification  
            logger.info("=" * 50)
            logger.info("🦎 PHASE 2: Lemur Species Classification Training")
            lemur_results = self.run_lemur_classification_training()
            pipeline_results['model_results']['lemur_classifier'] = lemur_results
            pipeline_results['training_session']['models_trained'].append('lemur_classifier')
            
            # 3. Calculate conservation impact
            logger.info("=" * 50)
            logger.info("🌿 PHASE 3: Conservation Impact Assessment")
            conservation_impact = self.conservation_metrics.generate_conservation_report(
                pipeline_results['model_results']
            )
            pipeline_results['conservation_impact'] = conservation_impact
            
            # 4. Log to W&B
            if wandb.run:
                wandb.log({{
                    'pipeline_completion': 1,
                    'models_trained': len(pipeline_results['training_session']['models_trained']),
                    'overall_conservation_score': conservation_impact.get('conservation_summary', {{}}).get('overall_conservation_score', 0)
                }})
            
            pipeline_results['training_session']['end_time'] = datetime.now().isoformat()
            pipeline_results['training_session']['status'] = 'completed'
            
            logger.info("🎉 Training pipeline completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Training pipeline failed: {{e}}")
            pipeline_results['training_session']['status'] = 'failed'
            pipeline_results['training_session']['error'] = str(e)
            raise
        
        return pipeline_results
    
    def save_training_results(self, results: Dict):
        """Save comprehensive training results."""
        results_dir = self.base_path / "evaluation" / "performance_metrics"
        results_file = results_dir / f"training_results_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"📊 Training results saved: {{results_file}}")

def main():
    """Main training execution."""
    logger.info("🌍 MADAGASCAR CONSERVATION AI - TRAINING ORCHESTRATOR")
    logger.info("=" * 60)
    
    # Initialize orchestrator
    orchestrator = MadagascarTrainingOrchestrator()
    
    # Run full training pipeline
    results = orchestrator.run_full_training_pipeline()
    
    # Save results
    orchestrator.save_training_results(results)
    
    # Display summary
    logger.info("\\n📋 TRAINING SUMMARY:")
    logger.info(f"   Models trained: {{len(results['training_session']['models_trained'])}}")
    logger.info(f"   Status: {{results['training_session']['status']}}")
    logger.info(f"   Device: {{results['training_session']['device']}}")
    
    if wandb.run:
        wandb.finish()

if __name__ == "__main__":
    main()
'''
        
        orchestrator_file = self.training_path / "training_orchestrator.py"
        with open(orchestrator_file, 'w') as f:
            f.write(orchestrator_code)
        
        logger.info(f"✅ Training orchestrator created: {orchestrator_file}")
    
    def setup_phase2_step2(self) -> None:
        """Execute complete Step 2 setup for Phase 2."""
        logger.info("🚀 Phase 2 Step 2: Advanced Training Pipeline Setup")
        logger.info("=" * 55)
        
        try:
            # Create directory structure
            self.create_training_directories()
            
            # Set up hyperparameter optimization
            self.create_hyperparameter_optimization_configs()
            
            # Set up W&B integration
            self.create_wandb_integration()
            
            # Create conservation metrics framework
            self.create_conservation_metrics_framework()
            
            # Create training orchestrator
            self.create_training_orchestrator()
            
            logger.info("\n🎉 Step 2 Complete: Advanced Training Pipeline Setup!")
            logger.info("=" * 52)
            logger.info("✅ Training directory structure created")
            logger.info("✅ Hyperparameter optimization configured (Optuna)")
            logger.info("✅ Experiment tracking setup (W&B)")
            logger.info("✅ Conservation metrics framework implemented")
            logger.info("✅ Training orchestrator ready")
            logger.info(f"\n🔧 Hardware Configuration:")
            logger.info(f"   💻 Device: {self.device}")
            logger.info(f"   🧠 Training ready: {torch.cuda.is_available() or (hasattr(torch.backends, 'mps') and torch.backends.mps.is_available())}")
            logger.info("\n🎯 Training Pipeline Features:")
            logger.info("   🔬 Automated hyperparameter optimization")
            logger.info("   📊 Real-time experiment tracking")
            logger.info("   🌿 Conservation-specific metrics")
            logger.info("   🏆 Multi-model orchestration")
            logger.info("   ⚡ Hardware-optimized training")
            logger.info("\n🚀 Ready for Step 3: Execute Specialized Training!")
            
        except Exception as e:
            logger.error(f"❌ Step 2 failed: {e}")
            raise

def main():
    """Main execution function."""
    # Initialize training pipeline setup
    base_path = Path(__file__).parent.parent.parent
    setup = MadagascarTrainingPipelineSetup(base_path)
    
    # Execute Step 2
    setup.setup_phase2_step2()

if __name__ == "__main__":
    main()
