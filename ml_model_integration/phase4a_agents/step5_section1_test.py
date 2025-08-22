"""
Step 5 Section 1: Threat Detection Foundation
============================================
Build foundation for threat detection with computer vision and ML capabilities.
"""

import sys
import os
import json
import numpy as np
import cv2
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from PIL import Image

# Import from previous steps
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
from step4_section1_test import SpeciesConfidence, MadagascarSpecies

class ThreatType(Enum):
    """Types of conservation threats in Madagascar."""
    DEFORESTATION = "deforestation"
    ILLEGAL_LOGGING = "illegal_logging"
    POACHING = "poaching"
    HUMAN_INTRUSION = "human_intrusion"
    MINING = "mining"
    SLASH_AND_BURN = "slash_and_burn"
    CHARCOAL_PRODUCTION = "charcoal_production"
    CATTLE_GRAZING = "cattle_grazing"
    INFRASTRUCTURE_DEVELOPMENT = "infrastructure_development"
    CLIMATE_IMPACT = "climate_impact"
    INVASIVE_SPECIES = "invasive_species"
    UNKNOWN_THREAT = "unknown_threat"

class ThreatSeverity(Enum):
    """Threat severity levels."""
    MINIMAL = "minimal"      # 0.0 - 0.2
    LOW = "low"             # 0.2 - 0.4
    MODERATE = "moderate"    # 0.4 - 0.6
    HIGH = "high"           # 0.6 - 0.8
    CRITICAL = "critical"   # 0.8 - 1.0

class ThreatUrgency(Enum):
    """Response urgency levels."""
    ROUTINE = "routine"           # Regular monitoring
    ELEVATED = "elevated"         # Increased surveillance
    URGENT = "urgent"             # Immediate investigation
    EMERGENCY = "emergency"       # Immediate intervention
    CRISIS = "crisis"             # Emergency response

@dataclass
class ThreatDetection:
    """Threat detection result."""
    detection_id: str
    threat_type: ThreatType
    severity: float  # 0.0 to 1.0
    severity_level: ThreatSeverity
    urgency: ThreatUrgency
    confidence: float
    location: Optional[Tuple[float, float]] = None  # (lat, lon)
    timestamp: datetime = None
    image_path: Optional[str] = None
    bounding_box: Optional[Tuple[int, int, int, int]] = None  # (x, y, w, h)
    source: str = "unknown"
    evidence: Dict[str, Any] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
        if self.evidence is None:
            self.evidence = {}
        if self.metadata is None:
            self.metadata = {}
        
        # Auto-calculate severity level
        if self.severity < 0.2:
            self.severity_level = ThreatSeverity.MINIMAL
        elif self.severity < 0.4:
            self.severity_level = ThreatSeverity.LOW
        elif self.severity < 0.6:
            self.severity_level = ThreatSeverity.MODERATE
        elif self.severity < 0.8:
            self.severity_level = ThreatSeverity.HIGH
        else:
            self.severity_level = ThreatSeverity.CRITICAL
        
        # Auto-calculate urgency based on threat type and severity
        self._calculate_urgency()
    
    def _calculate_urgency(self):
        """Calculate response urgency based on threat type and severity."""
        # High-urgency threat types
        high_urgency_threats = {
            ThreatType.POACHING,
            ThreatType.ILLEGAL_LOGGING,
            ThreatType.SLASH_AND_BURN,
            ThreatType.MINING
        }
        
        # Medium-urgency threat types
        medium_urgency_threats = {
            ThreatType.DEFORESTATION,
            ThreatType.HUMAN_INTRUSION,
            ThreatType.CHARCOAL_PRODUCTION,
            ThreatType.INFRASTRUCTURE_DEVELOPMENT
        }
        
        if self.threat_type in high_urgency_threats:
            if self.severity >= 0.8:
                self.urgency = ThreatUrgency.CRISIS
            elif self.severity >= 0.6:
                self.urgency = ThreatUrgency.EMERGENCY
            elif self.severity >= 0.4:
                self.urgency = ThreatUrgency.URGENT
            else:
                self.urgency = ThreatUrgency.ELEVATED
        elif self.threat_type in medium_urgency_threats:
            if self.severity >= 0.8:
                self.urgency = ThreatUrgency.EMERGENCY
            elif self.severity >= 0.6:
                self.urgency = ThreatUrgency.URGENT
            elif self.severity >= 0.4:
                self.urgency = ThreatUrgency.ELEVATED
            else:
                self.urgency = ThreatUrgency.ROUTINE
        else:
            # Low-urgency threats
            if self.severity >= 0.8:
                self.urgency = ThreatUrgency.URGENT
            elif self.severity >= 0.6:
                self.urgency = ThreatUrgency.ELEVATED
            else:
                self.urgency = ThreatUrgency.ROUTINE

