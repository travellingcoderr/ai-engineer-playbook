# RAG System Azure Deployment

This folder contains project-specific Azure deployment assets for `projects/rag_system`.

What stays here:
- project-specific Terraform
- project-specific Helm values
- project-specific docs and workflow inputs

What stays shared:
- Helm chart:
  - `deploy/helm/charts/fastapi-service`
- reusable Azure templates and patterns:
  - `deploy/azure/README.md`

## Layout

- `values.yaml`
- `quickstart.md`
- `architecture.md`
- `terraform/`

The shared GitHub OIDC federated credential example lives here:
- `deploy/azure/github-federated-credential.main.json.example`

## Recommended Pattern

1. GitHub Actions bootstraps remote Terraform state
2. Terraform creates Azure infra
3. GitHub Actions builds and pushes the image to ACR
4. GitHub Actions deploys with the shared FastAPI Helm chart
5. Point DNS to the ingress IP
6. Use cert-manager + Let's Encrypt for trusted HTTPS
7. Store runtime secrets in Key Vault and inject them through AKS CSI

## Service Notes

Compared with `research_agent`, `rag_system` is more likely to need:
- vector store settings
- embedding settings
- document ingestion-related configuration
- possibly persistent storage choices later

Start simple, then expand the values and Key Vault secrets only when the code path actually needs them.
