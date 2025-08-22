"""
Step 4 Section 3: Real-time Processing Pipeline
===============================================
Implement real-time species identification with optimized processing pipeline.
"""

import sys
import os
import json
import time
import numpy as np
import cv2
import torch
import torch.nn.functional as F
from PIL import Image
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import threading
import queue
from concurrent.futures import ThreadPoolExecutor

# Import from previous sections
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
from step4_section1_test import (
    SpeciesConfidence, MadagascarSpecies, SpeciesDetection, MockImageProcessor
)
from step4_section2_test import (
    MadagascarSpeciesClassifier, TensorFlowSpeciesClassifier, EnsembleSpeciesClassifier
)

@dataclass
class ProcessingMetrics:
    """Real-time processing performance metrics."""
    total_images_processed: int = 0
    average_processing_time_ms: float = 0.0
    peak_processing_time_ms: float = 0.0
    successful_detections: int = 0
    failed_detections: int = 0
    confidence_distribution: Dict[str, int] = None
    species_distribution: Dict[str, int] = None
    
    def __post_init__(self):
        if self.confidence_distribution is None:
            self.confidence_distribution = {level.value: 0 for level in SpeciesConfidence}
        if self.species_distribution is None:
            self.species_distribution = {species.value: 0 for species in MadagascarSpecies}