class MockThreatDetector:
    """Mock threat detector for testing basic functionality."""
    
    def __init__(self):
        self.threat_indicators = {
            # Deforestation indicators
            "deforestation": {
                "keywords": ["cleared", "cut", "logged", "bare", "stumps"],
                "color_patterns": ["brown", "bare_soil"],
                "probability": 0.7
            },
            
            # Human activity indicators
            "human_activity": {
                "keywords": ["people", "vehicles", "structures", "smoke"],
                "color_patterns": ["smoke_gray", "vehicle_colors"],
                "probability": 0.6
            },
            
            # Fire/burning indicators
            "fire_activity": {
                "keywords": ["fire", "smoke", "burning", "ash"],
                "color_patterns": ["smoke_gray", "fire_orange"],
                "probability": 0.8
            }
        }
        
        # Madagascar-specific threat patterns
        self.madagascar_threats = {
            ThreatType.DEFORESTATION: {"base_probability": 0.3, "severity_range": (0.4, 0.9)},
            ThreatType.ILLEGAL_LOGGING: {"base_probability": 0.2, "severity_range": (0.5, 0.95)},
            ThreatType.SLASH_AND_BURN: {"base_probability": 0.25, "severity_range": (0.6, 0.9)},
            ThreatType.CHARCOAL_PRODUCTION: {"base_probability": 0.15, "severity_range": (0.4, 0.8)},
            ThreatType.CATTLE_GRAZING: {"base_probability": 0.2, "severity_range": (0.3, 0.7)},
            ThreatType.HUMAN_INTRUSION: {"base_probability": 0.1, "severity_range": (0.3, 0.85)},
            ThreatType.MINING: {"base_probability": 0.05, "severity_range": (0.7, 0.95)},
            ThreatType.INVASIVE_SPECIES: {"base_probability": 0.1, "severity_range": (0.2, 0.6)}
        }
    
    def simulate_threat_detection(self, image_path: str, target_threat: str = None) -> ThreatDetection:
        """Simulate threat detection for testing."""
        try:
            # Select threat type
            if target_threat and target_threat in [t.value for t in ThreatType]:
                threat_type = ThreatType(target_threat)
            else:
                # Weighted random selection
                threat_weights = [info["base_probability"] for info in self.madagascar_threats.values()]
                threat_types = list(self.madagascar_threats.keys())
                threat_type = np.random.choice(threat_types, p=np.array(threat_weights)/sum(threat_weights))
            
            # Generate threat properties
            threat_info = self.madagascar_threats[threat_type]
            severity = np.random.uniform(*threat_info["severity_range"])
            confidence = 0.6 + np.random.random() * 0.35  # 0.6 to 0.95
            
            # Simulate bounding box for threat area
            bbox = (
                int(np.random.random() * 200),  # x
                int(np.random.random() * 200),  # y
                int(300 + np.random.random() * 300),  # width
                int(200 + np.random.random() * 200)   # height
            )
            
            # Simulate evidence
            evidence = {
                "visual_indicators": self._generate_visual_evidence(threat_type),
                "spatial_analysis": {
                    "affected_area_hectares": severity * 10,
                    "proximity_to_protected_area_km": np.random.uniform(0.1, 5.0),
                    "forest_loss_percentage": severity * 100 if threat_type in [ThreatType.DEFORESTATION, ThreatType.ILLEGAL_LOGGING] else 0
                },
                "temporal_analysis": {
                    "time_since_last_detection_days": int(np.random.uniform(1, 30)),
                    "threat_progression_rate": severity * 0.1
                }
            }
            
            detection = ThreatDetection(
                detection_id=f"mock_threat_{datetime.utcnow().timestamp()}",
                threat_type=threat_type,
                severity=severity,
                severity_level=ThreatSeverity.HIGH,  # Will be auto-calculated
                urgency=ThreatUrgency.URGENT,  # Will be auto-calculated
                confidence=confidence,
                location=(-18.9 + np.random.uniform(-2, 2), 47.5 + np.random.uniform(-2, 2)),  # Madagascar coords
                image_path=image_path,
                bounding_box=bbox,
                source="mock_threat_detector",
                evidence=evidence,
                metadata={
                    "detection_method": "computer_vision_simulation",
                    "processing_time_ms": int(100 + np.random.random() * 200),
                    "model_version": "mock_v1.0",
                    "image_resolution": (640, 480)
                }
            )
            
            return detection
            
        except Exception as e:
            print(f"⚠️  Mock threat detection error: {e}")
            return None
    
    def _generate_visual_evidence(self, threat_type: ThreatType) -> List[str]:
        """Generate visual evidence indicators for threat type."""
        evidence_map = {
            ThreatType.DEFORESTATION: [
                "Tree stumps visible",
                "Cleared forest patches", 
                "Bare soil exposure",
                "Heavy machinery tracks"
            ],
            ThreatType.ILLEGAL_LOGGING: [
                "Cut tree logs stacked",
                "Logging road access",
                "Selective tree removal",
                "Fresh cut marks"
            ],
            ThreatType.SLASH_AND_BURN: [
                "Smoke plumes visible",
                "Charred vegetation",
                "Active fire spots",
                "Agricultural clearing pattern"
            ],
            ThreatType.POACHING: [
                "Snare traps detected",
                "Illegal camp structures",
                "Vehicle tracks off-road",
                "Wildlife carcass remains"
            ],
            ThreatType.HUMAN_INTRUSION: [
                "Unauthorized personnel",
                "New trail creation",
                "Temporary structures",
                "Vegetation disturbance"
            ],
            ThreatType.MINING: [
                "Excavation pits",
                "Mining equipment",
                "Water pollution",
                "Soil disruption"
            ],
            ThreatType.CATTLE_GRAZING: [
                "Cattle presence",
                "Overgrazing damage",
                "Trampled vegetation",
                "Water source contamination"
            ],
            ThreatType.CHARCOAL_PRODUCTION: [
                "Charcoal kilns",
                "Wood pile stacks",
                "Smoke emissions",
                "Forest degradation"
            ]
        }
        
        base_evidence = evidence_map.get(threat_type, ["Unknown threat indicators"])
        # Return 2-4 random evidence items
        return np.random.choice(base_evidence, size=min(len(base_evidence), np.random.randint(2, 5)), replace=False).tolist()

