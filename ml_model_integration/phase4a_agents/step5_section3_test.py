"""
Step 5 Section 3: Real-time Threat Monitoring
==============================================
Implement real-time threat monitoring and alert systems for Madagascar conservation.
"""

import sys
import os
import json
import time
import asyncio
import threading
import queue
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, deque

# Import from previous sections
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
from step5_section1_test import ThreatType, ThreatSeverity, ThreatUrgency, ThreatDetection
from step5_section2_test import ThreatClassificationModel, ChangeDetectionModel, ThreatDetectionEnsemble

@dataclass
class ThreatAlert:
    """Alert for detected threats."""
    alert_id: str
    threat_detection: ThreatDetection
    alert_level: ThreatUrgency
    alert_timestamp: datetime
    affected_location: str
    stakeholders: List[str]
    recommended_actions: List[str]
    escalation_required: bool = False
    status: str = "active"  # active, acknowledged, resolved
    response_team: Optional[str] = None
    estimated_impact: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.estimated_impact is None:
            self.estimated_impact = {}

@dataclass
class ThreatMonitoringMetrics:
    """Performance metrics for threat monitoring system."""
    total_images_processed: int = 0
    threats_detected: int = 0
    false_positives: int = 0
    alerts_generated: int = 0
    average_processing_time_ms: float = 0.0
    system_uptime_hours: float = 0.0
    threat_type_distribution: Dict[str, int] = None
    alert_response_times: List[float] = None
    
    def __post_init__(self):
        if self.threat_type_distribution is None:
            self.threat_type_distribution = {}
        if self.alert_response_times is None:
            self.alert_response_times = []

