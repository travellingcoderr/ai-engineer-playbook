# Master K8s API Project Guide

This guide consolidates all documentation for the project, covering architecture, infrastructure setup, and deployment.

---

## 1. Kubernetes Architecture Overview
Kubernetes (K8s) automates the deployment, scaling, and management of containerized applications.

### Key Relationships
- **Cluster**: The entire system.
- **Node**: A machine (VM or physical) in the cluster.
- **Pod**: A group of one or more containers running on a Node.

### Networking Basics
- **Pod IP**: Internal, transient address for a single Pod.
- **Cluster IP**: Stable internal address for a Service (set of Pods).
- **Ingress IP**: External entry point for traffic from the internet.
- **Ingress vs. Egress**: Ingress is incoming traffic; Egress is outgoing traffic.

---

## 2. Infrastructure Setup (Add-ons)
Before deploying your application, install these cluster-level components:

| Component | Purpose | Helm Install Command |
| :--- | :--- | :--- |
| **Traefik** | Ingress Controller / Gateway | `helm install traefik traefik/traefik` |
| **cert-manager** | TLS Automation | `helm install cert-manager jetstack/cert-manager` |
| **ExternalDNS** | DNS Sync | `helm install external-dns external-dns/external-dns` |
| **Prometheus** | Monitoring | `helm install prometheus prometheus-community/kube-prometheus-stack` |

---

## 3. Azure Resource Mapping
How K8s components translate to Azure native services:
- **Cluster**: AKS (Azure Kubernetes Service)
- **Networking**: Azure Application Gateway / Front Door
- **Secrets**: Azure Key Vault. Use the **Secret Store CSI Driver** to sync vault secrets into your Pods.

---

## 4. Azure Key Vault Integration
To use secure secrets from Key Vault:

1. **Enable the CSI Driver on AKS**:
   ```bash
   az aks enable-addons --addons azure-keyvault-secrets-provider --name aks-research-agent-dev --resource-group rg-research-agent-dev
   ```
2. **Assign Permissions**:
   The AKS identity needs the "Key Vault Secrets User" role.
   ```bash
   # Get Identity ID
   SUBSCRIPTION_ID=$(az account show --subscription "BhargaviSub" --query id -o tsv)
   IDENTITY_ID=$(az aks show -n aks-research-agent-dev -g rg-research-agent-dev --query "identityProfile.kubeletidentity.objectId" -o tsv)
   # Assign Role
   az role assignment create --role "Key Vault Secrets User" --assignee $IDENTITY_ID --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/rg-research-agent-dev/providers/Microsoft.KeyVault/vaults/kv-research-agent-dev007"
   ```

### Important: RBAC Roles (Data Plane)
Azure Key Vault distinguishes between the **Management Plane** (creating the vault) and the **Data Plane** (reading/writing secrets). To see secrets in the Azure Portal, you need specific roles:

| Identity | Role | Purpose |
| :--- | :--- | :--- |
| **AKS Cluster** | `Key Vault Secrets User` | **Read-only** access to fetch secrets into pods (Least Privilege). |
| **Developer (You)**| `Key Vault Secrets Officer`| **Full access** to Create, View, and Edit secrets in the Portal. |

If you see an "Unauthorized" message in the Portal, assign the **Secrets Officer** role to yourself:
```bash
MY_USER_ID=$(az ad signed-in-user show --query id -o tsv)
az role assignment create --role "Key Vault Secrets Officer" \
  --assignee $MY_USER_ID \
  --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/rg-research-agent-dev/providers/Microsoft.KeyVault/vaults/kv-research-agent-dev007"
```

---
3. **Configure Helm**:
   Update `values.yaml` with your `keyvault.name`, `keyvault.tenantId`, and a list of secrets.
   ```yaml
   keyvault:
     name: "kv-name"
     tenantId: "tenant-id"
     secrets:
       - name: "vault-secret-name"
         key: "ENV_VAR_NAME"
   ```
   The `base-api-chart` will automatically loop through this list to create the `SecretProviderClass` and inject the environment variables.

---