def test_threat_type_definitions():
    """Test threat type and severity definitions."""
    print("⚠️  Testing Threat Type Definitions...")
    
    try:
        # Test threat types
        threat_count = len(ThreatType)
        print(f"✅ Madagascar threat types defined: {threat_count} types")
        
        # Test specific threats
        deforestation = ThreatType.DEFORESTATION
        poaching = ThreatType.POACHING
        logging = ThreatType.ILLEGAL_LOGGING
        
        print(f"✅ Deforestation threat: {deforestation.value}")
        print(f"✅ Poaching threat: {poaching.value}")
        print(f"✅ Illegal logging threat: {logging.value}")
        
        # Test severity levels
        severity_levels = [level.value for level in ThreatSeverity]
        print(f"✅ Threat severity levels: {severity_levels}")
        
        # Test urgency levels
        urgency_levels = [level.value for level in ThreatUrgency]
        print(f"✅ Response urgency levels: {urgency_levels}")
        
        return True
        
    except Exception as e:
        print(f"❌ Threat type definitions error: {e}")
        return False

def test_threat_detection_dataclass():
    """Test threat detection dataclass functionality."""
    print("\n📊 Testing Threat Detection Dataclass...")
    
    try:
        # Test basic detection creation
        detection = ThreatDetection(
            detection_id="test_threat_001",
            threat_type=ThreatType.DEFORESTATION,
            severity=0.75,
            severity_level=ThreatSeverity.HIGH,  # Should be auto-calculated
            urgency=ThreatUrgency.URGENT,  # Should be auto-calculated
            confidence=0.88,
            location=(-18.947, 48.458),  # Maromizaha
            source="test_detector"
        )
        
        print(f"✅ Detection created: {detection.threat_type.value}")
        print(f"✅ Severity: {detection.severity}")
        print(f"✅ Auto-calculated severity level: {detection.severity_level.value}")
        print(f"✅ Auto-calculated urgency: {detection.urgency.value}")
        print(f"✅ Location: {detection.location}")
        
        # Test severity level auto-calculation
        test_severities = [0.1, 0.3, 0.5, 0.7, 0.9]
        expected_levels = [
            ThreatSeverity.MINIMAL,
            ThreatSeverity.LOW,
            ThreatSeverity.MODERATE,
            ThreatSeverity.HIGH,
            ThreatSeverity.CRITICAL
        ]
        
        for severity, expected in zip(test_severities, expected_levels):
            test_detection = ThreatDetection(
                detection_id=f"test_{severity}",
                threat_type=ThreatType.DEFORESTATION,
                severity=severity,
                severity_level=ThreatSeverity.LOW,  # Will be overridden
                urgency=ThreatUrgency.ROUTINE,  # Will be overridden
                confidence=0.8
            )
            
            if test_detection.severity_level == expected:
                print(f"✅ Severity {severity} → {expected.value}")
            else:
                print(f"❌ Severity {severity} → expected {expected.value}, got {test_detection.severity_level.value}")
                return False
        
        # Test urgency calculation for high-risk threats
        poaching_detection = ThreatDetection(
            detection_id="urgency_test",
            threat_type=ThreatType.POACHING,
            severity=0.85,
            severity_level=ThreatSeverity.CRITICAL,
            urgency=ThreatUrgency.ROUTINE,  # Will be overridden
            confidence=0.9
        )
        
        if poaching_detection.urgency == ThreatUrgency.CRISIS:
            print("✅ High-severity poaching correctly flagged as CRISIS")
        else:
            print(f"❌ Expected CRISIS urgency, got {poaching_detection.urgency.value}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Threat detection dataclass error: {e}")
        return False

