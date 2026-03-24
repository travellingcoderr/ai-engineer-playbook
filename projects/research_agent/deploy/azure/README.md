# Research Agent Azure Deployment

This folder contains project-specific Azure infrastructure and deployment assets for `projects/research_agent`.

## What This Folder Owns

- Azure resource creation for this project
- ACR image build and push for this project
- project-specific Helm values for this project
- Project-scoped environment files

The reusable Helm chart used by this project lives globally at:
- `deploy/helm/charts/fastapi-service`

## Layout

- `.env.example`: shell-based configuration for Azure CLI scripts
- `scripts/`: Azure CLI automation for infra, image build, and deployment
- `terraform/`: Terraform-based infrastructure for this project
- `values.yaml`: project-specific values for the global FastAPI Helm chart
- `architecture.md`: ingress, egress, and network diagram
- `github-federated-credential.main.json.example`: GitHub OIDC federated credential template for the `main` branch

## Recommendation

Use this folder as the source of truth for `research_agent` infrastructure.

If you want shell scripts:
- use `.env`
- run the scripts in `scripts/`

If you want Terraform:
- copy `terraform/envvars.auto.tfvars.example` to `terraform/envvars.auto.tfvars`
- run Terraform from `terraform/`

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

## Option A: Azure CLI + `.env`

Copy the example file:

```bash
cp projects/research_agent/deploy/azure/.env.example projects/research_agent/deploy/azure/.env
```

Update values, then run:

```bash
./projects/research_agent/deploy/azure/scripts/create-infra(1).sh
./projects/research_agent/deploy/azure/scripts/build-and-push(2).sh
./projects/research_agent/deploy/azure/scripts/create-tls-secret(3).sh /path/to/tls.crt /path/to/tls.key
./projects/research_agent/deploy/azure/scripts/deploy(4).sh
```

## Option B: Terraform

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

Then build and deploy:

```bash
./projects/research_agent/deploy/azure/scripts/build-and-push(2).sh
./projects/research_agent/deploy/azure/scripts/deploy(4).sh
```

If you want Terraform to assign GitHub Actions access too:
- set `github_actions_client_id` to the same value you use for `AZURE_CLIENT_ID`
- set `enable_github_actions_role_assignments = true`

## Default Azure Resources

The scripts and Terraform create:
- Resource Group
- Azure Container Registry
- AKS cluster
- ACR attachment to AKS
- Azure Key Vault
- Kubernetes namespace for this app

## Typical End-to-End Flow

1. Create Azure resources
2. Get AKS credentials
3. Build image from `projects/research_agent/Dockerfile`
4. Push image to ACR
5. Deploy Helm chart
6. Check service external IP

The deployment uses:
- global shared chart: `deploy/helm/charts/fastapi-service`
- project values: `projects/research_agent/deploy/azure/values.yaml`

## Script Order

Use the shell scripts in this order:

1. `create-infra(1).sh`
2. `build-and-push(2).sh`
3. `create-tls-secret(3).sh` only if ingress TLS is enabled
4. `deploy(4).sh`

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

## Ingress And TLS

The chart supports an ingress resource in front of the service.

Default traffic flow:
- Internet client -> public IP on ingress controller -> ingress rule -> Kubernetes Service -> research-agent pods

TLS:
- TLS terminates at the ingress controller
- the ingress controller presents the certificate for your hostname
- traffic from ingress to the service inside the cluster is HTTP in this starter setup

This starter expects the TLS certificate to be available as a Kubernetes TLS secret.

Create it with:

```bash
./projects/research_agent/deploy/azure/scripts/create-tls-secret(3).sh /path/to/tls.crt /path/to/tls.key
```

Then deploy the chart.

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
- `ACR_NAME`
- `AKS_RESOURCE_GROUP`
- `AKS_NAME`
- `KEY_VAULT_NAME`
- `AKS_KEYVAULT_CSI_CLIENT_ID`
- `RESEARCH_AGENT_HOST`
- `RESEARCH_AGENT_TLS_SECRET_NAME`

Recommended auth mode:
- GitHub OIDC with `azure/login@v2`

If the workflow shows `No subscriptions found`, the federated identity is trusted but the Entra application still lacks Azure RBAC on your subscription or resource group. This Terraform setup can now assign:
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
