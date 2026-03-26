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
  ./scripts/github/set-service-github-config.sh <service>

Supported services:
  research_agent
  rag_system

Optional environment overrides:
  SERVICE_HOST
  SERVICE_TLS_SECRET_NAME
  SERVICE_RESOURCE_GROUP
  SERVICE_LOCATION
  SERVICE_ACR_NAME
  SERVICE_AKS_NAME
  SERVICE_AKS_NODE_COUNT
  SERVICE_AKS_VM_SIZE
  SERVICE_AKS_NODE_POOL_MAX_SURGE
  SERVICE_AKS_NAMESPACE
  SERVICE_KEY_VAULT_NAME
  TFSTATE_RESOURCE_GROUP
  TFSTATE_STORAGE_ACCOUNT
  TFSTATE_CONTAINER
  TFSTATE_KEY
  KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON
  ENABLE_RBAC_ROLE_ASSIGNMENTS
  ENABLE_GITHUB_ACTIONS_SUBSCRIPTION_ROLE_ASSIGNMENTS
  ENABLE_GITHUB_ACTIONS_SUBSCRIPTION_CONTRIBUTOR
  ENABLE_GITHUB_ACTIONS_USER_ACCESS_ADMINISTRATOR
  ENABLE_RESEARCH_AGENT_DEPLOY
  ENABLE_RAG_SYSTEM_DEPLOY
  UPDATE_SECRETS (default: true)

Required secret environment variables (unless UPDATE_SECRETS=false):
  AZURE_CLIENT_ID
  AZURE_TENANT_ID
  AZURE_SUBSCRIPTION_ID
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || $# -ne 1 ]]; then
  usage
  exit $([[ $# -eq 1 ]] && echo 0 || echo 1)
fi

service="$1"
service_key_upper=""
workflow_input=""

case "${service}" in
  research_agent)
    service_key_upper="RESEARCH_AGENT"
    workflow_input="research_agent"
    : "${SERVICE_HOST:=research.purpletechllc.com}"
    : "${SERVICE_TLS_SECRET_NAME:=research-agent-tls}"
    : "${SERVICE_RESOURCE_GROUP:=rg-research-agent-dev}"
    : "${SERVICE_LOCATION:=eastus}"
    : "${SERVICE_ACR_NAME:=researchagentacrdev}"
    : "${SERVICE_AKS_NAME:=aks-research-agent-dev}"
    : "${SERVICE_AKS_NODE_COUNT:=1}"
    : "${SERVICE_AKS_VM_SIZE:=Standard_DC2as_v5}"
    : "${SERVICE_AKS_NODE_POOL_MAX_SURGE:=0}"
    : "${SERVICE_AKS_NAMESPACE:=research-agent-dev}"
    : "${SERVICE_KEY_VAULT_NAME:=kv-research-agent-dev007}"
    : "${TFSTATE_KEY:=research-agent-dev.tfstate}"
    ;;
  rag_system)
    service_key_upper="RAG_SYSTEM"
    workflow_input="rag_system"
    : "${SERVICE_HOST:=rag.purpletechllc.com}"
    : "${SERVICE_TLS_SECRET_NAME:=rag-system-tls}"
    : "${SERVICE_RESOURCE_GROUP:=rg-rag-system-dev}"
    : "${SERVICE_LOCATION:=eastus}"
    : "${SERVICE_ACR_NAME:=ragsystemacrdev}"
    : "${SERVICE_AKS_NAME:=aks-rag-system-dev}"
    : "${SERVICE_AKS_NODE_COUNT:=1}"
    : "${SERVICE_AKS_VM_SIZE:=Standard_DC2as_v5}"
    : "${SERVICE_AKS_NODE_POOL_MAX_SURGE:=0}"
    : "${SERVICE_AKS_NAMESPACE:=rag-system-dev}"
    : "${SERVICE_KEY_VAULT_NAME:=kv-rag-system-dev001}"
    : "${TFSTATE_KEY:=rag-system-dev.tfstate}"
    ;;
  *)
    echo "Unsupported service: ${service}"
    usage
    exit 1
    ;;
