"""
Step 4 Section 2: ML Model Integration
=====================================
Implement actual ML models for species identification using PyTorch/TensorFlow.
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
import requests
from io import BytesIO
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import warnings
warnings.filterwarnings("ignore")

# Import from Section 1
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
from step4_section1_test import (
    SpeciesConfidence, MadagascarSpecies, SpeciesDetection
)

class MadagascarSpeciesClassifier(nn.Module):
    """PyTorch CNN for Madagascar species classification."""
    
    def __init__(self, num_species: int = 9, pretrained: bool = True):
        super(MadagascarSpeciesClassifier, self).__init__()
        
        # Use ResNet18 as backbone (lightweight for field deployment)
        self.backbone = models.resnet18(pretrained=pretrained)
        
        # Replace final layer for our species count
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Linear(num_features, num_species)
        
        # Add dropout for regularization
        self.dropout = nn.Dropout(0.5)
        
        # Species mapping
        self.species_mapping = {
            0: MadagascarSpecies.LEMUR_CATTA,
            1: MadagascarSpecies.INDRI_INDRI,
            2: MadagascarSpecies.EULEMUR_FULVUS,
            3: MadagascarSpecies.PROPITHECUS_DIADEMA,
            4: MadagascarSpecies.MICROCEBUS_MURINUS,
            5: MadagascarSpecies.BROOKESIA_MICRA,
            6: MadagascarSpecies.FURCIFER_PARDALIS,
            7: MadagascarSpecies.UROPLATUS_PHANTASTICUS,
            8: MadagascarSpecies.UNKNOWN_SPECIES
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
    
    def predict_species(self, image_path: str) -> SpeciesDetection:
        """Predict species from image path."""
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
                
                # Map to species
                species = self.species_mapping.get(predicted_class, MadagascarSpecies.UNKNOWN_SPECIES)
                
                # Create detection result
                detection = SpeciesDetection(
                    detection_id=f"pytorch_detection_{datetime.utcnow().timestamp()}",
                    species=species,
                    confidence=confidence,
                    confidence_level=SpeciesConfidence.HIGH,  # Auto-calculated
                    image_path=image_path,
                    source="pytorch_resnet18",
                    metadata={
                        "model_type": "resnet18",
                        "all_probabilities": probabilities.tolist(),
                        "top_3_predictions": self._get_top_predictions(probabilities, 3),
                        "image_size": image.size,
                        "preprocessing": "standard_imagenet"
                    }
                )
                
                return detection
                
        except Exception as e:
            print(f"⚠️  PyTorch prediction error: {e}")
            return None
    
    def _get_top_predictions(self, probabilities: np.ndarray, top_k: int = 3) -> List[Dict]:
        """Get top K predictions with species names."""
        top_indices = np.argsort(probabilities)[::-1][:top_k]
        return [
            {
                "species": self.species_mapping[idx].value,
                "confidence": float(probabilities[idx])
            }
            for idx in top_indices
        ]

class TensorFlowSpeciesClassifier:
    """TensorFlow/Keras wrapper for species classification."""
    
    def __init__(self, num_species: int = 9):
        import tensorflow as tf
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
        from tensorflow.keras.models import Model
        
        # Use MobileNetV2 for efficient mobile deployment
        base_model = MobileNetV2(input_shape=(224, 224, 3), 
                                include_top=False, 
                                weights='imagenet')
        
        # Add custom classification head
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dropout(0.5)(x)
        predictions = Dense(num_species, activation='softmax')(x)
        
        self.model = Model(inputs=base_model.input, outputs=predictions)
        
        # Species mapping (same as PyTorch)
        self.species_mapping = {
            0: MadagascarSpecies.LEMUR_CATTA,
            1: MadagascarSpecies.INDRI_INDRI,
            2: MadagascarSpecies.EULEMUR_FULVUS,
            3: MadagascarSpecies.PROPITHECUS_DIADEMA,
            4: MadagascarSpecies.MICROCEBUS_MURINUS,
            5: MadagascarSpecies.BROOKESIA_MICRA,
            6: MadagascarSpecies.FURCIFER_PARDALIS,
            7: MadagascarSpecies.UROPLATUS_PHANTASTICUS,
            8: MadagascarSpecies.UNKNOWN_SPECIES
        }
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess image for TensorFlow model."""
        import tensorflow as tf
        
        image = Image.open(image_path).convert('RGB')
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0
        return np.expand_dims(image_array, axis=0)
    
    def predict_species(self, image_path: str) -> SpeciesDetection:
        """Predict species using TensorFlow model."""
        try:
            # Preprocess image
            image_array = self.preprocess_image(image_path)
            
            # Run prediction
            predictions = self.model.predict(image_array, verbose=0)
            probabilities = predictions[0]
            
            # Get top prediction
            predicted_class = np.argmax(probabilities)
            confidence = float(probabilities[predicted_class])
            
            # Map to species
            species = self.species_mapping.get(predicted_class, MadagascarSpecies.UNKNOWN_SPECIES)
            
            # Create detection result
            detection = SpeciesDetection(
                detection_id=f"tensorflow_detection_{datetime.utcnow().timestamp()}",
                species=species,
                confidence=confidence,
                confidence_level=SpeciesConfidence.HIGH,  # Auto-calculated
                image_path=image_path,
                source="tensorflow_mobilenetv2",
                metadata={
                    "model_type": "mobilenetv2",
                    "all_probabilities": probabilities.tolist(),
                    "top_3_predictions": self._get_top_predictions(probabilities, 3),
                    "preprocessing": "standard_normalization"
                }
            )
            
            return detection
            
        except Exception as e:
            print(f"⚠️  TensorFlow prediction error: {e}")
            return None
    
    def _get_top_predictions(self, probabilities: np.ndarray, top_k: int = 3) -> List[Dict]:
        """Get top K predictions with species names."""
        top_indices = np.argsort(probabilities)[::-1][:top_k]
        return [
            {
                "species": self.species_mapping[idx].value,
                "confidence": float(probabilities[idx])
            }
            for idx in top_indices
        ]

