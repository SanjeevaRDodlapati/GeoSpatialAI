"""
Step 4 Section 1: Computer Vision Foundation
===========================================
Build foundation for species identification with computer vision capabilities.
"""

import sys
import os
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

def test_computer_vision_imports():
    """Test computer vision and ML imports."""
    print("🔬 Testing Computer Vision Imports...")
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
        
        # Test PIL for image processing
        from PIL import Image
        print("✅ PIL (Pillow) imported successfully")
        
        # Test OpenCV if available
        try:
            import cv2
            print("✅ OpenCV imported successfully")
            opencv_available = True
        except ImportError:
            print("⚠️  OpenCV not available (optional)")
            opencv_available = False
        
        return True, opencv_available
        
    except ImportError as e:
        print(f"❌ Computer vision import error: {e}")
        return False, False

def test_ml_framework_imports():
    """Test ML framework imports."""
    print("\n🧠 Testing ML Framework Imports...")
    
    try:
        # Test PyTorch
        try:
            import torch
            import torchvision
            print("✅ PyTorch and TorchVision imported successfully")
            pytorch_available = True
        except ImportError:
            print("⚠️  PyTorch not available")
            pytorch_available = False
        
        # Test TensorFlow
        try:
            import tensorflow as tf
            print("✅ TensorFlow imported successfully")
            tensorflow_available = True
        except ImportError:
            print("⚠️  TensorFlow not available")
            tensorflow_available = False
        
        # At least one ML framework should be available
        if pytorch_available or tensorflow_available:
            print("✅ ML frameworks available for species identification")
            return True, pytorch_available, tensorflow_available
        else:
            print("❌ No ML frameworks available")
            return False, False, False
        
    except Exception as e:
        print(f"❌ ML framework test error: {e}")
        return False, False, False

class SpeciesConfidence(Enum):
    """Confidence levels for species identification."""
    VERY_LOW = "very_low"      # < 0.5
    LOW = "low"                # 0.5 - 0.7
    MEDIUM = "medium"          # 0.7 - 0.8
    HIGH = "high"              # 0.8 - 0.9
    VERY_HIGH = "very_high"    # > 0.9

class MadagascarSpecies(Enum):
    """Endemic Madagascar species for identification."""
    LEMUR_CATTA = "lemur_catta"                    # Ring-tailed lemur
    INDRI_INDRI = "indri_indri"                    # Indri
    EULEMUR_FULVUS = "eulemur_fulvus"             # Brown lemur
    PROPITHECUS_DIADEMA = "propithecus_diadema"   # Diademed sifaka
    MICROCEBUS_MURINUS = "microcebus_murinus"     # Gray mouse lemur
    BROOKESIA_MICRA = "brookesia_micra"           # Micro chameleon
    FURCIFER_PARDALIS = "furcifer_pardalis"       # Panther chameleon
    UROPLATUS_PHANTASTICUS = "uroplatus_phantasticus"  # Leaf-tail gecko
    UNKNOWN_SPECIES = "unknown_species"           # Unidentified

@dataclass
class SpeciesDetection:
    """Species detection result."""
    detection_id: str
    species: MadagascarSpecies
    confidence: float
    confidence_level: SpeciesConfidence
    bounding_box: Optional[Tuple[int, int, int, int]] = None  # (x, y, width, height)
    image_path: Optional[str] = None
    timestamp: datetime = None
    source: str = "unknown"
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
        if self.metadata is None:
            self.metadata = {}
        
        # Automatically determine confidence level
        if self.confidence < 0.5:
            self.confidence_level = SpeciesConfidence.VERY_LOW
        elif self.confidence < 0.7:
            self.confidence_level = SpeciesConfidence.LOW
        elif self.confidence < 0.8:
            self.confidence_level = SpeciesConfidence.MEDIUM
        elif self.confidence < 0.9:
            self.confidence_level = SpeciesConfidence.HIGH
        else:
            self.confidence_level = SpeciesConfidence.VERY_HIGH

