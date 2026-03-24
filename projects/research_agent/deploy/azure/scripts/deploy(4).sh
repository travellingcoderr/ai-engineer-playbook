#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../../" && pwd)"
ENV_FILE="$PROJECT_ROOT/projects/research_agent/deploy/azure/.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE"
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

: "${AKS_NAMESPACE:?Missing AKS_NAMESPACE}"
: "${HELM_RELEASE_NAME:?Missing HELM_RELEASE_NAME}"
: "${ACR_NAME:?Missing ACR_NAME}"
: "${IMAGE_NAME:?Missing IMAGE_NAME}"
: "${IMAGE_TAG:?Missing IMAGE_TAG}"
: "${INGRESS_HOST:?Missing INGRESS_HOST}"
: "${TLS_SECRET_NAME:?Missing TLS_SECRET_NAME}"
: "${KEY_VAULT_NAME:?Missing KEY_VAULT_NAME}"

helm upgrade --install "$HELM_RELEASE_NAME" \
  "$PROJECT_ROOT/deploy/helm/charts/fastapi-service" \
  --namespace "$AKS_NAMESPACE" \
  --create-namespace \
  -f "$PROJECT_ROOT/projects/research_agent/deploy/azure/values.yaml" \
  --set image.repository="${ACR_NAME}.azurecr.io/${IMAGE_NAME}" \
  --set image.tag="${IMAGE_TAG}" \
  --set ingress.enabled=true \
  --set ingress.host="${INGRESS_HOST}" \
  --set ingress.tls.enabled=true \
  --set ingress.tls.secretName="${TLS_SECRET_NAME}" \
  --set keyVault.enabled=true \
  --set keyVault.name="${KEY_VAULT_NAME}"