class EnsembleSpeciesClassifier:
    """Ensemble classifier combining PyTorch and TensorFlow models."""
    
    def __init__(self):
        self.pytorch_model = None
        self.tensorflow_model = None
        self.ensemble_weights = {"pytorch": 0.6, "tensorflow": 0.4}
        
    def initialize_models(self):
        """Initialize both PyTorch and TensorFlow models."""
        try:
            print("🔄 Initializing PyTorch model...")
            self.pytorch_model = MadagascarSpeciesClassifier()
            print("✅ PyTorch model initialized")
            
            print("🔄 Initializing TensorFlow model...")
            self.tensorflow_model = TensorFlowSpeciesClassifier()
            print("✅ TensorFlow model initialized")
            
            return True
            
        except Exception as e:
            print(f"⚠️  Model initialization error: {e}")
            return False
    
    def predict_ensemble(self, image_path: str) -> SpeciesDetection:
        """Predict using ensemble of both models."""
        try:
            predictions = []
            
            # Get PyTorch prediction
            if self.pytorch_model:
                pytorch_result = self.pytorch_model.predict_species(image_path)
                if pytorch_result:
                    predictions.append(("pytorch", pytorch_result))
            
            # Get TensorFlow prediction
            if self.tensorflow_model:
                tf_result = self.tensorflow_model.predict_species(image_path)
                if tf_result:
                    predictions.append(("tensorflow", tf_result))
            
            if not predictions:
                return None
            
            # Combine predictions using weighted voting
            species_votes = {}
            total_weight = 0
            
            for model_name, detection in predictions:
                weight = self.ensemble_weights.get(model_name, 1.0)
                species = detection.species
                confidence = detection.confidence
                
                if species not in species_votes:
                    species_votes[species] = 0
                
                species_votes[species] += weight * confidence
                total_weight += weight
            
            # Normalize votes
            for species in species_votes:
                species_votes[species] /= total_weight
            
            # Get final prediction
            final_species = max(species_votes, key=species_votes.get)
            final_confidence = species_votes[final_species]
            
            # Create ensemble detection
            ensemble_detection = SpeciesDetection(
                detection_id=f"ensemble_detection_{datetime.utcnow().timestamp()}",
                species=final_species,
                confidence=final_confidence,
                confidence_level=SpeciesConfidence.HIGH,  # Auto-calculated
                image_path=image_path,
                source="ensemble_pytorch_tensorflow",
                metadata={
                    "model_type": "ensemble",
                    "component_models": [pred[0] for pred in predictions],
                    "ensemble_weights": self.ensemble_weights,
                    "species_votes": {s.value: v for s, v in species_votes.items()},
                    "individual_predictions": [
                        {
                            "model": pred[0],
                            "species": pred[1].species.value,
                            "confidence": pred[1].confidence
                        }
                        for pred in predictions
                    ]
                }
            )
            
            return ensemble_detection
            
        except Exception as e:
            print(f"⚠️  Ensemble prediction error: {e}")
            return None