### Why use the Secret Store CSI Driver?
Unlike traditional Kubernetes Secrets (which are stored in plain base64 in the cluster's database), the **Secret Store CSI Driver** provides several enterprise-grade benefits:

1.  **Direct Integration**: Secrets stay in **Azure Key Vault** (your single source of truth) and are only fetched when the Pod starts.
2.  **Mounted as Files**: Secrets are safely mounted into the pod's filesystem at `/mnt/secrets-store/`. This is the most secure way to handle sensitive data like SSH keys or certificates.
3.  **Environment Sync**: We've configured the chart to "sync" these mounted files into environment variables. This gives you the best of both worlds: high security and easy access in your Python code (`os.getenv("APP_SECRET")`).
4.  **No Hardcoding**: Your `values.yaml` only contains "pointers" (names) to your secrets, not the actual values. Even if your Helm chart is leaked, your secrets remain safe in the vault.

---

## 4. API Service Walkthrough

### Build & Push to Azure Registry (ACR)
AKS clusters cannot see your local images. You must push them to a registry like Azure Container Registry (ACR) and give the cluster permission to pull them.

1. **Login to ACR**:
   ```bash
   az acr login --name researchagentacrdev
   ```
2. **Link AKS to ACR (RBAC)**:
   This gives your cluster "AcrPull" permissions. While `--attach-acr` works for most cases, manually assigning the role to both the **Cluster Identity** and the **Kubelet Identity** ensures complete coverage:
   ```bash
   # Get Subscriptions and Resource Info
   SUB_ID=$(az account show --query id -o tsv)
   RG="rg-research-agent-dev"
   ACR_NAME="researchagentacrdev"
   AKS_NAME="aks-research-agent-dev"

   # 1. Assign to Kubelet Identity (used for pulling images)
   KUBELET_ID=$(az aks show -n $AKS_NAME -g $RG --query "identityProfile.kubeletidentity.objectId" -o tsv)
   az role assignment create --role "AcrPull" --assignee $KUBELET_ID --scope "/subscriptions/$SUB_ID/resourceGroups/$RG/providers/Microsoft.ContainerRegistry/registries/$ACR_NAME"

   # 2. Assign to Cluster Identity (backup/management)
   CLUSTER_ID=$(az aks show -n $AKS_NAME -g $RG --query "identity.principalId" -o tsv)
   az role assignment create --role "AcrPull" --assignee $CLUSTER_ID --scope "/subscriptions/$SUB_ID/resourceGroups/$RG/providers/Microsoft.ContainerRegistry/registries/$ACR_NAME"
   ```
3. **Tag the Image**:
   ```bash
   docker tag k8s-api-service:latest researchagentacrdev.azurecr.io/k8s-api-service:latest
   ```
4. **Push the Image**:
   ```bash
   docker push researchagentacrdev.azurecr.io/k8s-api-service:latest
   ```

### Deploy the Service (to a dedicated namespace)
Once the image is in ACR, deploy the chart to the `my-api-ns` namespace:

1. **Create the Namespace**:
   ```bash
   kubectl create namespace my-api-ns
   ```
2. **Build Dependencies**:
   ```bash
   cd k8s/helm
   helm dependency build
   ```
3. **Install/Upgrade**:
   ```bash
   helm upgrade --install my-api . -n my-api-ns \
     --set base-api-chart.image.repository=researchagentacrdev.azurecr.io/k8s-api-service \
     --set base-api-chart.keyvault.name=kv-research-agent-dev007 \
     --set base-api-chart.keyvault.tenantId=2c206d8b-26d4-40af-ad87-4498355a7b51
   ```
4. **View Pods**:
   ```bash
   kubectl get pods -n my-api-ns
   ```
5. **View Logs**:
   ```bash
   kubectl logs -f <pod-name> -n my-api-ns
   ```
6. **View Events**:
   ```bash
   kubectl get events -n my-api-ns
   ```
7. **View SecretProviderClass**:
   ```bash
   kubectl describe secretproviderclass <name> -n my-api-ns
   ```
8. **View Secret**:
   ```bash
   kubectl get secret <name> -n my-api-ns
   ```
9. **View ConfigMap**:
   ```bash
   kubectl get configmap <name> -n my-api-ns
   ```
10. **View Deployment**:
    ```bash
    kubectl get deployment <name> -n my-api-ns
    ```
11. **View Service**:
    ```bash
    kubectl get service <name> -n my-api-ns
    ```
12. **View Ingress**:
    ```bash
    kubectl get ingress <name> -n my-api-ns
    ```
13. **View NetworkPolicy**:
    ```bash
    kubectl get networkpolicy <name> -n my-api-ns
    ```
14. **View HorizontalPodAutoscaler**:
    ```bash
    kubectl get horizontalpodautoscaler <name> -n my-api-ns
    ```
15. **View VerticalPodAutoscaler**:
    ```bash
    kubectl get verticalpodautoscaler <name> -n my-api-ns
    ```
16. **View PodDisruptionBudget**:
    ```bash
    kubectl get poddisruptionbudget <name> -n my-api-ns
    ```
17. **View ResourceQuota**:
    ```bash
    kubectl get resourcequota <name> -n my-api-ns
    ```
18. **View LimitRange**:
    ```bash
    kubectl get limitrange <name> -n my-api-ns
    ```
19. **View PersistentVolumeClaim**:
    ```bash
    kubectl get persistentvolumeclaim <name> -n my-api-ns
    ```
20. **View PersistentVolume**:
    ```bash
    kubectl get persistentvolume <name>
    ```
21. **View StorageClass**:
    ```bash
    kubectl get storageclass
    ```
22. **View Node**:
    ```bash
    kubectl get node
    ```
23. **View NodePool**:
    ```bash
    kubectl get nodepool -n my-api-ns
    ```
24. **View NodePool**:
    ```bash
    kubectl get nodepool -n my-api-ns
    ```

### Triggering a Redeploy
If you've updated your code/image or fixed a permission issue, you can force Kubernetes to pull the new version:

1. **Option A: Restart the Deployment (Recommended)**:
   ```bash
   kubectl rollout restart deployment/my-api -n my-api-ns
   ```
   *This is the fastest way to tell all pods to fetch the image again.*

2. **Option B: Re-push the Image**:
   If you've made code changes, rebuild and push:
   ```bash
   docker build --platform linux/amd64 -t researchagentacrdev.azurecr.io/k8s-api-service:latest -f k8s/Dockerfile k8s/
   docker push researchagentacrdev.azurecr.io/k8s-api-service:latest
   ```
   *Note: Our `pullPolicy: Always` ensures AKS will pick this up on its next restart.*

---

## 5. Troubleshooting & Context
If you encounter "INSTALLATION FAILED" or connection errors, verify your Kubernetes context:

### Check Current Context
```bash
kubectl config current-context
```

### Check Cluster Info
```bash
kubectl cluster-info
```

### Switch Context
If you are using Docker Desktop but want to target Minikube (or vice versa):
```bash
kubectl config use-context minikube
```

### Troubleshoot "Waiting" Pods
If your pods are stuck in `ContainerCreating` or `ImagePullBackOff`, run these commands:

1. **Describe the Pod (Most Important)**:
   ```bash
   kubectl describe pod <pod-name>
   ```
   *Look at the "Events" section at the bottom. It will tell you if the image pull failed or if the Key Vault mount failed.*

2. **Check Cluster Events**:
   ```bash
   kubectl get events --sort-by=.lastTimestamp
   ```

3. **Check SecretProviderClass Status**:
   ```bash
   kubectl describe secretproviderclass <name>
   ```

### Common Authentication Errors
If you see `ManagedIdentityCredential authentication failed`:
- Ensure the `keyvault.clientID` in `values.yaml` matches your AKS Kubelet identity. (I've updated this for you).
- Ensure the role assignment for `Key Vault Secrets User` is active.

---

### Debugging Pods Like a Pro
If your pods aren't running, follow this 3-step checklist to find the "Why":

1. **The "What"**: `kubectl get pods -n my-api-ns`
   *   Find the pod name and see its status (`Pending`, `CrashLoopBackOff`, `ImagePullBackOff`).

2. **The "Why"**: `kubectl describe pod <pod-name> -n my-api-ns`
   *   **CRITICAL**: Look at the **Events** section at the bottom. 
   *   If you see `no match for platform`, you forgot the `--platform linux/amd64` flag in `docker build`.
   *   If you see `FailedMount` or `401 Unauthorized`, your Key Vault or ACR role assignments are likely missing or propagating.

3. **The "Live State"**: `kubectl logs -f <pod-name> -n my-api-ns`
   *   If the status is `CrashLoopBackOff`, the error is in your Python code. Check the logs for the traceback!

---

### Verify Endpoints (Port Forwarding)
Since you haven't hooked up a domain name yet, use **`port-forward`** to test your API locally:

1. **Start the Port Forward**:
   ```bash   
   # Map local port 8080 to the Service's port 80
   kubectl port-forward svc/my-api 8080:80 -n my-api-ns
   ```

2. **Test in Browser**:
   *   **Check Secret Injection**: [http://localhost:8080/secret](http://localhost:8080/secret) 
   *   **Check Environment Variables**: [http://localhost:8080/env](http://localhost:8080/env) 
   *   **Check Metrics**: [http://localhost:8080/metrics](http://localhost:8080/metrics) 
   *   **Health Check**: [http://localhost:8080/health](http://localhost:8080/health)

Congratulations! Your production-ready K8s API is fully deployed and secure.

---

### Personal Domain & SSL/TLS (Production)
We are using **Traefik** as the Ingress Controller and **cert-manager** to automatically handle SSL certificates via Let's Encrypt.

1. **How it works (The Chain)**:
   `Domain Name (api.purpletechllc.com)` -> `Azure LB (Public IP: 48.194.18.171)` -> `Traefik Pod` -> `Ingress Resource (Rules)` -> `API Service` -> `API Pod`.

2. **Certificate Automation**:
   Because of the `cert-manager.io/cluster-issuer: "letsencrypt-prod"` annotation in your Ingress, cert-manager will:
   - Request an SSL certificate from Let's Encrypt.
   - Prove ownership of your domain.
   - Store the certificate in a secret called `api-tls`.
   - Traefik automatically picks up this secret and secures your traffic with HTTPS.

3. **Deploy with Domain**:
   After updating your DNS and `values.yaml`:
   ```bash
   # From k8s/helm/
   helm upgrade --install my-api . -n my-api-ns
   ```

4. **Verify Certificate**:
   ```bash
   kubectl get certificate -n my-api-ns
   ```
   *Wait until the status is "Ready: True".*


** More Info
How Traefik works in Azure (Simplified):
The Public IP (48.194.18.171): When we installed Traefik with Service Type: LoadBalancer, Kubernetes talked to Azure and said: "Hey, give me a public IP and an Azure Load Balancer." Azure then provisioned that IP and linked it directly to the Traefik pods.

The Routing (Ingress): When a request for api.purpletechllc.com hits that IP, it enters the Traefik Pod. Traefik looks at its "Rule Book" (the Ingress Resource we created).

Rule: "If the host is api.purpletechllc.com, send it to the my-api service on port 80."
Getting to the Pod IP: The my-api service is a ClusterIP, which is like a load balancer inside the cluster. It knows the private IP addresses of all your API pods. It picks one and sends the traffic there.

The Magic of SSL (TLS): Because you added the cert-manager.io/cluster-issuer annotation, cert-manager woke up, contacted Let's Encrypt, and said: "Someone claims they own api.purpletechllc.com. Let me verify." It proved ownership through a challenge, got the SSL certificate, and saved it in a secret called api-tls. Traefik then uses that secret to encrypt your traffic with HTTPS.
---

### SSL Verification & Status Checks
If your certificate is not yet active, use these commands to find out why:

1. **Check the Issuer Status**:
   ```bash
   kubectl get clusterissuer letsencrypt-prod
   ```
   *Status must be "Ready: True".*

2. **Check the Certificate Progress**:
   ```bash
   kubectl get certificate -n my-api-ns
   ```

3. **Check the "Order" (Communication with Let's Encrypt)**:
   ```bash
   kubectl get orders -n my-api-ns
   ```

4. **Check the "Challenge" (Domain Verification Progress)**:
   ```bash
   kubectl get challenges -n my-api-ns
   ```
   *If this is stuck, your DNS A Record might not have propagated yet.*

---

### 🧰 The "Super-Toolbox" (One Command to Rule Them All)
If you ever feel lost or something isn't "just working," start here:

1. **The "Describe" Command**:
   ```bash
   kubectl describe <resource_type> <name> -n my-api-ns
   ```
   *Use this for EVERYTHING: pods, services, ingress, certificates, etc. Look at the "Events" section!*

2. **The "Logs" Command (For Application Crashes)**:
   ```bash
   kubectl logs -f <pod-name> -n my-api-ns
   ```
   *If the status is "CrashLoopBackOff," this will show you your Python traceback.*

3. **The "Global View" Command**:
   ```bash
   kubectl get events -A --sort-by=.lastTimestamp
   ```
   *See what's happening across the entire cluster in real-time.*

4. **The "Quick List" (All Resources)**:
   ```bash
   kubectl get all -n my-api-ns
   ```
