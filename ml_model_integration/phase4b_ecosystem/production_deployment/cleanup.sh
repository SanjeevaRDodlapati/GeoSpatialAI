#!/bin/bash

echo "🧹 Cleaning up Madagascar Conservation AI Ecosystem"
echo "================================================="

# Delete all resources
kubectl delete namespace conservation-prod --ignore-not-found=true

# Wait for namespace deletion
echo "⏳ Waiting for namespace deletion..."
kubectl wait --for=delete namespace/conservation-prod --timeout=300s

echo "✅ Cleanup completed!"