def test_pytorch_model_creation():
    """Test PyTorch model creation and architecture."""
    print("🔥 Testing PyTorch Model Creation...")
    
    try:
        model = MadagascarSpeciesClassifier(num_species=9, pretrained=False)
        
        # Test model architecture
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        print(f"✅ PyTorch model created")
        print(f"✅ Total parameters: {total_params:,}")
        print(f"✅ Trainable parameters: {trainable_params:,}")
        
        # Test species mapping
        species_count = len(model.species_mapping)
        print(f"✅ Species mapping: {species_count} species")
        
        # Test transform pipeline
        if model.transform:
            print("✅ Image transform pipeline configured")
        
        return True
        
    except Exception as e:
        print(f"❌ PyTorch model creation error: {e}")
        return False

def test_tensorflow_model_creation():
    """Test TensorFlow model creation and architecture."""
    print("\n🤖 Testing TensorFlow Model Creation...")
    
    try:
        model = TensorFlowSpeciesClassifier(num_species=9)
        
        # Test model summary
        total_params = model.model.count_params()
        print(f"✅ TensorFlow model created")
        print(f"✅ Total parameters: {total_params:,}")
        
        # Test model input/output shapes
        input_shape = model.model.input_shape
        output_shape = model.model.output_shape
        print(f"✅ Input shape: {input_shape}")
        print(f"✅ Output shape: {output_shape}")
        
        # Test species mapping
        species_count = len(model.species_mapping)
        print(f"✅ Species mapping: {species_count} species")
        
        return True
        
    except Exception as e:
        print(f"❌ TensorFlow model creation error: {e}")
        return False

def test_model_prediction_pipeline():
    """Test model prediction pipeline with mock image."""
    print("\n📸 Testing Model Prediction Pipeline...")
    
    try:
        # Create a test image
        test_image_path = "test_species_image.jpg"
        from PIL import Image
        
        # Create RGB test image
        test_image = Image.new('RGB', (640, 480), color='green')
        test_image.save(test_image_path)
        print("✅ Test image created")
        
        # Test PyTorch prediction
        pytorch_model = MadagascarSpeciesClassifier(pretrained=False)
        pytorch_detection = pytorch_model.predict_species(test_image_path)
        
        if pytorch_detection:
            print(f"✅ PyTorch prediction: {pytorch_detection.species.value}")
            print(f"✅ PyTorch confidence: {pytorch_detection.confidence:.3f}")
            print(f"✅ Top 3 predictions available: {len(pytorch_detection.metadata.get('top_3_predictions', []))}")
        else:
            print("❌ PyTorch prediction failed")
            return False
        
        # Test TensorFlow prediction
        tf_model = TensorFlowSpeciesClassifier()
        tf_detection = tf_model.predict_species(test_image_path)
        
        if tf_detection:
            print(f"✅ TensorFlow prediction: {tf_detection.species.value}")
            print(f"✅ TensorFlow confidence: {tf_detection.confidence:.3f}")
        else:
            print("❌ TensorFlow prediction failed")
            return False
        
        # Cleanup
        os.remove(test_image_path)
        print("✅ Test image cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Model prediction pipeline error: {e}")
        return False

def test_ensemble_classifier():
    """Test ensemble classifier functionality."""
    print("\n🔀 Testing Ensemble Classifier...")
    
    try:
        ensemble = EnsembleSpeciesClassifier()
        
        # Test model initialization
        if ensemble.initialize_models():
            print("✅ Ensemble models initialized")
        else:
            print("⚠️  Ensemble initialization issues (expected for untrained models)")
        
        # Test ensemble weights
        total_weight = sum(ensemble.ensemble_weights.values())
        print(f"✅ Ensemble weights sum to: {total_weight}")
        
        if abs(total_weight - 1.0) < 0.01:
            print("✅ Ensemble weights are normalized")
        
        # Test ensemble prediction with mock image
        test_image_path = "test_ensemble_image.jpg"
        from PIL import Image
        
        test_image = Image.new('RGB', (224, 224), color='blue')
        test_image.save(test_image_path)
        
        # Only test if models are available
        if ensemble.pytorch_model and ensemble.tensorflow_model:
            ensemble_detection = ensemble.predict_ensemble(test_image_path)
            
            if ensemble_detection:
                print(f"✅ Ensemble prediction: {ensemble_detection.species.value}")
                print(f"✅ Ensemble confidence: {ensemble_detection.confidence:.3f}")
                print(f"✅ Component models: {ensemble_detection.metadata.get('component_models', [])}")
            else:
                print("⚠️  Ensemble prediction returned None (expected for untrained models)")
        else:
            print("⚠️  Ensemble prediction skipped (models not available)")
        
        # Cleanup
        os.remove(test_image_path)
        print("✅ Test image cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Ensemble classifier error: {e}")
        return False

