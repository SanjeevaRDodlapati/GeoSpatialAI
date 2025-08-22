"""
ML Model Integration Coordinator
===============================

This module coordinates the integration of all pre-trained ML models
into the GeoSpatialAI conservation platform, providing a unified interface
for multi-modal conservation AI capabilities.

Integration Components:
- YOLOv8 Wildlife Detection
- BirdNET Acoustic Monitoring  
- SAM Habitat Segmentation
- PRITHVI Earth Observation (Phase 2)

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
from datetime import datetime
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import phase 1 foundation models
try:
    from phase1_foundation_models.yolov8_wildlife_detection import MadagascarWildlifeDetector
    from phase1_foundation_models.birdnet_acoustic_monitoring import MadagascarBirdAcousticMonitor
    from phase1_foundation_models.sam_habitat_segmentation import MadagascarHabitatSegmenter
    FOUNDATION_MODELS_AVAILABLE = True
    logger.info("✅ Foundation models loaded successfully")
except ImportError as e:
    try:
        # Try absolute imports
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'phase1_foundation_models'))
        from yolov8_wildlife_detection import MadagascarWildlifeDetector
        from birdnet_acoustic_monitoring import MadagascarBirdAcousticMonitor  
        from sam_habitat_segmentation import MadagascarHabitatSegmenter
        FOUNDATION_MODELS_AVAILABLE = True
        logger.info("✅ Foundation models loaded successfully (absolute import)")
    except ImportError as e2:
        FOUNDATION_MODELS_AVAILABLE = False
        logger.warning(f"⚠️ Foundation models not available: {e2}")

class ConservationAIOrchestrator:
    """
    Unified orchestrator for multi-modal conservation AI capabilities.
    
    This class coordinates all ML models to provide comprehensive
    conservation intelligence from multiple data sources.
    """
    
    def __init__(self, 
                 config: Optional[Dict] = None,
                 enable_wildlife_detection: bool = True,
                 enable_acoustic_monitoring: bool = True,
                 enable_habitat_segmentation: bool = True):
        """
        Initialize the Conservation AI Orchestrator.
        
        Parameters:
        -----------
        config : Dict, optional
            Configuration dictionary for model settings
        enable_wildlife_detection : bool, default=True
            Enable YOLOv8 wildlife detection
        enable_acoustic_monitoring : bool, default=True
            Enable BirdNET acoustic monitoring
        enable_habitat_segmentation : bool, default=True
            Enable SAM habitat segmentation
        """
        
        self.config = config or self._load_default_config()
        self.models = {}
        self.analysis_history = []
        self.performance_metrics = {}
        
        # Initialize enabled models
        if FOUNDATION_MODELS_AVAILABLE:
            self._initialize_models(
                enable_wildlife_detection,
                enable_acoustic_monitoring,
                enable_habitat_segmentation
            )
        else:
            logger.error("❌ Foundation models not available. Please install dependencies.")
    
    def _load_default_config(self) -> Dict:
        """Load default configuration for all models."""
        
        return {
            'wildlife_detection': {
                'confidence_threshold': 0.6,
                'model_type': 'yolov8n',
                'device': 'auto'
            },
            'acoustic_monitoring': {
                'confidence_threshold': 0.7,
                'sample_rate': 48000,
                'segment_length': 3.0
            },
            'habitat_segmentation': {
                'model_type': 'vit_h',
                'device': 'auto'
            },
            'integration': {
                'max_workers': 4,
                'timeout_seconds': 300,
                'save_all_results': True
            }
        }
    
    def _initialize_models(self, 
                          wildlife_detection: bool,
                          acoustic_monitoring: bool,
                          habitat_segmentation: bool):
        """Initialize requested ML models."""
        
        logger.info("🚀 Initializing Conservation AI models...")
        
        # Initialize wildlife detection
        if wildlife_detection:
            try:
                wildlife_config = self.config['wildlife_detection']
                self.models['wildlife_detector'] = MadagascarWildlifeDetector(
                    confidence_threshold=wildlife_config['confidence_threshold'],
                    device=wildlife_config['device']
                )
                logger.info("✅ Wildlife detection model initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize wildlife detection: {e}")
        
        # Initialize acoustic monitoring
        if acoustic_monitoring:
            try:
                acoustic_config = self.config['acoustic_monitoring']
                self.models['acoustic_monitor'] = MadagascarBirdAcousticMonitor(
                    confidence_threshold=acoustic_config['confidence_threshold'],
                    sample_rate=acoustic_config['sample_rate'],
                    segment_length=acoustic_config['segment_length']
                )
                logger.info("✅ Acoustic monitoring model initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize acoustic monitoring: {e}")
        
        # Initialize habitat segmentation
        if habitat_segmentation:
            try:
                segmentation_config = self.config['habitat_segmentation']
                self.models['habitat_segmenter'] = MadagascarHabitatSegmenter(
                    model_type=segmentation_config['model_type'],
                    device=segmentation_config['device']
                )
                logger.info("✅ Habitat segmentation model initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize habitat segmentation: {e}")
        
        logger.info(f"🎯 Initialized {len(self.models)} models successfully")
    
    def comprehensive_conservation_analysis(self,
                                          image_path: Optional[str] = None,
                                          audio_path: Optional[str] = None,
                                          satellite_image_path: Optional[str] = None,
                                          analysis_name: str = "comprehensive_analysis") -> Dict:
        """
        Perform comprehensive multi-modal conservation analysis.
        
        Parameters:
        -----------
        image_path : str, optional
            Path to wildlife/camera trap image
        audio_path : str, optional
            Path to acoustic recording
        satellite_image_path : str, optional
            Path to satellite/aerial imagery
        analysis_name : str
            Name for this analysis session
            
        Returns:
        --------
        Dict containing comprehensive conservation analysis results
        """
        
        logger.info(f"🔍 Starting comprehensive conservation analysis: {analysis_name}")
        
        start_time = datetime.now()
        results = {
            'analysis_name': analysis_name,
            'timestamp': start_time.isoformat(),
            'inputs': {
                'image_path': image_path,
                'audio_path': audio_path,
                'satellite_image_path': satellite_image_path
            },
            'model_results': {},
            'integrated_insights': {},
            'conservation_recommendations': []
        }
        
        # Parallel processing for different data types
        with ThreadPoolExecutor(max_workers=self.config['integration']['max_workers']) as executor:
            
            futures = {}
            
            # Wildlife detection analysis
            if image_path and 'wildlife_detector' in self.models:
                futures['wildlife'] = executor.submit(
                    self._analyze_wildlife_image, image_path
                )
            
            # Acoustic analysis
            if audio_path and 'acoustic_monitor' in self.models:
                futures['acoustic'] = executor.submit(
                    self._analyze_audio_recording, audio_path
                )
            
            # Habitat segmentation analysis
            if satellite_image_path and 'habitat_segmenter' in self.models:
                futures['habitat'] = executor.submit(
                    self._analyze_satellite_image, satellite_image_path
                )
            
            # Collect results
            for analysis_type, future in futures.items():
                try:
                    results['model_results'][analysis_type] = future.result(
                        timeout=self.config['integration']['timeout_seconds']
                    )
                    logger.info(f"✅ {analysis_type} analysis completed")
                except Exception as e:
                    logger.error(f"❌ {analysis_type} analysis failed: {e}")
                    results['model_results'][analysis_type] = {'error': str(e)}
        
        # Integrate results and generate insights
        results['integrated_insights'] = self._integrate_analysis_results(results['model_results'])
        results['conservation_recommendations'] = self._generate_conservation_recommendations(results)
        
        # Calculate processing time
        end_time = datetime.now()
        results['processing_time_seconds'] = (end_time - start_time).total_seconds()
        
        # Save results
        if self.config['integration']['save_all_results']:
            self._save_comprehensive_results(results)
        
        # Update history
        self.analysis_history.append(results)
        
        logger.info(f"🎉 Comprehensive analysis completed in {results['processing_time_seconds']:.1f}s")
        return results
    
    def _analyze_wildlife_image(self, image_path: str) -> Dict:
        """Analyze wildlife image using YOLO detection."""
        
        detector = self.models['wildlife_detector']
        return detector.detect_species(
            image_input=image_path,
            save_results=True,
            output_dir="integrated_analysis/wildlife"
        )
    
    def _analyze_audio_recording(self, audio_path: str) -> Dict:
        """Analyze audio recording using BirdNET classification."""
        
        monitor = self.models['acoustic_monitor']
        return monitor.process_audio_file(
            audio_path=audio_path,
            save_results=True,
            output_dir="integrated_analysis/acoustic"
        )
    
    def _analyze_satellite_image(self, satellite_image_path: str) -> Dict:
        """Analyze satellite image using SAM segmentation."""
        
        segmenter = self.models['habitat_segmenter']
        return segmenter.segment_habitat_image(
            image_input=satellite_image_path,
            save_results=True,
            output_dir="integrated_analysis/habitat"
        )
    
    def _integrate_analysis_results(self, model_results: Dict) -> Dict:
        """
        Integrate results from multiple models to generate conservation insights.
        """
        
        insights = {
            'species_diversity': self._calculate_species_diversity(model_results),
            'habitat_quality': self._assess_habitat_quality(model_results),
            'conservation_threats': self._identify_conservation_threats(model_results),
            'ecosystem_health': self._evaluate_ecosystem_health(model_results),
            'biodiversity_index': self._calculate_biodiversity_index(model_results)
        }
        
        return insights
    
    def _calculate_species_diversity(self, model_results: Dict) -> Dict:
        """Calculate overall species diversity from all detection methods."""
        
        species_detected = set()
        detection_methods = []
        
        # Wildlife detection species
        if 'wildlife' in model_results and 'detections' in model_results['wildlife']:
            for detection in model_results['wildlife']['detections']:
                species_detected.add(detection['species'])
            detection_methods.append('visual')
        
        # Acoustic detection species
        if 'acoustic' in model_results and 'species_detections' in model_results['acoustic']:
            for detection in model_results['acoustic']['species_detections']:
                species_detected.add(detection['species'])
            detection_methods.append('acoustic')
        
        return {
            'total_species_detected': len(species_detected),
            'species_list': list(species_detected),
            'detection_methods_used': detection_methods,
            'multi_modal_validation': len(detection_methods) > 1
        }
    
    def _assess_habitat_quality(self, model_results: Dict) -> Dict:
        """Assess habitat quality based on segmentation and species data."""
        
        quality_assessment = {
            'overall_score': 0.0,
            'factors': [],
            'recommendations': []
        }
        
        # Habitat segmentation quality indicators
        if 'habitat' in model_results and 'habitat_analysis' in model_results['habitat']:
            habitat_analysis = model_results['habitat']['habitat_analysis']
            
            # High conservation priority area percentage
            priority_area = habitat_analysis.get('conservation_priority_area', 0)
            if priority_area > 50:
                quality_assessment['factors'].append('High priority habitat coverage')
                quality_assessment['overall_score'] += 0.3
            
            # Low fragmentation
            fragmentation = habitat_analysis.get('habitat_fragmentation', 1)
            if fragmentation < 0.3:
                quality_assessment['factors'].append('Low habitat fragmentation')
                quality_assessment['overall_score'] += 0.3
        
        # Species diversity as quality indicator
        if 'wildlife' in model_results:
            species_count = model_results['wildlife'].get('species_count', 0)
            if species_count > 2:
                quality_assessment['factors'].append('High species diversity')
                quality_assessment['overall_score'] += 0.2
        
        # Acoustic diversity
        if 'acoustic' in model_results:
            acoustic_species = len(model_results['acoustic'].get('species_detections', []))
            if acoustic_species > 1:
                quality_assessment['factors'].append('Acoustic species diversity')
                quality_assessment['overall_score'] += 0.2
        
        # Normalize score
        quality_assessment['overall_score'] = min(quality_assessment['overall_score'], 1.0)
        
        return quality_assessment
    
    def _identify_conservation_threats(self, model_results: Dict) -> List[Dict]:
        """Identify potential conservation threats from analysis results."""
        
        threats = []
        
        # Habitat fragmentation threat
        if 'habitat' in model_results:
            habitat_analysis = model_results['habitat'].get('habitat_analysis', {})
            fragmentation = habitat_analysis.get('habitat_fragmentation', 0)
            
            if fragmentation > 0.5:
                threats.append({
                    'threat_type': 'Habitat Fragmentation',
                    'severity': 'High' if fragmentation > 0.7 else 'Medium',
                    'description': f'Fragmentation index: {fragmentation:.2f}',
                    'source': 'habitat_segmentation'
                })
        
        # Agricultural expansion threat
        if 'habitat' in model_results:
            ecosystem_summary = model_results['habitat'].get('ecosystem_summary', {})
            if 'agricultural' in str(ecosystem_summary.get('dominant_ecosystem', '')):
                threats.append({
                    'threat_type': 'Agricultural Expansion',
                    'severity': 'Medium',
                    'description': 'Agricultural land use detected in analysis area',
                    'source': 'habitat_segmentation'
                })
        
        # Low species detection threat
        species_count = 0
        if 'wildlife' in model_results:
            species_count += model_results['wildlife'].get('species_count', 0)
        if 'acoustic' in model_results:
            species_count += len(model_results['acoustic'].get('species_detections', []))
        
        if species_count < 2:
            threats.append({
                'threat_type': 'Low Species Diversity',
                'severity': 'Medium',
                'description': f'Only {species_count} species detected across all methods',
                'source': 'species_detection'
            })
        
        return threats
    
    def _evaluate_ecosystem_health(self, model_results: Dict) -> Dict:
        """Evaluate overall ecosystem health from integrated analysis."""
        
        health_indicators = {
            'species_richness': 0,
            'habitat_integrity': 0,
            'acoustic_activity': 0,
            'overall_health': 'Unknown'
        }
        
        # Species richness indicator
        total_species = 0
        if 'wildlife' in model_results:
            total_species += model_results['wildlife'].get('species_count', 0)
        if 'acoustic' in model_results:
            total_species += len(model_results['acoustic'].get('species_detections', []))
        
        health_indicators['species_richness'] = min(total_species / 5.0, 1.0)  # Normalize to max 5 species
        
        # Habitat integrity indicator
        if 'habitat' in model_results:
            habitat_analysis = model_results['habitat'].get('habitat_analysis', {})
            priority_area = habitat_analysis.get('conservation_priority_area', 0) / 100.0
            fragmentation = 1 - habitat_analysis.get('habitat_fragmentation', 1)
            health_indicators['habitat_integrity'] = (priority_area + fragmentation) / 2.0
        
        # Acoustic activity indicator
        if 'acoustic' in model_results:
            classified_segments = model_results['acoustic'].get('classified_segments', 0)
            total_segments = model_results['acoustic'].get('total_segments', 1)
            health_indicators['acoustic_activity'] = classified_segments / total_segments
        
        # Overall health assessment
        avg_health = np.mean([
            health_indicators['species_richness'],
            health_indicators['habitat_integrity'],
            health_indicators['acoustic_activity']
        ])
        
        if avg_health > 0.7:
            health_indicators['overall_health'] = 'Good'
        elif avg_health > 0.4:
            health_indicators['overall_health'] = 'Fair'
        else:
            health_indicators['overall_health'] = 'Poor'
        
        return health_indicators
    
    def _calculate_biodiversity_index(self, model_results: Dict) -> float:
        """Calculate a composite biodiversity index from all analysis methods."""
        
        # Collect species observations from all methods
        species_observations = []
        
        # Visual detections
        if 'wildlife' in model_results and 'detections' in model_results['wildlife']:
            for detection in model_results['wildlife']['detections']:
                species_observations.append({
                    'species': detection['species'],
                    'confidence': detection['confidence'],
                    'method': 'visual'
                })
        
        # Acoustic detections
        if 'acoustic' in model_results and 'species_detections' in model_results['acoustic']:
            for detection in model_results['acoustic']['species_detections']:
                species_observations.append({
                    'species': detection['species'],
                    'confidence': detection['max_confidence'],
                    'method': 'acoustic'
                })
        
        if not species_observations:
            return 0.0
        
        # Calculate Shannon diversity index
        species_counts = {}
        for obs in species_observations:
            species = obs['species']
            if species not in species_counts:
                species_counts[species] = 0
            species_counts[species] += 1
        
        total_observations = len(species_observations)
        shannon_index = 0
        
        for count in species_counts.values():
            if count > 0:
                p = count / total_observations
                shannon_index -= p * np.log(p)
        
        # Normalize to 0-1 scale (assuming max diversity of ~2.0)
        biodiversity_index = min(shannon_index / 2.0, 1.0)
        
        return biodiversity_index
    
    def _generate_conservation_recommendations(self, analysis_results: Dict) -> List[Dict]:
        """Generate conservation recommendations based on integrated analysis."""
        
        recommendations = []
        
        integrated_insights = analysis_results.get('integrated_insights', {})
        
        # Species diversity recommendations
        species_diversity = integrated_insights.get('species_diversity', {})
        if species_diversity.get('total_species_detected', 0) < 3:
            recommendations.append({
                'category': 'Species Conservation',
                'priority': 'High',
                'action': 'Enhance habitat connectivity to support species movement',
                'rationale': 'Low species diversity detected across monitoring methods'
            })
        
        # Habitat quality recommendations
        habitat_quality = integrated_insights.get('habitat_quality', {})
        if habitat_quality.get('overall_score', 0) < 0.5:
            recommendations.append({
                'category': 'Habitat Management',
                'priority': 'High',
                'action': 'Implement habitat restoration measures',
                'rationale': f"Habitat quality score: {habitat_quality.get('overall_score', 0):.2f}"
            })
        
        # Threat-based recommendations
        threats = integrated_insights.get('conservation_threats', [])
        for threat in threats:
            if threat['severity'] == 'High':
                recommendations.append({
                    'category': 'Threat Mitigation',
                    'priority': 'Critical',
                    'action': f"Address {threat['threat_type']} immediately",
                    'rationale': threat['description']
                })
        
        # Ecosystem health recommendations
        ecosystem_health = integrated_insights.get('ecosystem_health', {})
        if ecosystem_health.get('overall_health') == 'Poor':
            recommendations.append({
                'category': 'Ecosystem Restoration',
                'priority': 'High',
                'action': 'Comprehensive ecosystem rehabilitation program',
                'rationale': 'Multiple health indicators show ecosystem degradation'
            })
        
        # Monitoring recommendations
        if not integrated_insights.get('species_diversity', {}).get('multi_modal_validation'):
            recommendations.append({
                'category': 'Monitoring Enhancement',
                'priority': 'Medium',
                'action': 'Implement multi-modal species monitoring',
                'rationale': 'Current monitoring uses only single detection method'
            })
        
        return recommendations
    
    def _save_comprehensive_results(self, results: Dict):
        """Save comprehensive analysis results to file."""
        
        output_dir = Path("integrated_analysis/comprehensive_results")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"comprehensive_analysis_{timestamp}.json"
        filepath = output_dir / filename
        
        # Convert numpy arrays to lists for JSON serialization
        json_results = json.loads(json.dumps(results, default=self._numpy_to_list))
        
        with open(filepath, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        logger.info(f"💾 Comprehensive results saved to: {filepath}")
    
    def _numpy_to_list(self, obj):
        """Convert numpy arrays to lists for JSON serialization."""
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def get_platform_status(self) -> Dict:
        """Get status of all integrated ML models and platform capabilities."""
        
        status = {
            'timestamp': datetime.now().isoformat(),
            'models_initialized': len(self.models),
            'available_capabilities': list(self.models.keys()),
            'analysis_sessions_completed': len(self.analysis_history),
            'model_status': {}
        }
        
        # Check individual model status
        for model_name, model in self.models.items():
            if hasattr(model, 'model') and model.model is not None:
                status['model_status'][model_name] = 'Ready'
            else:
                status['model_status'][model_name] = 'Not Available'
        
        # Performance metrics
        if self.analysis_history:
            processing_times = [session.get('processing_time_seconds', 0) 
                              for session in self.analysis_history]
            status['performance_metrics'] = {
                'average_processing_time': np.mean(processing_times),
                'total_processing_time': sum(processing_times),
                'fastest_analysis': min(processing_times),
                'slowest_analysis': max(processing_times)
            }
        
        return status
    
    def batch_process_conservation_data(self, 
                                       data_directory: str,
                                       file_patterns: Dict[str, str]) -> pd.DataFrame:
        """
        Batch process conservation data from a directory structure.
        
        Parameters:
        -----------
        data_directory : str
            Root directory containing conservation data
        file_patterns : Dict[str, str]
            File patterns for different data types
            Example: {'images': '*.jpg', 'audio': '*.wav', 'satellite': '*_sat.tif'}
            
        Returns:
        --------
        pandas.DataFrame with batch processing results
        """
        
        logger.info(f"🗂️ Starting batch processing of: {data_directory}")
        
        data_dir = Path(data_directory)
        if not data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {data_directory}")
        
        # Find all files matching patterns
        file_sets = {}
        for data_type, pattern in file_patterns.items():
            file_sets[data_type] = list(data_dir.glob(pattern))
            logger.info(f"📁 Found {len(file_sets[data_type])} {data_type} files")
        
        # Process files in batches
        batch_results = []
        
        # Determine processing strategy based on available files
        max_files = max([len(files) for files in file_sets.values()] + [0])
        
        for i in range(max_files):
            batch_input = {}
            
            # Collect files for this batch
            for data_type, files in file_sets.items():
                if i < len(files):
                    batch_input[f"{data_type}_path"] = str(files[i])
            
            if batch_input:
                logger.info(f"🔍 Processing batch {i+1}/{max_files}")
                
                try:
                    result = self.comprehensive_conservation_analysis(
                        image_path=batch_input.get('images_path'),
                        audio_path=batch_input.get('audio_path'),
                        satellite_image_path=batch_input.get('satellite_path'),
                        analysis_name=f"batch_{i+1}"
                    )
                    
                    # Extract summary for DataFrame
                    summary = {
                        'batch_id': i + 1,
                        'timestamp': result['timestamp'],
                        'processing_time': result['processing_time_seconds'],
                        'species_detected': result['integrated_insights']['species_diversity']['total_species_detected'],
                        'habitat_quality_score': result['integrated_insights']['habitat_quality']['overall_score'],
                        'ecosystem_health': result['integrated_insights']['ecosystem_health']['overall_health'],
                        'biodiversity_index': result['integrated_insights']['biodiversity_index'],
                        'conservation_threats': len(result['integrated_insights']['conservation_threats']),
                        'recommendations': len(result['conservation_recommendations'])
                    }
                    
                    batch_results.append(summary)
                    
                except Exception as e:
                    logger.error(f"❌ Failed to process batch {i+1}: {e}")
                    batch_results.append({
                        'batch_id': i + 1,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
        
        # Convert to DataFrame and save
        results_df = pd.DataFrame(batch_results)
        
        if not results_df.empty:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            results_file = f"batch_conservation_analysis_{timestamp}.csv"
            results_df.to_csv(results_file, index=False)
            logger.info(f"📊 Batch results saved to: {results_file}")
        
        logger.info(f"✅ Batch processing complete. Processed {len(batch_results)} items.")
        return results_df

# Example usage and testing functions

def run_phase1_implementation_test():
    """Test Phase 1 foundation model integration."""
    
    logger.info("🚀 Testing Phase 1 Foundation Model Integration")
    
    # Initialize orchestrator
    orchestrator = ConservationAIOrchestrator()
    
    # Check platform status
    status = orchestrator.get_platform_status()
    print("\n📊 Platform Status:")
    print(json.dumps(status, indent=2))
    
    # Test individual model capabilities
    if 'wildlife_detector' in orchestrator.models:
        print("\n🦎 Wildlife Detection: Available")
    if 'acoustic_monitor' in orchestrator.models:
        print("🐦 Acoustic Monitoring: Available")
    if 'habitat_segmenter' in orchestrator.models:
        print("🌿 Habitat Segmentation: Available")
    
    return orchestrator

def create_sample_analysis():
    """Create a sample conservation analysis for demonstration."""
    
    logger.info("🎯 Creating sample conservation analysis")
    
    orchestrator = ConservationAIOrchestrator()
    
    # This would use actual data files in real deployment
    sample_result = {
        'analysis_name': 'sample_madagascar_analysis',
        'timestamp': datetime.now().isoformat(),
        'integrated_insights': {
            'species_diversity': {
                'total_species_detected': 3,
                'species_list': ['lemur_catta', 'vanga_curvirostris', 'coua_caerulea'],
                'multi_modal_validation': True
            },
            'habitat_quality': {
                'overall_score': 0.75,
                'factors': ['High priority habitat coverage', 'Low habitat fragmentation']
            },
            'ecosystem_health': {
                'overall_health': 'Good',
                'species_richness': 0.8,
                'habitat_integrity': 0.7,
                'acoustic_activity': 0.75
            },
            'biodiversity_index': 0.82
        },
        'conservation_recommendations': [
            {
                'category': 'Monitoring Enhancement',
                'priority': 'Medium',
                'action': 'Continue multi-modal monitoring',
                'rationale': 'Current monitoring provides good coverage'
            }
        ]
    }
    
    print("\n🌟 Sample Conservation Analysis:")
    print(json.dumps(sample_result, indent=2))
    
    return sample_result

if __name__ == "__main__":
    logger.info("🌍 GeoSpatialAI ML Model Integration - Phase 1 Implementation")
    
    # Run implementation test
    orchestrator = run_phase1_implementation_test()
    
    # Create sample analysis
    sample_analysis = create_sample_analysis()
    
    print("\n✅ Phase 1 foundation model integration ready for deployment!")
    print("\nNext steps:")
    print("1. Install required dependencies: pip install -r requirements_ml_integration.txt")
    print("2. Download model checkpoints")
    print("3. Test with real conservation data")
    print("4. Proceed to Phase 2: Madagascar specialization")
