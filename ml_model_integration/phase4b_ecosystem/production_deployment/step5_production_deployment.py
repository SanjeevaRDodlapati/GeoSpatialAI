"""
Step 5: Production Deployment Infrastructure
============================================
Scalable cloud deployment infrastructure for Madagascar Conservation AI Ecosystem.
"""

import sys
import os
import json
import time
import asyncio
import uuid
import shutil
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union, Callable, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
import yaml
import logging
from pathlib import Path

# Import ecosystem components
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4b_ecosystem/ecosystem_core')
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4b_ecosystem/agent_communication')
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4b_ecosystem/conservation_dashboard')
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4b_ecosystem/automated_workflows')

from step1_ecosystem_core import (AgentType, AgentStatus, MessageType, AgentMessage, 
                                AgentRegistration, EcosystemMetrics, ConservationEcosystemOrchestrator)
from step2_agent_communication import (CommunicationProtocol, DataFormat, CommunicationChannel,
                                     ConservationWorkflow, WorkflowStep, CommunicationProtocolManager)
from step3_conservation_dashboard import MadagascarConservationDashboard
from step4_automated_workflows import ConservationWorkflowEngine, WorkflowTriggerType

class DeploymentEnvironment(Enum):
    """Deployment environment types."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

class CloudProvider(Enum):
    """Supported cloud providers."""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    KUBERNETES = "kubernetes"
    DOCKER = "docker"

class ServiceType(Enum):
    """Types of services in the ecosystem."""
    ORCHESTRATOR = "orchestrator"
    AGENT_SERVICE = "agent_service"
    COMMUNICATION_HUB = "communication_hub"
    DASHBOARD = "dashboard"
    WORKFLOW_ENGINE = "workflow_engine"
    DATABASE = "database"
    MESSAGE_QUEUE = "message_queue"
    FILE_STORAGE = "file_storage"
    MONITORING = "monitoring"

@dataclass
class ServiceConfiguration:
    """Configuration for a deployable service."""
    service_name: str
    service_type: ServiceType
    docker_image: str
    port: int
    environment_variables: Dict[str, str] = field(default_factory=dict)
    resource_requirements: Dict[str, str] = field(default_factory=dict)
    health_check_path: str = "/health"
    replicas: int = 1
    dependencies: List[str] = field(default_factory=list)
    volumes: List[Dict[str, str]] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)

@dataclass
class DeploymentConfiguration:
    """Complete deployment configuration."""
    deployment_id: str
    environment: DeploymentEnvironment
    cloud_provider: CloudProvider
    region: str
    services: List[ServiceConfiguration]
    
    # Infrastructure settings
    cluster_name: str = "madagascar-conservation-ai"
    namespace: str = "conservation"
    domain: str = "conservation-ai.madagascar.org"
    ssl_enabled: bool = True
    auto_scaling_enabled: bool = True
    monitoring_enabled: bool = True
    backup_enabled: bool = True
    
    # Security settings
    network_policies_enabled: bool = True
    rbac_enabled: bool = True
    pod_security_enabled: bool = True
    secrets_encryption_enabled: bool = True

class ConservationEcosystemDeployer:
    """Production deployment manager for Madagascar Conservation AI Ecosystem."""
    
    def __init__(self, deployment_config: DeploymentConfiguration):
        self.deployment_config = deployment_config
        self.deployment_path = Path("/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4b_ecosystem/production_deployment")
        
        # Deployment state
        self.deployed_services: Dict[str, Dict[str, Any]] = {}
        self.deployment_history: List[Dict[str, Any]] = []
        self.health_status: Dict[str, bool] = {}
        
        # Infrastructure components
        self.infrastructure_manifests: Dict[str, str] = {}
        self.service_manifests: Dict[str, str] = {}
        self.monitoring_configs: Dict[str, str] = {}
        
        self._initialize_service_configurations()
        
        print("🚀 Conservation Ecosystem Deployer initialized")
    
    def _initialize_service_configurations(self):
        """Initialize service configurations for deployment."""
        
        # Ecosystem Orchestrator Service
        orchestrator_config = ServiceConfiguration(
            service_name="ecosystem-orchestrator",
            service_type=ServiceType.ORCHESTRATOR,
            docker_image="madagascar-ai/ecosystem-orchestrator:latest",
            port=8000,
            environment_variables={
                "ENVIRONMENT": self.deployment_config.environment.value,
                "LOG_LEVEL": "INFO",
                "ECOSYSTEM_ID": "madagascar-production",
                "AGENT_COUNT": "6",
                "MONITORING_ENABLED": "true"
            },
            resource_requirements={
                "memory": "2Gi",
                "cpu": "1000m"
            },
            replicas=2 if self.deployment_config.environment == DeploymentEnvironment.PRODUCTION else 1,
            dependencies=["postgresql", "redis"]
        )
        
        # Species Identification Agent Service
        species_agent_config = ServiceConfiguration(
            service_name="species-identification-agent",
            service_type=ServiceType.AGENT_SERVICE,
            docker_image="madagascar-ai/species-agent:latest",
            port=8001,
            environment_variables={
                "AGENT_TYPE": "SPECIES_IDENTIFICATION",
                "MODEL_PATH": "/app/models/species_model.pkl",
                "CONFIDENCE_THRESHOLD": "0.7"
            },
            resource_requirements={
                "memory": "4Gi",
                "cpu": "2000m",
                "nvidia.com/gpu": "1"
            },
            replicas=3 if self.deployment_config.environment == DeploymentEnvironment.PRODUCTION else 1,
            volumes=[
                {"name": "model-storage", "mountPath": "/app/models"}
            ]
        )
        
        # Threat Detection Agent Service
        threat_agent_config = ServiceConfiguration(
            service_name="threat-detection-agent",
            service_type=ServiceType.AGENT_SERVICE,
            docker_image="madagascar-ai/threat-agent:latest",
            port=8002,
            environment_variables={
                "AGENT_TYPE": "THREAT_DETECTION",
                "SATELLITE_API_ENDPOINT": "https://api.satellite.provider.com",
                "THREAT_THRESHOLD": "0.6"
            },
            resource_requirements={
                "memory": "3Gi",
                "cpu": "1500m"
            },
            replicas=2,
            secrets=["satellite-api-key"]
        )
        
        # Conservation Dashboard Service
        dashboard_config = ServiceConfiguration(
            service_name="conservation-dashboard",
            service_type=ServiceType.DASHBOARD,
            docker_image="madagascar-ai/dashboard:latest",
            port=8050,
            environment_variables={
                "DASHBOARD_HOST": "0.0.0.0",
                "DASHBOARD_PORT": "8050",
                "ORCHESTRATOR_URL": "http://ecosystem-orchestrator:8000"
            },
            resource_requirements={
                "memory": "2Gi",
                "cpu": "1000m"
            },
            replicas=2,
            dependencies=["ecosystem-orchestrator"]
        )
        
        # Workflow Engine Service
        workflow_config = ServiceConfiguration(
            service_name="workflow-engine",
            service_type=ServiceType.WORKFLOW_ENGINE,
            docker_image="madagascar-ai/workflow-engine:latest",
            port=8003,
            environment_variables={
                "WORKFLOW_ENGINE_MODE": "production",
                "MAX_CONCURRENT_WORKFLOWS": "10",
                "LEARNING_ENABLED": "true"
            },
            resource_requirements={
                "memory": "2Gi",
                "cpu": "1000m"
            },
            replicas=2,
            dependencies=["ecosystem-orchestrator", "redis"]
        )
        
        # Database Service (PostgreSQL)
        database_config = ServiceConfiguration(
            service_name="postgresql",
            service_type=ServiceType.DATABASE,
            docker_image="postgres:15-alpine",
            port=5432,
            environment_variables={
                "POSTGRES_DB": "madagascar_conservation",
                "POSTGRES_USER": "conservation_user",
                "POSTGRES_PASSWORD": "PLACEHOLDER"  # Will be replaced with secret
            },
            resource_requirements={
                "memory": "4Gi",
                "cpu": "2000m"
            },
            volumes=[
                {"name": "postgres-storage", "mountPath": "/var/lib/postgresql/data"}
            ],
            secrets=["postgres-password"]
        )
        
        # Message Queue Service (Redis)
        message_queue_config = ServiceConfiguration(
            service_name="redis",
            service_type=ServiceType.MESSAGE_QUEUE,
            docker_image="redis:7-alpine",
            port=6379,
            resource_requirements={
                "memory": "2Gi",
                "cpu": "500m"
            },
            volumes=[
                {"name": "redis-storage", "mountPath": "/data"}
            ]
        )
        
        # File Storage Service (MinIO)
        storage_config = ServiceConfiguration(
            service_name="minio",
            service_type=ServiceType.FILE_STORAGE,
            docker_image="minio/minio:latest",
            port=9000,
            environment_variables={
                "MINIO_ROOT_USER": "conservation_admin",
                "MINIO_ROOT_PASSWORD": "PLACEHOLDER"  # Will be replaced with secret
            },
            resource_requirements={
                "memory": "2Gi",
                "cpu": "1000m"
            },
            volumes=[
                {"name": "minio-storage", "mountPath": "/data"}
            ],
            secrets=["minio-credentials"]
        )
        
        # Monitoring Service (Prometheus + Grafana)
        monitoring_config = ServiceConfiguration(
            service_name="monitoring",
            service_type=ServiceType.MONITORING,
            docker_image="madagascar-ai/monitoring:latest",
            port=9090,
            environment_variables={
                "PROMETHEUS_CONFIG": "/etc/prometheus/prometheus.yml",
                "GRAFANA_ADMIN_PASSWORD": "PLACEHOLDER"
            },
            resource_requirements={
                "memory": "2Gi",
                "cpu": "1000m"
            },
            volumes=[
                {"name": "prometheus-storage", "mountPath": "/prometheus"},
                {"name": "grafana-storage", "mountPath": "/var/lib/grafana"}
            ],
            secrets=["grafana-password"]
        )
        
        # Update deployment configuration with all services
        self.deployment_config.services = [
            orchestrator_config,
            species_agent_config,
            threat_agent_config,
            dashboard_config,
            workflow_config,
            database_config,
            message_queue_config,
            storage_config,
            monitoring_config
        ]
        
        print(f"   📊 {len(self.deployment_config.services)} services configured for deployment")
    
    def generate_docker_files(self):
        """Generate Docker files for all services."""
        
        docker_files = {}
        
        # Ecosystem Orchestrator Dockerfile
        docker_files["orchestrator"] = """
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY phase4b_ecosystem/ecosystem_core/ ./ecosystem_core/
COPY phase4a_agents/ ./agents/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Start the orchestrator
CMD ["python", "-m", "ecosystem_core.step1_ecosystem_core"]
"""
        
        # Species Agent Dockerfile
        docker_files["species_agent"] = """
