#!/usr/bin/env bash

set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required."
  echo "Install: https://cli.github.com/"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI is not authenticated."
  echo "Run: gh auth login"
  exit 1
fi

usage() {
  cat <<'EOF'
Usage:
  AZURE_CLIENT_ID=... AZURE_TENANT_ID=... AZURE_SUBSCRIPTION_ID=... \
  ./scripts/github/set-rag-system-github-config.sh

Optional environment overrides:
  RAG_SYSTEM_HOST
  RAG_SYSTEM_TLS_SECRET_NAME
  RAG_SYSTEM_RESOURCE_GROUP
  RAG_SYSTEM_LOCATION
  RAG_SYSTEM_ACR_NAME
  RAG_SYSTEM_AKS_NAME
  RAG_SYSTEM_AKS_NODE_COUNT
  RAG_SYSTEM_AKS_VM_SIZE
  RAG_SYSTEM_AKS_NAMESPACE
  RAG_SYSTEM_KEY_VAULT_NAME
  TFSTATE_RESOURCE_GROUP
  TFSTATE_STORAGE_ACCOUNT
  TFSTATE_CONTAINER
  TFSTATE_KEY
  KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON

Required secret environment variables (unless UPDATE_SECRETS=false):
  AZURE_CLIENT_ID
  AZURE_TENANT_ID
  AZURE_SUBSCRIPTION_ID

Optional environment overrides:
  UPDATE_SECRETS (default: true)
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

: "${UPDATE_SECRETS:=true}"

if [[ "${UPDATE_SECRETS}" == "true" ]]; then
  : "${AZURE_CLIENT_ID:?AZURE_CLIENT_ID is required}"
  : "${AZURE_TENANT_ID:?AZURE_TENANT_ID is required}"
  : "${AZURE_SUBSCRIPTION_ID:?AZURE_SUBSCRIPTION_ID is required}"
fi

: "${RAG_SYSTEM_HOST:=rag.purpletechllc.com}"
: "${RAG_SYSTEM_TLS_SECRET_NAME:=rag-system-tls}"
: "${RAG_SYSTEM_RESOURCE_GROUP:=rg-rag-system-dev}"
: "${RAG_SYSTEM_LOCATION:=eastus}"
: "${RAG_SYSTEM_ACR_NAME:=ragsystemacrdev}"
: "${RAG_SYSTEM_AKS_NAME:=aks-rag-system-dev}"
: "${RAG_SYSTEM_AKS_NODE_COUNT:=1}"
: "${RAG_SYSTEM_AKS_VM_SIZE:=Standard_DC2as_v5}"
: "${RAG_SYSTEM_AKS_NAMESPACE:=rag-system-dev}"
: "${RAG_SYSTEM_KEY_VAULT_NAME:=kv-rag-system-dev001}"
: "${TFSTATE_RESOURCE_GROUP:=rg-tfstate-shared-dev}"
: "${TFSTATE_STORAGE_ACCOUNT:=tfstateaiengplaybook01}"
: "${TFSTATE_CONTAINER:=tfstate}"
: "${TFSTATE_KEY:=rag-system-dev.tfstate}"
: "${KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON:=[]}"

if [[ -z "${TFSTATE_STORAGE_ACCOUNT}" ]]; then
  echo "TFSTATE_STORAGE_ACCOUNT is required and must be globally unique in Azure."
  exit 1
fi

set_repo_variable() {
  local name="$1"
  local value="$2"
  echo "Setting repo variable ${name}"
  gh variable set "${name}" --body "${value}"
}

set_repo_secret() {
  local name="$1"
  local value="$2"
  echo "Setting repo secret ${name}"
  gh secret set "${name}" --body "${value}"
}

if [[ "${UPDATE_SECRETS}" == "true" ]]; then
  set_repo_secret "AZURE_CLIENT_ID" "${AZURE_CLIENT_ID}"
  set_repo_secret "AZURE_TENANT_ID" "${AZURE_TENANT_ID}"
  set_repo_secret "AZURE_SUBSCRIPTION_ID" "${AZURE_SUBSCRIPTION_ID}"
fi

set_repo_variable "RAG_SYSTEM_HOST" "${RAG_SYSTEM_HOST}"
set_repo_variable "RAG_SYSTEM_TLS_SECRET_NAME" "${RAG_SYSTEM_TLS_SECRET_NAME}"
set_repo_variable "RAG_SYSTEM_RESOURCE_GROUP" "${RAG_SYSTEM_RESOURCE_GROUP}"
set_repo_variable "RAG_SYSTEM_LOCATION" "${RAG_SYSTEM_LOCATION}"
set_repo_variable "RAG_SYSTEM_ACR_NAME" "${RAG_SYSTEM_ACR_NAME}"
set_repo_variable "RAG_SYSTEM_AKS_NAME" "${RAG_SYSTEM_AKS_NAME}"
set_repo_variable "RAG_SYSTEM_AKS_NODE_COUNT" "${RAG_SYSTEM_AKS_NODE_COUNT}"
set_repo_variable "RAG_SYSTEM_AKS_VM_SIZE" "${RAG_SYSTEM_AKS_VM_SIZE}"
set_repo_variable "RAG_SYSTEM_AKS_NAMESPACE" "${RAG_SYSTEM_AKS_NAMESPACE}"
set_repo_variable "RAG_SYSTEM_KEY_VAULT_NAME" "${RAG_SYSTEM_KEY_VAULT_NAME}"
set_repo_variable "TFSTATE_RESOURCE_GROUP" "${TFSTATE_RESOURCE_GROUP}"
set_repo_variable "TFSTATE_STORAGE_ACCOUNT" "${TFSTATE_STORAGE_ACCOUNT}"
set_repo_variable "TFSTATE_CONTAINER" "${TFSTATE_CONTAINER}"
set_repo_variable "TFSTATE_KEY" "${TFSTATE_KEY}"
set_repo_variable "KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON" "${KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON}"

cat <<EOF

Applied rag-system GitHub configuration.

Settings:
  UPDATE_SECRETS=${UPDATE_SECRETS}

Variables:
  RAG_SYSTEM_HOST=${RAG_SYSTEM_HOST}
  RAG_SYSTEM_TLS_SECRET_NAME=${RAG_SYSTEM_TLS_SECRET_NAME}
  RAG_SYSTEM_RESOURCE_GROUP=${RAG_SYSTEM_RESOURCE_GROUP}
  RAG_SYSTEM_LOCATION=${RAG_SYSTEM_LOCATION}
  RAG_SYSTEM_ACR_NAME=${RAG_SYSTEM_ACR_NAME}
  RAG_SYSTEM_AKS_NAME=${RAG_SYSTEM_AKS_NAME}
  RAG_SYSTEM_AKS_NODE_COUNT=${RAG_SYSTEM_AKS_NODE_COUNT}
  RAG_SYSTEM_AKS_VM_SIZE=${RAG_SYSTEM_AKS_VM_SIZE}
  RAG_SYSTEM_AKS_NAMESPACE=${RAG_SYSTEM_AKS_NAMESPACE}
  RAG_SYSTEM_KEY_VAULT_NAME=${RAG_SYSTEM_KEY_VAULT_NAME}
  TFSTATE_RESOURCE_GROUP=${TFSTATE_RESOURCE_GROUP}
  TFSTATE_STORAGE_ACCOUNT=${TFSTATE_STORAGE_ACCOUNT}
  TFSTATE_CONTAINER=${TFSTATE_CONTAINER}
  TFSTATE_KEY=${TFSTATE_KEY}
  KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON=${KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON}

Next:
  gh workflow run rag-system-aks.yml
EOF
