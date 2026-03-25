# Research Agent Azure Deployment

This folder contains project-specific Azure infrastructure and deployment assets for `projects/research_agent`.

## What This Folder Owns

- Azure resource creation for this project
- ACR image build and push for this project
- project-specific Helm values for this project

The reusable Helm chart used by this project lives globally at:
- `deploy/helm/charts/fastapi-service`

The reusable Azure deployment pattern for all services is documented here:
- `deploy/azure/README.md`

## Layout

- `terraform/`: Terraform-based infrastructure for this project
- `values.yaml`: project-specific values for the global FastAPI Helm chart
- `architecture.md`: ingress, egress, and network diagram
- `cert-manager-letsencrypt-sop.md`: step-by-step HTTPS automation guide using cert-manager and Let's Encrypt

The shared GitHub OIDC federated credential example lives here:
- `deploy/azure/github-federated-credential.main.json.example`

## Recommendation

Use this folder as the source of truth for `research_agent` infrastructure.

For a fresh start, prefer the GitHub Actions Terraform flow:
- GitHub bootstraps the Terraform backend
- Terraform creates Azure resources
- the workflow builds the image
- the workflow deploys Helm to AKS

This avoids local `terraform apply`, local kubeconfig management, and local image pushes.

## Important Note

For container images, the correct Azure service is **Azure Container Registry (ACR)**, not a normal Storage Account.

## Required Tools

- Azure CLI
- kubectl
- Helm
- Terraform if you want IaC

Official install links:
- Azure CLI: <https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest>
- kubectl install: <https://kubernetes.io/docs/tasks/tools/install-kubectl/>
- Helm install: <https://helm.sh/docs/intro/install/>
- Terraform install: <https://developer.hashicorp.com/terraform/install>

## Terraform Reference Path

Copy the tfvars file:

```bash
cp \
  projects/research_agent/deploy/azure/terraform/envvars.auto.tfvars.example \
  projects/research_agent/deploy/azure/terraform/envvars.auto.tfvars
```

Update values, then run:

```bash
cd projects/research_agent/deploy/azure/terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan
az aks get-credentials \
  --resource-group "$(terraform output -raw resource_group_name)" \
  --name "$(terraform output -raw aks_name)" \
  --overwrite-existing
kubectl create namespace "$(terraform output -raw aks_namespace)" --dry-run=client -o yaml | kubectl apply -f -
```

## Preferred Fresh-Start Order: GitHub Actions + Terraform

This is the recommended order when you want GitHub Actions to create everything for `research_agent`.

1. Configure GitHub OIDC for Azure login
2. Add the required GitHub secrets and variables for:
   - Azure auth
   - Terraform backend storage
   - `research_agent` resource names
   - ingress hostname
3. Push to `main` or run `.github/workflows/research-agent-aks.yml` manually
4. The workflow bootstraps the Terraform backend in Azure Storage
5. The workflow runs `terraform init`, `plan`, and `apply`
6. The workflow reads Terraform outputs for:
   - ACR login server
   - AKS cluster name
   - AKS namespace
   - Key Vault name
   - AKS Key Vault CSI client ID
7. The workflow builds and pushes the image to ACR
8. The workflow gets AKS context and deploys Helm
9. DNS points your hostname at the ingress public IP
10. cert-manager issues or renews the TLS certificate

### Why The Backend Is Bootstrapped Before Terraform

Terraform state must live somewhere durable across workflow runs.

For this setup, GitHub Actions first creates:
- a Resource Group for Terraform state
- a Storage Account
- a Blob container

That backend bootstrap is done with Azure CLI because Terraform cannot store its own state in Azure Blob until the backend exists.

### GitHub RBAC Requirement For A Fresh Start

If you want GitHub Actions to create everything from nothing, the GitHub OIDC application needs enough Azure RBAC to:
- create the Terraform state resource group and storage account
- create the application resource group and infrastructure
- read or write ACR and AKS as part of deployment

The practical starting point is:
- `Contributor` on the Azure subscription

After the workflow-created infrastructure exists, Terraform also assigns narrower project roles for the ongoing deployment path.

If you want Terraform to assign GitHub Actions access too:
- set `github_actions_client_id` to the same value you use for `AZURE_CLIENT_ID`
- set `enable_github_actions_role_assignments = true`

If you want Terraform to assign Key Vault secret write access too:
- set `key_vault_secrets_officer_object_ids` to the Entra object IDs of the users, groups, or service principals that should be allowed to create/update secrets in this vault
- this is separate from the AKS CSI identity, which only needs read access at runtime

## Default Azure Resources

Terraform creates:
- Resource Group
- Azure Container Registry
- AKS cluster
- ACR attachment to AKS
- Azure Key Vault
- Kubernetes namespace for this app
- Azure RBAC role assignments for:
  - AKS to pull from ACR
  - AKS to read Key Vault secrets
  - GitHub Actions to access Azure resources, if enabled
  - designated secret administrators to write Key Vault secrets, if configured

## Typical End-to-End Flow

1. Terraform creates Azure resources
2. GitHub Actions builds the image from `projects/research_agent/Dockerfile`
3. GitHub Actions pushes the image to ACR
4. GitHub Actions deploys the Helm chart
5. Check ingress, DNS, and HTTPS

The deployment uses:
- global shared chart: `deploy/helm/charts/fastapi-service`
- project values: `projects/research_agent/deploy/azure/values.yaml`

## Key Vault Secret Injection