def test_mock_threat_detector():
    """Test mock threat detector functionality."""
    print("\n🎭 Testing Mock Threat Detector...")
    
    try:
        detector = MockThreatDetector()
        
        # Test Madagascar threat patterns
        madagascar_threat_count = len(detector.madagascar_threats)
        print(f"✅ Madagascar threat patterns: {madagascar_threat_count} types")
        
        # Test threat indicator system
        indicator_count = len(detector.threat_indicators)
        print(f"✅ Threat indicators defined: {indicator_count} categories")
        
        # Test mock image creation and detection
        test_image_path = "test_threat_image.jpg"
        test_image = Image.new('RGB', (640, 480), color='brown')  # Simulate deforestation
        test_image.save(test_image_path)
        
        # Test targeted threat detection
        detection = detector.simulate_threat_detection(test_image_path, "deforestation")
        
        if detection:
            print(f"✅ Mock detection generated: {detection.threat_type.value}")
            print(f"✅ Severity: {detection.severity:.2f}")
            print(f"✅ Confidence: {detection.confidence:.2f}")
            print(f"✅ Urgency: {detection.urgency.value}")
            print(f"✅ Evidence items: {len(detection.evidence.get('visual_indicators', []))}")
            print(f"✅ Location: {detection.location}")
        else:
            print("❌ Mock detection failed")
            return False
        
        # Test evidence generation
        evidence = detection.evidence
        required_evidence = ["visual_indicators", "spatial_analysis", "temporal_analysis"]
        
        for evidence_type in required_evidence:
            if evidence_type in evidence:
                print(f"✅ Evidence type present: {evidence_type}")
            else:
                print(f"❌ Missing evidence type: {evidence_type}")
                return False
        
        # Test visual indicators
        visual_indicators = evidence["visual_indicators"]
        if len(visual_indicators) >= 2:
            print(f"✅ Visual indicators: {visual_indicators}")
        else:
            print("❌ Insufficient visual indicators")
            return False
        
        # Cleanup
        os.remove(test_image_path)
        print("✅ Test image cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Mock threat detector error: {e}")
        return False

