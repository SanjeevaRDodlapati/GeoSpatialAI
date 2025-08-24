"""
GeoSpatialAI ML Model Integration System
=======================================

Main initialization and entry point for the integrated ML model system.
This module provides the primary interface for conservation researchers
and practitioners to access all ML capabilities.

Features:
- Unified interface for all ML models
- Conservation-focused analysis workflows
- Madagascar-specific adaptations
- Production-ready deployment capabilities

Author: GeoSpatialAI Development Team
Date: August 21, 2025
Version: 1.0.0
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional
import click
import yaml
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ml_integration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Version and system information
__version__ = "1.0.0"
__author__ = "GeoSpatialAI Development Team"
__system_name__ = "Conservation AI Platform"

def check_dependencies():
    """Check if all required dependencies are installed."""
    
    logger.info("🔍 Checking system dependencies...")
    
    required_packages = [
        'torch',
        'torchvision', 
        'ultralytics',
        'librosa',
        'cv2',
        'numpy',
        'pandas',
        'matplotlib',
        'geopandas',
        'rasterio',
        'scipy',
        'scikit-learn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} available")
        except ImportError:
            missing_packages.append(package)
            logger.warning(f"❌ {package} not found")
    
    if missing_packages:
        logger.error(f"Missing packages: {missing_packages}")
        print("\n🚨 Missing Dependencies:")
        print("Please install missing packages with:")
        print(f"pip install -r requirements_ml_integration.txt")
        return False
    else:
        logger.info("✅ All dependencies satisfied")
        return True

def verify_model_availability():
    """Verify that ML models can be loaded."""
    
    logger.info("🤖 Verifying ML model availability...")
    
    model_status = {}
    
    # Check YOLOv8
    try:
        from ultralytics import YOLO
        # Import centralized model path configuration
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        sys.path.append(str(project_root))
        from src.utils.model_paths import get_yolo_path
        
        # Import centralized model path configuration
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        sys.path.append(str(project_root))
        from src.utils.model_paths import get_yolo_path
        
        yolo_model = YOLO(get_yolo_path())  # Use centralized path configuration
        model_status['yolov8'] = 'Available'
        logger.info("✅ YOLOv8 model available")
    except Exception as e:
        model_status['yolov8'] = f'Error: {e}'
        logger.warning(f"⚠️ YOLOv8 issue: {e}")
    
    # Check BirdNET dependencies
    try:
        import librosa
        import tensorflow as tf
        model_status['birdnet'] = 'Dependencies available'
        logger.info("✅ BirdNET dependencies available")
    except Exception as e:
        model_status['birdnet'] = f'Error: {e}'
        logger.warning(f"⚠️ BirdNET dependency issue: {e}")
    
    # Check SAM dependencies
    try:
        import cv2
        import torch
        model_status['sam'] = 'Dependencies available'
        logger.info("✅ SAM dependencies available")
    except Exception as e:
        model_status['sam'] = f'Error: {e}'
        logger.warning(f"⚠️ SAM dependency issue: {e}")
    
    return model_status

def create_project_structure():
    """Create necessary project directories for ML integration."""
    
    logger.info("📁 Creating project structure...")
    
    directories = [
        'ml_model_integration/data/input',
        'ml_model_integration/data/output',
        'models/checkpoints',                    # Use unified models directory
        'models/configs',                        # Use unified models directory
        'ml_model_integration/results/wildlife_detection',
        'ml_model_integration/results/acoustic_monitoring',
        'ml_model_integration/results/habitat_segmentation',
        'ml_model_integration/results/integrated_analysis',
        'ml_model_integration/logs',
        'ml_model_integration/cache'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"📂 Created: {directory}")
    
    logger.info("✅ Project structure created")

def create_default_config():
    """Create default configuration file for ML integration system."""
    
    config = {
        'system': {
            'name': __system_name__,
            'version': __version__,
            'deployment_mode': 'development',  # development, production
            'log_level': 'INFO'
        },
        'models': {
            'wildlife_detection': {
                'model_type': 'yolov8n',
                'confidence_threshold': 0.6,
                'device': 'auto',
                'batch_size': 16,
                'enable_tracking': True
            },
            'acoustic_monitoring': {
                'model_type': 'birdnet',
                'confidence_threshold': 0.7,
                'sample_rate': 48000,
                'segment_length': 3.0,
                'overlap': 0.0,
                'enable_preprocessing': True
            },
            'habitat_segmentation': {
                'model_type': 'vit_h',
                'device': 'auto',
                'batch_size': 1,
                'enable_postprocessing': True
            }
        },
        'madagascar_specialization': {
            'species_database': 'data/madagascar_species.json',
            'endemic_species_priority': True,
            'conservation_status_filtering': True,
            'spatial_context': {
                'boundary_file': 'data/madagascar_boundary.geojson',
                'protected_areas': 'data/protected_areas.geojson',
                'elevation_model': 'data/madagascar_dem.tif'
            }
        },
        'integration': {
            'max_workers': 4,
            'timeout_seconds': 300,
            'save_all_results': True,
            'enable_batch_processing': True,
            'cache_predictions': True
        },
        'output': {
            'base_directory': 'ml_model_integration/results',
            'create_reports': True,
            'generate_visualizations': True,
            'export_formats': ['json', 'csv', 'geojson']
        },
        'performance': {
            'enable_monitoring': True,
            'memory_limit_gb': 8,
            'gpu_memory_fraction': 0.8,
            'enable_mixed_precision': False
        }
    }
    
    config_file = Path('ml_model_integration/config.yaml')
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)
    
    logger.info(f"⚙️ Default configuration created: {config_file}")
    return config

def load_configuration(config_path: Optional[str] = None) -> Dict:
    """Load system configuration from YAML file."""
    
    if config_path is None:
        config_path = 'ml_model_integration/config.yaml'
    
    config_file = Path(config_path)
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"📋 Configuration loaded from: {config_file}")
    else:
        logger.warning(f"⚠️ Config file not found: {config_file}. Creating default...")
        config = create_default_config()
    
    return config

def initialize_ml_system(config_path: Optional[str] = None):
    """Initialize the complete ML integration system."""
    
    print(f"""
