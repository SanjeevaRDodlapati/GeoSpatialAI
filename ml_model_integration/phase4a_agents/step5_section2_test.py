"""
Step 5 Section 2: Threat Detection ML Models
============================================
Implement ML models for threat detection using computer vision and classification.
"""

import sys
import os
import json
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import cv2
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import warnings
warnings.filterwarnings("ignore")

# Import from previous sections
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
from step5_section1_test import ThreatType, ThreatSeverity, ThreatUrgency, ThreatDetection

class ThreatClassificationModel(nn.Module):
    """PyTorch CNN for threat classification."""
    
    def __init__(self, num_threat_types: int = 12, pretrained: bool = True):
        super(ThreatClassificationModel, self).__init__()
        
        # Use ResNet34 as backbone (good balance of accuracy and speed)
        self.backbone = models.resnet34(pretrained=pretrained)
        
        # Replace final layer for our threat types
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Linear(num_features, num_threat_types)
        
        # Add dropout for regularization
        self.dropout = nn.Dropout(0.5)
        
        # Threat type mapping
        self.threat_mapping = {
            0: ThreatType.DEFORESTATION,
            1: ThreatType.ILLEGAL_LOGGING,
            2: ThreatType.POACHING,
            3: ThreatType.HUMAN_INTRUSION,
            4: ThreatType.MINING,
            5: ThreatType.SLASH_AND_BURN,
            6: ThreatType.CHARCOAL_PRODUCTION,
            7: ThreatType.CATTLE_GRAZING,
            8: ThreatType.INFRASTRUCTURE_DEVELOPMENT,
            9: ThreatType.CLIMATE_IMPACT,
            10: ThreatType.INVASIVE_SPECIES,
            11: ThreatType.UNKNOWN_THREAT
        }
        
        # Image preprocessing pipeline
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    def forward(self, x):
        """Forward pass through the network."""
        features = self.backbone(x)
        return F.softmax(features, dim=1)
    
    def predict_threat(self, image_path: str) -> ThreatDetection:
        """Predict threat from image path."""
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0)
            
            # Run inference
            self.eval()
            with torch.no_grad():
                outputs = self(image_tensor)
                probabilities = outputs[0].numpy()
                
                # Get top prediction
                predicted_class = np.argmax(probabilities)
                confidence = float(probabilities[predicted_class])
                
                # Map to threat type
                threat_type = self.threat_mapping.get(predicted_class, ThreatType.UNKNOWN_THREAT)
                
                # Estimate severity based on confidence and threat type
                severity = self._estimate_severity(threat_type, confidence, probabilities)
                
                # Create detection result
                detection = ThreatDetection(
                    detection_id=f"pytorch_threat_{datetime.utcnow().timestamp()}",
                    threat_type=threat_type,
                    severity=severity,
                    severity_level=ThreatSeverity.HIGH,  # Auto-calculated
                    urgency=ThreatUrgency.URGENT,  # Auto-calculated
                    confidence=confidence,
                    image_path=image_path,
                    source="pytorch_threat_classifier",
                    evidence={
                        "classification_probabilities": probabilities.tolist(),
                        "top_3_predictions": self._get_top_predictions(probabilities, 3),
                        "visual_analysis": self._analyze_image_features(image)
                    },
                    metadata={
                        "model_type": "resnet34_threat_classifier",
                        "image_size": image.size,
                        "preprocessing": "imagenet_normalization",
                        "prediction_method": "cnn_classification"
                    }
                )
                
                return detection
                
        except Exception as e:
            print(f"⚠️  PyTorch threat prediction error: {e}")
            return None
    
    def _estimate_severity(self, threat_type: ThreatType, confidence: float, probabilities: np.ndarray) -> float:
        """Estimate threat severity based on multiple factors."""
        # Base severity from confidence
        base_severity = confidence
        
        # Threat-specific severity adjustments
        severity_multipliers = {
            ThreatType.POACHING: 1.2,
            ThreatType.ILLEGAL_LOGGING: 1.15,
            ThreatType.MINING: 1.1,
            ThreatType.SLASH_AND_BURN: 1.1,
            ThreatType.DEFORESTATION: 1.0,
            ThreatType.HUMAN_INTRUSION: 0.9,
            ThreatType.CATTLE_GRAZING: 0.8,
            ThreatType.INVASIVE_SPECIES: 0.7,
            ThreatType.CLIMATE_IMPACT: 0.6
        }
        
        multiplier = severity_multipliers.get(threat_type, 1.0)
        
        # Consider probability distribution (high entropy = uncertain = lower severity)
        entropy = -np.sum(probabilities * np.log(probabilities + 1e-8))
        entropy_factor = 1.0 - (entropy / np.log(len(probabilities))) * 0.3  # Reduce by up to 30%
        
        # Calculate final severity
        severity = base_severity * multiplier * entropy_factor
        
        # Clamp to [0, 1] range
        return max(0.0, min(1.0, severity))
    
    def _get_top_predictions(self, probabilities: np.ndarray, top_k: int = 3) -> List[Dict]:
        """Get top K threat predictions."""
        top_indices = np.argsort(probabilities)[::-1][:top_k]
        return [
            {
                "threat_type": self.threat_mapping[idx].value,
                "probability": float(probabilities[idx]),
                "severity_estimate": self._estimate_severity(self.threat_mapping[idx], probabilities[idx], probabilities)
            }
            for idx in top_indices
        ]
    
    def _analyze_image_features(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze image features for visual evidence."""
        try:
            # Convert to numpy array for analysis
            img_array = np.array(image)
            
            # Color analysis
            mean_rgb = np.mean(img_array, axis=(0, 1))
            
            # Texture analysis (simplified)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            texture_variance = np.var(gray)
            
            # Edge detection for structural analysis
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            
            return {
                "color_profile": {
                    "mean_red": float(mean_rgb[0]),
                    "mean_green": float(mean_rgb[1]),
                    "mean_blue": float(mean_rgb[2]),
                    "dominant_color": "green" if mean_rgb[1] > mean_rgb[0] and mean_rgb[1] > mean_rgb[2] else "brown"
                },
                "texture_analysis": {
                    "variance": float(texture_variance),
                    "complexity": "high" if texture_variance > 1000 else "low"
                },
                "structural_analysis": {
                    "edge_density": float(edge_density),
                    "structure_complexity": "high" if edge_density > 0.1 else "low"
                }
            }
            
        except Exception as e:
            print(f"⚠️  Image feature analysis error: {e}")
            return {"error": str(e)}

class ChangeDetectionModel:
    """Model for detecting environmental changes over time."""
    
    def __init__(self):
        self.change_thresholds = {
            "deforestation": 0.3,
            "vegetation_loss": 0.25,
            "infrastructure": 0.4,
            "water_change": 0.2
        }
    
    def detect_changes(self, image_before: str, image_after: str) -> Dict[str, Any]:
        """Detect changes between two images."""
        try:
            # Load images
            img_before = cv2.imread(image_before)
            img_after = cv2.imread(image_after)
            
            if img_before is None or img_after is None:
                raise ValueError("Could not load one or both images")
            
            # Resize images to same size
            height, width = img_before.shape[:2]
            img_after = cv2.resize(img_after, (width, height))
            
            # Convert to HSV for better vegetation analysis
            hsv_before = cv2.cvtColor(img_before, cv2.COLOR_BGR2HSV)
            hsv_after = cv2.cvtColor(img_after, cv2.COLOR_BGR2HSV)
            
            # Vegetation mask (green areas)
            vegetation_mask_before = self._create_vegetation_mask(hsv_before)
            vegetation_mask_after = self._create_vegetation_mask(hsv_after)
            
            # Calculate vegetation loss
            vegetation_before = np.sum(vegetation_mask_before) / vegetation_mask_before.size
            vegetation_after = np.sum(vegetation_mask_after) / vegetation_mask_after.size
            vegetation_change = vegetation_before - vegetation_after
            
            # Overall change detection
            diff_image = cv2.absdiff(img_before, img_after)
            change_magnitude = np.mean(diff_image) / 255.0
            
            # Analyze change type
            change_analysis = self._analyze_change_type(
                img_before, img_after, vegetation_change, change_magnitude
            )
            
            return {
                "change_detected": change_magnitude > 0.1,
                "change_magnitude": float(change_magnitude),
                "vegetation_change": float(vegetation_change),
                "vegetation_loss_percentage": float(vegetation_change * 100),
                "change_type": change_analysis["type"],
                "severity": change_analysis["severity"],
                "confidence": change_analysis["confidence"],
                "analysis": {
                    "vegetation_before": float(vegetation_before),
                    "vegetation_after": float(vegetation_after),
                    "affected_area_percentage": float(change_magnitude * 100)
                }
            }
            
        except Exception as e:
            print(f"⚠️  Change detection error: {e}")
            return {"error": str(e)}
    
    def _create_vegetation_mask(self, hsv_image: np.ndarray) -> np.ndarray:
        """Create mask for vegetation areas."""
        # Define HSV range for vegetation (green areas)
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([85, 255, 255])
        
        mask = cv2.inRange(hsv_image, lower_green, upper_green)
        return mask / 255.0  # Normalize to 0-1
    
    def _analyze_change_type(self, img_before: np.ndarray, img_after: np.ndarray, 
                           vegetation_change: float, change_magnitude: float) -> Dict[str, Any]:
        """Analyze type of change detected."""
        change_type = "unknown"
        severity = 0.0
        confidence = 0.0
        
        # Deforestation detection
        if vegetation_change > self.change_thresholds["deforestation"]:
            change_type = "deforestation"
            severity = min(1.0, vegetation_change / 0.5)  # Scale to 0-1
            confidence = 0.8 if vegetation_change > 0.4 else 0.6
        
        # Infrastructure development
        elif change_magnitude > self.change_thresholds["infrastructure"]:
            # Check for linear structures (roads, buildings)
            gray_before = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
            gray_after = cv2.cvtColor(img_after, cv2.COLOR_BGR2GRAY)
            
            edges_before = cv2.Canny(gray_before, 50, 150)
            edges_after = cv2.Canny(gray_after, 50, 150)
            
            edge_increase = (np.sum(edges_after) - np.sum(edges_before)) / edges_after.size
            
            if edge_increase > 0.1:
                change_type = "infrastructure_development"
                severity = min(1.0, edge_increase * 10)
                confidence = 0.7
            else:
                change_type = "vegetation_disturbance"
                severity = change_magnitude
                confidence = 0.5
        
        # Minor vegetation loss
        elif vegetation_change > self.change_thresholds["vegetation_loss"]:
            change_type = "vegetation_loss"
            severity = vegetation_change / 0.3
            confidence = 0.6
        
        # General disturbance
        elif change_magnitude > 0.1:
            change_type = "environmental_disturbance"
            severity = change_magnitude
            confidence = 0.4
        
        return {
            "type": change_type,
            "severity": float(severity),
            "confidence": float(confidence)
        }

class ThreatDetectionEnsemble:
    """Ensemble model combining multiple threat detection approaches."""
    
    def __init__(self):
        self.classification_model = ThreatClassificationModel(pretrained=False)  # Use untrained for testing
        self.change_detection_model = ChangeDetectionModel()
        self.ensemble_weights = {
            "classification": 0.7,
            "change_detection": 0.3
        }
    
    def predict_threat_ensemble(self, image_path: str, reference_image: str = None) -> ThreatDetection:
        """Predict threat using ensemble of models."""
        try:
            predictions = []
            
            # Get classification prediction
            classification_result = self.classification_model.predict_threat(image_path)
            if classification_result:
                predictions.append(("classification", classification_result))
            
            # Get change detection if reference image provided
            change_result = None
            if reference_image and os.path.exists(reference_image):
                change_analysis = self.change_detection_model.detect_changes(reference_image, image_path)
                
                if change_analysis.get("change_detected", False):
                    # Convert change analysis to threat detection
                    change_threat = self._change_to_threat(change_analysis, image_path)
                    if change_threat:
                        predictions.append(("change_detection", change_threat))
                        change_result = change_analysis
            
            if not predictions:
                return None
            
            # Combine predictions
            final_threat = self._combine_predictions(predictions, image_path)
            
            # Add ensemble metadata
            if final_threat:
                final_threat.metadata.update({
                    "ensemble_method": "weighted_combination",
                    "component_models": [pred[0] for pred in predictions],
                    "ensemble_weights": self.ensemble_weights,
                    "change_analysis": change_result
                })
            
            return final_threat
            
        except Exception as e:
            print(f"⚠️  Ensemble prediction error: {e}")
            return None
    
    def _change_to_threat(self, change_analysis: Dict[str, Any], image_path: str) -> ThreatDetection:
        """Convert change detection analysis to threat detection."""
        try:
            change_type = change_analysis.get("change_type", "unknown")
            
            # Map change types to threat types
            change_to_threat_mapping = {
                "deforestation": ThreatType.DEFORESTATION,
                "vegetation_loss": ThreatType.DEFORESTATION,
                "infrastructure_development": ThreatType.INFRASTRUCTURE_DEVELOPMENT,
                "vegetation_disturbance": ThreatType.CATTLE_GRAZING,
                "environmental_disturbance": ThreatType.UNKNOWN_THREAT
            }
            
            threat_type = change_to_threat_mapping.get(change_type, ThreatType.UNKNOWN_THREAT)
            severity = change_analysis.get("severity", 0.5)
            confidence = change_analysis.get("confidence", 0.5)
            
            detection = ThreatDetection(
                detection_id=f"change_detection_{datetime.utcnow().timestamp()}",
                threat_type=threat_type,
                severity=severity,
                severity_level=ThreatSeverity.MODERATE,  # Auto-calculated
                urgency=ThreatUrgency.ELEVATED,  # Auto-calculated
                confidence=confidence,
                image_path=image_path,
                source="change_detection_model",
                evidence={
                    "change_analysis": change_analysis,
                    "detection_method": "temporal_comparison"
                },
                metadata={
                    "model_type": "change_detection",
                    "change_type": change_type
                }
            )
            
            return detection
            
        except Exception as e:
            print(f"⚠️  Change to threat conversion error: {e}")
            return None
    
    def _combine_predictions(self, predictions: List[Tuple[str, ThreatDetection]], 
                           image_path: str) -> ThreatDetection:
        """Combine multiple threat predictions."""
        try:
            if len(predictions) == 1:
                return predictions[0][1]
            
            # Weighted combination of threats
            threat_scores = {}
            total_weight = 0
            
            for model_name, detection in predictions:
                weight = self.ensemble_weights.get(model_name, 1.0)
                threat_type = detection.threat_type
                confidence = detection.confidence
                severity = detection.severity
                
                if threat_type not in threat_scores:
                    threat_scores[threat_type] = {
                        "weighted_confidence": 0,
                        "weighted_severity": 0,
                        "total_weight": 0,
                        "detections": []
                    }
                
                threat_scores[threat_type]["weighted_confidence"] += weight * confidence
                threat_scores[threat_type]["weighted_severity"] += weight * severity
                threat_scores[threat_type]["total_weight"] += weight
                threat_scores[threat_type]["detections"].append((model_name, detection))
                total_weight += weight
            
            # Find best threat prediction
            best_threat = None
            best_score = 0
            
            for threat_type, scores in threat_scores.items():
                avg_confidence = scores["weighted_confidence"] / scores["total_weight"]
                avg_severity = scores["weighted_severity"] / scores["total_weight"]
                combined_score = avg_confidence * avg_severity
                
                if combined_score > best_score:
                    best_score = combined_score
                    best_threat = {
                        "threat_type": threat_type,
                        "confidence": avg_confidence,
                        "severity": avg_severity,
                        "detections": scores["detections"]
                    }
            
            if best_threat:
                # Create combined detection
                combined_detection = ThreatDetection(
                    detection_id=f"ensemble_threat_{datetime.utcnow().timestamp()}",
                    threat_type=best_threat["threat_type"],
                    severity=best_threat["severity"],
                    severity_level=ThreatSeverity.MODERATE,  # Auto-calculated
                    urgency=ThreatUrgency.ELEVATED,  # Auto-calculated
                    confidence=best_threat["confidence"],
                    image_path=image_path,
                    source="ensemble_threat_detector",
                    evidence={
                        "component_predictions": [
                            {
                                "model": model_name,
                                "threat_type": det.threat_type.value,
                                "confidence": det.confidence,
                                "severity": det.severity
                            }
                            for model_name, det in best_threat["detections"]
                        ]
                    },
                    metadata={
                        "model_type": "ensemble_threat_detector",
                        "combination_method": "weighted_voting",
                        "num_models": len(predictions)
                    }
                )
                
                return combined_detection
            
            return None
            
        except Exception as e:
            print(f"⚠️  Prediction combination error: {e}")
            return None

def test_threat_classification_model():
    """Test threat classification model."""
    print("🔥 Testing Threat Classification Model...")
    
    try:
        model = ThreatClassificationModel(num_threat_types=12, pretrained=False)
        
        # Test model architecture
        total_params = sum(p.numel() for p in model.parameters())
        print(f"✅ Threat classification model created")
        print(f"✅ Total parameters: {total_params:,}")
        print(f"✅ Threat mapping: {len(model.threat_mapping)} types")
        
        # Test threat type mapping
        for idx, threat_type in model.threat_mapping.items():
            if idx < 3:  # Show first 3
                print(f"✅ Index {idx}: {threat_type.value}")
        
        # Test image transform pipeline
        if model.transform:
            print("✅ Image transform pipeline configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Threat classification model error: {e}")
        return False

def test_change_detection_model():
    """Test change detection model."""
    print("\n📊 Testing Change Detection Model...")
    
    try:
        model = ChangeDetectionModel()
        
        # Test threshold configuration
        thresholds = model.change_thresholds
        print(f"✅ Change detection thresholds: {len(thresholds)} types")
        
        for change_type, threshold in thresholds.items():
            print(f"✅ {change_type}: threshold {threshold}")
        
        # Test with mock images
        test_image_before = "test_before.jpg"
        test_image_after = "test_after.jpg"
        
        # Create test images with slight differences
        img_before = Image.new('RGB', (400, 400), color='green')  # Forest
        img_after = Image.new('RGB', (400, 400), color='brown')   # Deforested
        
        img_before.save(test_image_before)
        img_after.save(test_image_after)
        
        # Test change detection
        change_result = model.detect_changes(test_image_before, test_image_after)
        
        if "error" not in change_result:
            print(f"✅ Change detection successful")
            print(f"✅ Change detected: {change_result['change_detected']}")
            print(f"✅ Change type: {change_result['change_type']}")
            print(f"✅ Vegetation loss: {change_result['vegetation_loss_percentage']:.1f}%")
            print(f"✅ Severity: {change_result['severity']:.2f}")
        else:
            print(f"❌ Change detection failed: {change_result['error']}")
            return False
        
        # Cleanup
        os.remove(test_image_before)
        os.remove(test_image_after)
        print("✅ Test images cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Change detection model error: {e}")
        return False

def test_threat_prediction_pipeline():
    """Test threat prediction pipeline."""
    print("\n🔍 Testing Threat Prediction Pipeline...")
    
    try:
        # Create test image
        test_image_path = "test_threat_prediction.jpg"
        test_image = Image.new('RGB', (224, 224), color='brown')  # Simulate deforestation
        test_image.save(test_image_path)
        
        # Test classification model prediction
        classification_model = ThreatClassificationModel(pretrained=False)
        threat_detection = classification_model.predict_threat(test_image_path)
        
        if threat_detection:
            print(f"✅ Threat prediction successful: {threat_detection.threat_type.value}")
            print(f"✅ Severity: {threat_detection.severity:.2f}")
            print(f"✅ Confidence: {threat_detection.confidence:.2f}")
            print(f"✅ Urgency: {threat_detection.urgency.value}")
            
            # Check evidence
            evidence = threat_detection.evidence
            if "classification_probabilities" in evidence:
                print("✅ Classification probabilities available")
            if "top_3_predictions" in evidence:
                top_predictions = evidence["top_3_predictions"]
                print(f"✅ Top 3 predictions: {len(top_predictions)} items")
            if "visual_analysis" in evidence:
                print("✅ Visual analysis available")
        else:
            print("❌ Threat prediction failed")
            return False
        
        # Cleanup
        os.remove(test_image_path)
        print("✅ Test image cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Threat prediction pipeline error: {e}")
        return False

def test_ensemble_threat_detection():
    """Test ensemble threat detection."""
    print("\n🔀 Testing Ensemble Threat Detection...")
    
    try:
        ensemble = ThreatDetectionEnsemble()
        
        # Test ensemble configuration
        weights = ensemble.ensemble_weights
        total_weight = sum(weights.values())
        print(f"✅ Ensemble weights: {weights}")
        print(f"✅ Total weight: {total_weight}")
        
        # Create test images
        test_image_path = "test_ensemble.jpg"
        reference_image_path = "test_reference.jpg"
        
        # Create images with different characteristics
        test_image = Image.new('RGB', (400, 400), color='brown')
        reference_image = Image.new('RGB', (400, 400), color='green')
        
        test_image.save(test_image_path)
        reference_image.save(reference_image_path)
        
        # Test ensemble prediction with change detection
        ensemble_detection = ensemble.predict_threat_ensemble(
            test_image_path, 
            reference_image_path
        )
        
        if ensemble_detection:
            print(f"✅ Ensemble prediction: {ensemble_detection.threat_type.value}")
            print(f"✅ Ensemble confidence: {ensemble_detection.confidence:.2f}")
            print(f"✅ Ensemble severity: {ensemble_detection.severity:.2f}")
            
            # Check ensemble metadata
            metadata = ensemble_detection.metadata
            if "component_models" in metadata:
                models_used = metadata["component_models"]
                print(f"✅ Component models: {models_used}")
            
            if "change_analysis" in metadata and metadata["change_analysis"]:
                print("✅ Change analysis included in ensemble")
        else:
            print("❌ Ensemble prediction failed")
            return False
        
        # Test ensemble with single image (no change detection)
        single_detection = ensemble.predict_threat_ensemble(test_image_path)
        
        if single_detection:
            print("✅ Single image ensemble prediction successful")
        else:
            print("⚠️  Single image ensemble prediction returned None (acceptable)")
        
        # Cleanup
        os.remove(test_image_path)
        os.remove(reference_image_path)
        print("✅ Test images cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Ensemble threat detection error: {e}")
        return False

def test_threat_severity_estimation():
    """Test threat severity estimation logic."""
    print("\n⚖️  Testing Threat Severity Estimation...")
    
    try:
        model = ThreatClassificationModel(pretrained=False)
        
        # Test severity estimation for different threat types
        test_scenarios = [
            (ThreatType.POACHING, 0.8, "should be amplified"),
            (ThreatType.CATTLE_GRAZING, 0.8, "should be reduced"),
            (ThreatType.MINING, 0.6, "should be amplified"),
            (ThreatType.INVASIVE_SPECIES, 0.6, "should be reduced")
        ]
        
        for threat_type, base_confidence, expectation in test_scenarios:
            # Create mock probability distribution
            probabilities = np.random.random(12)
            probabilities = probabilities / np.sum(probabilities)  # Normalize
            
            estimated_severity = model._estimate_severity(threat_type, base_confidence, probabilities)
            
            print(f"✅ {threat_type.value}: base {base_confidence:.2f} → severity {estimated_severity:.2f} ({expectation})")
            
            # Verify severity is in valid range
            if 0.0 <= estimated_severity <= 1.0:
                print(f"   ✅ Severity in valid range")
            else:
                print(f"   ❌ Severity out of range: {estimated_severity}")
                return False
        
        # Test entropy effect on severity
        # High entropy (uncertain) should reduce severity
        high_entropy_probs = np.ones(12) / 12  # Uniform distribution = high entropy
        low_entropy_probs = np.zeros(12)
        low_entropy_probs[0] = 1.0  # All probability on one class = low entropy
        
        high_entropy_severity = model._estimate_severity(ThreatType.DEFORESTATION, 0.8, high_entropy_probs)
        low_entropy_severity = model._estimate_severity(ThreatType.DEFORESTATION, 0.8, low_entropy_probs)
        
        if low_entropy_severity > high_entropy_severity:
            print("✅ Entropy effect working: low entropy > high entropy severity")
        else:
            print("❌ Entropy effect not working correctly")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Threat severity estimation error: {e}")
        return False

def test_visual_feature_analysis():
    """Test visual feature analysis capabilities."""
    print("\n👁️  Testing Visual Feature Analysis...")
    
    try:
        model = ThreatClassificationModel(pretrained=False)
        
        # Create test images with different characteristics
        test_images = [
            ("forest.jpg", Image.new('RGB', (224, 224), color='green')),
            ("deforested.jpg", Image.new('RGB', (224, 224), color='brown')),
            ("mixed.jpg", Image.new('RGB', (224, 224), color='yellow'))
        ]
        
        for image_name, image in test_images:
            image.save(image_name)
            
            # Analyze visual features
            features = model._analyze_image_features(image)
            
            if "error" not in features:
                print(f"✅ {image_name} analysis successful")
                
                # Check feature categories
                required_categories = ["color_profile", "texture_analysis", "structural_analysis"]
                for category in required_categories:
                    if category in features:
                        print(f"   ✅ {category} available")
                    else:
                        print(f"   ❌ {category} missing")
                        return False
                
                # Check color analysis
                color_profile = features["color_profile"]
                dominant_color = color_profile.get("dominant_color", "unknown")
                print(f"   • Dominant color: {dominant_color}")
                
                # Check texture analysis
                texture = features["texture_analysis"]
                complexity = texture.get("complexity", "unknown")
                print(f"   • Texture complexity: {complexity}")
                
            else:
                print(f"❌ {image_name} analysis failed: {features['error']}")
                return False
            
            # Cleanup
            os.remove(image_name)
        
        print("✅ Test images cleaned up")
        return True
        
    except Exception as e:
        print(f"❌ Visual feature analysis error: {e}")
        return False

def main():
    """Run Section 2 tests."""
    print("🔥 STEP 5 - SECTION 2: Threat Detection ML Models")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Threat classification model
    if test_threat_classification_model():
        tests_passed += 1
    
    # Test 2: Change detection model
    if test_change_detection_model():
        tests_passed += 1
    
    # Test 3: Threat prediction pipeline
    if test_threat_prediction_pipeline():
        tests_passed += 1
    
    # Test 4: Ensemble threat detection
    if test_ensemble_threat_detection():
        tests_passed += 1
    
    # Test 5: Threat severity estimation
    if test_threat_severity_estimation():
        tests_passed += 1
    
    # Test 6: Visual feature analysis
    if test_visual_feature_analysis():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Section 2 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 2 PASSED - Ready for Section 3")
        print("\n🎯 Next: Implement real-time threat monitoring and alert systems")
        return True
    else:
        print("❌ Section 2 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