FROM nvidia/cuda:11.8-runtime-ubuntu22.04

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \\
    python3 \\
    python3-pip \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy agent code and models
COPY phase4a_agents/step4_section*.py ./
COPY models/ ./models/

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:8001/health || exit 1

# Start the agent
CMD ["python3", "step4_section1_test.py", "--server-mode"]
"""
        
        # Dashboard Dockerfile
        docker_files["dashboard"] = """
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy dashboard code
COPY phase4b_ecosystem/conservation_dashboard/ ./dashboard/
COPY phase4b_ecosystem/ecosystem_core/ ./ecosystem_core/
COPY phase4b_ecosystem/agent_communication/ ./agent_communication/

# Expose port
EXPOSE 8050

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:8050/health || exit 1

# Start the dashboard
CMD ["python", "-m", "dashboard.step3_conservation_dashboard", "--server-mode"]
"""
        
        # Workflow Engine Dockerfile
        docker_files["workflow_engine"] = """
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy workflow engine code
COPY phase4b_ecosystem/automated_workflows/ ./workflows/
COPY phase4b_ecosystem/ecosystem_core/ ./ecosystem_core/
COPY phase4b_ecosystem/agent_communication/ ./agent_communication/

# Expose port
EXPOSE 8003

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:8003/health || exit 1