🌍 {__system_name__} v{__version__}
=======================================
Madagascar Conservation AI Platform
Initializing ML Model Integration System...
    """)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Please install requirements.")
        return False
    
    # Create project structure
    create_project_structure()
    
    # Load configuration
    config = load_configuration(config_path)
    
    # Verify models
    model_status = verify_model_availability()
    
    # Initialize orchestrator
    try:
        from .conservation_ai_orchestrator import ConservationAIOrchestrator
        
        orchestrator = ConservationAIOrchestrator(config=config['models'])
        platform_status = orchestrator.get_platform_status()
        
        print("\n✅ System Initialization Complete!")
        print(f"📊 Models Available: {len(platform_status['available_capabilities'])}")
        print(f"🤖 Active Models: {', '.join(platform_status['available_capabilities'])}")
        
        return orchestrator
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize orchestrator: {e}")
        print(f"❌ System initialization failed: {e}")
        return None

# CLI Interface using Click
@click.group()
@click.version_option(version=__version__)
def cli():
    """GeoSpatialAI ML Model Integration CLI"""
    pass

@cli.command()
@click.option('--config', '-c', help='Path to configuration file')
def init(config):
    """Initialize the ML integration system"""
    orchestrator = initialize_ml_system(config)
    if orchestrator:
        print("🎉 Initialization successful! System ready for use.")
    else:
        print("❌ Initialization failed. Check logs for details.")

@cli.command()
def status():
    """Check system status and model availability"""
    
    print("🔍 Checking system status...")
    
    # Dependency check
    deps_ok = check_dependencies()
    
    # Model status
    model_status = verify_model_availability()
    
    print("\n📊 System Status Report:")
    print(f"Dependencies: {'✅ OK' if deps_ok else '❌ Issues'}")
    
    print("\n🤖 Model Status:")
    for model, status in model_status.items():
        status_icon = "✅" if "Error" not in status else "❌"
        print(f"  {model}: {status_icon} {status}")

@cli.command()
@click.option('--image', '-i', help='Path to wildlife image')
@click.option('--audio', '-a', help='Path to audio recording')
@click.option('--satellite', '-s', help='Path to satellite image')
@click.option('--output', '-o', default='analysis_results', help='Output directory')
def analyze(image, audio, satellite, output):
    """Run comprehensive conservation analysis"""
    
    if not any([image, audio, satellite]):
        print("❌ Please provide at least one input file (image, audio, or satellite)")
        return
    
    print("🔍 Starting comprehensive conservation analysis...")
    
    try:
        from .conservation_ai_orchestrator import ConservationAIOrchestrator
        
        orchestrator = ConservationAIOrchestrator()
        
        result = orchestrator.comprehensive_conservation_analysis(
            image_path=image,
            audio_path=audio,
            satellite_image_path=satellite,
            analysis_name=f"cli_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        print(f"✅ Analysis complete!")
        print(f"📊 Species detected: {result['integrated_insights']['species_diversity']['total_species_detected']}")
        print(f"🌿 Habitat quality: {result['integrated_insights']['habitat_quality']['overall_score']:.2f}")
        print(f"🔬 Biodiversity index: {result['integrated_insights']['biodiversity_index']:.2f}")
        print(f"💡 Recommendations: {len(result['conservation_recommendations'])}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")

@cli.command()
@click.option('--directory', '-d', required=True, help='Directory containing conservation data')
@click.option('--images', default='*.jpg', help='Image file pattern')
@click.option('--audio', default='*.wav', help='Audio file pattern')
@click.option('--satellite', default='*_sat.tif', help='Satellite image pattern')
def batch(directory, images, audio, satellite):
    """Run batch processing on a directory of conservation data"""
    
    print(f"🗂️ Starting batch processing of: {directory}")
    
    try:
        from .conservation_ai_orchestrator import ConservationAIOrchestrator
        
        orchestrator = ConservationAIOrchestrator()
        
        file_patterns = {
            'images': images,
            'audio': audio,
            'satellite': satellite
        }
        
        results_df = orchestrator.batch_process_conservation_data(
            data_directory=directory,
            file_patterns=file_patterns
        )
        
        print(f"✅ Batch processing complete!")
        print(f"📊 Processed {len(results_df)} items")
        if len(results_df) > 0:
            print(f"🌟 Average biodiversity index: {results_df['biodiversity_index'].mean():.2f}")
            print(f"🎯 Conservation recommendations: {results_df['recommendations'].sum()}")
        
    except Exception as e:
        print(f"❌ Batch processing failed: {e}")

@cli.command()
def demo():
    """Run demonstration of ML integration capabilities"""
    
    print("🎯 Running ML Integration Demo...")
    
    try:
        from .conservation_ai_orchestrator import run_phase1_implementation_test, create_sample_analysis
        
        # Test implementation
        orchestrator = run_phase1_implementation_test()
        
        # Create sample analysis
        sample_result = create_sample_analysis()
        
        print("\n🌟 Demo completed successfully!")
        print("The system is ready for real conservation data analysis.")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

@cli.command()
def install_models():
    """Download and install required ML model checkpoints"""
    
    print("📥 Downloading ML model checkpoints...")
    
    # YOLOv8 model
    try:
        from ultralytics import YOLO
        from src.utils.model_paths import get_yolo_path
        print("🔽 Loading YOLOv8 model...")
        yolo = YOLO(get_yolo_path())
        print("✅ YOLOv8 model ready")
    except Exception as e:
        print(f"❌ YOLOv8 download failed: {e}")
    
    # Additional model downloads would go here
    print("✅ Model installation complete!")

if __name__ == "__main__":
    cli()