esac

: "${UPDATE_SECRETS:=true}"

if [[ "${UPDATE_SECRETS}" == "true" ]]; then
  : "${AZURE_CLIENT_ID:?AZURE_CLIENT_ID is required}"
  : "${AZURE_TENANT_ID:?AZURE_TENANT_ID is required}"
  : "${AZURE_SUBSCRIPTION_ID:?AZURE_SUBSCRIPTION_ID is required}"
fi

: "${TFSTATE_RESOURCE_GROUP:=rg-tfstate-shared-dev}"
: "${TFSTATE_STORAGE_ACCOUNT:=tfstateaiengplaybook01}"
: "${TFSTATE_CONTAINER:=tfstate}"
: "${KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON:=[]}"
: "${ENABLE_RBAC_ROLE_ASSIGNMENTS:=true}"
: "${ENABLE_GITHUB_ACTIONS_SUBSCRIPTION_ROLE_ASSIGNMENTS:=false}"
: "${ENABLE_GITHUB_ACTIONS_SUBSCRIPTION_CONTRIBUTOR:=false}"
: "${ENABLE_GITHUB_ACTIONS_USER_ACCESS_ADMINISTRATOR:=false}"
: "${ENABLE_RESEARCH_AGENT_DEPLOY:=true}"
: "${ENABLE_RAG_SYSTEM_DEPLOY:=true}"

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

set_repo_variable "${service_key_upper}_HOST" "${SERVICE_HOST}"
set_repo_variable "${service_key_upper}_TLS_SECRET_NAME" "${SERVICE_TLS_SECRET_NAME}"
set_repo_variable "${service_key_upper}_RESOURCE_GROUP" "${SERVICE_RESOURCE_GROUP}"
set_repo_variable "${service_key_upper}_LOCATION" "${SERVICE_LOCATION}"
set_repo_variable "${service_key_upper}_ACR_NAME" "${SERVICE_ACR_NAME}"
set_repo_variable "${service_key_upper}_AKS_NAME" "${SERVICE_AKS_NAME}"
set_repo_variable "${service_key_upper}_AKS_NODE_COUNT" "${SERVICE_AKS_NODE_COUNT}"
set_repo_variable "${service_key_upper}_AKS_VM_SIZE" "${SERVICE_AKS_VM_SIZE}"
set_repo_variable "${service_key_upper}_AKS_NODE_POOL_MAX_SURGE" "${SERVICE_AKS_NODE_POOL_MAX_SURGE}"
set_repo_variable "${service_key_upper}_AKS_NAMESPACE" "${SERVICE_AKS_NAMESPACE}"
set_repo_variable "${service_key_upper}_KEY_VAULT_NAME" "${SERVICE_KEY_VAULT_NAME}"
set_repo_variable "TFSTATE_RESOURCE_GROUP" "${TFSTATE_RESOURCE_GROUP}"
set_repo_variable "TFSTATE_STORAGE_ACCOUNT" "${TFSTATE_STORAGE_ACCOUNT}"
set_repo_variable "TFSTATE_CONTAINER" "${TFSTATE_CONTAINER}"
set_repo_variable "KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON" "${KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON}"
set_repo_variable "ENABLE_RBAC_ROLE_ASSIGNMENTS" "${ENABLE_RBAC_ROLE_ASSIGNMENTS}"
set_repo_variable "ENABLE_GITHUB_ACTIONS_SUBSCRIPTION_ROLE_ASSIGNMENTS" "${ENABLE_GITHUB_ACTIONS_SUBSCRIPTION_ROLE_ASSIGNMENTS}"
set_repo_variable "ENABLE_GITHUB_ACTIONS_SUBSCRIPTION_CONTRIBUTOR" "${ENABLE_GITHUB_ACTIONS_SUBSCRIPTION_CONTRIBUTOR}"
set_repo_variable "ENABLE_GITHUB_ACTIONS_USER_ACCESS_ADMINISTRATOR" "${ENABLE_GITHUB_ACTIONS_USER_ACCESS_ADMINISTRATOR}"
set_repo_variable "ENABLE_RESEARCH_AGENT_DEPLOY" "${ENABLE_RESEARCH_AGENT_DEPLOY}"
set_repo_variable "ENABLE_RAG_SYSTEM_DEPLOY" "${ENABLE_RAG_SYSTEM_DEPLOY}"