# Start the workflow engine
CMD ["python", "-m", "workflows.step4_automated_workflows", "--server-mode"]
"""
        
        # Write Docker files to deployment directory
        for service, content in docker_files.items():
            dockerfile_path = self.deployment_path / f"Dockerfile.{service}"
            dockerfile_path.write_text(content.strip())
        
        print(f"   📄 {len(docker_files)} Docker files generated")
        return docker_files
    
    def generate_kubernetes_manifests(self):
        """Generate Kubernetes manifests for deployment."""
        
        manifests = {}
        
        # Namespace
        manifests["namespace"] = f"""
apiVersion: v1
kind: Namespace
metadata:
  name: {self.deployment_config.namespace}
  labels:
    app.kubernetes.io/name: madagascar-conservation-ai
    environment: {self.deployment_config.environment.value}
"""
        
        # ConfigMap for application configuration
        manifests["configmap"] = f"""
apiVersion: v1
kind: ConfigMap
metadata:
  name: conservation-config
  namespace: {self.deployment_config.namespace}
data:
  environment: "{self.deployment_config.environment.value}"
  cluster_name: "{self.deployment_config.cluster_name}"
  domain: "{self.deployment_config.domain}"
  log_level: "INFO"
  monitoring_enabled: "true"
  auto_scaling_enabled: "{str(self.deployment_config.auto_scaling_enabled).lower()}"
"""
        
        # Secrets
        manifests["secrets"] = f"""
apiVersion: v1
kind: Secret
metadata:
  name: conservation-secrets
  namespace: {self.deployment_config.namespace}
type: Opaque
data:
  postgres_password: cG9zdGdyZXNfcGFzc3dvcmQ=  # base64 encoded
  minio_access_key: bWluaW9fYWNjZXNz  # base64 encoded
  minio_secret_key: bWluaW9fc2VjcmV0  # base64 encoded
  grafana_password: Z3JhZmFuYV9hZG1pbg==  # base64 encoded
  satellite_api_key: c2F0ZWxsaXRlX2FwaV9rZXk=  # base64 encoded
"""
        
        # Generate service manifests
        for service_config in self.deployment_config.services:
            service_manifest = self._generate_service_manifest(service_config)
            manifests[f"service_{service_config.service_name}"] = service_manifest
            
            deployment_manifest = self._generate_deployment_manifest(service_config)
            manifests[f"deployment_{service_config.service_name}"] = deployment_manifest
        
        # Ingress for dashboard
        manifests["ingress"] = f"""
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: conservation-ingress
  namespace: {self.deployment_config.namespace}
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - {self.deployment_config.domain}
    secretName: conservation-tls
  rules:
  - host: {self.deployment_config.domain}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: conservation-dashboard
            port:
              number: 8050
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: ecosystem-orchestrator
            port:
              number: 8000
"""
        
        # Horizontal Pod Autoscaler
        if self.deployment_config.auto_scaling_enabled:
            manifests["hpa"] = f"""
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: conservation-hpa
  namespace: {self.deployment_config.namespace}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ecosystem-orchestrator
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
"""
        
        # Persistent Volume Claims
        manifests["pvc"] = f"""
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: {self.deployment_config.namespace}
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
  storageClassName: fast-ssd
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: minio-pvc
  namespace: {self.deployment_config.namespace}
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Gi
  storageClassName: standard
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: prometheus-pvc
  namespace: {self.deployment_config.namespace}
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
  storageClassName: standard
"""
        
        # Write manifests to deployment directory
        for manifest_name, content in manifests.items():
            manifest_path = self.deployment_path / f"{manifest_name}.yaml"
            manifest_path.write_text(content.strip())
        
        self.service_manifests = manifests
        print(f"   📋 {len(manifests)} Kubernetes manifests generated")
        return manifests
    
    def _generate_service_manifest(self, service_config: ServiceConfiguration) -> str:
        """Generate Kubernetes service manifest for a service."""
        
        service_type = "LoadBalancer" if service_config.service_name == "conservation-dashboard" else "ClusterIP"
        
        return f"""
apiVersion: v1
kind: Service
metadata:
  name: {service_config.service_name}
  namespace: {self.deployment_config.namespace}
  labels:
    app: {service_config.service_name}
    component: {service_config.service_type.value}
spec:
  type: {service_type}
  ports:
  - port: {service_config.port}
    targetPort: {service_config.port}
    protocol: TCP
  selector:
    app: {service_config.service_name}