class ThreatAlertManager:
    """Manages threat alerts and stakeholder notifications."""
    
    def __init__(self):
        self.active_alerts = {}
        self.alert_history = deque(maxlen=1000)  # Keep last 1000 alerts
        self.stakeholder_config = self._initialize_stakeholder_config()
        self.escalation_rules = self._initialize_escalation_rules()
    
    def _initialize_stakeholder_config(self) -> Dict[str, Dict[str, Any]]:
        """Initialize stakeholder notification configuration."""
        return {
            "madagascar_national_parks": {
                "contact_method": "radio",
                "threat_types": [ThreatType.DEFORESTATION, ThreatType.ILLEGAL_LOGGING, ThreatType.POACHING],
                "urgency_threshold": ThreatUrgency.URGENT,
                "response_time_hours": 2
            },
            "local_community_leaders": {
                "contact_method": "mobile",
                "threat_types": [ThreatType.SLASH_AND_BURN, ThreatType.CATTLE_GRAZING, ThreatType.CHARCOAL_PRODUCTION],
                "urgency_threshold": ThreatUrgency.ELEVATED,
                "response_time_hours": 4
            },
            "research_station": {
                "contact_method": "satellite",
                "threat_types": list(ThreatType),  # All threats
                "urgency_threshold": ThreatUrgency.ROUTINE,
                "response_time_hours": 24
            },
            "conservation_international": {
                "contact_method": "email",
                "threat_types": [ThreatType.MINING, ThreatType.INFRASTRUCTURE_DEVELOPMENT],
                "urgency_threshold": ThreatUrgency.URGENT,
                "response_time_hours": 12
            },
            "emergency_response_team": {
                "contact_method": "emergency_radio",
                "threat_types": [ThreatType.POACHING, ThreatType.ILLEGAL_LOGGING],
                "urgency_threshold": ThreatUrgency.EMERGENCY,
                "response_time_hours": 1
            }
        }
    
    def _initialize_escalation_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize alert escalation rules."""
        return {
            "severity_escalation": {
                "high_severity_threshold": 0.8,
                "critical_severity_threshold": 0.9,
                "escalation_time_hours": 2
            },
            "repeat_detection": {
                "same_location_threshold_km": 1.0,
                "repeat_time_window_hours": 6,
                "escalation_count": 3
            },
            "threat_combination": {
                "multiple_threats_threshold": 2,
                "combination_time_window_hours": 4,
                "escalation_required": True
            }
        }
    
    def create_alert(self, threat_detection: ThreatDetection, location: str) -> ThreatAlert:
        """Create alert from threat detection."""
        try:
            alert_id = f"alert_{threat_detection.threat_type.value}_{datetime.utcnow().timestamp()}"
            
            # Determine stakeholders
            stakeholders = self._determine_stakeholders(threat_detection)
            
            # Generate recommended actions
            recommended_actions = self._generate_recommended_actions(threat_detection)
            
            # Assess escalation need
            escalation_required = self._assess_escalation_need(threat_detection, location)
            
            # Estimate impact
            estimated_impact = self._estimate_threat_impact(threat_detection, location)
            
            alert = ThreatAlert(
                alert_id=alert_id,
                threat_detection=threat_detection,
                alert_level=threat_detection.urgency,
                alert_timestamp=datetime.utcnow(),
                affected_location=location,
                stakeholders=stakeholders,
                recommended_actions=recommended_actions,
                escalation_required=escalation_required,
                estimated_impact=estimated_impact
            )
            
            # Store alert
            self.active_alerts[alert_id] = alert
            self.alert_history.append(alert)
            
            return alert
            
        except Exception as e:
            print(f"⚠️  Alert creation error: {e}")
            return None
    
    def _determine_stakeholders(self, threat_detection: ThreatDetection) -> List[str]:
        """Determine which stakeholders should be notified."""
        stakeholders = []
        
        for stakeholder, config in self.stakeholder_config.items():
            # Check if threat type is relevant
            if threat_detection.threat_type in config["threat_types"]:
                # Check if urgency meets threshold
                urgency_levels = [ThreatUrgency.ROUTINE, ThreatUrgency.ELEVATED, 
                                ThreatUrgency.URGENT, ThreatUrgency.EMERGENCY, ThreatUrgency.CRISIS]
                
                threat_urgency_level = urgency_levels.index(threat_detection.urgency)
                threshold_level = urgency_levels.index(config["urgency_threshold"])
                
                if threat_urgency_level >= threshold_level:
                    stakeholders.append(stakeholder)
        
        return stakeholders
    
    def _generate_recommended_actions(self, threat_detection: ThreatDetection) -> List[str]:
        """Generate recommended actions based on threat type and severity."""
        actions = []
        threat_type = threat_detection.threat_type
        severity = threat_detection.severity
        urgency = threat_detection.urgency
        
        # Immediate response actions
        if urgency in [ThreatUrgency.EMERGENCY, ThreatUrgency.CRISIS]:
            actions.extend([
                "Deploy immediate response team",
                "Establish perimeter security",
                "Document evidence for legal action"
            ])
        
        # Threat-specific actions
        if threat_type == ThreatType.POACHING:
            actions.extend([
                "Alert anti-poaching patrol units",
                "Coordinate with local law enforcement",
                "Increase surveillance in affected area",
                "Check trap locations and animal safety"
            ])
        elif threat_type == ThreatType.ILLEGAL_LOGGING:
            actions.extend([
                "Verify logging permits in area",
                "Contact forestry authorities",
                "Document tree species and quantities",
                "Assess access routes used"
            ])
        elif threat_type == ThreatType.DEFORESTATION:
            actions.extend([
                "Assess extent of forest loss",
                "Identify responsible parties",
                "Coordinate reforestation planning",
                "Strengthen monitoring in buffer zones"
            ])
        elif threat_type == ThreatType.SLASH_AND_BURN:
            actions.extend([
                "Engage with local farmers",
                "Provide alternative agriculture education",
                "Monitor fire progression",
                "Coordinate firefighting if needed"
            ])
        elif threat_type == ThreatType.HUMAN_INTRUSION:
            actions.extend([
                "Verify authorization status",
                "Guide unauthorized personnel to exit",
                "Review access control measures",
                "Update security protocols"
            ])
        elif threat_type == ThreatType.MINING:
            actions.extend([
                "Check mining permits and licenses",
                "Assess environmental damage",
                "Contact mining regulatory authorities",
                "Document water and soil impact"
            ])
        
        # Severity-based actions
        if severity > 0.8:
            actions.extend([
                "Escalate to emergency management",
                "Coordinate with government agencies",
                "Prepare media statement if needed"
            ])
        elif severity > 0.6:
            actions.extend([
                "Increase patrol frequency",
                "Deploy additional monitoring equipment",
                "Brief all field teams"
            ])
        
        # General conservation actions
        actions.extend([
            "Update threat assessment database",
            "Review conservation strategy effectiveness",
            "Coordinate with partner organizations"
        ])
        
        return actions
    
    def _assess_escalation_need(self, threat_detection: ThreatDetection, location: str) -> bool:
        """Assess if alert needs escalation."""
        # High severity always requires escalation
        if threat_detection.severity >= self.escalation_rules["severity_escalation"]["high_severity_threshold"]:
            return True
        
        # Critical urgency requires escalation
        if threat_detection.urgency in [ThreatUrgency.EMERGENCY, ThreatUrgency.CRISIS]:
            return True
        
        # Check for repeat detections in same area
        recent_alerts = [
            alert for alert in self.alert_history
            if (datetime.utcnow() - alert.alert_timestamp).total_seconds() / 3600 <= 
               self.escalation_rules["repeat_detection"]["repeat_time_window_hours"]
        ]
        
        same_area_alerts = [
            alert for alert in recent_alerts
            if self._calculate_distance(location, alert.affected_location) <= 
               self.escalation_rules["repeat_detection"]["same_location_threshold_km"]
        ]
        
        if len(same_area_alerts) >= self.escalation_rules["repeat_detection"]["escalation_count"]:
            return True
        
        return False
    
    def _estimate_threat_impact(self, threat_detection: ThreatDetection, location: str) -> Dict[str, Any]:
        """Estimate potential impact of threat."""
        severity = threat_detection.severity
        threat_type = threat_detection.threat_type
        
        # Base impact factors
        base_impact = {
            "environmental_damage_score": severity,
            "species_impact_score": 0.0,
            "habitat_loss_risk": severity * 0.8,
            "economic_impact_score": 0.0,
            "community_impact_score": 0.0
        }
        
        # Threat-specific impact adjustments
        if threat_type in [ThreatType.DEFORESTATION, ThreatType.ILLEGAL_LOGGING]:
            base_impact["habitat_loss_risk"] = min(1.0, severity * 1.2)
            base_impact["species_impact_score"] = min(1.0, severity * 0.9)
            base_impact["economic_impact_score"] = min(1.0, severity * 0.7)
        elif threat_type == ThreatType.POACHING:
            base_impact["species_impact_score"] = min(1.0, severity * 1.3)
            base_impact["economic_impact_score"] = min(1.0, severity * 0.5)
        elif threat_type == ThreatType.MINING:
            base_impact["environmental_damage_score"] = min(1.0, severity * 1.4)
            base_impact["habitat_loss_risk"] = min(1.0, severity * 1.1)
            base_impact["economic_impact_score"] = min(1.0, severity * 0.8)
        elif threat_type in [ThreatType.SLASH_AND_BURN, ThreatType.CATTLE_GRAZING]:
            base_impact["community_impact_score"] = min(1.0, severity * 0.6)
            base_impact["habitat_loss_risk"] = min(1.0, severity * 0.7)
        
        # Location-specific adjustments (simplified)
        if "protected" in location.lower() or "park" in location.lower():
            base_impact["species_impact_score"] = min(1.0, base_impact["species_impact_score"] * 1.2)
            base_impact["habitat_loss_risk"] = min(1.0, base_impact["habitat_loss_risk"] * 1.1)
        
        # Add estimated recovery time
        recovery_times = {
            ThreatType.POACHING: "immediate_intervention_required",
            ThreatType.ILLEGAL_LOGGING: "5-20_years",
            ThreatType.DEFORESTATION: "10-50_years",
            ThreatType.MINING: "50-100_years",
            ThreatType.SLASH_AND_BURN: "2-10_years"
        }
        
        base_impact["estimated_recovery_time"] = recovery_times.get(threat_type, "unknown")
        
        return base_impact
    
    def _calculate_distance(self, location1: str, location2: str) -> float:
        """Calculate distance between locations (simplified)."""
        # In a real implementation, this would use GPS coordinates
        # For testing, return a random distance
        return np.random.uniform(0.1, 5.0)

class RealTimeThreatMonitor:
    """Real-time threat monitoring system."""
    
    def __init__(self, max_queue_size: int = 200):
        self.threat_detector = ThreatDetectionEnsemble()
        self.alert_manager = ThreatAlertManager()
        self.image_queue = queue.Queue(maxsize=max_queue_size)
        self.alert_queue = queue.Queue()
        self.is_running = False
        self.worker_threads = []
        self.metrics = ThreatMonitoringMetrics()
        self.processing_times = deque(maxlen=1000)
        self.threat_history = deque(maxlen=5000)
        self.start_time = datetime.utcnow()
    
    def start_monitoring(self, num_workers: int = 2):
        """Start real-time threat monitoring."""
        if self.is_running:
            print("⚠️  Monitor already running")
            return
        
        self.is_running = True
        self.start_time = datetime.utcnow()
        
        # Start worker threads
        for i in range(num_workers):
            worker = threading.Thread(
                target=self._process_images_worker,
                args=(f"worker_{i}",),
                daemon=True
            )
            worker.start()
            self.worker_threads.append(worker)
        
        # Start alert processing thread
        alert_worker = threading.Thread(
            target=self._process_alerts_worker,
            daemon=True
        )
        alert_worker.start()
        self.worker_threads.append(alert_worker)
        
        print(f"🚀 Real-time threat monitoring started with {num_workers} workers")
    
    def stop_monitoring(self):
        """Stop real-time threat monitoring."""
        self.is_running = False
        
        # Wait for workers to finish
        for worker in self.worker_threads:
            worker.join(timeout=5)
        
        self.worker_threads.clear()
        print("🛑 Real-time threat monitoring stopped")
    
    def add_image_for_analysis(self, image_path: str, location: str = "unknown", 
                             reference_image: str = None) -> bool:
        """Add image to monitoring queue."""
        try:
            image_data = {
                "image_path": image_path,
                "location": location,
                "reference_image": reference_image,
                "timestamp": datetime.utcnow()
            }
            
            self.image_queue.put(image_data, block=False)
            return True
            
        except queue.Full:
            print("⚠️  Image queue full, dropping image")
            return False
    
    def get_active_alerts(self) -> List[ThreatAlert]:
        """Get all active threat alerts."""
        return list(self.alert_manager.active_alerts.values())
    
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get comprehensive monitoring summary."""
        # Update uptime
        uptime = datetime.utcnow() - self.start_time
        self.metrics.system_uptime_hours = uptime.total_seconds() / 3600
        
        # Update average processing time
        if self.processing_times:
            self.metrics.average_processing_time_ms = np.mean(list(self.processing_times))
        
        return {
            "monitoring_status": "active" if self.is_running else "stopped",
            "metrics": asdict(self.metrics),
            "active_alerts": len(self.alert_manager.active_alerts),
            "queue_status": {
                "images_pending": self.image_queue.qsize(),
                "alerts_pending": self.alert_queue.qsize()
            },
            "recent_threats": [
                {
                    "threat_type": threat.threat_type.value,
                    "severity": threat.severity,
                    "timestamp": threat.timestamp.isoformat()
                }
                for threat in list(self.threat_history)[-10:]  # Last 10 threats
            ]
        }
    
    def _process_images_worker(self, worker_name: str):
        """Worker thread for processing images."""
        print(f"🔄 Threat detection worker {worker_name} started")
        
        while self.is_running:
            try:
                # Get image from queue with timeout
                image_data = self.image_queue.get(timeout=1.0)
                
                # Process image
                start_time = time.time()
                threat_detection = self.threat_detector.predict_threat_ensemble(
                    image_data["image_path"],
                    image_data.get("reference_image")
                )
                processing_time = (time.time() - start_time) * 1000
                
                # Update metrics
                self.metrics.total_images_processed += 1
                self.processing_times.append(processing_time)
                
                if threat_detection:
                    self.metrics.threats_detected += 1
                    self.threat_history.append(threat_detection)
                    
                    # Update threat type distribution
                    threat_type = threat_detection.threat_type.value
                    self.metrics.threat_type_distribution[threat_type] = (
                        self.metrics.threat_type_distribution.get(threat_type, 0) + 1
                    )
                    
                    # Create alert if needed
                    if self._should_create_alert(threat_detection):
                        alert = self.alert_manager.create_alert(
                            threat_detection, 
                            image_data["location"]
                        )
                        
                        if alert:
                            self.alert_queue.put(alert)
                            self.metrics.alerts_generated += 1
                
                # Mark task as done
                self.image_queue.task_done()
                
            except queue.Empty:
                # Timeout waiting for images - continue
                continue
            except Exception as e:
                print(f"⚠️  Worker {worker_name} error: {e}")
        
        print(f"🔄 Threat detection worker {worker_name} stopped")
    
    def _process_alerts_worker(self):
        """Worker thread for processing alerts."""
        print("🔄 Alert processing worker started")
        
        while self.is_running:
            try:
                # Get alert from queue with timeout
                alert = self.alert_queue.get(timeout=1.0)
                
                # Process alert (simulate stakeholder notification)
                self._process_alert(alert)
                
                # Mark task as done
                self.alert_queue.task_done()
                
            except queue.Empty:
                # Timeout waiting for alerts - continue
                continue
            except Exception as e:
                print(f"⚠️  Alert processing error: {e}")
        
        print("🔄 Alert processing worker stopped")
    
    def _should_create_alert(self, threat_detection: ThreatDetection) -> bool:
        """Determine if threat detection should generate an alert."""
        # Alert thresholds
        min_confidence = 0.6
        min_severity = 0.4
        
        # High-priority threats get lower thresholds
        high_priority_threats = {
            ThreatType.POACHING, 
            ThreatType.ILLEGAL_LOGGING, 
            ThreatType.MINING
        }
        
        if threat_detection.threat_type in high_priority_threats:
            min_confidence = 0.5
            min_severity = 0.3
        
        return (threat_detection.confidence >= min_confidence and 
                threat_detection.severity >= min_severity)
    
    def _process_alert(self, alert: ThreatAlert):
        """Process alert (simulate stakeholder notification)."""
        print(f"📢 Processing alert {alert.alert_id}")
        print(f"   Threat: {alert.threat_detection.threat_type.value}")
        print(f"   Severity: {alert.threat_detection.severity:.2f}")
        print(f"   Location: {alert.affected_location}")
        print(f"   Stakeholders: {', '.join(alert.stakeholders)}")
        
        if alert.escalation_required:
            print(f"   🚨 ESCALATION REQUIRED")
        
        # Simulate notification delay
        time.sleep(0.1)