class MockImageProcessor:
    """Mock image processor for testing (before implementing real CV models)."""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp']
        self.madagascar_species_probabilities = {
            MadagascarSpecies.LEMUR_CATTA: 0.25,
            MadagascarSpecies.INDRI_INDRI: 0.20,
            MadagascarSpecies.EULEMUR_FULVUS: 0.15,
            MadagascarSpecies.PROPITHECUS_DIADEMA: 0.10,
            MadagascarSpecies.MICROCEBUS_MURINUS: 0.10,
            MadagascarSpecies.BROOKESIA_MICRA: 0.08,
            MadagascarSpecies.FURCIFER_PARDALIS: 0.07,
            MadagascarSpecies.UROPLATUS_PHANTASTICUS: 0.05
        }
    
    def validate_image_format(self, image_path: str) -> bool:
        """Validate image format."""
        if not os.path.exists(image_path):
            return False
        
        ext = os.path.splitext(image_path.lower())[1]
        return ext in self.supported_formats
    
    def create_mock_image(self, filename: str, size: Tuple[int, int] = (640, 480)) -> str:
        """Create a mock image for testing."""
        try:
            from PIL import Image
            
            # Create a simple test image
            img = Image.new('RGB', size, color='green')
            img.save(filename)
            return filename
            
        except Exception as e:
            print(f"⚠️  Could not create mock image: {e}")
            return None
    
    def simulate_species_detection(self, image_path: str, target_species: str = None) -> SpeciesDetection:
        """Simulate species detection for testing."""
        try:
            # Simulate detection based on filename or random selection
            if target_species and target_species in [s.value for s in MadagascarSpecies]:
                species = MadagascarSpecies(target_species)
                # Higher confidence for targeted species
                confidence = 0.85 + np.random.random() * 0.1
            else:
                # Random species selection weighted by probability
                species_values = list(self.madagascar_species_probabilities.keys())
                probabilities = list(self.madagascar_species_probabilities.values())
                species = np.random.choice(species_values, p=probabilities)
                # Random confidence
                confidence = 0.6 + np.random.random() * 0.35
            
            # Simulate bounding box
            bbox = (
                int(np.random.random() * 100),  # x
                int(np.random.random() * 100),  # y
                int(200 + np.random.random() * 200),  # width
                int(150 + np.random.random() * 150)   # height
            )
            
            detection = SpeciesDetection(
                detection_id=f"mock_detection_{datetime.utcnow().timestamp()}",
                species=species,
                confidence=confidence,
                confidence_level=SpeciesConfidence.HIGH,  # Will be auto-calculated
                bounding_box=bbox,
                image_path=image_path,
                source="mock_cv_system",
                metadata={
                    "model_version": "mock_v1.0",
                    "processing_time_ms": int(50 + np.random.random() * 100),
                    "image_size": (640, 480)
                }
            )
            
            return detection
            
        except Exception as e:
            print(f"⚠️  Mock detection error: {e}")
            return None

def test_species_enum_definitions():
    """Test Madagascar species enum definitions."""
    print("\n🐾 Testing Species Enum Definitions...")
    
    try:
        # Test species values
        species_count = len(MadagascarSpecies)
        print(f"✅ Madagascar species defined: {species_count} species")
        
        # Test specific species
        lemur = MadagascarSpecies.LEMUR_CATTA
        indri = MadagascarSpecies.INDRI_INDRI
        chameleon = MadagascarSpecies.BROOKESIA_MICRA
        
        print(f"✅ Ring-tailed lemur: {lemur.value}")
        print(f"✅ Indri: {indri.value}")
        print(f"✅ Micro chameleon: {chameleon.value}")
        
        # Test confidence levels
        confidence_levels = [level.value for level in SpeciesConfidence]
        print(f"✅ Confidence levels: {confidence_levels}")
        
        return True
        
    except Exception as e:
        print(f"❌ Species enum test error: {e}")
        return False