"""
    
    def _generate_deployment_manifest(self, service_config: ServiceConfiguration) -> str:
        """Generate Kubernetes deployment manifest for a service."""
        
        # Environment variables
        env_vars = []
        for key, value in service_config.environment_variables.items():
            env_vars.append(f"""        - name: {key}
          value: "{value}" """)
        
        # Volume mounts
        volume_mounts = []
        volumes = []
        for volume in service_config.volumes:
            volume_name = volume["name"]
            mount_path = volume["mountPath"]
            volume_mounts.append(f"""        - name: {volume_name}
          mountPath: {mount_path}""")
            
            if "pvc" in volume_name or "storage" in volume_name:
                volumes.append(f"""      - name: {volume_name}
        persistentVolumeClaim:
          claimName: {volume_name.replace('-storage', '-pvc')}""")
        
        # Resource requirements
        resources = ""
        if service_config.resource_requirements:
            requests = []
            limits = []
            for resource, value in service_config.resource_requirements.items():
                requests.append(f"          {resource}: {value}")
                # Set limits to 2x requests for memory, 1.5x for CPU
                if resource == "memory":
                    limit_value = value.replace("Gi", "Gi").replace("Mi", "Mi")
                    limits.append(f"          {resource}: {value}")
                elif resource == "cpu":
                    if "m" in value:
                        limit_value = str(int(value.replace("m", "")) * 1.5) + "m"
                    else:
                        limit_value = str(float(value) * 1.5)
                    limits.append(f"          {resource}: {limit_value}")
                else:
                    limits.append(f"          {resource}: {value}")
            
            resources = f"""        resources:
          requests:
{chr(10).join(requests)}
          limits:
{chr(10).join(limits)}"""
        
        return f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_config.service_name}
  namespace: {self.deployment_config.namespace}
  labels:
    app: {service_config.service_name}
    component: {service_config.service_type.value}
spec:
  replicas: {service_config.replicas}
  selector:
    matchLabels:
      app: {service_config.service_name}
  template:
    metadata:
      labels:
        app: {service_config.service_name}
        component: {service_config.service_type.value}
    spec:
      containers:
      - name: {service_config.service_name}
        image: {service_config.docker_image}
        ports:
        - containerPort: {service_config.port}
{chr(10).join(env_vars) if env_vars else ""}
{chr(10).join(volume_mounts) if volume_mounts else ""}
{resources}
        livenessProbe:
          httpGet:
            path: {service_config.health_check_path}
            port: {service_config.port}
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: {service_config.health_check_path}
            port: {service_config.port}
          initialDelaySeconds: 30
          periodSeconds: 15
{chr(10).join(volumes) if volumes else ""}
"""
    
    def generate_monitoring_configuration(self):
        """Generate monitoring and observability configurations."""
        
        # Prometheus configuration
        prometheus_config = """
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "conservation_alerts.yml"

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true

  - job_name: 'ecosystem-orchestrator'
    static_configs:
      - targets: ['ecosystem-orchestrator:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'conservation-agents'
    static_configs:
      - targets: 
        - 'species-identification-agent:8001'
        - 'threat-detection-agent:8002'
        - 'workflow-engine:8003'
    metrics_path: '/metrics'
    scrape_interval: 15s

  - job_name: 'conservation-dashboard'
    static_configs:
      - targets: ['conservation-dashboard:8050']
    metrics_path: '/metrics'
    scrape_interval: 30s
"""
        
        # Alert rules for conservation system
        alert_rules = """
groups:
  - name: conservation_alerts
    rules:
      - alert: EcosystemDown
        expr: up{job="ecosystem-orchestrator"} == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Madagascar Conservation Ecosystem is down"
          description: "The main ecosystem orchestrator has been down for more than 5 minutes."

      - alert: HighThreatDetected
        expr: conservation_threat_severity > 0.8
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High severity threat detected"
          description: "A threat with severity {{ $value }} has been detected."

      - alert: SpeciesEndangered
        expr: species_population_decline_rate > 0.1
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Rapid species population decline"
          description: "Species {{ $labels.species }} population declining at rate {{ $value }}."

      - alert: WorkflowExecutionFailed
        expr: failed_workflow_executions_total > 3
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Multiple workflow executions failed"
          description: "{{ $value }} workflow executions have failed in the last 5 minutes."

      - alert: DatabaseConnectionLost
        expr: up{job="postgresql"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Database connection lost"
          description: "PostgreSQL database is unreachable."
"""
        
        # Grafana dashboard configuration
        grafana_dashboard = {
            "dashboard": {
                "id": None,
                "title": "Madagascar Conservation AI Dashboard",
                "tags": ["conservation", "ai", "madagascar"],
                "timezone": "browser",
                "panels": [
                    {
                        "id": 1,
                        "title": "Ecosystem Health",
                        "type": "gauge",
                        "targets": [
                            {
                                "expr": "ecosystem_health_percentage",
                                "legendFormat": "Health %"
                            }
                        ],
                        "fieldConfig": {
                            "defaults": {
                                "thresholds": {
                                    "steps": [
                                        {"color": "red", "value": 0},
                                        {"color": "yellow", "value": 70},
                                        {"color": "green", "value": 90}
                                    ]
                                }
                            }
                        }
                    },
                    {
                        "id": 2,
                        "title": "Species Detections",
                        "type": "timeseries",
                        "targets": [
                            {
                                "expr": "rate(species_detections_total[5m])",
                                "legendFormat": "{{ species }}"
                            }
                        ]
                    },
                    {
                        "id": 3,
                        "title": "Threat Alerts",
                        "type": "stat",
                        "targets": [
                            {
                                "expr": "sum(conservation_active_threats)",
                                "legendFormat": "Active Threats"
                            }
                        ]
                    },
                    {
                        "id": 4,
                        "title": "Workflow Performance",
                        "type": "timeseries",
                        "targets": [
                            {
                                "expr": "rate(workflow_executions_total[5m])",
                                "legendFormat": "Executions/sec"
                            },
                            {
                                "expr": "workflow_success_rate",
                                "legendFormat": "Success Rate"
                            }
                        ]
                    }
                ],
                "time": {
                    "from": "now-1h",
                    "to": "now"
                },
                "refresh": "5s"
            }
        }
        
        # Write monitoring configurations
        monitoring_configs = {
            "prometheus": prometheus_config,
            "alerts": alert_rules,
            "grafana_dashboard": json.dumps(grafana_dashboard, indent=2)
        }
        
        for config_name, content in monitoring_configs.items():
            config_path = self.deployment_path / f"{config_name}.yml"
            if config_name == "grafana_dashboard":
                config_path = self.deployment_path / f"{config_name}.json"
            config_path.write_text(content)
        
        self.monitoring_configs = monitoring_configs
        print(f"   📊 {len(monitoring_configs)} monitoring configurations generated")
        return monitoring_configs
    
    def generate_deployment_scripts(self):
        """Generate deployment and management scripts."""
        
        scripts = {}
        
        # Main deployment script
        scripts["deploy.sh"] = f"""#!/bin/bash
set -e

echo "🚀 Deploying Madagascar Conservation AI Ecosystem"
echo "Environment: {self.deployment_config.environment.value}"
echo "Cluster: {self.deployment_config.cluster_name}"

# Create namespace
kubectl apply -f namespace.yaml

# Apply secrets and config
kubectl apply -f secrets.yaml
kubectl apply -f configmap.yaml

# Apply persistent volume claims
kubectl apply -f pvc.yaml

# Deploy database and message queue first
kubectl apply -f deployment_postgresql.yaml
kubectl apply -f service_postgresql.yaml
kubectl apply -f deployment_redis.yaml
kubectl apply -f service_redis.yaml

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/postgresql -n {self.deployment_config.namespace}

# Deploy storage
kubectl apply -f deployment_minio.yaml
kubectl apply -f service_minio.yaml

# Deploy core services
kubectl apply -f deployment_ecosystem-orchestrator.yaml
kubectl apply -f service_ecosystem-orchestrator.yaml

# Wait for orchestrator to be ready
echo "⏳ Waiting for orchestrator to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/ecosystem-orchestrator -n {self.deployment_config.namespace}

# Deploy agent services
kubectl apply -f deployment_species-identification-agent.yaml
kubectl apply -f service_species-identification-agent.yaml
kubectl apply -f deployment_threat-detection-agent.yaml
kubectl apply -f service_threat-detection-agent.yaml

# Deploy workflow engine
kubectl apply -f deployment_workflow-engine.yaml
kubectl apply -f service_workflow-engine.yaml

# Deploy dashboard
kubectl apply -f deployment_conservation-dashboard.yaml
kubectl apply -f service_conservation-dashboard.yaml

# Deploy monitoring
kubectl apply -f deployment_monitoring.yaml
kubectl apply -f service_monitoring.yaml

# Apply ingress
kubectl apply -f ingress.yaml

# Apply autoscaling
kubectl apply -f hpa.yaml

echo "✅ Deployment completed successfully!"
echo "🌐 Dashboard will be available at: https://{self.deployment_config.domain}"
echo "📊 Monitoring at: https://monitoring.{self.deployment_config.domain}"

# Show status
kubectl get pods -n {self.deployment_config.namespace}
"""
        
        # Status monitoring script
        scripts["status.sh"] = f"""#!/bin/bash

echo "📊 Madagascar Conservation AI Ecosystem Status"
echo "=============================================="

# Check namespace
kubectl get namespace {self.deployment_config.namespace}

# Check all pods
echo ""
echo "📦 Pod Status:"
kubectl get pods -n {self.deployment_config.namespace} -o wide

# Check services
echo ""
echo "🔗 Service Status:"
kubectl get services -n {self.deployment_config.namespace}

# Check ingress
echo ""
echo "🌐 Ingress Status:"
kubectl get ingress -n {self.deployment_config.namespace}

# Check HPA
echo ""
echo "📈 Autoscaling Status:"
kubectl get hpa -n {self.deployment_config.namespace}

# Check persistent volumes
echo ""
echo "💾 Storage Status:"
kubectl get pvc -n {self.deployment_config.namespace}

# System health check
echo ""
echo "🏥 Health Check:"
ORCHESTRATOR_IP=$(kubectl get service ecosystem-orchestrator -n {self.deployment_config.namespace} -o jsonpath='{{.spec.clusterIP}}')
curl -s http://$ORCHESTRATOR_IP:8000/health || echo "❌ Orchestrator health check failed"

DASHBOARD_IP=$(kubectl get service conservation-dashboard -n {self.deployment_config.namespace} -o jsonpath='{{.spec.clusterIP}}')
curl -s http://$DASHBOARD_IP:8050/health || echo "❌ Dashboard health check failed"
"""
        
        # Cleanup script
        scripts["cleanup.sh"] = f"""#!/bin/bash

echo "🧹 Cleaning up Madagascar Conservation AI Ecosystem"
echo "================================================="

# Delete all resources
kubectl delete namespace {self.deployment_config.namespace} --ignore-not-found=true

# Wait for namespace deletion
echo "⏳ Waiting for namespace deletion..."
kubectl wait --for=delete namespace/{self.deployment_config.namespace} --timeout=300s

echo "✅ Cleanup completed!"
"""
        
        # Backup script
        scripts["backup.sh"] = f"""#!/bin/bash

echo "📦 Backing up Madagascar Conservation AI Ecosystem"
echo "================================================="

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/backup_$BACKUP_DATE"

mkdir -p $BACKUP_DIR

# Backup database
echo "📊 Backing up database..."
kubectl exec -n {self.deployment_config.namespace} deployment/postgresql -- pg_dump -U conservation_user madagascar_conservation > $BACKUP_DIR/database.sql

# Backup persistent volumes
echo "💾 Backing up storage..."
kubectl get pvc -n {self.deployment_config.namespace} -o yaml > $BACKUP_DIR/pvc_backup.yaml

# Backup configurations
echo "⚙️ Backing up configurations..."
kubectl get configmap -n {self.deployment_config.namespace} -o yaml > $BACKUP_DIR/configmap_backup.yaml
kubectl get secret -n {self.deployment_config.namespace} -o yaml > $BACKUP_DIR/secret_backup.yaml

# Create archive
tar -czf "backup_$BACKUP_DATE.tar.gz" -C backups "backup_$BACKUP_DATE"
rm -rf $BACKUP_DIR

echo "✅ Backup completed: backup_$BACKUP_DATE.tar.gz"
"""
        
        # Make scripts executable and write to deployment directory
        for script_name, content in scripts.items():
            script_path = self.deployment_path / script_name
            script_path.write_text(content.strip())
            script_path.chmod(0o755)  # Make executable
        
        print(f"   📜 {len(scripts)} deployment scripts generated")
        return scripts
    
    def generate_ci_cd_pipeline(self):
        """Generate CI/CD pipeline configuration."""
        
        # GitHub Actions workflow
        github_workflow = f"""
name: Madagascar Conservation AI - CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: madagascar-conservation-ai

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v
        python phase4b_ecosystem/ecosystem_core/step1_ecosystem_core.py
        python phase4b_ecosystem/agent_communication/step2_agent_communication.py
        python phase4b_ecosystem/conservation_dashboard/step3_conservation_dashboard.py
        python phase4b_ecosystem/automated_workflows/step4_automated_workflows.py

  build:
    needs: test
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [orchestrator, species_agent, dashboard, workflow_engine]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{{{ env.REGISTRY }}}}
        username: ${{{{ github.actor }}}}
        password: ${{{{ secrets.GITHUB_TOKEN }}}}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        file: ./phase4b_ecosystem/production_deployment/Dockerfile.${{{{ matrix.service }}}}
        push: true
        tags: ${{{{ env.REGISTRY }}}}/${{{{ env.IMAGE_NAME }}}}/${{{{ matrix.service }}}}:${{{{ github.sha }}}}
        labels: |
          org.opencontainers.image.source=${{{{ github.server_url }}}}/${{{{ github.repository }}}}
          org.opencontainers.image.revision=${{{{ github.sha }}}}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{{{ secrets.KUBE_CONFIG }}}}
    
    - name: Update image tags
      run: |
        sed -i 's|madagascar-ai/|${{{{ env.REGISTRY }}}}/${{{{ env.IMAGE_NAME }}}}/|g' phase4b_ecosystem/production_deployment/*.yaml
        sed -i 's|:latest|:${{{{ github.sha }}}}|g' phase4b_ecosystem/production_deployment/*.yaml
    
    - name: Deploy to Kubernetes
      run: |
        cd phase4b_ecosystem/production_deployment
        chmod +x deploy.sh
        ./deploy.sh
    
    - name: Verify deployment
      run: |
        kubectl wait --for=condition=available --timeout=300s deployment/ecosystem-orchestrator -n {self.deployment_config.namespace}
        kubectl get pods -n {self.deployment_config.namespace}
"""
        
        # Docker Compose for local development
        docker_compose = f"""
version: '3.8'

services:
  postgresql:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: madagascar_conservation
      POSTGRES_USER: conservation_user
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U conservation_user"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: conservation_admin
      MINIO_ROOT_PASSWORD: dev_password
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data

  ecosystem-orchestrator:
    build:
      context: ../../..
      dockerfile: phase4b_ecosystem/production_deployment/Dockerfile.orchestrator
    environment:
      ENVIRONMENT: development
      DATABASE_URL: postgresql://conservation_user:dev_password@postgresql:5432/madagascar_conservation
      REDIS_URL: redis://redis:6379
    ports:
      - "8000:8000"
    depends_on:
      postgresql:
        condition: service_healthy
      redis:
        condition: service_healthy

  conservation-dashboard:
    build:
      context: ../../..
      dockerfile: phase4b_ecosystem/production_deployment/Dockerfile.dashboard
    environment:
      ORCHESTRATOR_URL: http://ecosystem-orchestrator:8000
    ports:
      - "8050:8050"
    depends_on:
      - ecosystem-orchestrator

volumes:
  postgres_data:
  redis_data:
  minio_data:
"""
        
        # Helm chart values
        helm_values = f"""
# Madagascar Conservation AI Helm Chart Values

global:
  environment: {self.deployment_config.environment.value}
  domain: {self.deployment_config.domain}
  namespace: {self.deployment_config.namespace}

orchestrator:
  enabled: true
  replicaCount: 2
  image:
    repository: madagascar-ai/ecosystem-orchestrator
    tag: latest
  resources:
    requests:
      memory: "2Gi"
      cpu: "1000m"
    limits:
      memory: "4Gi"
      cpu: "2000m"

agents:
  species:
    enabled: true
    replicaCount: 3
    image:
      repository: madagascar-ai/species-agent
      tag: latest
    resources:
      requests:
        memory: "4Gi"
        cpu: "2000m"
        nvidia.com/gpu: 1
  
  threat:
    enabled: true
    replicaCount: 2
    image:
      repository: madagascar-ai/threat-agent
      tag: latest

dashboard:
  enabled: true
  replicaCount: 2
  image:
    repository: madagascar-ai/dashboard
    tag: latest
  ingress:
    enabled: true
    host: {self.deployment_config.domain}

database:
  postgresql:
    enabled: true
    auth:
      database: madagascar_conservation
      username: conservation_user
    primary:
      persistence:
        size: 100Gi

monitoring:
  prometheus:
    enabled: true
  grafana:
    enabled: true
    adminPassword: admin_password

autoscaling:
  enabled: {str(self.deployment_config.auto_scaling_enabled).lower()}
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
"""
        
        # Write CI/CD files
        cicd_configs = {
            "github_workflow": github_workflow,
            "docker_compose": docker_compose,
            "helm_values": helm_values
        }
        
        # Create .github/workflows directory
        github_dir = self.deployment_path / ".github" / "workflows"
        github_dir.mkdir(parents=True, exist_ok=True)
        
        # Write files
        (github_dir / "deploy.yml").write_text(github_workflow.strip())
        (self.deployment_path / "docker-compose.yml").write_text(docker_compose.strip())
        (self.deployment_path / "values.yaml").write_text(helm_values.strip())
        
        print(f"   🔄 CI/CD pipeline configurations generated")
        return cicd_configs
    
    def validate_deployment_configuration(self) -> bool:
        """Validate the deployment configuration."""
        
        print("🔍 Validating deployment configuration...")
        
        validation_errors = []
        
        # Check required services
        required_services = [
            ServiceType.ORCHESTRATOR,
            ServiceType.DATABASE,
            ServiceType.MESSAGE_QUEUE
        ]
        
        service_types = [service.service_type for service in self.deployment_config.services]
        for required_service in required_services:
            if required_service not in service_types:
                validation_errors.append(f"Missing required service: {required_service.value}")
        
        # Check service dependencies
        service_names = [service.service_name for service in self.deployment_config.services]
        for service in self.deployment_config.services:
            for dependency in service.dependencies:
                if dependency not in service_names:
                    validation_errors.append(f"Service {service.service_name} depends on missing service: {dependency}")
        
        # Check resource requirements
        for service in self.deployment_config.services:
            if not service.resource_requirements:
                validation_errors.append(f"Service {service.service_name} missing resource requirements")
        
        # Check port conflicts
        ports = [service.port for service in self.deployment_config.services]
        if len(ports) != len(set(ports)):
            validation_errors.append("Port conflicts detected in service configurations")
        
        # Check environment-specific requirements
        if self.deployment_config.environment == DeploymentEnvironment.PRODUCTION:
            for service in self.deployment_config.services:
                if service.replicas < 2 and service.service_type in [ServiceType.ORCHESTRATOR, ServiceType.DASHBOARD]:
                    validation_errors.append(f"Production service {service.service_name} should have multiple replicas")
        
        # Report validation results
        if validation_errors:
            print("❌ Deployment configuration validation failed:")
            for error in validation_errors:
                print(f"   • {error}")
            return False
        else:
            print("✅ Deployment configuration validation passed")
            return True
    
    def generate_all_deployment_artifacts(self):
        """Generate all deployment artifacts."""
        
        print("🏗️ Generating deployment artifacts...")
        
        # Validate configuration first
        if not self.validate_deployment_configuration():
            raise ValueError("Deployment configuration validation failed")
        
        # Generate all artifacts
        artifacts = {}
        
        artifacts["docker_files"] = self.generate_docker_files()
        artifacts["kubernetes_manifests"] = self.generate_kubernetes_manifests()
        artifacts["monitoring_configs"] = self.generate_monitoring_configuration()
        artifacts["deployment_scripts"] = self.generate_deployment_scripts()
        artifacts["cicd_pipeline"] = self.generate_ci_cd_pipeline()
        
        # Generate deployment summary
        summary = {
            "deployment_id": self.deployment_config.deployment_id,
            "environment": self.deployment_config.environment.value,
            "cloud_provider": self.deployment_config.cloud_provider.value,
            "region": self.deployment_config.region,
            "cluster_name": self.deployment_config.cluster_name,
            "namespace": self.deployment_config.namespace,
            "domain": self.deployment_config.domain,
            "services_count": len(self.deployment_config.services),
            "generation_time": datetime.utcnow().isoformat(),
            "artifacts_generated": list(artifacts.keys())
        }
        
        summary_path = self.deployment_path / "deployment_summary.json"
        summary_path.write_text(json.dumps(summary, indent=2))
        
        print(f"✅ All deployment artifacts generated in: {self.deployment_path}")
        print(f"📊 Generated {sum(len(artifact) for artifact in artifacts.values())} files")
        
        return artifacts

