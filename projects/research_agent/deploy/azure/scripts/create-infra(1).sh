#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../../" && pwd)"
ENV_FILE="$PROJECT_ROOT/projects/research_agent/deploy/azure/.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE"
  echo "Copy .env.example to .env and set your values."
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

: "${AZURE_SUBSCRIPTION_ID:?Missing AZURE_SUBSCRIPTION_ID}"
: "${RESOURCE_GROUP:?Missing RESOURCE_GROUP}"
: "${LOCATION:?Missing LOCATION}"
: "${ACR_NAME:?Missing ACR_NAME}"
: "${AKS_NAME:?Missing AKS_NAME}"
: "${AKS_NODE_COUNT:?Missing AKS_NODE_COUNT}"
: "${AKS_VM_SIZE:?Missing AKS_VM_SIZE}"
: "${AKS_NAMESPACE:?Missing AKS_NAMESPACE}"
: "${KEY_VAULT_NAME:?Missing KEY_VAULT_NAME}"

az account set --subscription "$AZURE_SUBSCRIPTION_ID"

ADDONS=()
if [[ "${AKS_ENABLE_KEYVAULT_CSI:-true}" == "true" ]]; then
  ADDONS+=("azure-keyvault-secrets-provider")
fi
if [[ "${AKS_ENABLE_APP_ROUTING:-true}" == "true" ]]; then
  ADDONS+=("web_application_routing")
fi
ADDONS_ARG="$(IFS=,; echo "${ADDONS[*]}")"

az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

az acr create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$ACR_NAME" \
  --sku Basic

az aks create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$AKS_NAME" \
  --node-count "$AKS_NODE_COUNT" \
  --node-vm-size "$AKS_VM_SIZE" \
  --generate-ssh-keys

if [[ -n "$ADDONS_ARG" ]]; then
  az aks enable-addons \
    --resource-group "$RESOURCE_GROUP" \
    --name "$AKS_NAME" \
    --addons "$ADDONS_ARG"
fi

az aks update \
  --resource-group "$RESOURCE_GROUP" \
  --name "$AKS_NAME" \
  --attach-acr "$ACR_NAME"

az keyvault create \
  --name "$KEY_VAULT_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --enable-rbac-authorization true

CSI_CLIENT_ID="$(az aks show \
  --resource-group "$RESOURCE_GROUP" \
  --name "$AKS_NAME" \
  --query "addonProfiles.azureKeyvaultSecretsProvider.identity.clientId" \
  --output tsv)"

if [[ -n "${CSI_CLIENT_ID}" && "${AKS_ENABLE_KEYVAULT_CSI:-true}" == "true" ]]; then
  az role assignment create \
    --assignee "$CSI_CLIENT_ID" \
    --role "Key Vault Secrets User" \
    --scope "$(az keyvault show --name "$KEY_VAULT_NAME" --query id -o tsv)" \
    >/dev/null || true

  az role assignment create \
    --assignee "$CSI_CLIENT_ID" \
    --role "Key Vault Certificate User" \
    --scope "$(az keyvault show --name "$KEY_VAULT_NAME" --query id -o tsv)" \
    >/dev/null || true
fi

az aks get-credentials \
  --resource-group "$RESOURCE_GROUP" \
  --name "$AKS_NAME" \
  --overwrite-existing

kubectl create namespace "$AKS_NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

echo "Infrastructure created for research_agent."