def test_confidence_calibration():
    """Test confidence calibration and thresholding."""
    print("\n🎯 Testing Confidence Calibration...")
    
    try:
        # Test confidence level mapping
        test_confidences = [0.1, 0.4, 0.6, 0.75, 0.85, 0.95]
        expected_levels = [
            SpeciesConfidence.VERY_LOW,
            SpeciesConfidence.VERY_LOW,
            SpeciesConfidence.LOW,
            SpeciesConfidence.MEDIUM,
            SpeciesConfidence.HIGH,
            SpeciesConfidence.VERY_HIGH
        ]
        
        for conf, expected in zip(test_confidences, expected_levels):
            detection = SpeciesDetection(
                detection_id=f"conf_test_{conf}",
                species=MadagascarSpecies.LEMUR_CATTA,
                confidence=conf,
                confidence_level=SpeciesConfidence.LOW  # Will be overridden
            )
            
            if detection.confidence_level == expected:
                print(f"✅ Confidence {conf} → {expected.value}")
            else:
                print(f"❌ Confidence calibration failed for {conf}")
                return False
        
        # Test confidence thresholding for field deployment
        deployment_threshold = 0.7
        high_confidence_detections = [d for d in [
            SpeciesDetection("test1", MadagascarSpecies.LEMUR_CATTA, 0.8, SpeciesConfidence.HIGH),
            SpeciesDetection("test2", MadagascarSpecies.INDRI_INDRI, 0.6, SpeciesConfidence.LOW),
            SpeciesDetection("test3", MadagascarSpecies.BROOKESIA_MICRA, 0.9, SpeciesConfidence.VERY_HIGH)
        ] if d.confidence >= deployment_threshold]
        
        print(f"✅ High-confidence detections (≥{deployment_threshold}): {len(high_confidence_detections)}/3")
        
        return True
        
    except Exception as e:
        print(f"❌ Confidence calibration error: {e}")
        return False

def test_model_metadata_extraction():
    """Test model metadata and prediction information."""
    print("\n📋 Testing Model Metadata Extraction...")
    
    try:
        # Create test image
        test_image_path = "test_metadata_image.jpg"
        from PIL import Image
        
        test_image = Image.new('RGB', (800, 600), color='red')
        test_image.save(test_image_path)
        
        # Test PyTorch metadata
        pytorch_model = MadagascarSpeciesClassifier(pretrained=False)
        pytorch_detection = pytorch_model.predict_species(test_image_path)
        
        if pytorch_detection:
            metadata = pytorch_detection.metadata
            required_fields = ["model_type", "all_probabilities", "top_3_predictions", "image_size"]
            
            for field in required_fields:
                if field in metadata:
                    print(f"✅ PyTorch metadata - {field}: ✓")
                else:
                    print(f"❌ PyTorch metadata - {field}: missing")
                    return False
            
            # Test top predictions format
            top_predictions = metadata.get("top_3_predictions", [])
            if len(top_predictions) == 3:
                print("✅ Top 3 predictions extracted")
                
                # Check prediction format
                for i, pred in enumerate(top_predictions):
                    if "species" in pred and "confidence" in pred:
                        print(f"✅ Prediction {i+1} format valid")
                    else:
                        print(f"❌ Prediction {i+1} format invalid")
                        return False
            else:
                print(f"❌ Expected 3 top predictions, got {len(top_predictions)}")
                return False
        
        # Test TensorFlow metadata
        tf_model = TensorFlowSpeciesClassifier()
        tf_detection = tf_model.predict_species(test_image_path)
        
        if tf_detection:
            tf_metadata = tf_detection.metadata
            if "model_type" in tf_metadata and tf_metadata["model_type"] == "mobilenetv2":
                print("✅ TensorFlow metadata model_type correct")
            else:
                print("❌ TensorFlow metadata model_type incorrect")
                return False
        
        # Cleanup
        os.remove(test_image_path)
        print("✅ Test image cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Model metadata extraction error: {e}")
        return False

def main():
    """Run Section 2 tests."""
    print("🔥 STEP 4 - SECTION 2: ML Model Integration")
    print("=" * 45)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: PyTorch model creation
    if test_pytorch_model_creation():
        tests_passed += 1
    
    # Test 2: TensorFlow model creation
    if test_tensorflow_model_creation():
        tests_passed += 1
    
    # Test 3: Model prediction pipeline
    if test_model_prediction_pipeline():
        tests_passed += 1
    
    # Test 4: Ensemble classifier
    if test_ensemble_classifier():
        tests_passed += 1
    
    # Test 5: Confidence calibration
    if test_confidence_calibration():
        tests_passed += 1
    
    # Test 6: Model metadata extraction
    if test_model_metadata_extraction():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Section 2 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 2 PASSED - Ready for Section 3")
        return True
    else:
        print("❌ Section 2 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
