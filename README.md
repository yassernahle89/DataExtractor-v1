# 🚀 DataExtractor Deployment on Azure Kubernetes Service (AKS)

This repository contains all the instructions to **build, push, and deploy** your microservices on **Azure Kubernetes Service (AKS)** with **Azure Container Registry (ACR)**.

---

## 📋 Prerequisites

Before starting, ensure you have:

- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)  
- [kubectl](https://kubernetes.io/docs/tasks/tools/)  
- [Docker](https://docs.docker.com/get-docker/)  
- An **Azure Subscription**  

---

## ⚙️ Step 1: Create a Resource Group

All resources will be organized under one group:

```bash
az group create --name redpandaResourceGroup --location eastus
```
## 🛠️ Step 2: Create an Azure Container Registry (ACR)

Create a private registry to store your Docker images:

```bash
az acr create --resource-group redpandaResourceGroup \
  --name dokcerregistery \
  --sku Basic
```
## 🏗️ Step 3: Build and Push Docker Images

Tag and push your service images to ACR. Example for one service (csv-service):

```bash
# Replace <acrLoginServer> with the ACR login server (e.g., dokcerregistery.azurecr.io)
ACR_LOGIN_SERVER=dokcerregistery.azurecr.io

# Build Docker image
docker build -t $ACR_LOGIN_SERVER/csv-service:v1 ./csv-service

# Push image to ACR
docker push $ACR_LOGIN_SERVER/csv-service:v1

```
## ☸️ Step 4: Create AKS Cluster

Create a Kubernetes cluster and attach it to your ACR:

```bash
az aks create \
  --resource-group redpandaResourceGroup \
  --name RedpandaConsumers \
  --node-count 1 \
  --node-vm-size Standard_D2s_v3 \
  --enable-addons monitoring \
  --generate-ssh-keys \
  --attach-acr dokcerregistery
```
## 🔑 Step 5: Connect to the AKS Cluster

Get the cluster credentials to use kubectl:

```bash
az aks get-credentials --resource-group redpandaResourceGroup --name RedpandaConsumers
```

## 📦 Step 6: Deploy Services

Apply the Kubernetes manifest file (kube_service.yaml) to deploy your services:

```bash
kubectl apply -f kube_service.yaml
```