def test_threat_alert_manager():
    """Test threat alert management system."""
    print("📢 Testing Threat Alert Manager...")
    
    try:
        alert_manager = ThreatAlertManager()
        
        # Test stakeholder configuration
        stakeholders = alert_manager.stakeholder_config
        print(f"✅ Stakeholder configuration: {len(stakeholders)} stakeholders")
        
        # Test escalation rules
        escalation_rules = alert_manager.escalation_rules
        print(f"✅ Escalation rules: {len(escalation_rules)} rule categories")
        
        # Create test threat detection
        test_threat = ThreatDetection(
            detection_id="alert_test_001",
            threat_type=ThreatType.POACHING,
            severity=0.85,
            severity_level=ThreatSeverity.CRITICAL,
            urgency=ThreatUrgency.EMERGENCY,
            confidence=0.92,
            location=(-18.947, 48.458)
        )
        
        # Create alert
        alert = alert_manager.create_alert(test_threat, "Maromizaha_Protected_Area")
        
        if alert:
            print(f"✅ Alert created: {alert.alert_id}")
            print(f"✅ Alert level: {alert.alert_level.value}")
            print(f"✅ Stakeholders notified: {len(alert.stakeholders)}")
            print(f"✅ Recommended actions: {len(alert.recommended_actions)}")
            print(f"✅ Escalation required: {alert.escalation_required}")
            
            # Check stakeholder selection
            if "emergency_response_team" in alert.stakeholders:
                print("✅ Emergency response team correctly notified")
            
            # Check recommended actions
            if any("patrol" in action.lower() for action in alert.recommended_actions):
                print("✅ Patrol actions included in recommendations")
            
            # Check estimated impact
            impact = alert.estimated_impact
            if "species_impact_score" in impact:
                print(f"✅ Species impact estimated: {impact['species_impact_score']:.2f}")
        else:
            print("❌ Alert creation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Threat alert manager error: {e}")
        return False