The Helm chart supports AKS Secrets Store CSI with Azure Key Vault.

What this gives you:
- secrets mounted into the pod filesystem
- optional sync of those values into a Kubernetes Secret
- environment variable injection from the synced Kubernetes Secret

Typical flow:
1. Store `OPENAI_API_KEY` in Azure Key Vault
2. Enable Key Vault CSI on AKS
3. Grant the AKS Key Vault CSI identity access to the vault
4. Deploy the chart with `keyVault.enabled=true`
5. The pod mounts `/mnt/secrets-store`
6. The chart syncs the value to `research-agent-kv-secrets`
7. The deployment reads it into env vars

Why there are multiple Key Vault roles:
- the AKS Key Vault CSI identity needs read access so pods can consume secrets at runtime
- a human user or CI admin identity needs write access to create and rotate secrets in the vault
- GitHub Actions does not need Key Vault secret write access for this deployment flow unless you explicitly want the workflow to manage secrets too

## Ingress And TLS

The chart supports an ingress resource in front of the service.

Default traffic flow:
- Internet client -> public IP on ingress controller -> ingress rule -> Kubernetes Service -> research-agent pods

TLS:
- TLS terminates at the ingress controller
- the ingress controller presents the certificate for your hostname
- traffic from ingress to the service inside the cluster is HTTP in this starter setup

Production recommendation:
- use cert-manager with Let's Encrypt
- let cert-manager manage the Kubernetes TLS secret automatically
- do not manage `tls.crt` / `tls.key` by hand for the long-term production path

The detailed SOP is here:
- `cert-manager-letsencrypt-sop.md`

The default ingress class is the AKS web application routing class:
- `webapprouting.kubernetes.azure.com`

Note:
- Microsoft recommends planning for Gateway API long term.
- The current AKS managed NGINX application routing path remains supported, but upstream Ingress NGINX is being retired. See official AKS guidance below.

## GitHub Actions

There is a project-specific workflow here:
- `.github/workflows/research-agent-aks.yml`

Required GitHub repository secrets:
- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`

Required GitHub repository variables:
- `RESEARCH_AGENT_HOST`
- `RESEARCH_AGENT_TLS_SECRET_NAME`
- `RESEARCH_AGENT_RESOURCE_GROUP`
- `RESEARCH_AGENT_LOCATION`
- `RESEARCH_AGENT_ACR_NAME`
- `RESEARCH_AGENT_AKS_NAME`
- `RESEARCH_AGENT_AKS_NODE_COUNT`
- `RESEARCH_AGENT_AKS_VM_SIZE`
- `RESEARCH_AGENT_AKS_NAMESPACE`
- `RESEARCH_AGENT_KEY_VAULT_NAME`
- `TFSTATE_RESOURCE_GROUP`
- `TFSTATE_STORAGE_ACCOUNT`
- `TFSTATE_CONTAINER`
- `TFSTATE_KEY`

Optional GitHub repository variables:
- `KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON`

Recommended auth mode:
- GitHub OIDC with `azure/login@v2`

If the workflow shows `No subscriptions found`, the federated identity is trusted but the Entra application still lacks Azure RBAC on your subscription. For a fresh start, the application needs enough access to create the backend storage and the app resource group first. This Terraform setup can then assign project-level roles such as:
- `Contributor` on the project resource group
- `AcrPush` on the project ACR
- `AcrPull` on the project ACR

## Useful Commands

```bash
kubectl get pods -n research-agent-dev
kubectl get svc -n research-agent-dev
kubectl describe deploy research-agent -n research-agent-dev
kubectl logs deploy/research-agent -n research-agent-dev
```

## Final Production Flow

This is the recommended steady-state deployment model for `research_agent`.

1. Create infrastructure with Terraform
2. Use Terraform to assign:
   - AKS runtime roles
   - GitHub Actions deployment roles
   - Key Vault secret writer roles for human/admin identities
3. Build and push the app image to ACR
4. Deploy the app to AKS with Helm
5. Configure DNS:
   - `research.purpletechllc.com -> ingress public IP`
6. Install `cert-manager`
7. Create a `ClusterIssuer` for Let's Encrypt
8. Configure ingress to use:
   - host `research.purpletechllc.com`
   - annotation `cert-manager.io/cluster-issuer: letsencrypt-prod`
9. Let cert-manager create and renew the TLS secret automatically
10. Store runtime secrets in Azure Key Vault:
   - `openai-api-key`
   - `tavily-api-key`
11. Let AKS Key Vault CSI sync those secrets into the pod env
12. Validate:
   - `https://research.purpletechllc.com/health`
   - `https://research.purpletechllc.com/docs`
   - `POST /research`

## Next Improvements

- workload identity
- CI/CD
- autoscaling tuning
- private endpoints and tighter egress controls
- Gateway API migration path

## Official References

- AKS app routing: <https://learn.microsoft.com/en-us/azure/aks/app-routing>
- AKS Key Vault CSI provider: <https://learn.microsoft.com/en-us/azure/aks/csi-secrets-store-configuration-options>
- AKS identity access for Key Vault CSI: <https://learn.microsoft.com/en-us/azure/aks/csi-secrets-store-identity-access>
- AKS TLS with Secrets Store CSI: <https://learn.microsoft.com/en-us/azure/aks/csi-secrets-store-nginx-tls>
- AKS with GitHub Actions: <https://learn.microsoft.com/en-us/azure/aks/kubernetes-action>
