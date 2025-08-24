"""
PRITHVI Inference Engine
High-performance inference system for Earth observation analysis.
"""

import torch
import numpy as np
import time
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import logging
import json
from pathlib import Path

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.prithvi import SimplifiedPRITHVI, PRITHVIConfig, create_change_detection_model
from data.global_data import GlobalDataManager, global_data_manager

logger = logging.getLogger(__name__)

class InferenceEngine:
    """
    High-performance inference engine for PRITHVI Earth observation models.
    """
    
    def __init__(self, model: Optional[SimplifiedPRITHVI] = None, device: str = "auto"):
        """
        Initialize inference engine.
        
        Args:
            model: PRITHVI model instance (creates default if None)
            device: Device to use ("auto", "cpu", "cuda", "mps")
        """
        self.device = self._setup_device(device)
        self.model = model or create_change_detection_model()
        self.model.to(self.device)
        self.model.eval()
        
        self.data_manager = global_data_manager
        self.inference_history = []
        
        # Performance tracking
        self.total_inferences = 0
        self.total_inference_time = 0.0
        
        logger.info(f"Initialized inference engine on {self.device}")
        logger.info(f"Model parameters: {self.model.get_parameter_count():,}")
        
    def _setup_device(self, device: str) -> torch.device:
        """Setup computation device."""
        if device == "auto":
            if torch.cuda.is_available():
                return torch.device("cuda")
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return torch.device("mps")
            else:
                return torch.device("cpu")
        else:
            return torch.device(device)
    
    def preprocess_data(self, data: np.ndarray) -> torch.Tensor:
        """
        Preprocess satellite data for inference.
        
        Args:
            data: Input satellite data array
            
        Returns:
            Preprocessed tensor ready for inference
        """
        # Convert to tensor and ensure correct format
        if isinstance(data, np.ndarray):
            tensor = torch.from_numpy(data).float()
        else:
            tensor = data.float()
        
        # Ensure correct dimensions: (batch, channels, height, width)
        if tensor.dim() == 3:  # (H, W, C) -> (1, C, H, W)
            tensor = tensor.permute(2, 0, 1).unsqueeze(0)
        elif tensor.dim() == 4 and tensor.shape[-1] <= 10:  # (B, H, W, C) -> (B, C, H, W)
            tensor = tensor.permute(0, 3, 1, 2)
        
        # Normalize if values are in [0, 255] range
        if tensor.max() > 1.0:
            tensor = tensor / 255.0
        
        # Move to device
        tensor = tensor.to(self.device)
        
        return tensor
    
    def run_inference(self, data: np.ndarray, task: str = "change_detection") -> Dict[str, Any]:
        """
        Run inference on satellite data.
        
        Args:
            data: Input satellite data
            task: Type of analysis task
            
        Returns:
            Inference results dictionary
        """
        start_time = time.time()
        
        # Preprocess data
        input_tensor = self.preprocess_data(data)
        
        # Run inference
        with torch.no_grad():
            logits = self.model(input_tensor)
            probabilities = torch.softmax(logits, dim=1)
            prediction = torch.argmax(probabilities, dim=1)
            confidence = torch.max(probabilities, dim=1)[0]
        
        inference_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Extract results
        prediction_value = prediction.cpu().item()
        confidence_value = confidence.cpu().item()
        prob_values = probabilities.cpu().numpy().tolist()[0]
        
        # Create result dictionary
        result = {
            "task": task,
            "prediction": prediction_value,
            "confidence": confidence_value,
            "probabilities": prob_values,
            "inference_time_ms": inference_time,
            "timestamp": datetime.now().isoformat()
        }
        
        # Update performance tracking
        self.total_inferences += 1
        self.total_inference_time += inference_time
        
        # Store in history
        self.inference_history.append(result)
        
        logger.debug(f"Inference completed in {inference_time:.1f}ms")
        
        return result
    
    def batch_inference(self, data_batch: List[np.ndarray], 
                       task: str = "change_detection") -> List[Dict[str, Any]]:
        """
        Run batch inference on multiple samples.
        
        Args:
            data_batch: List of satellite data arrays
            task: Type of analysis task
            
        Returns:
            List of inference results
        """
        results = []
        
        for i, data in enumerate(data_batch):
            result = self.run_inference(data, task)
            result["batch_index"] = i
            results.append(result)
            
        logger.info(f"Completed batch inference on {len(data_batch)} samples")
        
        return results
    
    def analyze_conservation_area(self, area_name: str, source_name: str = "sentinel2",
                                num_samples: int = 10) -> Dict[str, Any]:
        """
        Analyze a specific conservation area.
        
        Args:
            area_name: Name of conservation area
            source_name: Satellite data source
            num_samples: Number of samples to analyze
            
        Returns:
            Analysis results
        """
        start_time = time.time()
        
        # Get area information
        area = self.data_manager.get_conservation_area(area_name)
        if not area:
            raise ValueError(f"Conservation area '{area_name}' not found")
        
        # Generate synthetic data for analysis
        data = self.data_manager.generate_sample_data(
            area_name, source_name, num_samples
        )
        
        # Run inference on each sample
        results = []
        for i in range(num_samples):
            sample_data = data[i]  # Shape: (224, 224, channels)
            result = self.run_inference(sample_data, "change_detection")
            result["sample_id"] = i
            results.append(result)
        
        # Analyze results
        predictions = [r["prediction"] for r in results]
        confidences = [r["confidence"] for r in results]
        
        analysis_summary = {
            "area_name": area.name,
            "country": area.country,
            "ecosystem_type": area.ecosystem_type,
            "satellite_source": source_name,
            "num_samples": num_samples,
            "analysis_results": {
                "change_detected_samples": sum(predictions),
                "no_change_samples": len(predictions) - sum(predictions),
                "change_detection_rate": np.mean(predictions),
                "average_confidence": np.mean(confidences),
                "min_confidence": np.min(confidences),
                "max_confidence": np.max(confidences)
            },
            "individual_results": results,
            "total_analysis_time_ms": (time.time() - start_time) * 1000,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Analyzed {area.name}: {sum(predictions)}/{num_samples} samples showed change")
        
        return analysis_summary
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        if self.total_inferences == 0:
            return {"message": "No inferences performed yet"}
        
        avg_inference_time = self.total_inference_time / self.total_inferences
        throughput = 1000.0 / avg_inference_time  # inferences per second
        
        recent_results = self.inference_history[-100:]  # Last 100 results
        recent_times = [r["inference_time_ms"] for r in recent_results]
        
        return {
            "total_inferences": self.total_inferences,
            "total_time_ms": self.total_inference_time,
            "average_inference_time_ms": avg_inference_time,
            "throughput_per_second": throughput,
            "recent_average_ms": np.mean(recent_times) if recent_times else 0,
            "recent_min_ms": np.min(recent_times) if recent_times else 0,
            "recent_max_ms": np.max(recent_times) if recent_times else 0,
            "device": str(self.device),
            "model_parameters": self.model.get_parameter_count()
        }
    
    def save_results(self, filepath: str) -> None:
        """Save inference results to file."""
        results_data = {
            "inference_history": self.inference_history,
            "performance_stats": self.get_performance_stats(),
            "model_info": self.model.get_model_info(),
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(results_data, f, indent=2, default=str)
        
        logger.info(f"Saved {len(self.inference_history)} results to {filepath}")
    
    def load_results(self, filepath: str) -> None:
        """Load inference results from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.inference_history = data.get("inference_history", [])
        self.total_inferences = len(self.inference_history)
        
        # Recalculate performance stats
        if self.inference_history:
            self.total_inference_time = sum(r["inference_time_ms"] for r in self.inference_history)
        
        logger.info(f"Loaded {len(self.inference_history)} results from {filepath}")
    
    def clear_history(self) -> None:
        """Clear inference history and reset counters."""
        self.inference_history.clear()
        self.total_inferences = 0
        self.total_inference_time = 0.0
        logger.info("Cleared inference history")

# Convenience functions
def create_inference_engine(device: str = "auto") -> InferenceEngine:
    """Create a new inference engine."""
    return InferenceEngine(device=device)

def quick_analysis(area_name: str, num_samples: int = 5) -> Dict[str, Any]:
    """Quick analysis of a conservation area."""
    engine = create_inference_engine()
    return engine.analyze_conservation_area(area_name, num_samples=num_samples)

if __name__ == "__main__":
    # Example usage
    engine = create_inference_engine()
    
    print("PRITHVI Inference Engine")
    print(f"Device: {engine.device}")
    print(f"Model parameters: {engine.model.get_parameter_count():,}")
    
    # Quick test
    test_data = np.random.rand(224, 224, 6)  # Random satellite data
    result = engine.run_inference(test_data)
    
    print(f"\nTest inference:")
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.3f}")
    print(f"Time: {result['inference_time_ms']:.1f}ms")