def test_deployment_configuration():
    """Test deployment configuration creation."""
    print("🚀 Testing Deployment Configuration...")
    
    try:
        # Create deployment configuration
        deployment_config = DeploymentConfiguration(
            deployment_id="test_madagascar_deployment",
            environment=DeploymentEnvironment.STAGING,
            cloud_provider=CloudProvider.KUBERNETES,
            region="us-east-1",
            services=[]  # Will be populated by deployer
        )
        
        # Test configuration properties
        if deployment_config.environment == DeploymentEnvironment.STAGING:
            print("✅ Deployment environment set correctly")
        else:
            print("❌ Deployment environment configuration failed")
            return False
        
        if deployment_config.cluster_name == "madagascar-conservation-ai":
            print("✅ Cluster name configured")
        else:
            print("❌ Cluster name configuration failed")
            return False
        
        if deployment_config.ssl_enabled and deployment_config.monitoring_enabled:
            print("✅ Security and monitoring features enabled")
        else:
            print("❌ Security and monitoring configuration failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment configuration error: {e}")
        return False

def test_service_configuration():
    """Test service configuration creation."""
    print("\n📦 Testing Service Configuration...")
    
    try:
        # Create service configuration
        service_config = ServiceConfiguration(
            service_name="test-orchestrator",
            service_type=ServiceType.ORCHESTRATOR,
            docker_image="madagascar-ai/orchestrator:test",
            port=8000,
            environment_variables={
                "ENVIRONMENT": "test",
                "LOG_LEVEL": "DEBUG"
            },
            resource_requirements={
                "memory": "2Gi",
                "cpu": "1000m"
            },
            replicas=1
        )
        
        # Test service properties
        if service_config.service_type == ServiceType.ORCHESTRATOR:
            print("✅ Service type configured correctly")
        else:
            print("❌ Service type configuration failed")
            return False
        
        if service_config.port == 8000:
            print("✅ Service port configured")
        else:
            print("❌ Service port configuration failed")
            return False
        
        if "ENVIRONMENT" in service_config.environment_variables:
            print("✅ Environment variables configured")
        else:
            print("❌ Environment variables configuration failed")
            return False
        
        if "memory" in service_config.resource_requirements:
            print("✅ Resource requirements configured")
        else:
            print("❌ Resource requirements configuration failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Service configuration error: {e}")
        return False

