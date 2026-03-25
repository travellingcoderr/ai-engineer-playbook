# Research Agent Azure Quickstart

This file documents the GitHub Actions + Terraform path.

## Prerequisites

Install:
- Azure CLI
- kubectl
- Helm

Links:
- <https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest>
- <https://kubernetes.io/docs/tasks/tools/install-kubectl/>
- <https://helm.sh/docs/intro/install/>

## Preferred Path: GitHub Actions + Terraform

Use this when you want Azure resources created by the workflow instead of from your machine.

### 1. Configure GitHub secrets

- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`

### 2. Configure GitHub variables

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

Optional:
- `KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON`

Helper script:

```bash
AZURE_CLIENT_ID="<client-id>" \
AZURE_TENANT_ID="<tenant-id>" \
AZURE_SUBSCRIPTION_ID="db909f94-f59e-4ca4-acad-e2839e7af5f4" \
TFSTATE_STORAGE_ACCOUNT="<globally-unique-storage-account>" \
./scripts/github/set-service-github-config.sh research_agent
```

### 3. Push to `main` or run the workflow manually

Workflow:

```text
.github/workflows/services-aks.yml
```

### 4. Let the workflow run in this order

1. bootstrap Terraform backend storage
2. `terraform init`
3. `terraform plan`
4. `terraform apply`
5. Docker build + push to ACR
6. Helm deploy to AKS

### 5. Verify

```bash
kubectl get pods -n research-agent-dev
kubectl get ingress -n research-agent-dev
```

## Typical Next Steps

- Add your app secret to Azure Key Vault
- Point DNS for `INGRESS_HOST` to the ingress public IP
- Follow `cert-manager-letsencrypt-sop.md` to enable trusted HTTPS with automatic renewal
