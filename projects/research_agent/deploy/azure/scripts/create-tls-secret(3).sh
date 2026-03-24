#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../../" && pwd)"
ENV_FILE="$PROJECT_ROOT/projects/research_agent/deploy/azure/.env"

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <tls.crt path> <tls.key path>"
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE"
  exit 1
fi

TLS_CERT_PATH="$1"
TLS_KEY_PATH="$2"

set -a
source "$ENV_FILE"
set +a

: "${AKS_NAMESPACE:?Missing AKS_NAMESPACE}"
: "${TLS_SECRET_NAME:?Missing TLS_SECRET_NAME}"

kubectl create secret tls "$TLS_SECRET_NAME" \
  --namespace "$AKS_NAMESPACE" \
  --cert="$TLS_CERT_PATH" \
  --key="$TLS_KEY_PATH" \
  --dry-run=client -o yaml | kubectl apply -f -