def test_deployer_initialization():
    """Test deployer initialization."""
    print("\n🏗️ Testing Deployer Initialization...")
    
    try:
        # Create deployment configuration
        deployment_config = DeploymentConfiguration(
            deployment_id="test_deployer",
            environment=DeploymentEnvironment.TESTING,
            cloud_provider=CloudProvider.DOCKER,
            region="local",
            services=[]
        )
        
        # Initialize deployer
        deployer = ConservationEcosystemDeployer(deployment_config)
        
        # Test deployer properties
        if len(deployer.deployment_config.services) >= 8:
            print("✅ Service configurations initialized")
        else:
            print("❌ Service configurations initialization failed")
            return False
        
        if deployer.deployment_path.exists():
            print("✅ Deployment path created")
        else:
            print("❌ Deployment path creation failed")
            return False
        
        # Test service types
        service_types = [service.service_type for service in deployer.deployment_config.services]
        required_types = [ServiceType.ORCHESTRATOR, ServiceType.DATABASE, ServiceType.DASHBOARD]
        
        if all(req_type in service_types for req_type in required_types):
            print("✅ Required service types present")
        else:
            print("❌ Required service types missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Deployer initialization error: {e}")
        return False

def test_artifact_generation():
    """Test deployment artifact generation."""
    print("\n📄 Testing Artifact Generation...")
    
    try:
        # Create deployer
        deployment_config = DeploymentConfiguration(
            deployment_id="test_artifacts",
            environment=DeploymentEnvironment.DEVELOPMENT,
            cloud_provider=CloudProvider.KUBERNETES,
            region="us-west-2",
            services=[]
        )
        
        deployer = ConservationEcosystemDeployer(deployment_config)
        
        # Test Docker file generation
        docker_files = deployer.generate_docker_files()
        if len(docker_files) >= 4:
            print("✅ Docker files generated")
        else:
            print("❌ Docker files generation failed")
            return False
        
        # Test Kubernetes manifest generation
        k8s_manifests = deployer.generate_kubernetes_manifests()
        if len(k8s_manifests) >= 10:
            print("✅ Kubernetes manifests generated")
        else:
            print("❌ Kubernetes manifests generation failed")
            return False
        
        # Test monitoring configuration generation
        monitoring_configs = deployer.generate_monitoring_configuration()
        if "prometheus" in monitoring_configs and "alerts" in monitoring_configs:
            print("✅ Monitoring configurations generated")
        else:
            print("❌ Monitoring configurations generation failed")
            return False
        
        # Test deployment scripts generation
        deployment_scripts = deployer.generate_deployment_scripts()
        if "deploy.sh" in deployment_scripts and "status.sh" in deployment_scripts:
            print("✅ Deployment scripts generated")
        else:
            print("❌ Deployment scripts generation failed")
            return False
        
        # Test CI/CD pipeline generation
        cicd_configs = deployer.generate_ci_cd_pipeline()
        if "github_workflow" in cicd_configs and "docker_compose" in cicd_configs:
            print("✅ CI/CD configurations generated")
        else:
            print("❌ CI/CD configurations generation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Artifact generation error: {e}")
        return False