def test_threat_urgency_calculation():
    """Test threat urgency calculation logic."""
    print("\n⏰ Testing Threat Urgency Calculation...")
    
    try:
        # Test high-urgency threats
        high_urgency_scenarios = [
            (ThreatType.POACHING, 0.9, ThreatUrgency.CRISIS),
            (ThreatType.ILLEGAL_LOGGING, 0.8, ThreatUrgency.CRISIS),
            (ThreatType.SLASH_AND_BURN, 0.7, ThreatUrgency.EMERGENCY),
            (ThreatType.MINING, 0.5, ThreatUrgency.URGENT)
        ]
        
        for threat_type, severity, expected_urgency in high_urgency_scenarios:
            detection = ThreatDetection(
                detection_id=f"urgency_test_{threat_type.value}",
                threat_type=threat_type,
                severity=severity,
                severity_level=ThreatSeverity.HIGH,
                urgency=ThreatUrgency.ROUTINE,  # Will be overridden
                confidence=0.85
            )
            
            if detection.urgency == expected_urgency:
                print(f"✅ {threat_type.value} (severity {severity}) → {expected_urgency.value}")
            else:
                print(f"❌ {threat_type.value} urgency calculation incorrect: expected {expected_urgency.value}, got {detection.urgency.value}")
                return False
        
        # Test medium-urgency threats
        medium_urgency_scenarios = [
            (ThreatType.DEFORESTATION, 0.9, ThreatUrgency.EMERGENCY),
            (ThreatType.HUMAN_INTRUSION, 0.6, ThreatUrgency.URGENT),
            (ThreatType.CATTLE_GRAZING, 0.3, ThreatUrgency.ROUTINE)
        ]
        
        for threat_type, severity, expected_urgency in medium_urgency_scenarios:
            detection = ThreatDetection(
                detection_id=f"urgency_test_{threat_type.value}",
                threat_type=threat_type,
                severity=severity,
                severity_level=ThreatSeverity.MODERATE,
                urgency=ThreatUrgency.ROUTINE,  # Will be overridden
                confidence=0.8
            )
            
            if detection.urgency == expected_urgency:
                print(f"✅ {threat_type.value} (severity {severity}) → {expected_urgency.value}")
            else:
                print(f"❌ {threat_type.value} urgency calculation incorrect")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Threat urgency calculation error: {e}")
        return False

def test_threat_serialization():
    """Test threat detection serialization for storage."""
    print("\n💾 Testing Threat Detection Serialization...")
    
    try:
        # Create a complex threat detection
        detection = ThreatDetection(
            detection_id="serialization_test",
            threat_type=ThreatType.ILLEGAL_LOGGING,
            severity=0.82,
            severity_level=ThreatSeverity.CRITICAL,
            urgency=ThreatUrgency.EMERGENCY,
            confidence=0.91,
            location=(-18.947, 48.458),
            image_path="/test/path/threat_image.jpg",
            bounding_box=(100, 150, 400, 300),
            source="test_serialization",
            evidence={
                "visual_indicators": ["Cut tree logs stacked", "Fresh cut marks"],
                "spatial_analysis": {
                    "affected_area_hectares": 8.2,
                    "proximity_to_protected_area_km": 1.5
                }
            },
            metadata={"test": True, "model_version": "v1.0"}
        )
        
        # Convert to dictionary for JSON serialization
        detection_dict = {
            "detection_id": detection.detection_id,
            "threat_type": detection.threat_type.value,
            "severity": detection.severity,
            "severity_level": detection.severity_level.value,
            "urgency": detection.urgency.value,
            "confidence": detection.confidence,
            "location": detection.location,
            "image_path": detection.image_path,
            "bounding_box": detection.bounding_box,
            "timestamp": detection.timestamp.isoformat(),
            "source": detection.source,
            "evidence": detection.evidence,
            "metadata": detection.metadata
        }
        
        # Test JSON serialization
        json_str = json.dumps(detection_dict, indent=2)
        print("✅ Threat detection serialized to JSON")
        
        # Test JSON deserialization
        loaded_dict = json.loads(json_str)
        print("✅ Threat detection deserialized from JSON")
        
        # Verify data integrity
        if (loaded_dict["threat_type"] == detection.threat_type.value and
            loaded_dict["severity"] == detection.severity and
            loaded_dict["urgency"] == detection.urgency.value and
            loaded_dict["location"] == list(detection.location)):
            print("✅ Data integrity verified after serialization")
        else:
            print("❌ Data integrity check failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Threat serialization error: {e}")
        return False

