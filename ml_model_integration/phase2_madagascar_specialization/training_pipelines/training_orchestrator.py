#!/usr/bin/env python3
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
        self.device = "mps"
        
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
                name=f"training_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                tags=["orchestrated_training", "phase2", "madagascar"]
            )
            logger.info("✅ W&B initialized")
        except Exception as e:
            logger.warning(f"⚠️ W&B initialization failed: {e}")
    
    def load_training_configurations(self) -> Dict:
        """Load all training configurations."""
        configs = {}
        
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
            logger.info(f"🏆 Best YOLOv8 parameters: {best_params}")
        else:
            # Use default parameters
            best_params = {}
        
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
        params = {
            'learning_rate': trial.suggest_loguniform('learning_rate', 1e-4, 1e-1),
            'batch_size': trial.suggest_categorical('batch_size', [8, 16, 24, 32]),
            'epochs': 20  # Reduced for optimization
        }
        
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
        
        pipeline_results = {
            'training_session': {
                'start_time': datetime.now().isoformat(),
                'device': self.device,
                'models_trained': []
            },
            'model_results': {},
            'conservation_impact': {}
        }
        
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
                wandb.log({
                    'pipeline_completion': 1,
                    'models_trained': len(pipeline_results['training_session']['models_trained']),
                    'overall_conservation_score': conservation_impact.get('conservation_summary', {}).get('overall_conservation_score', 0)
                })
            
            pipeline_results['training_session']['end_time'] = datetime.now().isoformat()
            pipeline_results['training_session']['status'] = 'completed'
            
            logger.info("🎉 Training pipeline completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Training pipeline failed: {e}")
            pipeline_results['training_session']['status'] = 'failed'
            pipeline_results['training_session']['error'] = str(e)
            raise
        
        return pipeline_results
    
    def save_training_results(self, results: Dict):
        """Save comprehensive training results."""
        results_dir = self.base_path / "evaluation" / "performance_metrics"
        results_file = results_dir / f"training_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"📊 Training results saved: {results_file}")

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
    logger.info("\n📋 TRAINING SUMMARY:")
    logger.info(f"   Models trained: {len(results['training_session']['models_trained'])}")
    logger.info(f"   Status: {results['training_session']['status']}")
    logger.info(f"   Device: {results['training_session']['device']}")
    
    if wandb.run:
        wandb.finish()

if __name__ == "__main__":
    main()
