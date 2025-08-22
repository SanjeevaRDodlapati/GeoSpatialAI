#!/bin/bash

echo "📦 Backing up Madagascar Conservation AI Ecosystem"
echo "================================================="

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/backup_$BACKUP_DATE"

mkdir -p $BACKUP_DIR

# Backup database
echo "📊 Backing up database..."
kubectl exec -n conservation-prod deployment/postgresql -- pg_dump -U conservation_user madagascar_conservation > $BACKUP_DIR/database.sql

# Backup persistent volumes
echo "💾 Backing up storage..."
kubectl get pvc -n conservation-prod -o yaml > $BACKUP_DIR/pvc_backup.yaml

# Backup configurations
echo "⚙️ Backing up configurations..."
kubectl get configmap -n conservation-prod -o yaml > $BACKUP_DIR/configmap_backup.yaml
kubectl get secret -n conservation-prod -o yaml > $BACKUP_DIR/secret_backup.yaml

# Create archive
tar -czf "backup_$BACKUP_DATE.tar.gz" -C backups "backup_$BACKUP_DATE"
rm -rf $BACKUP_DIR

echo "✅ Backup completed: backup_$BACKUP_DATE.tar.gz"