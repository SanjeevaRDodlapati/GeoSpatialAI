#!/bin/bash
set -e

echo "🚀 Deploying Madagascar Conservation AI Ecosystem"
echo "Environment: production"
echo "Cluster: madagascar-conservation-ai-prod"

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
kubectl wait --for=condition=available --timeout=300s deployment/postgresql -n conservation-prod

# Deploy storage
kubectl apply -f deployment_minio.yaml
kubectl apply -f service_minio.yaml

# Deploy core services
kubectl apply -f deployment_ecosystem-orchestrator.yaml
kubectl apply -f service_ecosystem-orchestrator.yaml

# Wait for orchestrator to be ready
echo "⏳ Waiting for orchestrator to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/ecosystem-orchestrator -n conservation-prod

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
echo "🌐 Dashboard will be available at: https://conservation.madagascar.org"
echo "📊 Monitoring at: https://monitoring.conservation.madagascar.org"

# Show status
kubectl get pods -n conservation-prod