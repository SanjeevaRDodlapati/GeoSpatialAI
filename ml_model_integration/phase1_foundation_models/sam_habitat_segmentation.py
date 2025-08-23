"""
Segment Anything Model (SAM) Habitat Segmentation Integration
===========================================================

This module integrates Meta AI's Segment Anything Model for automated
habitat boundary detection and ecosystem segmentation in satellite imagery.

Integration with GeoSpatialAI Platform:
- Land cover analysis: projects/project_4_land_cover_analysis/
- Connectivity mapping: projects/project_8_landscape_connectivity/
- Real-time monitoring: applications/real_time_monitoring/

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
    import torch
    import torchvision.transforms as transforms
    from segment_anything import SamPredictor, sam_model_registry
    import supervision as sv
    SAM_AVAILABLE = True
    logger.info("✅ SAM dependencies loaded successfully")
except ImportError as e:
    SAM_AVAILABLE = False
    logger.warning(f"⚠️ SAM dependencies not available: {e}")
    logger.warning("Run: pip install segment-anything torch torchvision supervision")

try:
    import rasterio
    from rasterio.transform import from_bounds
    import geopandas as gpd
    from shapely.geometry import Polygon, MultiPolygon
    import fiona
    GEOSPATIAL_AVAILABLE = True
    logger.info("✅ Geospatial dependencies available")
except ImportError as e:
    GEOSPATIAL_AVAILABLE = False
    logger.warning(f"⚠️ Geospatial dependencies not available: {e}")

class MadagascarHabitatSegmenter:
    """
    SAM-based habitat segmentation system optimized for Madagascar ecosystems.
    
    This class provides automated habitat boundary detection and ecosystem
    segmentation capabilities for conservation planning and monitoring.
    """
    
    def __init__(self, 
                 model_type: str = "vit_h",
                 model_path: Optional[str] = None,
                 device: str = 'auto'):
        """
        Initialize the Madagascar Habitat Segmenter.
        
        Parameters:
        -----------
        model_type : str, default="vit_h"
            SAM model type ('vit_h', 'vit_l', 'vit_b')
        model_path : str, optional
            Path to SAM model checkpoint. If None, downloads pre-trained model.
        device : str, default='auto'
            Device for inference ('cpu', 'cuda', 'mps', or 'auto').
        """
        
        self.model_type = model_type
        self.device = self._setup_device(device)
        self.sam_predictor = None
        self.madagascar_ecosystems = self._load_madagascar_ecosystems()
        self.segmentation_history = []
        
        # Initialize model
        if SAM_AVAILABLE:
            self._load_sam_model(model_path)
        else:
            logger.error("SAM not available. Please install required dependencies.")
    
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
    
    def _load_sam_model(self, model_path: Optional[str] = None):
        """Load SAM model for habitat segmentation."""
        try:
            if model_path and Path(model_path).exists():
                logger.info(f"📁 Loading SAM model from: {model_path}")
                checkpoint_path = model_path
            else:
                # Download pre-trained SAM model
                logger.info(f"🌐 Loading pre-trained SAM model: {self.model_type}")
                checkpoint_path = self._download_sam_checkpoint()
            
            # Initialize SAM model
            sam = sam_model_registry[self.model_type](checkpoint=checkpoint_path)
            sam.to(device=self.device)
            
            # Create predictor
            self.sam_predictor = SamPredictor(sam)
            
            logger.info("✅ SAM model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load SAM model: {e}")
            self.sam_predictor = None
    
    def _download_sam_checkpoint(self) -> str:
        """Download SAM model checkpoint if not available."""
        
        # SAM model URLs
        sam_urls = {
            "vit_h": "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth",
            "vit_l": "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth",
            "vit_b": "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"
        }
        
        # Create models directory
        models_dir = Path("models/sam")
        models_dir.mkdir(parents=True, exist_ok=True)
        
        checkpoint_filename = f"sam_{self.model_type}.pth"
        checkpoint_path = models_dir / checkpoint_filename
        
        if not checkpoint_path.exists():
            logger.info(f"📥 Downloading SAM {self.model_type} model...")
            
            import urllib.request
            urllib.request.urlretrieve(sam_urls[self.model_type], checkpoint_path)
            
            logger.info(f"✅ Model downloaded to: {checkpoint_path}")
        
        return str(checkpoint_path)
    
    def _load_madagascar_ecosystems(self) -> Dict[str, Dict]:
        """
        Load Madagascar ecosystem type definitions for targeted segmentation.
        
        Based on Madagascar's unique biogeography and conservation priorities.
        """
        
        ecosystems = {
            'tropical_rainforest': {
                'name': 'Tropical Rainforest',
                'description': 'High-diversity humid forests in eastern Madagascar',
                'conservation_priority': 'Critical',
                'typical_species': ['Lemur catta', 'Vanga curvirostris'],
                'characteristics': {
                    'canopy_cover': '>80%',
                    'elevation': '0-1200m',
                    'rainfall': '>1500mm/year'
                }
            },
            'spiny_forest': {
                'name': 'Spiny Forest',
                'description': 'Unique xerophytic forests in southern Madagascar',
                'conservation_priority': 'Critical',
                'typical_species': ['Propithecus verreauxi'],
                'characteristics': {
                    'canopy_cover': '20-60%',
                    'elevation': '0-500m',
                    'rainfall': '<600mm/year'
                }
            },
            'deciduous_forest': {
                'name': 'Deciduous Forest',
                'description': 'Seasonal dry forests in western Madagascar',
                'conservation_priority': 'High',
                'typical_species': ['Coua caerulea'],
                'characteristics': {
                    'canopy_cover': '60-80%',
                    'elevation': '0-800m',
                    'rainfall': '600-1200mm/year'
                }
            },
            'mangrove': {
                'name': 'Mangrove Forest',
                'description': 'Coastal mangrove ecosystems',
                'conservation_priority': 'High',
                'typical_species': ['Various coastal birds'],
                'characteristics': {
                    'canopy_cover': '40-80%',
                    'elevation': '0-5m',
                    'salinity': 'High'
                }
            },
            'highland_grassland': {
                'name': 'Highland Grassland',
                'description': 'High-altitude grasslands and montane vegetation',
                'conservation_priority': 'Medium',
                'typical_species': ['Endemic grassland species'],
                'characteristics': {
                    'canopy_cover': '<20%',
                    'elevation': '>1200m',
                    'temperature': 'Cool'
                }
            },
            'wetland': {
                'name': 'Wetland',
                'description': 'Freshwater wetlands and lakes',
                'conservation_priority': 'High',
                'typical_species': ['Waterbirds', 'Aquatic species'],
                'characteristics': {
                    'water_presence': 'Permanent/seasonal',
                    'vegetation': 'Aquatic/semi-aquatic'
                }
            },
            'agricultural': {
                'name': 'Agricultural Land',
                'description': 'Human-modified landscapes',
                'conservation_priority': 'Low',
                'typical_species': ['Generalist species'],
                'characteristics': {
                    'land_use': 'Crop production',
                    'modification': 'High'
                }
            },
            'urban': {
                'name': 'Urban/Built Area',
                'description': 'Cities, towns, and infrastructure',
                'conservation_priority': 'Low',
                'typical_species': ['Urban-adapted species'],
                'characteristics': {
                    'built_density': 'High',
                    'natural_cover': '<10%'
                }
            }
        }
        
        logger.info(f"🌿 Loaded {len(ecosystems)} Madagascar ecosystem definitions")
        return ecosystems
    
    def segment_habitat_image(self, 
                             image_input: Union[str, np.ndarray, Image.Image],
                             prompts: Optional[List[Dict]] = None,
                             save_results: bool = False,
                             output_dir: Optional[str] = None) -> Dict:
        """
        Segment habitat types in satellite/aerial imagery.
        
        Parameters:
        -----------
        image_input : str, np.ndarray, or PIL.Image
            Input image (file path, numpy array, or PIL Image)
        prompts : List[Dict], optional
            Segmentation prompts (points, boxes, text)
        save_results : bool, default=False
            Whether to save segmentation results
        output_dir : str, optional
            Directory to save results
            
        Returns:
        --------
        Dict containing segmentation results and habitat analysis
        """
        
        if self.sam_predictor is None:
            logger.error("❌ SAM model not loaded. Cannot perform segmentation.")
            return {'error': 'Model not available'}
        
        try:
            # Process input image
            image = self._process_image_input(image_input)
            
            # Set image for SAM predictor
            self.sam_predictor.set_image(image)
            
            # Generate segmentation prompts if not provided
            if prompts is None:
                prompts = self._generate_ecosystem_prompts(image)
            
            # Perform segmentation for each prompt
            segments = []
            for i, prompt in enumerate(prompts):
                segment_result = self._process_single_prompt(prompt, i)
                if segment_result:
                    segments.append(segment_result)
            
            # Analyze segmented habitats
            habitat_analysis = self._analyze_habitat_segments(segments, image)
            
            # Create comprehensive result
            result = {
                'timestamp': datetime.now().isoformat(),
                'image_shape': image.shape,
                'total_prompts': len(prompts),
                'successful_segments': len(segments),
                'segments': segments,
                'habitat_analysis': habitat_analysis,
                'ecosystem_summary': self._summarize_ecosystems(habitat_analysis)
            }
            
            # Save results if requested
            if save_results:
                self._save_segmentation_results(result, image, output_dir)
            
            # Update history
            self.segmentation_history.append(result)
            
            logger.info(f"🎯 Generated {len(segments)} habitat segments")
            return result
            
        except Exception as e:
            logger.error(f"❌ Habitat segmentation failed: {e}")
            return {'error': str(e)}
    
    def _process_image_input(self, image_input: Union[str, np.ndarray, Image.Image]) -> np.ndarray:
        """Process various image input formats."""
        
        if isinstance(image_input, str):
            # File path
            if not Path(image_input).exists():
                raise FileNotFoundError(f"Image file not found: {image_input}")
            image = cv2.imread(image_input)
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
        elif isinstance(image_input, np.ndarray):
            # Numpy array
            if len(image_input.shape) == 3 and image_input.shape[2] == 3:
                return image_input
            else:
                raise ValueError("Image array must be RGB format (H, W, 3)")
            
        elif isinstance(image_input, Image.Image):
            # PIL Image
            return np.array(image_input.convert('RGB'))
            
        else:
            raise ValueError(f"Unsupported image input type: {type(image_input)}")
    
    def _generate_ecosystem_prompts(self, image: np.ndarray) -> List[Dict]:
        """
        Generate segmentation prompts for Madagascar ecosystem types.
        
        This creates strategic prompts to identify different habitat types.
        """
        
        height, width = image.shape[:2]
        prompts = []
        
        # Grid-based prompts for comprehensive coverage
        grid_size = 5
        for i in range(grid_size):
            for j in range(grid_size):
                x = int((j + 0.5) * width / grid_size)
                y = int((i + 0.5) * height / grid_size)
                
                prompts.append({
                    'type': 'point',
                    'coordinates': [x, y],
                    'label': 1,  # Foreground
                    'ecosystem_hint': self._guess_ecosystem_from_location(i, j, grid_size)
                })
        
        # Edge-based prompts for boundary detection
        edge_prompts = [
            {'type': 'point', 'coordinates': [width//4, height//4], 'label': 1},
            {'type': 'point', 'coordinates': [3*width//4, height//4], 'label': 1},
            {'type': 'point', 'coordinates': [width//4, 3*height//4], 'label': 1},
            {'type': 'point', 'coordinates': [3*width//4, 3*height//4], 'label': 1}
        ]
        
        prompts.extend(edge_prompts)
        
        logger.info(f"🎯 Generated {len(prompts)} segmentation prompts")
        return prompts
    
    def _guess_ecosystem_from_location(self, i: int, j: int, grid_size: int) -> str:
        """Guess likely ecosystem type based on image grid position."""
        
        # Simple heuristic based on typical Madagascar landscape patterns
        # This would be enhanced with actual geographic context
        
        if i == 0 or i == grid_size - 1 or j == 0 or j == grid_size - 1:
            # Edge areas might be different ecosystems
            return 'edge_transition'
        elif i < grid_size // 2:
            # Upper areas might be montane
            return 'highland_grassland'
        else:
            # Lower areas might be forest
            return 'tropical_rainforest'
    
    def _process_single_prompt(self, prompt: Dict, prompt_id: int) -> Optional[Dict]:
        """Process a single segmentation prompt."""
        
        try:
            if prompt['type'] == 'point':
                input_point = np.array([prompt['coordinates']])
                input_label = np.array([prompt['label']])
                
                masks, scores, logits = self.sam_predictor.predict(
                    point_coords=input_point,
                    point_labels=input_label,
                    multimask_output=True
                )
                
                # Select best mask
                best_mask_idx = np.argmax(scores)
                best_mask = masks[best_mask_idx]
                best_score = scores[best_mask_idx]
                
                # Analyze mask properties
                mask_properties = self._analyze_mask_properties(best_mask)
                
                return {
                    'prompt_id': prompt_id,
                    'prompt': prompt,
                    'mask': best_mask,
                    'score': float(best_score),
                    'properties': mask_properties,
                    'estimated_ecosystem': self._classify_mask_ecosystem(best_mask, mask_properties)
                }
                
        except Exception as e:
            logger.warning(f"⚠️ Failed to process prompt {prompt_id}: {e}")
            return None
    
    def _analyze_mask_properties(self, mask: np.ndarray) -> Dict:
        """Analyze properties of a segmentation mask."""
        
        # Basic geometric properties
        area = np.sum(mask)
        total_pixels = mask.shape[0] * mask.shape[1]
        area_ratio = area / total_pixels
        
        # Shape analysis
        contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Contour properties
            perimeter = cv2.arcLength(largest_contour, True)
            contour_area = cv2.contourArea(largest_contour)
            
            # Shape metrics
            if perimeter > 0:
                circularity = 4 * np.pi * contour_area / (perimeter * perimeter)
            else:
                circularity = 0
            
            # Bounding box
            x, y, w, h = cv2.boundingRect(largest_contour)
            aspect_ratio = w / h if h > 0 else 0
            
        else:
            circularity = 0
            aspect_ratio = 1
            x = y = w = h = 0
        
        properties = {
            'area_pixels': int(area),
            'area_ratio': float(area_ratio),
            'circularity': float(circularity),
            'aspect_ratio': float(aspect_ratio),
            'bounding_box': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
            'perimeter': float(perimeter) if 'perimeter' in locals() else 0
        }
        
        return properties
    
    def _classify_mask_ecosystem(self, mask: np.ndarray, properties: Dict) -> str:
        """
        Classify mask as a specific Madagascar ecosystem type.
        
        This uses heuristics based on shape and size properties.
        Real implementation would use spectral analysis and ML classification.
        """
        
        area_ratio = properties['area_ratio']
        circularity = properties['circularity']
        aspect_ratio = properties['aspect_ratio']
        
        # Simple classification heuristics
        if area_ratio > 0.5:
            # Large areas might be primary habitat
            if circularity > 0.7:
                return 'wetland'  # Circular water bodies
            else:
                return 'tropical_rainforest'  # Large forest patches
                
        elif area_ratio > 0.1:
            # Medium areas
            if aspect_ratio > 2.0:
                return 'mangrove'  # Linear coastal features
            else:
                return 'deciduous_forest'  # Medium forest patches
                
        else:
            # Small areas
            if circularity < 0.3:
                return 'agricultural'  # Irregular human-modified areas
            else:
                return 'highland_grassland'  # Small natural patches
    
    def _analyze_habitat_segments(self, segments: List[Dict], image: np.ndarray) -> Dict:
        """Analyze segmented habitats for conservation insights."""
        
        analysis = {
            'ecosystem_counts': {},
            'total_coverage': {},
            'conservation_priority_area': 0,
            'habitat_fragmentation': 0,
            'connectivity_analysis': {}
        }
        
        total_pixels = image.shape[0] * image.shape[1]
        
        # Count ecosystems and calculate coverage
        for segment in segments:
            ecosystem = segment['estimated_ecosystem']
            area = segment['properties']['area_pixels']
            
            if ecosystem not in analysis['ecosystem_counts']:
                analysis['ecosystem_counts'][ecosystem] = 0
                analysis['total_coverage'][ecosystem] = 0
            
            analysis['ecosystem_counts'][ecosystem] += 1
            analysis['total_coverage'][ecosystem] += area
        
        # Calculate coverage percentages
        for ecosystem in analysis['total_coverage']:
            coverage_ratio = analysis['total_coverage'][ecosystem] / total_pixels
            analysis['total_coverage'][ecosystem] = {
                'pixels': analysis['total_coverage'][ecosystem],
                'percentage': coverage_ratio * 100
            }
        
        # Assess conservation priority
        priority_ecosystems = ['tropical_rainforest', 'spiny_forest', 'mangrove']
        for ecosystem in priority_ecosystems:
            if ecosystem in analysis['total_coverage']:
                analysis['conservation_priority_area'] += analysis['total_coverage'][ecosystem]['percentage']
        
        # Calculate fragmentation index (simplified)
        forest_segments = [s for s in segments if 'forest' in s['estimated_ecosystem']]
        if len(forest_segments) > 0:
            avg_forest_size = np.mean([s['properties']['area_ratio'] for s in forest_segments])
            analysis['habitat_fragmentation'] = 1 - avg_forest_size  # Higher = more fragmented
        
        return analysis
    
    def _summarize_ecosystems(self, habitat_analysis: Dict) -> Dict:
        """Create ecosystem summary with conservation recommendations."""
        
        summary = {
            'dominant_ecosystem': None,
            'ecosystem_diversity': 0,
            'conservation_status': 'Unknown',
            'recommendations': []
        }
        
        # Find dominant ecosystem
        if habitat_analysis['ecosystem_counts']:
            dominant_ecosystem = max(habitat_analysis['ecosystem_counts'], 
                                   key=habitat_analysis['ecosystem_counts'].get)
            summary['dominant_ecosystem'] = dominant_ecosystem
        
        # Calculate ecosystem diversity (Shannon index)
        total_segments = sum(habitat_analysis['ecosystem_counts'].values())
        if total_segments > 0:
            shannon_index = 0
            for count in habitat_analysis['ecosystem_counts'].values():
                if count > 0:
                    p = count / total_segments
                    shannon_index -= p * np.log(p)
            summary['ecosystem_diversity'] = shannon_index
        
        # Conservation status assessment
        priority_area = habitat_analysis.get('conservation_priority_area', 0)
        fragmentation = habitat_analysis.get('habitat_fragmentation', 0)
        
        if priority_area > 50 and fragmentation < 0.3:
            summary['conservation_status'] = 'Good'
        elif priority_area > 30 and fragmentation < 0.5:
            summary['conservation_status'] = 'Moderate'
        else:
            summary['conservation_status'] = 'Concern'
        
        # Generate recommendations
        if fragmentation > 0.5:
            summary['recommendations'].append('Habitat connectivity restoration needed')
        if priority_area < 30:
            summary['recommendations'].append('Increase protected area coverage')
        if 'agricultural' in habitat_analysis['ecosystem_counts']:
            summary['recommendations'].append('Monitor agricultural expansion')
        
        return summary
    
    def _save_segmentation_results(self, results: Dict, image: np.ndarray, output_dir: Optional[str] = None):
        """Save segmentation results including visualizations."""
        
        if output_dir is None:
            output_dir = "habitat_segmentation_results"
        
        Path(output_dir).mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON results
        json_file = Path(output_dir) / f"segmentation_results_{timestamp}.json"
        
        # Convert numpy arrays to lists for JSON serialization
        json_results = json.loads(json.dumps(results, default=self._numpy_to_list))
        
        with open(json_file, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        # Save visualization
        self._create_segmentation_visualization(results, image, output_dir, timestamp)
        
        logger.info(f"💾 Results saved to: {output_dir}")
    
    def _numpy_to_list(self, obj):
        """Convert numpy arrays to lists for JSON serialization."""
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def _create_segmentation_visualization(self, results: Dict, image: np.ndarray, 
                                         output_dir: str, timestamp: str):
        """Create and save segmentation visualization."""
        
        # Create overlay image
        overlay = image.copy()
        
        # Color mapping for ecosystems
        ecosystem_colors = {
            'tropical_rainforest': [0, 255, 0],      # Green
            'spiny_forest': [255, 165, 0],           # Orange
            'deciduous_forest': [34, 139, 34],       # Forest Green
            'mangrove': [0, 100, 0],                 # Dark Green
            'highland_grassland': [255, 255, 0],     # Yellow
            'wetland': [0, 0, 255],                  # Blue
            'agricultural': [139, 69, 19],           # Brown
            'urban': [128, 128, 128]                 # Gray
        }
        
        # Apply masks with colors
        for segment in results.get('segments', []):
            mask = np.array(segment['mask'])
            ecosystem = segment['estimated_ecosystem']
            color = ecosystem_colors.get(ecosystem, [255, 255, 255])
            
            # Create colored mask
            colored_mask = np.zeros_like(image)
            colored_mask[mask] = color
            
            # Blend with original image
            alpha = 0.5
            overlay = cv2.addWeighted(overlay, 1-alpha, colored_mask, alpha, 0)
        
        # Save visualization
        viz_file = Path(output_dir) / f"habitat_segmentation_viz_{timestamp}.png"
        cv2.imwrite(str(viz_file), cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
        
        logger.info(f"🎨 Visualization saved to: {viz_file}")

# Utility functions for integration with existing platform

def integrate_with_land_cover_analysis(satellite_image_path: str) -> Dict:
    """
    Integration function for enhancing land cover analysis with SAM.
    
    This function connects with projects/project_4_land_cover_analysis/
    """
    
    segmenter = MadagascarHabitatSegmenter()
    
    if not segmenter.sam_predictor:
        logger.error("❌ Cannot initialize habitat segmenter. Check SAM installation.")
        return {'error': 'SAM not available'}
    
    results = segmenter.segment_habitat_image(
        image_input=satellite_image_path,
        save_results=True,
        output_dir="enhanced_land_cover_results"
    )
    
    return results

def validate_habitat_boundaries(segmentation_results: Dict, 
                              existing_boundaries: 'gpd.GeoDataFrame') -> Dict:
    """
    Validate SAM-generated habitat boundaries against existing data.
    
    This provides quality control for automated segmentation.
    """
    
    validation_results = {
        'boundary_agreement': 0.0,
        'new_habitat_areas': [],
        'validation_confidence': 0.0
    }
    
    # Implementation would compare SAM results with existing boundary data
    # This integrates with existing geospatial datasets
    
    return validation_results

# Example usage and testing
if __name__ == "__main__":
    logger.info("🚀 Testing SAM Habitat Segmentation Integration")
    
    # Initialize segmenter
    segmenter = MadagascarHabitatSegmenter()
    
    if segmenter.sam_predictor:
        logger.info("✅ SAM habitat segmenter initialized successfully")
        
        # Test with sample satellite image (if available)
        # results = segmenter.segment_habitat_image("sample_satellite_image.png")
        # print(json.dumps(results, indent=2))
        
        # Get ecosystem mapping info
        print("🌿 Madagascar Ecosystem Types:")
        for ecosystem, info in segmenter.madagascar_ecosystems.items():
            priority = info['conservation_priority']
            print(f"  {ecosystem}: {info['name']} (Priority: {priority})")
    
    else:
        logger.warning("⚠️ SAM habitat segmenter not available. Install dependencies first.")
        print("\nTo install required dependencies:")
        print("pip install segment-anything torch torchvision supervision")
