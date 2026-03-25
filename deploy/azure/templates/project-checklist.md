# Azure Project Checklist

Use this checklist when creating Azure deployment support for a new project.

## 1. Project Folder

Create:

```text
projects/<service>/deploy/azure/
```

Add:
- `values.yaml`
- `README.md`
- `quickstart.md`
- `architecture.md`
- `terraform/`

## 2. Runtime Inputs

Decide:
- container port
- required non-secret env vars
- required Key Vault secrets
- ingress hostname
- namespace

## 3. Docker

Create:
- project-specific slim requirements file
- project Dockerfile

Confirm:
- only needed project files are copied into build context

## 4. Terraform

Set:
- resource group
- ACR
- AKS
- Key Vault
- RBAC for AKS runtime
- RBAC for GitHub Actions
- RBAC for secret admins

## 5. Helm

Reuse:
- `deploy/helm/charts/fastapi-service`

Customize:
- `projects/<service>/deploy/azure/values.yaml`

## 6. GitHub Actions

Create:
- `.github/workflows/<service>-aks.yml`

Set secrets:
- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`

Set variables:
- `<SERVICE>_HOST`
- `<SERVICE>_TLS_SECRET_NAME`
- `<SERVICE>_RESOURCE_GROUP`
- `<SERVICE>_LOCATION`
- `<SERVICE>_ACR_NAME`
- `<SERVICE>_AKS_NAME`
- `<SERVICE>_AKS_NODE_COUNT`
- `<SERVICE>_AKS_VM_SIZE`
- `<SERVICE>_AKS_NAMESPACE`
- `<SERVICE>_KEY_VAULT_NAME`
- `TFSTATE_RESOURCE_GROUP`
- `TFSTATE_STORAGE_ACCOUNT`
- `TFSTATE_CONTAINER`
- `TFSTATE_KEY`

## 7. DNS + TLS

Set:
- DNS `A` record to ingress IP
- cert-manager + Let's Encrypt
- ingress host annotation and TLS secret

If the DNS zone is hosted in Azure DNS:
- optionally use `deploy/azure/terraform/modules/public_dns_record`

If the DNS zone is external:
- create the DNS record in the provider UI

## 8. Validate

Check:
- pods
- service
- ingress
- certificate
- Key Vault secret sync
- app health
- public endpoint
