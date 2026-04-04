#!/bin/bash

# InsureDoc Master Environment Setup
# This script generates a unified .env file for the entire platform.

echo "🚀 Starting InsureDoc Master Setup (Unified Docker-Native)..."

# 1. CREATE MASTER ROOT .ENV
cat <<EOF > .env
# --- COMMON CONFIG ---
AZURE_AUTH_BYPASS=true

# --- INGESTION SERVICE ---
INGESTION_PORT=3001
VECTOR_STORE_PROVIDER=chroma
CHROMA_URL=http://chromadb:8000

# --- CLAIM SERVICE ---
CLAIM_PORT=3002
MONGODB_URL=mongodb://mongodb:27017/insuredoc
DB_PROVIDER=local

# --- ORCHESTRATOR SERVICE ---
ORCHESTRATOR_PORT=3003
INGESTION_URL=http://ingestion-service:3001
CLAIM_SERVICE_URL=http://claim-service:3002

# --- AZURE OPENAI CREDENTIALS (REPLACE THESE) ---
AZURE_OPENAI_INSTANCE_NAME=your-instance-name
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-01
EOF

echo "✅ Master .env created at project root"

# 2. CLEANUP OLD FRAGMENTED ENVS (IF ANY)
rm -f ingestion-service/.env claim-service/.env orchestrator-service/.env

echo "🎉 Master Setup Complete!"
echo "👉 1. Edit the '.env' file at the root with your actual Azure details."
echo "👉 2. Run: docker-compose up --build"
