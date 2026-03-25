# Reusable Azure Deployment Pattern

This folder documents the standard Azure deployment pattern for services in this repository.

Goal:
- keep Helm charts reusable and shared
- keep each project's Azure infra, values, and scripts local to that project
- make new service onboarding mostly a rename-and-fill exercise

## Standard Layout

For any project named `<service>`:

```text
projects/<service>/deploy/azure/
  values.yaml
  README.md
  quickstart.md
  architecture.md
  cert-manager-letsencrypt-sop.md
  terraform/
    versions.tf
    variables.tf
    main.tf
    outputs.tf
    envvars.auto.tfvars.example
```

Shared repo-wide assets:

```text
deploy/helm/charts/fastapi-service/
.github/workflows/<service>-aks.yml
deploy/azure/terraform/modules/
deploy/azure/github-federated-credential.main.json.example
deploy/azure/oidc-setup.md
```

## What Stays Global

- reusable Helm chart
- reusable deployment conventions
- general Azure documentation
- reusable Terraform modules

## What Stays Project-Specific

- resource names
- ports
- image name
- domain name
- Key Vault secret mappings
- Terraform state and variables
- GitHub workflow for that service

## Reusable Pattern

This is the recommended standard for all FastAPI services in this repo:

1. GitHub Actions bootstraps the Terraform backend in Azure Storage
2. Terraform creates:
   - Resource Group
   - ACR
   - AKS
   - Key Vault
   - RBAC for AKS runtime
   - optional RBAC for GitHub Actions
   - optional RBAC for secret administrators
3. GitHub Actions builds and pushes the image to ACR
4. Helm deploys the service using the shared chart
5. Ingress exposes the service
6. DNS points a hostname to the ingress IP
7. cert-manager + Let's Encrypt secures HTTPS
8. AKS Key Vault CSI injects runtime secrets

Important bootstrap note:
- Terraform cannot use Azure Blob state until the storage backend already exists
- the workflow should create that backend first with Azure CLI
- after that, Terraform owns the application infrastructure lifecycle

## Shared Terraform Modules

The shared Terraform now has three module layers:

- `deploy/azure/terraform/modules/aks_core_infra`
  - creates Resource Group, ACR, AKS, Key Vault
- `deploy/azure/terraform/modules/aks_security_rbac`
  - assigns RBAC for AKS runtime, GitHub Actions, and Key Vault secret admins
- `deploy/azure/terraform/modules/aks_service`
  - convenience composition module that calls both of the above
- `deploy/azure/terraform/modules/public_dns_record`
  - creates an Azure DNS A record that points a hostname to a public ingress IP

Recommended usage:
- use `aks_service` for most application projects
- use the smaller modules directly only if a project needs a non-standard split of infra and RBAC responsibilities
- use `public_dns_record` only when your DNS zone is hosted in Azure DNS

Important note:
- if your domain is hosted somewhere else, like DreamHost, Cloudflare, or GoDaddy, do not use the `public_dns_record` module
- in that case, create the DNS record in your DNS provider UI instead

### Example: Use `public_dns_record` In A Project

Use this only if your DNS zone is hosted in Azure DNS.

Example:

```hcl
module "public_dns_record" {
  source = "../../../../../deploy/azure/terraform/modules/public_dns_record"

  dns_zone_name           = "purpletechllc.com"
  dns_resource_group_name = "rg-shared-dns"
  record_name             = "research"
  ipv4_address            = "20.75.248.23"
  ttl                     = 300
}
```

This creates:

```text
research.purpletechllc.com -> 20.75.248.23
```

Typical usage:
- apply infra first
- get the ingress public IP
- then create or update the Azure DNS record with that IP

## Minimum Per-Project Changes

When cloning the pattern for a new project, change only these first:

- service name
- image name
- container port
- resource group name
- ACR name
- AKS name
- namespace
- Key Vault name
- ingress host
- required Key Vault secret names
- GitHub workflow file name

## Files To Reuse

- shared Helm chart:
  - `deploy/helm/charts/fastapi-service`
- project templates:
  - `deploy/azure/templates/project-values.yaml`
  - `deploy/azure/templates/project-dotenv.example`
  - `deploy/azure/templates/project-envvars.auto.tfvars.example`
  - `deploy/azure/templates/project-github-workflow.yml`
  - `deploy/azure/templates/project-checklist.md`

## Recommended Naming Convention

For a service called `my_service`:

- resource group: `rg-my-service-dev`
- aks: `aks-my-service-dev`
- acr: `myserviceacrdev`
- namespace: `my-service-dev`
- key vault: `kv-my-service-dev001`
- hostname: `my-service.example.com`
- image: `my-service`

## Notes

- use hyphenated Key Vault secret names:
  - `openai-api-key`, not `OPENAI_API_KEY`
- keep pod env var names app-friendly:
  - `OPENAI_API_KEY`
- prefer `ClusterIP` services and public ingress
- prefer cert-manager over manual TLS secrets
- prefer project-specific slim requirements files for Docker images

## Recommended First Copy Source

The current reference implementation is:

- `projects/research_agent/deploy/azure`

Use it as the working example, then normalize new services against the templates in this folder rather than copy-pasting everything blindly.