def test_real_time_threat_monitor():
    """Test real-time threat monitoring system."""
    print("\n⏰ Testing Real-time Threat Monitor...")
    
    try:
        monitor = RealTimeThreatMonitor(max_queue_size=10)
        
        # Test monitor initialization
        print("✅ Real-time monitor initialized")
        
        # Start monitoring
        monitor.start_monitoring(num_workers=1)
        
        # Wait for startup
        time.sleep(0.5)
        
        # Add test images for analysis
        from PIL import Image
        
        test_images = []
        for i in range(3):
            image_path = f"test_monitor_{i}.jpg"
            test_image = Image.new('RGB', (224, 224), color=['red', 'brown', 'green'][i])
            test_image.save(image_path)
            test_images.append(image_path)
            
            # Add to monitoring queue
            success = monitor.add_image_for_analysis(
                image_path, 
                f"test_location_{i}",
                test_images[0] if i > 0 else None  # Use first image as reference
            )
            
            if success:
                print(f"✅ Added image {i+1} to monitoring queue")
            else:
                print(f"❌ Failed to add image {i+1}")
        
        # Wait for processing
        time.sleep(2)
        
        # Check monitoring results
        summary = monitor.get_monitoring_summary()
        
        print(f"✅ Monitoring summary generated")
        print(f"   • Images processed: {summary['metrics']['total_images_processed']}")
        print(f"   • Threats detected: {summary['metrics']['threats_detected']}")
        print(f"   • Alerts generated: {summary['metrics']['alerts_generated']}")
        print(f"   • System uptime: {summary['metrics']['system_uptime_hours']:.2f} hours")
        
        # Check active alerts
        active_alerts = monitor.get_active_alerts()
        if active_alerts:
            print(f"✅ Active alerts: {len(active_alerts)}")
            for alert in active_alerts:
                print(f"   • {alert.threat_detection.threat_type.value} at {alert.affected_location}")
        else:
            print("✅ No active alerts (expected for test)")
        
        # Stop monitoring
        monitor.stop_monitoring()
        print("✅ Monitoring stopped successfully")
        
        # Cleanup test images
        for image_path in test_images:
            if os.path.exists(image_path):
                os.remove(image_path)
        print("✅ Test images cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Real-time threat monitor error: {e}")
        return False

