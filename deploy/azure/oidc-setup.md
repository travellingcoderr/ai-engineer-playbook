# GitHub OIDC Setup

This file explains when the shared federated credential example is used and how to create the credential in Azure.

## What This Is For

GitHub Actions uses OpenID Connect (OIDC) so workflows can log in to Azure without storing a client secret in GitHub.

In this repo, that is the auth model used by:
- `.github/workflows/research-agent-aks.yml`
- `.github/workflows/rag-system-aks.yml`

The shared example JSON lives here:
- `deploy/azure/github-federated-credential.main.json.example`

## When You Use This File

Use it when you are setting up a new Azure Entra application for GitHub Actions and need to add a federated credential for:
- this repository
- the `main` branch

You typically do this once per Azure Entra application.

You do not need one federated credential file per project because the credential trusts:
- the GitHub repository
- the Git branch

The project-specific Azure permissions are handled later by Azure RBAC and Terraform.

## What The Subject Means

The important field is:

```text
repo:travellingcoderr/ai-engineer-playbook:ref:refs/heads/main
```

That means:
- repo: `travellingcoderr/ai-engineer-playbook`
- branch: `main`

If your repo or default branch changes, update the subject accordingly.

## Azure CLI Command

First create or identify the Azure Entra application used by GitHub Actions.

Then run:

```bash
az ad app federated-credential create \
  --id "<AZURE_CLIENT_ID>" \
  --parameters @deploy/azure/github-federated-credential.main.json.example
```

`<AZURE_CLIENT_ID>` should be the application client ID you store in the GitHub secret:
- `AZURE_CLIENT_ID`

## Related GitHub Secrets

After the federated credential exists, the workflows use:
- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`

## Important Note

The federated credential only establishes trust between GitHub and Azure Entra ID.

It does not grant Azure access by itself.

The Azure Entra application still needs Azure RBAC, for example:
- subscription-level access for first-time Terraform backend bootstrap
- project-level access for ACR, AKS, and Key Vault related deployment work

## Bootstrap Limitation

Terraform can look up the GitHub Actions service principal from the application client ID and assign Azure RBAC to it.

However, Terraform cannot solve the first login failure for the same GitHub identity if that identity has no Azure access yet.

Why:
- `azure/login@v2` must succeed before the workflow can run Terraform
- if the identity has no subscription access, the workflow stops before Terraform starts

So the first subscription-level access still has to come from:
- a one-time manual Azure role assignment by an admin
- or a different already-authorized bootstrap identity

After that, Terraform can manage the ongoing RBAC for the GitHub identity.