def test_madagascar_threat_coverage():
    """Test Madagascar-specific threat coverage."""
    print("\n🇲🇬 Testing Madagascar Threat Coverage...")
    
    try:
        detector = MockThreatDetector()
        
        # Test threat type coverage for Madagascar
        madagascar_threats = list(detector.madagascar_threats.keys())
        
        # Critical Madagascar threats that should be covered
        critical_threats = [
            ThreatType.DEFORESTATION,
            ThreatType.ILLEGAL_LOGGING,
            ThreatType.SLASH_AND_BURN,
            ThreatType.CHARCOAL_PRODUCTION,
            ThreatType.CATTLE_GRAZING,
            ThreatType.MINING
        ]
        
        for threat in critical_threats:
            if threat in madagascar_threats:
                threat_info = detector.madagascar_threats[threat]
                print(f"✅ {threat.value}: probability {threat_info['base_probability']}, severity range {threat_info['severity_range']}")
            else:
                print(f"❌ Critical threat missing: {threat.value}")
                return False
        
        # Test probability distribution
        total_probability = sum(info["base_probability"] for info in detector.madagascar_threats.values())
        print(f"✅ Total threat probability: {total_probability:.2f}")
        
        # Test evidence generation for each threat type
        print("✅ Evidence generation test:")
        for threat_type in madagascar_threats[:5]:  # Test first 5
            evidence = detector._generate_visual_evidence(threat_type)
            if len(evidence) >= 2:
                print(f"   • {threat_type.value}: {len(evidence)} evidence items")
            else:
                print(f"❌ Insufficient evidence for {threat_type.value}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Madagascar threat coverage error: {e}")
        return False

def main():
    """Run Section 1 tests."""
    print("⚠️  STEP 5 - SECTION 1: Threat Detection Foundation")
    print("=" * 52)
    
    tests_passed = 0
    total_tests = 7
    
    # Test 1: Threat type definitions
    if test_threat_type_definitions():
        tests_passed += 1
    
    # Test 2: Threat detection dataclass
    if test_threat_detection_dataclass():
        tests_passed += 1
    
    # Test 3: Mock threat detector
    if test_mock_threat_detector():
        tests_passed += 1
    
    # Test 4: Threat urgency calculation
    if test_threat_urgency_calculation():
        tests_passed += 1
    
    # Test 5: Threat serialization
    if test_threat_serialization():
        tests_passed += 1
    
    # Test 6: Madagascar threat coverage
    if test_madagascar_threat_coverage():
        tests_passed += 1
    
    # Test 7: Integration readiness
    print("\n🔗 Testing Integration Readiness...")
    try:
        # Test compatibility with previous step components
        from step4_section1_test import SpeciesDetection, MadagascarSpecies
        
        # Create test threat and species detection for integration
        threat_detection = ThreatDetection(
            detection_id="integration_test",
            threat_type=ThreatType.POACHING,
            severity=0.9,
            severity_level=ThreatSeverity.CRITICAL,
            urgency=ThreatUrgency.CRISIS,
            confidence=0.95
        )
        
        species_detection = SpeciesDetection(
            detection_id="integration_species_test",
            species=MadagascarSpecies.INDRI_INDRI,
            confidence=0.88,
            confidence_level=SpeciesConfidence.HIGH
        )
        
        print("✅ Integration compatibility verified")
        print(f"   • Threat: {threat_detection.threat_type.value} (urgency: {threat_detection.urgency.value})")
        print(f"   • Species: {species_detection.species.value} (confidence: {species_detection.confidence})")
        
        tests_passed += 1
        
    except Exception as e:
        print(f"❌ Integration readiness error: {e}")
    
    # Summary
    print(f"\n📊 Section 1 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 1 PASSED - Ready for Section 2")
        print("\n🎯 Next: Implement threat detection ML models and computer vision")
        return True
    else:
        print("❌ Section 1 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