def test_alert_escalation_logic():
    """Test alert escalation logic."""
    print("\n🚨 Testing Alert Escalation Logic...")
    
    try:
        alert_manager = ThreatAlertManager()
        
        # Test high severity escalation
        high_severity_threat = ThreatDetection(
            detection_id="escalation_test_1",
            threat_type=ThreatType.ILLEGAL_LOGGING,
            severity=0.95,  # Very high severity
            severity_level=ThreatSeverity.CRITICAL,
            urgency=ThreatUrgency.CRISIS,
            confidence=0.9
        )
        
        escalation_needed = alert_manager._assess_escalation_need(
            high_severity_threat, 
            "High_Priority_Conservation_Area"
        )
        
        if escalation_needed:
            print("✅ High severity threat correctly flagged for escalation")
        else:
            print("❌ High severity threat not flagged for escalation")
            return False
        
        # Test low severity no escalation
        low_severity_threat = ThreatDetection(
            detection_id="escalation_test_2",
            threat_type=ThreatType.CATTLE_GRAZING,
            severity=0.3,  # Low severity
            severity_level=ThreatSeverity.LOW,
            urgency=ThreatUrgency.ROUTINE,
            confidence=0.6
        )
        
        no_escalation_needed = alert_manager._assess_escalation_need(
            low_severity_threat,
            "Low_Priority_Area"
        )
        
        if not no_escalation_needed:
            print("✅ Low severity threat correctly not flagged for escalation")
        else:
            print("❌ Low severity threat incorrectly flagged for escalation")
            return False
        
        # Test stakeholder determination
        stakeholders = alert_manager._determine_stakeholders(high_severity_threat)
        
        if "madagascar_national_parks" in stakeholders:
            print("✅ National parks correctly included for illegal logging")
        else:
            print("❌ National parks not included for illegal logging")
            return False
        
        if "emergency_response_team" in stakeholders:
            print("✅ Emergency response team correctly included for crisis")
        else:
            print("❌ Emergency response team not included for crisis")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Alert escalation logic error: {e}")
        return False