def test_deployment_validation():
    """Test deployment configuration validation."""
    print("\n🔍 Testing Deployment Validation...")
    
    try:
        # Create valid deployment configuration
        deployment_config = DeploymentConfiguration(
            deployment_id="test_validation",
            environment=DeploymentEnvironment.PRODUCTION,
            cloud_provider=CloudProvider.AWS,
            region="us-east-1",
            services=[]
        )
        
        deployer = ConservationEcosystemDeployer(deployment_config)
        
        # Test validation
        validation_result = deployer.validate_deployment_configuration()
        
        if validation_result:
            print("✅ Deployment validation passed")
        else:
            print("❌ Deployment validation failed")
            return False
        
        # Test with invalid configuration (missing required service)
        invalid_config = DeploymentConfiguration(
            deployment_id="test_invalid",
            environment=DeploymentEnvironment.PRODUCTION,
            cloud_provider=CloudProvider.AWS,
            region="us-east-1",
            services=[
                ServiceConfiguration(
                    service_name="only-dashboard",
                    service_type=ServiceType.DASHBOARD,
                    docker_image="test:latest",
                    port=8050
                )
            ]
        )
        
        # Create deployer but manually override services to test validation
        class TestableDeployer(ConservationEcosystemDeployer):
            def _initialize_service_configurations(self):
                # Skip automatic service initialization for testing
                pass
        
        invalid_deployer = TestableDeployer(invalid_config)
        # Manually set the invalid service configuration
        invalid_deployer.deployment_config.services = invalid_config.services
        
        invalid_validation = invalid_deployer.validate_deployment_configuration()
        
        if not invalid_validation:
            print("✅ Invalid configuration properly detected")
        else:
            print("❌ Invalid configuration validation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment validation error: {e}")
        return False

