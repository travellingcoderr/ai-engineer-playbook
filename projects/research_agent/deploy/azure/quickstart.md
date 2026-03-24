# Research Agent Azure Quickstart

This is the shortest shell-script path to get `research_agent` deployed to AKS.

## Prerequisites

Install:
- Azure CLI
- kubectl
- Helm

Links:
- <https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest>
- <https://kubernetes.io/docs/tasks/tools/install-kubectl/>
- <https://helm.sh/docs/intro/install/>

## First-Time Setup

From the repo root:

```bash
cp projects/research_agent/deploy/azure/.env.example projects/research_agent/deploy/azure/.env
```

Edit the file:

```bash
open -a TextEdit projects/research_agent/deploy/azure/.env
```

Log in to Azure:

```bash
az login
```

## Run In Order

### 1. Create Azure infrastructure

```bash
./projects/research_agent/deploy/azure/scripts/create-infra(1).sh
```

### 2. Build the Docker image and push to ACR

```bash
./projects/research_agent/deploy/azure/scripts/build-and-push(2).sh
```

### 3. Create TLS secret for ingress

Only run this if you already have `tls.crt` and `tls.key`.

```bash
./projects/research_agent/deploy/azure/scripts/create-tls-secret(3).sh /path/to/tls.crt /path/to/tls.key
```

### 4. Deploy to AKS with Helm

```bash
./projects/research_agent/deploy/azure/scripts/deploy(4).sh
```

## Verify Deployment

```bash
kubectl get pods -n research-agent-dev
kubectl get svc -n research-agent-dev
kubectl get ingress -n research-agent-dev
kubectl logs deploy/research-agent -n research-agent-dev
```

## Typical Next Steps

- Add your app secret to Azure Key Vault
- Point DNS for `INGRESS_HOST` to the ingress public IP
- Create a valid TLS secret if you want HTTPS

## If You Want To Skip TLS For Now

You can skip step 3, but then you should disable TLS-related settings in:

- `projects/research_agent/deploy/azure/.env`
- `projects/research_agent/deploy/azure/values.yaml`

At minimum, make sure the ingress host value is correct for your environment.