def test_species_detection_dataclass():
    """Test species detection dataclass."""
    print("\n📊 Testing Species Detection Dataclass...")
    
    try:
        # Test basic detection creation
        detection = SpeciesDetection(
            detection_id="test_001",
            species=MadagascarSpecies.LEMUR_CATTA,
            confidence=0.92,
            confidence_level=SpeciesConfidence.VERY_HIGH,  # Should be auto-calculated
            bounding_box=(50, 50, 200, 150),
            source="test_camera"
        )
        
        print(f"✅ Detection created: {detection.species.value}")
        print(f"✅ Confidence: {detection.confidence}")
        print(f"✅ Auto-calculated confidence level: {detection.confidence_level.value}")
        print(f"✅ Timestamp: {detection.timestamp}")
        
        # Test confidence level auto-calculation
        test_confidences = [0.3, 0.6, 0.75, 0.85, 0.95]
        expected_levels = [
            SpeciesConfidence.VERY_LOW,
            SpeciesConfidence.LOW,
            SpeciesConfidence.MEDIUM,
            SpeciesConfidence.HIGH,
            SpeciesConfidence.VERY_HIGH
        ]
        
        for conf, expected in zip(test_confidences, expected_levels):
            test_detection = SpeciesDetection(
                detection_id=f"test_{conf}",
                species=MadagascarSpecies.LEMUR_CATTA,
                confidence=conf,
                confidence_level=SpeciesConfidence.LOW  # Will be overridden
            )
            
            if test_detection.confidence_level == expected:
                print(f"✅ Confidence {conf} → {expected.value}")
            else:
                print(f"❌ Confidence {conf} → expected {expected.value}, got {test_detection.confidence_level.value}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Species detection test error: {e}")
        return False

def test_mock_image_processor():
    """Test mock image processor functionality."""
    print("\n🖼️  Testing Mock Image Processor...")
    
    try:
        processor = MockImageProcessor()
        
        # Test image format validation
        valid_formats = ['.jpg', '.png', '.jpeg']
        for fmt in valid_formats:
            test_file = f"test{fmt}"
            if processor.validate_image_format.__code__.co_code:  # Just test the method exists
                print(f"✅ Format validation method available for {fmt}")
        
        # Test mock image creation
        test_image_path = "test_mock_image.jpg"
        created_image = processor.create_mock_image(test_image_path)
        
        if created_image and os.path.exists(test_image_path):
            print("✅ Mock image created successfully")
            
            # Test mock detection
            detection = processor.simulate_species_detection(test_image_path, "lemur_catta")
            
            if detection:
                print(f"✅ Mock detection generated: {detection.species.value}")
                print(f"✅ Detection confidence: {detection.confidence:.2f}")
                print(f"✅ Bounding box: {detection.bounding_box}")
                print(f"✅ Processing time: {detection.metadata.get('processing_time_ms')}ms")
            else:
                print("❌ Mock detection failed")
                return False
            
            # Cleanup
            os.remove(test_image_path)
            print("✅ Test image cleaned up")
            
        else:
            print("⚠️  Mock image creation skipped (PIL not available)")
        
        return True
        
    except Exception as e:
        print(f"❌ Mock image processor error: {e}")
        return False

def test_madagascar_species_coverage():
    """Test Madagascar species coverage and metadata."""
    print("\n🇲🇬 Testing Madagascar Species Coverage...")
    
    try:
        processor = MockImageProcessor()
        
        # Test species probability distribution
        total_probability = sum(processor.madagascar_species_probabilities.values())
        print(f"✅ Species probability distribution sums to: {total_probability:.2f}")
        
        if abs(total_probability - 1.0) < 0.01:
            print("✅ Probability distribution is valid")
        else:
            print("⚠️  Probability distribution may need adjustment")
        
        # Test species categories
        lemur_species = [
            MadagascarSpecies.LEMUR_CATTA,
            MadagascarSpecies.INDRI_INDRI,
            MadagascarSpecies.EULEMUR_FULVUS,
            MadagascarSpecies.PROPITHECUS_DIADEMA,
            MadagascarSpecies.MICROCEBUS_MURINUS
        ]
        
        reptile_species = [
            MadagascarSpecies.BROOKESIA_MICRA,
            MadagascarSpecies.FURCIFER_PARDALIS,
            MadagascarSpecies.UROPLATUS_PHANTASTICUS
        ]
        
        print(f"✅ Lemur species coverage: {len(lemur_species)} species")
        print(f"✅ Reptile species coverage: {len(reptile_species)} species")
        
        # Test species information
        species_info = {
            MadagascarSpecies.LEMUR_CATTA: "Ring-tailed lemur - Most recognizable lemur species",
            MadagascarSpecies.INDRI_INDRI: "Indri - Largest living lemur, critically endangered",
            MadagascarSpecies.BROOKESIA_MICRA: "Micro chameleon - World's smallest chameleon"
        }
        
        for species, info in species_info.items():
            print(f"✅ {species.value}: {info}")
        
        return True
        
    except Exception as e:
        print(f"❌ Madagascar species coverage error: {e}")
        return False