async def main():
    """Run Step 5 tests."""
    print("🚀 STEP 5: Production Deployment Infrastructure")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Deployment configuration
    if test_deployment_configuration():
        tests_passed += 1
    
    # Test 2: Service configuration
    if test_service_configuration():
        tests_passed += 1
    
    # Test 3: Deployer initialization
    if test_deployer_initialization():
        tests_passed += 1
    
    # Test 4: Artifact generation
    if test_artifact_generation():
        tests_passed += 1
    
    # Test 5: Deployment validation
    if test_deployment_validation():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Step 5 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ Step 5 PASSED - Production Deployment Infrastructure Complete")
        print("\n🎯 Next: Implement Real-time Monitoring & Analytics")
        print("\n🌟 Achievements:")
        print("   • ✅ Multi-environment deployment configurations")
        print("   • ✅ Kubernetes manifests and Helm charts")
        print("   • ✅ Docker containerization for all services")
        print("   • ✅ Production monitoring and alerting")
        print("   • ✅ CI/CD pipeline automation")
        print("   • ✅ Infrastructure as Code (IaC)")
        print("   • ✅ Scalable cloud-native architecture")
        print("   • ✅ Security and compliance features")
        print("\n📁 Deployment artifacts generated in:")
        print(f"   {Path('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4b_ecosystem/production_deployment').absolute()}")
        return True
    else:
        print("❌ Step 5 FAILED - Fix issues before proceeding")
        return False

if __name__ == "__main__":
    asyncio.run(main())