if [[ "${service}" == "research_agent" ]]; then
  set_repo_variable "TFSTATE_KEY_RESEARCH_AGENT" "${TFSTATE_KEY}"
elif [[ "${service}" == "rag_system" ]]; then
  set_repo_variable "TFSTATE_KEY_RAG_SYSTEM" "${TFSTATE_KEY}"
fi

cat <<EOF

Applied ${service} GitHub configuration.

Settings:
  UPDATE_SECRETS=${UPDATE_SECRETS}

Variables:
  ${service_key_upper}_HOST=${SERVICE_HOST}
  ${service_key_upper}_TLS_SECRET_NAME=${SERVICE_TLS_SECRET_NAME}
  ${service_key_upper}_RESOURCE_GROUP=${SERVICE_RESOURCE_GROUP}
  ${service_key_upper}_LOCATION=${SERVICE_LOCATION}
  ${service_key_upper}_ACR_NAME=${SERVICE_ACR_NAME}
  ${service_key_upper}_AKS_NAME=${SERVICE_AKS_NAME}
  ${service_key_upper}_AKS_NODE_COUNT=${SERVICE_AKS_NODE_COUNT}
  ${service_key_upper}_AKS_VM_SIZE=${SERVICE_AKS_VM_SIZE}
  ${service_key_upper}_AKS_NODE_POOL_MAX_SURGE=${SERVICE_AKS_NODE_POOL_MAX_SURGE}
  ${service_key_upper}_AKS_NAMESPACE=${SERVICE_AKS_NAMESPACE}
  ${service_key_upper}_KEY_VAULT_NAME=${SERVICE_KEY_VAULT_NAME}
  TFSTATE_RESOURCE_GROUP=${TFSTATE_RESOURCE_GROUP}
  TFSTATE_STORAGE_ACCOUNT=${TFSTATE_STORAGE_ACCOUNT}
  TFSTATE_CONTAINER=${TFSTATE_CONTAINER}
  TFSTATE_KEY=${TFSTATE_KEY}
  KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON=${KEY_VAULT_SECRETS_OFFICER_OBJECT_IDS_JSON}
  ENABLE_RBAC_ROLE_ASSIGNMENTS=${ENABLE_RBAC_ROLE_ASSIGNMENTS}
  ENABLE_GITHUB_ACTIONS_SUBSCRIPTION_ROLE_ASSIGNMENTS=${ENABLE_GITHUB_ACTIONS_SUBSCRIPTION_ROLE_ASSIGNMENTS}
  ENABLE_GITHUB_ACTIONS_SUBSCRIPTION_CONTRIBUTOR=${ENABLE_GITHUB_ACTIONS_SUBSCRIPTION_CONTRIBUTOR}
  ENABLE_GITHUB_ACTIONS_USER_ACCESS_ADMINISTRATOR=${ENABLE_GITHUB_ACTIONS_USER_ACCESS_ADMINISTRATOR}
  ENABLE_RESEARCH_AGENT_DEPLOY=${ENABLE_RESEARCH_AGENT_DEPLOY}
  ENABLE_RAG_SYSTEM_DEPLOY=${ENABLE_RAG_SYSTEM_DEPLOY}

Next:
  gh workflow run services-aks.yml -f service=${workflow_input}
EOF
