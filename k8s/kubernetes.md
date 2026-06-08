# ProductHub Kubernetes Deployment Guide

## Prerequisites

Install the following:

* Docker
* Kubernetes CLI (kubectl)
* Minikube
* Helm
* Git

Verify installation:

```bash
docker --version

kubectl version --client

minikube version

helm version
```

---

# Step 1: Start Minikube

```bash
minikube start --driver=docker
```

Verify:

```bash
kubectl get nodes
```

Expected:

```text
NAME       STATUS   ROLES           AGE
minikube   Ready    control-plane   1m
```

Check cluster:

```bash
kubectl cluster-info
```

---

# Step 2: Build Docker Image Inside Minikube

Configure Docker environment:

```bash
eval $(minikube docker-env)
```

Build image:

```bash
docker build -t producthub:1.0 .
```

Verify:

```bash
docker images | grep producthub
```

---

# Step 3: Create Namespace

Apply namespace:

```bash
kubectl apply -f k8s/namespace.yaml
```

Verify:

```bash
kubectl get namespaces
```

Expected:

```text
producthub
```

---

# Step 4: Create ConfigMap

Apply:

```bash
kubectl apply -f k8s/configmap.yaml
```

Verify:

```bash
kubectl get configmap -n producthub
```

Describe:

```bash
kubectl describe configmap producthub-config -n producthub
```

---

# Step 5: Create Secret

Apply:

```bash
kubectl apply -f k8s/secret.yaml
```

Verify:

```bash
kubectl get secrets -n producthub
```

---

# Step 6: Create Persistent Volume

Apply:

```bash
kubectl apply -f k8s/pv.yaml
```

Verify:

```bash
kubectl get pv
```

---

# Step 7: Create Persistent Volume Claim

Apply:

```bash
kubectl apply -f k8s/pvc.yaml
```

Verify:

```bash
kubectl get pvc -n producthub
```

Expected:

```text
STATUS: Bound
```

---

# Step 8: Deploy ProductHub Application

Apply deployment:

```bash
kubectl apply -f k8s/producthub-deployment.yaml
```

Verify:

```bash
kubectl get deployments -n producthub
```

Check pods:

```bash
kubectl get pods -n producthub
```

Expected:

```text
READY   STATUS
1/1     Running
```

Describe pod:

```bash
kubectl describe pod <pod-name> -n producthub
```

---

# Step 9: Create Service

Apply:

```bash
kubectl apply -f k8s/producthub-service.yaml
```

Verify:

```bash
kubectl get svc -n producthub
```

---

# Step 10: Access Application

Get URL:

```bash
minikube service producthub -n producthub --url
```

Test:

```bash
curl $(minikube service producthub -n producthub --url)/metrics
```

Expected:

```text
products_processed_total
api_requests_total
current_products
```

---

# Step 11: Install Prometheus

Add repository:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo update
```

Install:

```bash
helm install prometheus prometheus-community/prometheus \
-n monitoring \
--create-namespace
```

Verify:

```bash
kubectl get pods -n monitoring
```

Port Forward:

```bash
kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
```

Open:

```text
http://localhost:9090
```

---

# Step 12: Install Grafana

Add repository:

```bash
helm repo add grafana https://grafana.github.io/helm-charts

helm repo update
```

Install:

```bash
helm install grafana grafana/grafana \
-n monitoring
```

Verify:

```bash
kubectl get pods -n monitoring
```

Port Forward:

```bash
kubectl port-forward svc/grafana 3000:80 -n monitoring
```

Retrieve Admin Password:

```bash
kubectl get secret grafana \
-n monitoring \
-o jsonpath="{.data.admin-password}" \
| base64 --decode
```

Open:

```text
http://localhost:3000
```

Login:

```text
Username: admin
Password: <decoded-password>
```

---

# Step 13: Configure Grafana

Add Data Source:

```text
Connections
→ Data Sources
→ Add Data Source
→ Prometheus
```

URL:

```text
http://prometheus-server.monitoring.svc.cluster.local
```

Save & Test.

Expected:

```text
Successfully queried the Prometheus API
```

---

# Step 14: Install Ingress Controller

Enable:

```bash
minikube addons enable ingress
```

Verify:

```bash
kubectl get pods -n ingress-nginx
```

Expected:

```text
ingress-nginx-controller Running
```

---

# Step 15: Deploy Ingress

Apply:

```bash
kubectl apply -f k8s/ingress.yaml
```

Verify:

```bash
kubectl get ingress -n producthub
```

Get Minikube IP:

```bash
minikube ip
```

Update hosts file:

Linux:

```bash
sudo nano /etc/hosts
```

Add:

```text
<MINIKUBE_IP> producthub.local
```

Test:

```text
http://producthub.local
```

---

# Step 16: Helm Deployment

Create Chart:

```bash
helm create producthub-chart
```

Install:

```bash
helm install producthub ./producthub-chart \
-n producthub
```

Upgrade:

```bash
helm upgrade producthub ./producthub-chart \
-n producthub
```

Verify:

```bash
helm list -n producthub
```

---

# Troubleshooting

Check Pods:

```bash
kubectl get pods -A
```

Pod Logs:

```bash
kubectl logs <pod-name> -n producthub
```

Describe Pod:

```bash
kubectl describe pod <pod-name> -n producthub
```

Restart Deployment:

```bash
kubectl rollout restart deployment producthub -n producthub
```

Delete Namespace:

```bash
kubectl delete namespace producthub
```

---

# Useful Commands

```bash
kubectl get all -n producthub

kubectl get pods -A

kubectl get svc -A

kubectl get ingress -A

kubectl get pvc -A

kubectl get pv

helm list -A

minikube dashboard
```

---

# Architecture

Internet
│
▼
Ingress
│
▼
ProductHub Service
│
▼
ProductHub Deployment
│
▼
Persistent Volume Claim
│
▼
Persistent Volume

Monitoring Stack

ProductHub
│
▼
Prometheus
│
▼
Grafana

Configuration

ConfigMap
Secret

Deployment Management

Helm
GitHub Actions
Kubernetes
