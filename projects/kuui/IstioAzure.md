# Istio on Azure Kubernetes Service (AKS)

Microsoft provides a **managed Istio-based service mesh add-on** for AKS. This is the recommended approach for Azure environments as it simplifies lifecycle management and ensures compatibility.

## 🚀 Installation Guide

### 1. Prerequisites
Ensure you have the latest Azure CLI and the `aks-preview` extension if needed (though Istio is now GA in many regions).

```bash
# Update Azure CLI
az upgrade

# (Optional) Install mesh extension
az extension add --name aks-preview
az extension update --name aks-preview
```

### 2. Enable Istio Add-on
You can enable Istio for a new cluster or an existing one.

#### For a New Cluster:
```bash
az aks create \
    --resource-group myResourceGroup \
    --name myAKSCluster \
    --enable-asm \
    --generate-ssh-keys
```

#### For an Existing Cluster:
```bash
az aks mesh enable --resource-group myResourceGroup --name myAKSCluster
```

### 3. Verify the Installation
The managed Istio components are installed in the `aks-istio-system` namespace.

```bash
# Get credentials
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster

# Check pods
kubectl get pods -n aks-istio-system
```

### 4. Enable Sidecar Injection
To have Istio manage your pods, you must label the namespace. The managed add-on uses a revision-based labeling system.

```bash
# Find the installed revision
az aks show --resource-group myResourceGroup --name myAKSCluster --query 'serviceMeshProfile.istio.revisions'

# Label your namespace (e.g., for revision asm-1-20)
kubectl label namespace default istio.io/rev=asm-1-20
```

## 🛡️ Why Managed Istio?

| Feature | Managed Add-on | Manual (istioctl) |
| :--- | :--- | :--- |
| **Upgrades** | Automatic/Canary via Azure | Manual |
| **Support** | Microsoft Enterprise Support | Community / Self |
| **Lifecycle** | Integrated with AKS | Independent |
| **Certs** | Automatic Rotation | Manual |

## ⚠️ Important Considerations
*   **Unsupported Features**: Some niche Istio configurations might not be available in the managed add-on. Check the [official feature matrix](https://learn.microsoft.com/en-us/azure/aks/istio-about).
*   **OSM Conflict**: If you are using Open Service Mesh (OSM), you must disable it before enabling Istio.

> [!TIP]
> Use the **KUUI Service Mesh** tab to monitor your VirtualServices and Gateways once the add-on is active!