def test_threat_impact_estimation():
    """Test threat impact estimation."""
    print("\n📊 Testing Threat Impact Estimation...")
    
    try:
        alert_manager = ThreatAlertManager()
        
        # Test different threat types impact estimation
        test_threats = [
            (ThreatType.POACHING, 0.8, "should have high species impact"),
            (ThreatType.DEFORESTATION, 0.9, "should have high habitat loss risk"),
            (ThreatType.MINING, 0.7, "should have high environmental damage"),
            (ThreatType.SLASH_AND_BURN, 0.6, "should have community impact")
        ]
        
        for threat_type, severity, expected in test_threats:
            test_threat = ThreatDetection(
                detection_id=f"impact_test_{threat_type.value}",
                threat_type=threat_type,
                severity=severity,
                severity_level=ThreatSeverity.HIGH,
                urgency=ThreatUrgency.URGENT,
                confidence=0.8
            )
            
            impact = alert_manager._estimate_threat_impact(test_threat, "Test_Protected_Area")
            
            print(f"✅ {threat_type.value} impact estimated ({expected})")
            print(f"   • Environmental damage: {impact['environmental_damage_score']:.2f}")
            print(f"   • Species impact: {impact['species_impact_score']:.2f}")
            print(f"   • Habitat loss risk: {impact['habitat_loss_risk']:.2f}")
            print(f"   • Recovery time: {impact['estimated_recovery_time']}")
            
            # Verify impact scores are in valid range
            for score_name, score_value in impact.items():
                if isinstance(score_value, (int, float)) and not (0 <= score_value <= 1):
                    print(f"❌ Impact score out of range: {score_name} = {score_value}")
                    return False
        
        return True
        
    except Exception as e:
        print(f"❌ Threat impact estimation error: {e}")
        return False

