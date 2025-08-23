"""
YOLOv8 Wildlife Detection Integration
====================================

This module integrates YOLOv8 pre-trained wildlife detection models for 
real-time species identification in camera trap images and video streams.

Integration with GeoSpatialAI Platform:
- Real-time monitoring: applications/real_time_monitoring/
- Species validation: projects/project_7_advanced_species_habitat_dl/
- Conservation insights: Automated species occurrence tracking

Author: GeoSpatialAI Development Team
Date: August 21, 2025
Version: 1.0.0
"""

import os
import sys
import logging
from typing import List, Dict, Tuple, Optional, Union
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import cv2
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from ultralytics import YOLO
    import torch
    import torchvision.transforms as transforms
    YOLO_AVAILABLE = True
    logger.info("✅ YOLOv8 dependencies loaded successfully")
except ImportError as e:
    YOLO_AVAILABLE = False
    logger.warning(f"⚠️ YOLOv8 dependencies not available: {e}")
    logger.warning("Run: pip install ultralytics torch torchvision")

class MadagascarWildlifeDetector:
    """
    YOLOv8-based wildlife detection system optimized for Madagascar species.
    
    This class provides real-time species detection capabilities using
    pre-trained YOLOv8 models with Madagascar-specific optimizations.
    """
    
    def __init__(self, 
                 model_path: Optional[str] = None,
                 confidence_threshold: float = 0.5,
                 device: str = 'auto'):
        """
        Initialize the Madagascar Wildlife Detector.
        
        Parameters:
        -----------
        model_path : str, optional
            Path to custom YOLOv8 model. If None, uses pre-trained model.
        confidence_threshold : float, default=0.5
            Minimum confidence score for detection acceptance.
        device : str, default='auto'
            Device for inference ('cpu', 'cuda', 'mps', or 'auto').
        """
        
        self.confidence_threshold = confidence_threshold
        self.device = self._setup_device(device)
        self.model = None
        self.species_mapping = self._load_madagascar_species_mapping()
        self.detection_history = []
        
        # Initialize model
        if YOLO_AVAILABLE:
            self._load_model(model_path)
        else:
            logger.error("YOLOv8 not available. Please install required dependencies.")
    
    def _setup_device(self, device: str) -> str:
        """Setup computation device for inference."""
        if device == 'auto':
            if torch.cuda.is_available():
                device = 'cuda'
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                device = 'mps'  # Apple Silicon
            else:
                device = 'cpu'
        
        logger.info(f"🖥️ Using device: {device}")
        return device
    
    def _load_model(self, model_path: Optional[str] = None):
        """Load YOLOv8 model for wildlife detection."""
        try:
            if model_path and Path(model_path).exists():
                logger.info(f"📁 Loading custom model from: {model_path}")
                self.model = YOLO(model_path)
            else:
                # Use pre-trained YOLOv8 model (will be enhanced with wildlife-specific training)
                logger.info("🌐 Loading pre-trained YOLOv8 model")
                
                # Import centralized model path configuration
                import sys
                from pathlib import Path
                project_root = Path(__file__).parent.parent.parent
                sys.path.append(str(project_root))
                from src.utils.model_paths import get_yolo_path
                
                self.model = YOLO(get_yolo_path())  # Use centralized path configuration
                
            # Configure device
            if self.device != 'cpu':
                self.model.to(self.device)
                
            logger.info("✅ YOLOv8 model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load YOLOv8 model: {e}")
            self.model = None
    
    def _load_madagascar_species_mapping(self) -> Dict[str, Dict]:
        """
        Load Madagascar-specific species mapping and conservation information.
        
        This integrates with the existing species data from Project 5.
        """
        
        # Madagascar endemic species based on existing project data
        species_mapping = {
            'lemur_catta': {
                'common_name': 'Ring-tailed Lemur',
                'scientific_name': 'Lemur catta',
                'conservation_status': 'Endangered',
                'occurrences': 496,
                'priority': 'High',
                'habitat_model': 'Available'
            },
            'propithecus_verreauxi': {
                'common_name': "Verreaux's Sifaka",
                'scientific_name': 'Propithecus verreauxi',
                'conservation_status': 'Critically Endangered',
                'occurrences': 444,
                'priority': 'Critical',
                'habitat_model': 'Available'
            },
            'furcifer_pardalis': {
                'common_name': 'Panther Chameleon',
                'scientific_name': 'Furcifer pardalis',
                'conservation_status': 'Least Concern',
                'occurrences': 601,
                'priority': 'Medium',
                'habitat_model': 'Available'
            },
            'vanga_curvirostris': {
                'common_name': 'Hook-billed Vanga',
                'scientific_name': 'Vanga curvirostris',
                'conservation_status': 'Least Concern',
                'occurrences': 1000,
                'priority': 'Medium',
                'habitat_model': 'Available'
            },
            'coua_caerulea': {
                'common_name': 'Blue Coua',
                'scientific_name': 'Coua caerulea',
                'conservation_status': 'Least Concern',
                'occurrences': 1000,
                'priority': 'Medium',
                'habitat_model': 'Available'
            }
        }
        
        logger.info(f"📋 Loaded {len(species_mapping)} Madagascar species mappings")
        return species_mapping
    
    def detect_species(self, 
                      image_input: Union[str, np.ndarray, Image.Image],
                      save_results: bool = False,
                      output_dir: Optional[str] = None) -> Dict:
        """
        Detect wildlife species in an image.
        
        Parameters:
        -----------
        image_input : str, np.ndarray, or PIL.Image
            Input image (file path, numpy array, or PIL Image)
        save_results : bool, default=False
            Whether to save detection results
        output_dir : str, optional
            Directory to save results
            
        Returns:
        --------
        Dict containing detection results and metadata
        """
        
        if self.model is None:
            logger.error("❌ Model not loaded. Cannot perform detection.")
            return {'error': 'Model not available'}
        
        try:
            # Process input image
            image = self._process_image_input(image_input)
            
            # Run detection
            results = self.model(image, conf=self.confidence_threshold)
            
            # Process results
            detections = self._process_detections(results[0], image)
            
            # Add metadata
            detection_result = {
                'timestamp': datetime.now().isoformat(),
                'image_shape': image.shape if hasattr(image, 'shape') else 'Unknown',
                'model_confidence_threshold': self.confidence_threshold,
                'detections': detections,
                'species_count': len(set([d['species'] for d in detections])),
                'total_detections': len(detections)
            }
            
            # Save results if requested
            if save_results:
                self._save_detection_results(detection_result, output_dir)
            
            # Update history
            self.detection_history.append(detection_result)
            
            logger.info(f"🔍 Detected {len(detections)} objects in image")
            return detection_result
            
        except Exception as e:
            logger.error(f"❌ Detection failed: {e}")
            return {'error': str(e)}
    
    def _process_image_input(self, image_input: Union[str, np.ndarray, Image.Image]):
        """Process various image input formats."""
        
        if isinstance(image_input, str):
            # File path
            if not Path(image_input).exists():
                raise FileNotFoundError(f"Image file not found: {image_input}")
            return cv2.imread(image_input)
            
        elif isinstance(image_input, np.ndarray):
            # Numpy array
            return image_input
            
        elif isinstance(image_input, Image.Image):
            # PIL Image
            return cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)
            
        else:
            raise ValueError(f"Unsupported image input type: {type(image_input)}")
    
    def _process_detections(self, results, image) -> List[Dict]:
        """Process YOLO detection results into structured format."""
        
        detections = []
        
        if results.boxes is not None:
            boxes = results.boxes.xyxy.cpu().numpy()
            confidences = results.boxes.conf.cpu().numpy()
            classes = results.boxes.cls.cpu().numpy().astype(int)
            
            for i, (box, conf, cls) in enumerate(zip(boxes, confidences, classes)):
                x1, y1, x2, y2 = box
                
                # Map class to species (this will be enhanced with Madagascar-specific mapping)
                species_name = self._map_class_to_species(cls)
                
                detection = {
                    'detection_id': f"det_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}",
                    'species': species_name,
                    'confidence': float(conf),
                    'bbox': {
                        'x1': float(x1), 'y1': float(y1),
                        'x2': float(x2), 'y2': float(y2),
                        'width': float(x2 - x1),
                        'height': float(y2 - y1)
                    },
                    'conservation_info': self.species_mapping.get(species_name, {}),
                    'requires_attention': self._assess_conservation_priority(species_name, conf)
                }
                
                detections.append(detection)
        
        return detections
    
    def _map_class_to_species(self, class_id: int) -> str:
        """
        Map YOLO class ID to Madagascar species name.
        
        This will be enhanced when we have Madagascar-specific trained models.
        For now, uses generic COCO classes as baseline.
        """
        
        # Generic COCO class mapping (to be replaced with Madagascar-specific)
        coco_classes = {
            # Animals that might be relevant
            16: 'bird',
            17: 'cat',  # Could be fossa or small carnivores
            18: 'dog',  # Could be other mammals
            # Add more mappings as needed
        }
        
        generic_name = coco_classes.get(class_id, f'unknown_class_{class_id}')
        
        # TODO: Implement Madagascar-specific species mapping
        # This will be enhanced in Phase 2 with transfer learning
        
        return generic_name
    
    def _assess_conservation_priority(self, species_name: str, confidence: float) -> bool:
        """
        Assess if detection requires immediate conservation attention.
        
        Based on species conservation status and detection confidence.
        """
        
        if species_name in self.species_mapping:
            species_info = self.species_mapping[species_name]
            
            # High priority for endangered species with high confidence
            if (species_info.get('priority') in ['High', 'Critical'] and 
                confidence > 0.8):
                return True
                
            # Medium priority for other endemic species
            if confidence > 0.7:
                return True
        
        return False
    
    def _save_detection_results(self, results: Dict, output_dir: Optional[str] = None):
        """Save detection results to file."""
        
        if output_dir is None:
            output_dir = "detection_results"
        
        Path(output_dir).mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"detection_results_{timestamp}.json"
        filepath = Path(output_dir) / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"💾 Results saved to: {filepath}")
    
    def batch_process_images(self, 
                           image_directory: str,
                           output_directory: str = "batch_results",
                           image_extensions: List[str] = ['.jpg', '.jpeg', '.png', '.tiff']) -> pd.DataFrame:
        """
        Process a batch of images for species detection.
        
        Parameters:
        -----------
        image_directory : str
            Directory containing images to process
        output_directory : str
            Directory to save batch results
        image_extensions : List[str]
            Supported image file extensions
            
        Returns:
        --------
        pandas.DataFrame with batch processing results
        """
        
        logger.info(f"🗂️ Starting batch processing of: {image_directory}")
        
        image_dir = Path(image_directory)
        if not image_dir.exists():
            raise FileNotFoundError(f"Image directory not found: {image_directory}")
        
        # Find all images
        image_files = []
        for ext in image_extensions:
            image_files.extend(list(image_dir.glob(f"*{ext}")))
            image_files.extend(list(image_dir.glob(f"*{ext.upper()}")))
        
        logger.info(f"📸 Found {len(image_files)} images to process")
        
        # Process each image
        batch_results = []
        
        for i, image_file in enumerate(image_files):
            logger.info(f"🔍 Processing {i+1}/{len(image_files)}: {image_file.name}")
            
            try:
                result = self.detect_species(str(image_file), save_results=False)
                
                # Extract summary information
                summary = {
                    'image_file': str(image_file),
                    'timestamp': result.get('timestamp'),
                    'species_count': result.get('species_count', 0),
                    'total_detections': result.get('total_detections', 0),
                    'max_confidence': max([d['confidence'] for d in result.get('detections', [])], default=0),
                    'priority_detections': sum([d['requires_attention'] for d in result.get('detections', [])]),
                    'detected_species': list(set([d['species'] for d in result.get('detections', [])]))
                }
                
                batch_results.append(summary)
                
            except Exception as e:
                logger.error(f"❌ Failed to process {image_file}: {e}")
                batch_results.append({
                    'image_file': str(image_file),
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        # Convert to DataFrame
        results_df = pd.DataFrame(batch_results)
        
        # Save batch results
        Path(output_directory).mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = Path(output_directory) / f"batch_detection_results_{timestamp}.csv"
        results_df.to_csv(results_file, index=False)
        
        logger.info(f"✅ Batch processing complete. Results saved to: {results_file}")
        return results_df
    
    def get_detection_summary(self) -> Dict:
        """Get summary statistics of all detections."""
        
        if not self.detection_history:
            return {'message': 'No detections recorded yet'}
        
        total_detections = sum([d.get('total_detections', 0) for d in self.detection_history])
        unique_species = set()
        priority_detections = 0
        
        for detection_session in self.detection_history:
            for detection in detection_session.get('detections', []):
                unique_species.add(detection.get('species'))
                if detection.get('requires_attention'):
                    priority_detections += 1
        
        summary = {
            'total_processing_sessions': len(self.detection_history),
            'total_detections': total_detections,
            'unique_species_detected': len(unique_species),
            'species_list': list(unique_species),
            'priority_detections': priority_detections,
            'average_detections_per_session': total_detections / len(self.detection_history)
        }
        
        return summary

# Utility functions for integration with existing platform

def integrate_with_camera_traps(camera_trap_directory: str) -> pd.DataFrame:
    """
    Integration function for processing camera trap images.
    
    This function connects with the real-time monitoring system.
    """
    
    detector = MadagascarWildlifeDetector(confidence_threshold=0.6)
    
    if not detector.model:
        logger.error("❌ Cannot initialize detector. Check YOLOv8 installation.")
        return pd.DataFrame()
    
    results = detector.batch_process_images(
        image_directory=camera_trap_directory,
        output_directory="camera_trap_results"
    )
    
    return results

def validate_species_occurrences(detection_results: pd.DataFrame, 
                                existing_species_data: pd.DataFrame) -> Dict:
    """
    Validate detected species against existing occurrence data from Project 5.
    
    This provides quality control for automated detections.
    """
    
    validation_results = {
        'confirmed_species': [],
        'new_detections': [],
        'validation_accuracy': 0.0
    }
    
    # Implementation would compare detection results with existing species data
    # This integrates with projects/project_5_species_mapping/ data
    
    return validation_results

# Example usage and testing
if __name__ == "__main__":
    logger.info("🚀 Testing YOLOv8 Wildlife Detection Integration")
    
    # Initialize detector
    detector = MadagascarWildlifeDetector()
    
    if detector.model:
        logger.info("✅ YOLOv8 detector initialized successfully")
        
        # Test with sample image (if available)
        # results = detector.detect_species("sample_wildlife_image.jpg")
        # print(json.dumps(results, indent=2))
        
        # Get species mapping info
        print("🏷️ Madagascar Species Mapping:")
        for species, info in detector.species_mapping.items():
            print(f"  {species}: {info['common_name']} ({info['conservation_status']})")
    
    else:
        logger.warning("⚠️ YOLOv8 detector not available. Install dependencies first.")
        print("\nTo install required dependencies:")
        print("pip install ultralytics torch torchvision")