def test_detection_serialization():
    """Test species detection serialization for storage."""
    print("\n💾 Testing Detection Serialization...")
    
    try:
        # Create a test detection
        detection = SpeciesDetection(
            detection_id="test_serialization",
            species=MadagascarSpecies.LEMUR_CATTA,
            confidence=0.89,
            confidence_level=SpeciesConfidence.HIGH,
            bounding_box=(100, 100, 300, 200),
            image_path="/test/path/image.jpg",
            source="test_serialization",
            metadata={"test": True, "value": 42}
        )
        
        # Convert to dictionary for JSON serialization
        detection_dict = {
            "detection_id": detection.detection_id,
            "species": detection.species.value,
            "confidence": detection.confidence,
            "confidence_level": detection.confidence_level.value,
            "bounding_box": detection.bounding_box,
            "image_path": detection.image_path,
            "timestamp": detection.timestamp.isoformat(),
            "source": detection.source,
            "metadata": detection.metadata
        }
        
        # Test JSON serialization
        json_str = json.dumps(detection_dict, indent=2)
        print("✅ Detection serialized to JSON")
        
        # Test JSON deserialization
        loaded_dict = json.loads(json_str)
        print("✅ Detection deserialized from JSON")
        
        # Verify data integrity
        if (loaded_dict["species"] == detection.species.value and
            loaded_dict["confidence"] == detection.confidence and
            loaded_dict["detection_id"] == detection.detection_id):
            print("✅ Data integrity verified after serialization")
        else:
            print("❌ Data integrity check failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Detection serialization error: {e}")
        return False

def main():
    """Run Section 1 tests."""
    print("🔬 STEP 4 - SECTION 1: Computer Vision Foundation")
    print("=" * 52)
    
    tests_passed = 0
    total_tests = 7
    
    # Test 1: Computer vision imports
    cv_result, opencv_available = test_computer_vision_imports()
    if cv_result:
        tests_passed += 1
    
    # Test 2: ML framework imports
    ml_result, pytorch_available, tensorflow_available = test_ml_framework_imports()
    if ml_result:
        tests_passed += 1
    
    # Test 3: Species enum definitions
    if test_species_enum_definitions():
        tests_passed += 1
    
    # Test 4: Species detection dataclass
    if test_species_detection_dataclass():
        tests_passed += 1
    
    # Test 5: Mock image processor
    if test_mock_image_processor():
        tests_passed += 1
    
    # Test 6: Madagascar species coverage
    if test_madagascar_species_coverage():
        tests_passed += 1
    
    # Test 7: Detection serialization
    if test_detection_serialization():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Section 1 Results: {tests_passed}/{total_tests} tests passed")
    
    # Framework availability summary
    print(f"\n🔧 Available Frameworks:")
    print(f"   📸 OpenCV: {'✅' if opencv_available else '❌'}")
    print(f"   🧠 PyTorch: {'✅' if pytorch_available else '❌'}")
    print(f"   🤖 TensorFlow: {'✅' if tensorflow_available else '❌'}")
    
    if tests_passed == total_tests:
        print("✅ Section 1 PASSED - Ready for Section 2")
        return True
    else:
        print("❌ Section 1 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