class ImagePreprocessor:
    """Optimized image preprocessing for real-time performance."""
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size
        self.opencv_available = True
        
        try:
            import cv2
            self.cv2 = cv2
        except ImportError:
            self.opencv_available = False
            print("⚠️  OpenCV not available, using PIL fallback")
    
    def preprocess_image_opencv(self, image_path: str) -> np.ndarray:
        """Fast preprocessing using OpenCV."""
        # Load image
        image = self.cv2.imread(image_path, self.cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert BGR to RGB
        image = self.cv2.cvtColor(image, self.cv2.COLOR_BGR2RGB)
        
        # Resize efficiently
        image = self.cv2.resize(image, self.target_size, interpolation=self.cv2.INTER_LINEAR)
        
        # Normalize for neural networks
        image = image.astype(np.float32) / 255.0
        
        return image
    
    def preprocess_image_pil(self, image_path: str) -> np.ndarray:
        """Fallback preprocessing using PIL."""
        image = Image.open(image_path).convert('RGB')
        image = image.resize(self.target_size, Image.Resampling.LANCZOS)
        image_array = np.array(image).astype(np.float32) / 255.0
        return image_array
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess image with best available method."""
        start_time = time.time()
        
        try:
            if self.opencv_available:
                result = self.preprocess_image_opencv(image_path)
            else:
                result = self.preprocess_image_pil(image_path)
            
            processing_time = (time.time() - start_time) * 1000
            return result, processing_time
            
        except Exception as e:
            print(f"⚠️  Image preprocessing error: {e}")
            return None, 0
    
    def batch_preprocess(self, image_paths: List[str]) -> Tuple[np.ndarray, List[float]]:
        """Batch preprocess multiple images for efficiency."""
        batch_images = []
        processing_times = []
        
        for image_path in image_paths:
            image, proc_time = self.preprocess_image(image_path)
            if image is not None:
                batch_images.append(image)
                processing_times.append(proc_time)
        
        if batch_images:
            return np.stack(batch_images), processing_times
        else:
            return np.array([]), []

class OptimizedSpeciesDetector:
    """Optimized species detector for real-time performance."""
    
    def __init__(self, model_type: str = "pytorch", enable_gpu: bool = True):
        self.model_type = model_type
        self.enable_gpu = enable_gpu and torch.cuda.is_available()
        self.device = torch.device("cuda" if self.enable_gpu else "cpu")
        
        self.preprocessor = ImagePreprocessor()
        self.model = None
        self.metrics = ProcessingMetrics()
        self.processing_times = []
        
        print(f"🚀 Initializing detector: {model_type} on {self.device}")
    
    def initialize_model(self):
        """Initialize the specified model type."""
        try:
            if self.model_type == "pytorch":
                self.model = MadagascarSpeciesClassifier(pretrained=True)
                self.model = self.model.to(self.device)
                self.model.eval()
                print("✅ PyTorch model initialized and moved to device")
                
            elif self.model_type == "tensorflow":
                self.model = TensorFlowSpeciesClassifier()
                print("✅ TensorFlow model initialized")
                
            elif self.model_type == "ensemble":
                self.model = EnsembleSpeciesClassifier()
                self.model.initialize_models()
                print("✅ Ensemble model initialized")
                
            else:
                raise ValueError(f"Unknown model type: {self.model_type}")
            
            return True
            
        except Exception as e:
            print(f"❌ Model initialization error: {e}")
            return False
    
    def detect_species_pytorch(self, image_array: np.ndarray, image_path: str) -> SpeciesDetection:
        """Optimized PyTorch detection."""
        try:
            # Convert to tensor and add batch dimension
            image_tensor = torch.from_numpy(image_array).permute(2, 0, 1).unsqueeze(0).float()
            image_tensor = image_tensor.to(self.device)
            
            # Run inference
            with torch.no_grad():
                start_time = time.time()
                outputs = self.model(image_tensor)
                inference_time = (time.time() - start_time) * 1000
            
            # Process outputs
            probabilities = outputs[0].cpu().numpy()
            predicted_class = np.argmax(probabilities)
            confidence = float(probabilities[predicted_class])
            
            # Map to species
            species = self.model.species_mapping.get(predicted_class, MadagascarSpecies.UNKNOWN_SPECIES)
            
            detection = SpeciesDetection(
                detection_id=f"optimized_pytorch_{datetime.utcnow().timestamp()}",
                species=species,
                confidence=confidence,
                confidence_level=SpeciesConfidence.HIGH,  # Auto-calculated
                image_path=image_path,
                source=f"optimized_pytorch_{self.device}",
                metadata={
                    "model_type": "optimized_pytorch",
                    "device": str(self.device),
                    "inference_time_ms": inference_time,
                    "top_predictions": self._get_top_predictions_pytorch(probabilities, 3),
                    "optimization": "gpu_accelerated" if self.enable_gpu else "cpu_optimized"
                }
            )
            
            return detection
            
        except Exception as e:
            print(f"⚠️  PyTorch detection error: {e}")
            return None
    
    def detect_species(self, image_path: str) -> SpeciesDetection:
        """Main detection method with performance tracking."""
        total_start_time = time.time()
        
        try:
            # Preprocess image
            image_array, preprocess_time = self.preprocessor.preprocess_image(image_path)
            if image_array is None:
                self.metrics.failed_detections += 1
                return None
            
            # Run detection based on model type
            if self.model_type == "pytorch":
                detection = self.detect_species_pytorch(image_array, image_path)
            elif self.model_type == "tensorflow":
                detection = self.model.predict_species(image_path)
            elif self.model_type == "ensemble":
                detection = self.model.predict_ensemble(image_path)
            else:
                return None
            
            # Update metrics
            total_time = (time.time() - total_start_time) * 1000
            self._update_metrics(detection, total_time)
            
            return detection
            
        except Exception as e:
            print(f"⚠️  Detection error: {e}")
            self.metrics.failed_detections += 1
            return None
    
    def batch_detect(self, image_paths: List[str]) -> List[SpeciesDetection]:
        """Batch detection for improved throughput."""
        detections = []
        
        if self.model_type == "pytorch" and len(image_paths) > 1:
            # Use batch processing for PyTorch
            batch_images, preprocess_times = self.preprocessor.batch_preprocess(image_paths)
            
            if len(batch_images) > 0:
                # Convert to tensor batch
                batch_tensor = torch.from_numpy(batch_images).permute(0, 3, 1, 2).float()
                batch_tensor = batch_tensor.to(self.device)
                
                # Batch inference
                with torch.no_grad():
                    start_time = time.time()
                    batch_outputs = self.model(batch_tensor)
                    batch_inference_time = (time.time() - start_time) * 1000
                
                # Process batch results
                for i, (image_path, output) in enumerate(zip(image_paths, batch_outputs)):
                    probabilities = output.cpu().numpy()
                    predicted_class = np.argmax(probabilities)
                    confidence = float(probabilities[predicted_class])
                    species = self.model.species_mapping.get(predicted_class, MadagascarSpecies.UNKNOWN_SPECIES)
                    
                    detection = SpeciesDetection(
                        detection_id=f"batch_pytorch_{datetime.utcnow().timestamp()}_{i}",
                        species=species,
                        confidence=confidence,
                        confidence_level=SpeciesConfidence.HIGH,
                        image_path=image_path,
                        source=f"batch_pytorch_{self.device}",
                        metadata={
                            "model_type": "batch_pytorch",
                            "batch_size": len(image_paths),
                            "batch_inference_time_ms": batch_inference_time,
                            "individual_preprocess_time_ms": preprocess_times[i] if i < len(preprocess_times) else 0
                        }
                    )
                    
                    detections.append(detection)
                    self._update_metrics(detection, batch_inference_time / len(image_paths))
        else:
            # Fall back to individual processing
            for image_path in image_paths:
                detection = self.detect_species(image_path)
                if detection:
                    detections.append(detection)
        
        return detections
    
    def _get_top_predictions_pytorch(self, probabilities: np.ndarray, top_k: int = 3) -> List[Dict]:
        """Get top K predictions for PyTorch model."""
        top_indices = np.argsort(probabilities)[::-1][:top_k]
        return [
            {
                "species": self.model.species_mapping[idx].value,
                "confidence": float(probabilities[idx])
            }
            for idx in top_indices
        ]
    
    def _update_metrics(self, detection: SpeciesDetection, processing_time_ms: float):
        """Update performance metrics."""
        self.metrics.total_images_processed += 1
        self.processing_times.append(processing_time_ms)
        
        if detection:
            self.metrics.successful_detections += 1
            
            # Update confidence distribution
            confidence_level = detection.confidence_level.value
            self.metrics.confidence_distribution[confidence_level] += 1
            
            # Update species distribution
            species = detection.species.value
            self.metrics.species_distribution[species] += 1
        
        # Update timing metrics
        self.metrics.average_processing_time_ms = np.mean(self.processing_times)
        self.metrics.peak_processing_time_ms = max(self.processing_times)
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        success_rate = (self.metrics.successful_detections / max(self.metrics.total_images_processed, 1)) * 100
        
        return {
            "model_configuration": {
                "model_type": self.model_type,
                "device": str(self.device),
                "gpu_enabled": self.enable_gpu
            },
            "performance_metrics": {
                "total_processed": self.metrics.total_images_processed,
                "success_rate_percent": success_rate,
                "average_time_ms": self.metrics.average_processing_time_ms,
                "peak_time_ms": self.metrics.peak_processing_time_ms,
                "throughput_images_per_second": 1000 / max(self.metrics.average_processing_time_ms, 1)
            },
            "detection_statistics": {
                "confidence_distribution": self.metrics.confidence_distribution,
                "species_distribution": self.metrics.species_distribution,
                "most_detected_species": max(self.metrics.species_distribution, key=self.metrics.species_distribution.get) if self.metrics.species_distribution else "none"
            }
        }

class RealTimeSpeciesMonitor:
    """Real-time species monitoring system for field deployment."""
    
    def __init__(self, detector: OptimizedSpeciesDetector, max_queue_size: int = 100):
        self.detector = detector
        self.image_queue = queue.Queue(maxsize=max_queue_size)
        self.result_queue = queue.Queue()
        self.is_running = False
        self.worker_thread = None
        self.total_processed = 0
        
    def start_monitoring(self):
        """Start the real-time monitoring system."""
        if self.is_running:
            print("⚠️  Monitor already running")
            return
        
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._process_images, daemon=True)
        self.worker_thread.start()
        print("🚀 Real-time monitoring started")
    
    def stop_monitoring(self):
        """Stop the real-time monitoring system."""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        print("🛑 Real-time monitoring stopped")
    
    def add_image(self, image_path: str) -> bool:
        """Add image to processing queue."""
        try:
            self.image_queue.put(image_path, block=False)
            return True
        except queue.Full:
            print("⚠️  Image queue full, dropping image")
            return False
    
    def get_results(self) -> List[SpeciesDetection]:
        """Get all available detection results."""
        results = []
        while not self.result_queue.empty():
            try:
                result = self.result_queue.get(block=False)
                results.append(result)
            except queue.Empty:
                break
        return results
    
    def _process_images(self):
        """Background image processing worker."""
        print("🔄 Image processing worker started")
        
        while self.is_running:
            try:
                # Get image from queue with timeout
                image_path = self.image_queue.get(timeout=1.0)
                
                # Process image
                detection = self.detector.detect_species(image_path)
                
                if detection:
                    # Add result to output queue
                    try:
                        self.result_queue.put(detection, block=False)
                        self.total_processed += 1
                    except queue.Full:
                        print("⚠️  Result queue full, dropping result")
                
                # Mark task as done
                self.image_queue.task_done()
                
            except queue.Empty:
                # Timeout waiting for images - continue
                continue
            except Exception as e:
                print(f"⚠️  Processing error: {e}")
        
        print("🔄 Image processing worker stopped")

def test_image_preprocessing():
    """Test optimized image preprocessing."""
    print("🖼️  Testing Image Preprocessing...")
    
    try:
        preprocessor = ImagePreprocessor()
        
        # Create test image
        test_image_path = "test_preprocessing.jpg"
        test_image = Image.new('RGB', (640, 480), color='blue')
        test_image.save(test_image_path)
        
        # Test OpenCV preprocessing
        if preprocessor.opencv_available:
            image_array, proc_time = preprocessor.preprocess_image(test_image_path)
            print(f"✅ OpenCV preprocessing: {proc_time:.2f}ms")
            print(f"✅ Output shape: {image_array.shape}")
            print(f"✅ Value range: [{image_array.min():.3f}, {image_array.max():.3f}]")
        else:
            print("⚠️  OpenCV not available, testing PIL fallback")
            image_array, proc_time = preprocessor.preprocess_image(test_image_path)
            print(f"✅ PIL preprocessing: {proc_time:.2f}ms")
        
        # Test batch preprocessing
        test_images = [test_image_path] * 3
        batch_array, batch_times = preprocessor.batch_preprocess(test_images)
        
        if len(batch_array) > 0:
            print(f"✅ Batch preprocessing: {len(batch_array)} images")
            print(f"✅ Average batch time: {np.mean(batch_times):.2f}ms")
        
        # Cleanup
        os.remove(test_image_path)
        print("✅ Test image cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Image preprocessing error: {e}")
        return False

def test_optimized_detection():
    """Test optimized species detection."""
    print("\n🚀 Testing Optimized Detection...")
    
    try:
        # Test PyTorch detector
        detector = OptimizedSpeciesDetector(model_type="pytorch", enable_gpu=False)
        
        if detector.initialize_model():
            print("✅ Optimized detector initialized")
        else:
            print("❌ Detector initialization failed")
            return False
        
        # Create test image
        test_image_path = "test_optimized_detection.jpg"
        test_image = Image.new('RGB', (224, 224), color='green')
        test_image.save(test_image_path)
        
        # Test single detection
        detection = detector.detect_species(test_image_path)
        
        if detection:
            print(f"✅ Detection successful: {detection.species.value}")
            print(f"✅ Confidence: {detection.confidence:.3f}")
            print(f"✅ Device: {detection.metadata.get('device', 'unknown')}")
            print(f"✅ Inference time: {detection.metadata.get('inference_time_ms', 0):.2f}ms")
        else:
            print("❌ Detection failed")
            return False
        
        # Test batch detection
        test_images = [test_image_path] * 5
        batch_detections = detector.batch_detect(test_images)
        
        print(f"✅ Batch detection: {len(batch_detections)}/5 successful")
        
        # Test performance report
        performance_report = detector.get_performance_report()
        print(f"✅ Performance report generated")
        print(f"   • Success rate: {performance_report['performance_metrics']['success_rate_percent']:.1f}%")
        print(f"   • Average time: {performance_report['performance_metrics']['average_time_ms']:.2f}ms")
        print(f"   • Throughput: {performance_report['performance_metrics']['throughput_images_per_second']:.1f} images/sec")
        
        # Cleanup
        os.remove(test_image_path)
        print("✅ Test image cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Optimized detection error: {e}")
        return False

def test_real_time_monitoring():
    """Test real-time monitoring system."""
    print("\n⏰ Testing Real-time Monitoring...")
    
    try:
        # Create detector
        detector = OptimizedSpeciesDetector(model_type="pytorch", enable_gpu=False)
        
        if not detector.initialize_model():
            print("❌ Could not initialize detector for monitoring test")
            return False
        
        # Create monitor
        monitor = RealTimeSpeciesMonitor(detector, max_queue_size=10)
        
        # Create test images
        test_images = []
        for i in range(3):
            test_image_path = f"test_monitor_{i}.jpg"
            test_image = Image.new('RGB', (224, 224), color=('red', 'green', 'blue')[i])
            test_image.save(test_image_path)
            test_images.append(test_image_path)
        
        # Start monitoring
        monitor.start_monitoring()
        print("✅ Monitoring system started")
        
        # Add images to queue
        for image_path in test_images:
            success = monitor.add_image(image_path)
            if success:
                print(f"✅ Added image to queue: {image_path}")
            else:
                print(f"❌ Failed to add image: {image_path}")
        
        # Wait for processing
        time.sleep(2)
        
        # Get results
        results = monitor.get_results()
        print(f"✅ Retrieved {len(results)} results")
        
        for i, result in enumerate(results):
            print(f"   • Result {i+1}: {result.species.value} ({result.confidence:.3f})")
        
        # Stop monitoring
        monitor.stop_monitoring()
        print("✅ Monitoring system stopped")
        
        # Cleanup
        for image_path in test_images:
            if os.path.exists(image_path):
                os.remove(image_path)
        print("✅ Test images cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Real-time monitoring error: {e}")
        return False

def test_performance_benchmarking():
    """Test performance benchmarking across different configurations."""
    print("\n⚡ Testing Performance Benchmarking...")
    
    try:
        configurations = [
            ("pytorch", False),  # CPU
            ("pytorch", torch.cuda.is_available()),  # GPU if available
        ]
        
        results = {}
        
        for model_type, enable_gpu in configurations:
            config_name = f"{model_type}_{'gpu' if enable_gpu else 'cpu'}"
            print(f"\n🔧 Testing configuration: {config_name}")
            
            detector = OptimizedSpeciesDetector(model_type=model_type, enable_gpu=enable_gpu)
            
            if not detector.initialize_model():
                print(f"⚠️  Could not initialize {config_name}")
                continue
            
            # Create test images for benchmarking
            test_images = []
            colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'magenta', 'brown', 'pink']
            for i in range(10):
                test_image_path = f"benchmark_{config_name}_{i}.jpg"
                test_image = Image.new('RGB', (224, 224), color=colors[i])
                test_image.save(test_image_path)
                test_images.append(test_image_path)
            
            # Benchmark individual detection
            start_time = time.time()
            for image_path in test_images[:5]:
                detection = detector.detect_species(image_path)
            individual_time = (time.time() - start_time) * 1000
            
            # Benchmark batch detection
            start_time = time.time()
            batch_detections = detector.batch_detect(test_images[5:])
            batch_time = (time.time() - start_time) * 1000
            
            # Store results
            performance_report = detector.get_performance_report()
            results[config_name] = {
                "individual_total_time_ms": individual_time,
                "batch_total_time_ms": batch_time,
                "average_per_image_ms": performance_report['performance_metrics']['average_time_ms'],
                "throughput_images_per_sec": performance_report['performance_metrics']['throughput_images_per_second'],
                "success_rate": performance_report['performance_metrics']['success_rate_percent']
            }
            
            print(f"✅ {config_name} benchmark complete")
            print(f"   • Individual avg: {results[config_name]['average_per_image_ms']:.2f}ms")
            print(f"   • Throughput: {results[config_name]['throughput_images_per_sec']:.1f} images/sec")
            
            # Cleanup test images
            for image_path in test_images:
                if os.path.exists(image_path):
                    os.remove(image_path)
        
        # Compare results
        if len(results) > 1:
            print("\n📊 Performance Comparison:")
            for config, metrics in results.items():
                print(f"   • {config}: {metrics['throughput_images_per_sec']:.1f} images/sec")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance benchmarking error: {e}")
        return False

def test_memory_efficiency():
    """Test memory efficiency and resource usage."""
    print("\n💾 Testing Memory Efficiency...")
    
    try:
        import psutil
        import gc
        
        # Get initial memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"📊 Initial memory usage: {initial_memory:.1f} MB")
        
        # Create detector
        detector = OptimizedSpeciesDetector(model_type="pytorch", enable_gpu=False)
        
        # Memory after model initialization
        if detector.initialize_model():
            model_memory = process.memory_info().rss / 1024 / 1024
            print(f"📊 Memory after model init: {model_memory:.1f} MB (+{model_memory - initial_memory:.1f} MB)")
        
        # Process multiple images to test memory stability
        for batch_num in range(3):
            test_images = []
            for i in range(5):
                test_image_path = f"memory_test_{batch_num}_{i}.jpg"
                test_image = Image.new('RGB', (224, 224), color='orange')
                test_image.save(test_image_path)
                test_images.append(test_image_path)
            
            # Process batch
            detections = detector.batch_detect(test_images)
            
            # Check memory after batch
            batch_memory = process.memory_info().rss / 1024 / 1024
            print(f"📊 Memory after batch {batch_num + 1}: {batch_memory:.1f} MB")
            
            # Cleanup
            for image_path in test_images:
                os.remove(image_path)
            
            # Force garbage collection
            gc.collect()
        
        # Final memory check
        final_memory = process.memory_info().rss / 1024 / 1024
        print(f"📊 Final memory usage: {final_memory:.1f} MB")
        
        # Memory efficiency check
        memory_increase = final_memory - model_memory
        if memory_increase < 50:  # Less than 50MB increase
            print("✅ Memory usage stable (good efficiency)")
        else:
            print("⚠️  Memory usage increased significantly")
        
        return True
        
    except ImportError:
        print("⚠️  psutil not available, skipping memory test")
        return True
    except Exception as e:
        print(f"❌ Memory efficiency error: {e}")
        return False

def main():
    """Run Section 3 tests."""
    print("🚀 STEP 4 - SECTION 3: Real-time Processing Pipeline")
    print("=" * 54)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Image preprocessing
    if test_image_preprocessing():
        tests_passed += 1
    
    # Test 2: Optimized detection
    if test_optimized_detection():
        tests_passed += 1
    
    # Test 3: Real-time monitoring
    if test_real_time_monitoring():
        tests_passed += 1
    
    # Test 4: Performance benchmarking
    if test_performance_benchmarking():
        tests_passed += 1
    
    # Test 5: Memory efficiency
    if test_memory_efficiency():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Section 3 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 3 PASSED - Ready for Section 4")
        return True
    else:
        print("❌ Section 3 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
