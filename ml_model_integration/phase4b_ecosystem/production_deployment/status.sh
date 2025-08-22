#!/bin/bash

echo "📊 Madagascar Conservation AI Ecosystem Status"
echo "=============================================="

# Check namespace
kubectl get namespace conservation-prod

# Check all pods
echo ""
echo "📦 Pod Status:"
kubectl get pods -n conservation-prod -o wide

# Check services
echo ""
echo "🔗 Service Status:"
kubectl get services -n conservation-prod

# Check ingress
echo ""
echo "🌐 Ingress Status:"
kubectl get ingress -n conservation-prod

# Check HPA
echo ""
echo "📈 Autoscaling Status:"
kubectl get hpa -n conservation-prod

# Check persistent volumes
echo ""
echo "💾 Storage Status:"
kubectl get pvc -n conservation-prod

# System health check
echo ""
echo "🏥 Health Check:"
ORCHESTRATOR_IP=$(kubectl get service ecosystem-orchestrator -n conservation-prod -o jsonpath='{.spec.clusterIP}')
curl -s http://$ORCHESTRATOR_IP:8000/health || echo "❌ Orchestrator health check failed"

DASHBOARD_IP=$(kubectl get service conservation-dashboard -n conservation-prod -o jsonpath='{.spec.clusterIP}')
curl -s http://$DASHBOARD_IP:8050/health || echo "❌ Dashboard health check failed"