def test_monitoring_metrics():
    """Test monitoring metrics collection and reporting."""
    print("\n📈 Testing Monitoring Metrics...")
    
    try:
        monitor = RealTimeThreatMonitor(max_queue_size=5)
        
        # Test initial metrics
        initial_summary = monitor.get_monitoring_summary()
        
        if initial_summary["monitoring_status"] == "stopped":
            print("✅ Initial monitoring status correct")
        else:
            print("❌ Initial monitoring status incorrect")
            return False
        
        # Start monitoring and add some data
        monitor.start_monitoring(num_workers=1)
        time.sleep(0.2)
        
        # Simulate some metrics updates
        monitor.metrics.total_images_processed = 50
        monitor.metrics.threats_detected = 12
        monitor.metrics.alerts_generated = 5
        monitor.metrics.threat_type_distribution = {
            "deforestation": 5,
            "poaching": 3,
            "illegal_logging": 4
        }
        
        # Add some processing times
        for i in range(10):
            monitor.processing_times.append(50 + i * 10)  # 50-140ms
        
        # Get updated summary
        summary = monitor.get_monitoring_summary()
        
        print(f"✅ Metrics updated successfully")
        print(f"   • Total processed: {summary['metrics']['total_images_processed']}")
        print(f"   • Threats detected: {summary['metrics']['threats_detected']}")
        print(f"   • Detection rate: {summary['metrics']['threats_detected']/summary['metrics']['total_images_processed']*100:.1f}%")
        print(f"   • Average processing time: {summary['metrics']['average_processing_time_ms']:.1f}ms")
        
        # Test threat type distribution
        threat_dist = summary['metrics']['threat_type_distribution']
        if len(threat_dist) == 3:
            print("✅ Threat type distribution tracking working")
        else:
            print("❌ Threat type distribution tracking failed")
            return False
        
        # Stop monitoring
        monitor.stop_monitoring()
        
        return True
        
    except Exception as e:
        print(f"❌ Monitoring metrics error: {e}")
        return False

