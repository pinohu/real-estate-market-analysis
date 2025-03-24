#!/bin/bash

# Exit on error
set -e

# Create namespace if it doesn't exist
kubectl create namespace real-estate --dry-run=client -o yaml | kubectl apply -f -

# Apply all Kubernetes configurations
echo "Applying Kubernetes configurations..."

# Apply secrets first
kubectl apply -f secrets.yaml -n real-estate
kubectl apply -f grafana-secrets.yaml -n real-estate

# Apply persistent volume claims
kubectl apply -f db-pvc.yaml -n real-estate
kubectl apply -f prometheus-pvc.yaml -n real-estate
kubectl apply -f grafana-pvc.yaml -n real-estate

# Apply monitoring configurations
kubectl apply -f prometheus-config.yaml -n real-estate
kubectl apply -f prometheus-deployment.yaml -n real-estate
kubectl apply -f prometheus-service.yaml -n real-estate
kubectl apply -f grafana-deployment.yaml -n real-estate
kubectl apply -f grafana-service.yaml -n real-estate
kubectl apply -f grafana-dashboard.yaml -n real-estate

# Apply database configurations
kubectl apply -f db-deployment.yaml -n real-estate
kubectl apply -f db-service.yaml -n real-estate

# Apply Redis configurations
kubectl apply -f redis-deployment.yaml -n real-estate
kubectl apply -f redis-service.yaml -n real-estate

# Apply API configurations
kubectl apply -f api-deployment.yaml -n real-estate
kubectl apply -f api-service.yaml -n real-estate

# Apply frontend configurations
kubectl apply -f frontend-deployment.yaml -n real-estate
kubectl apply -f frontend-service.yaml -n real-estate

# Apply ingress configuration
kubectl apply -f ingress.yaml -n real-estate

echo "Deployment completed successfully!"

# Wait for pods to be ready
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=real-estate-api -n real-estate --timeout=300s
kubectl wait --for=condition=ready pod -l app=real-estate-frontend -n real-estate --timeout=300s
kubectl wait --for=condition=ready pod -l app=real-estate-db -n real-estate --timeout=300s
kubectl wait --for=condition=ready pod -l app=real-estate-redis -n real-estate --timeout=300s
kubectl wait --for=condition=ready pod -l app=prometheus -n real-estate --timeout=300s
kubectl wait --for=condition=ready pod -l app=grafana -n real-estate --timeout=300s

echo "All pods are ready!"

# Get service URLs
echo "Service URLs:"
echo "Frontend: http://app.realestate.com"
echo "API: http://api.realestate.com"
echo "Grafana: http://grafana.realestate.com" 