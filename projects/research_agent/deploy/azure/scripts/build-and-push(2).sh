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

: "${AZURE_SUBSCRIPTION_ID:?Missing AZURE_SUBSCRIPTION_ID}"
: "${ACR_NAME:?Missing ACR_NAME}"
: "${IMAGE_NAME:?Missing IMAGE_NAME}"
: "${IMAGE_TAG:?Missing IMAGE_TAG}"

az account set --subscription "$AZURE_SUBSCRIPTION_ID"

cd "$PROJECT_ROOT"

az acr build \
  --registry "$ACR_NAME" \
  --image "${IMAGE_NAME}:${IMAGE_TAG}" \
  --file projects/research_agent/Dockerfile \
  .