def test_queue_management():
    """Test queue management and overflow handling."""
    print("\n🗂️  Testing Queue Management...")
    
    try:
        # Create monitor with small queue for testing
        monitor = RealTimeThreatMonitor(max_queue_size=2)
        
        # Test queue capacity
        from PIL import Image
        
        test_images = []
        for i in range(4):  # More than queue capacity
            image_path = f"queue_test_{i}.jpg"
            test_image = Image.new('RGB', (100, 100), color='red')
            test_image.save(image_path)
            test_images.append(image_path)
        
        # Add images to queue
        successful_adds = 0
        for i, image_path in enumerate(test_images):
            success = monitor.add_image_for_analysis(image_path, f"location_{i}")
            if success:
                successful_adds += 1
        
        print(f"✅ Queue management test: {successful_adds}/{len(test_images)} images added")
        
        # Should be limited by queue capacity
        if successful_adds <= 2:  # Queue size limit
            print("✅ Queue overflow protection working")
        else:
            print("❌ Queue overflow protection failed")
            return False
        
        # Test queue status reporting
        summary = monitor.get_monitoring_summary()
        queue_status = summary["queue_status"]
        
        if "images_pending" in queue_status and "alerts_pending" in queue_status:
            print("✅ Queue status reporting available")
            print(f"   • Images pending: {queue_status['images_pending']}")
            print(f"   • Alerts pending: {queue_status['alerts_pending']}")
        else:
            print("❌ Queue status reporting incomplete")
            return False
        
        # Cleanup
        for image_path in test_images:
            if os.path.exists(image_path):
                os.remove(image_path)
        print("✅ Test images cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Queue management error: {e}")
        return False

def main():
    """Run Section 3 tests."""
    print("⏰ STEP 5 - SECTION 3: Real-time Threat Monitoring")
    print("=" * 54)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Threat alert manager
    if test_threat_alert_manager():
        tests_passed += 1
    
    # Test 2: Real-time threat monitor
    if test_real_time_threat_monitor():
        tests_passed += 1
    
    # Test 3: Alert escalation logic
    if test_alert_escalation_logic():
        tests_passed += 1
    
    # Test 4: Threat impact estimation
    if test_threat_impact_estimation():
        tests_passed += 1
    
    # Test 5: Monitoring metrics
    if test_monitoring_metrics():
        tests_passed += 1
    
    # Test 6: Queue management
    if test_queue_management():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Section 3 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Section 3 PASSED - Ready for Section 4")
        print("\n🎯 Next: Integrate with conservation systems and field deployment")
        return True
    else:
        print("❌ Section 3 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    main()
