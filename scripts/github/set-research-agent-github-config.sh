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
  ./scripts/github/set-research-agent-github-config.sh

Optional environment overrides:
  RESEARCH_AGENT_HOST
  RESEARCH_AGENT_TLS_SECRET_NAME
  RESEARCH_AGENT_RESOURCE_GROUP
  RESEARCH_AGENT_LOCATION
  RESEARCH_AGENT_ACR_NAME
  RESEARCH_AGENT_AKS_NAME
  RESEARCH_AGENT_AKS_NODE_COUNT
  RESEARCH_AGENT_AKS_VM_SIZE
  RESEARCH_AGENT_AKS_NAMESPACE
  RESEARCH_AGENT_KEY_VAULT_NAME
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

: "${RESEARCH_AGENT_HOST:=research.purpletechllc.com}"
: "${RESEARCH_AGENT_TLS_SECRET_NAME:=research-agent-tls}"
: "${RESEARCH_AGENT_RESOURCE_GROUP:=rg-research-agent-dev}"
: "${RESEARCH_AGENT_LOCATION:=eastus}"
: "${RESEARCH_AGENT_ACR_NAME:=researchagentacrdev}"
: "${RESEARCH_AGENT_AKS_NAME:=aks-research-agent-dev}"
: "${RESEARCH_AGENT_AKS_NODE_COUNT:=1}"
: "${RESEARCH_AGENT_AKS_VM_SIZE:=Standard_DC2as_v5}"
: "${RESEARCH_AGENT_AKS_NAMESPACE:=research-agent-dev}"
: "${RESEARCH_AGENT_KEY_VAULT_NAME:=kv-research-agent-dev007}"
: "${TFSTATE_RESOURCE_GROUP:=rg-tfstate-shared-dev}"
: "${TFSTATE_STORAGE_ACCOUNT:=tfstateaiengplaybook01}"
: "${TFSTATE_CONTAINER:=tfstate}"
: "${TFSTATE_KEY:=research-agent-dev.tfstate}"
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

set_repo_variable "RESEARCH_AGENT_HOST" "${RESEARCH_AGENT_HOST}"
set_repo_variable "RESEARCH_AGENT_TLS_SECRET_NAME" "${RESEARCH_AGENT_TLS_SECRET_NAME}"
set_repo_variable "RESEARCH_AGENT_RESOURCE_GROUP" "${RESEARCH_AGENT_RESOURCE_GROUP}"
set_repo_variable "RESEARCH_AGENT_LOCATION" "${RESEARCH_AGENT_LOCATION}"
set_repo_variable "RESEARCH_AGENT_ACR_NAME" "${RESEARCH_AGENT_ACR_NAME}"
set_repo_variable "RESEARCH_AGENT_AKS_NAME" "${RESEARCH_AGENT_AKS_NAME}"
set_repo_variable "RESEARCH_AGENT_AKS_NODE_COUNT" "${RESEARCH_AGENT_AKS_NODE_COUNT}"
set_repo_variable "RESEARCH_AGENT_AKS_VM_SIZE" "${RESEARCH_AGENT_AKS_VM_SIZE}"
set_repo_variable "RESEARCH_AGENT_AKS_NAMESPACE" "${RESEARCH_AGENT_AKS_NAMESPACE}"
set_repo_variable "RESEARCH_AGENT_KEY_VAULT_NAME" "${RESEARCH_AGENT_KEY_VAULT_NAME}"
set_repo_variable "TFSTATE_RESOURCE_GROUP" "${TFSTATE_RESOURCE_GROUP}"
set_repo_variable "TFSTATE_STORAGE_ACCOUNT" "${TFSTATE_STORAGE_ACCOUNT}"
set_repo_variable "TFSTATE_CONTAINER" "${TFSTATE_CONTAINER}"
set_repo_variable "TFSTATE_KEY" "${TFSTATE_KEY}"
set_repo_variable "KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON" "${KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON}"

cat <<EOF

Applied research-agent GitHub configuration.

Settings:
  UPDATE_SECRETS=${UPDATE_SECRETS}

Variables:
  RESEARCH_AGENT_HOST=${RESEARCH_AGENT_HOST}
  RESEARCH_AGENT_TLS_SECRET_NAME=${RESEARCH_AGENT_TLS_SECRET_NAME}
  RESEARCH_AGENT_RESOURCE_GROUP=${RESEARCH_AGENT_RESOURCE_GROUP}
  RESEARCH_AGENT_LOCATION=${RESEARCH_AGENT_LOCATION}
  RESEARCH_AGENT_ACR_NAME=${RESEARCH_AGENT_ACR_NAME}
  RESEARCH_AGENT_AKS_NAME=${RESEARCH_AGENT_AKS_NAME}
  RESEARCH_AGENT_AKS_NODE_COUNT=${RESEARCH_AGENT_AKS_NODE_COUNT}
  RESEARCH_AGENT_AKS_VM_SIZE=${RESEARCH_AGENT_AKS_VM_SIZE}
  RESEARCH_AGENT_AKS_NAMESPACE=${RESEARCH_AGENT_AKS_NAMESPACE}
  RESEARCH_AGENT_KEY_VAULT_NAME=${RESEARCH_AGENT_KEY_VAULT_NAME}
  TFSTATE_RESOURCE_GROUP=${TFSTATE_RESOURCE_GROUP}
  TFSTATE_STORAGE_ACCOUNT=${TFSTATE_STORAGE_ACCOUNT}
  TFSTATE_CONTAINER=${TFSTATE_CONTAINER}
  TFSTATE_KEY=${TFSTATE_KEY}
  KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON=${KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON}

Next:
  gh workflow run services-aks.yml -f service=research_agent
EOF
