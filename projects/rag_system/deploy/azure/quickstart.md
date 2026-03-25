# RAG System Azure Quickstart

Use the GitHub Actions + Terraform path.

1. Set the Azure OIDC GitHub secrets:
   - `AZURE_CLIENT_ID`
   - `AZURE_TENANT_ID`
   - `AZURE_SUBSCRIPTION_ID`

2. Set the GitHub variables for `rag_system`, including:
   - `RAG_SYSTEM_HOST`
   - `RAG_SYSTEM_TLS_SECRET_NAME`
   - `RAG_SYSTEM_RESOURCE_GROUP`
   - `RAG_SYSTEM_LOCATION`
   - `RAG_SYSTEM_ACR_NAME`
   - `RAG_SYSTEM_AKS_NAME`
   - `RAG_SYSTEM_AKS_NODE_COUNT`
   - `RAG_SYSTEM_AKS_VM_SIZE`
   - `RAG_SYSTEM_AKS_NAMESPACE`
   - `RAG_SYSTEM_KEY_VAULT_NAME`
   - `TFSTATE_RESOURCE_GROUP`
   - `TFSTATE_STORAGE_ACCOUNT`
   - `TFSTATE_CONTAINER`
   - `TFSTATE_KEY`

3. Optional helper:

```bash
AZURE_CLIENT_ID="<client-id>" \
AZURE_TENANT_ID="<tenant-id>" \
AZURE_SUBSCRIPTION_ID="<subscription-id>" \
TFSTATE_STORAGE_ACCOUNT="<globally-unique-storage-account>" \
./scripts/github/set-rag-system-github-config.sh
```

4. Push to `main` or run:

```bash
gh workflow run rag-system-aks.yml
```

5. Verify:

```bash
kubectl get pods -n rag-system-dev
kubectl get ingress -n rag-system-dev
```

For production HTTPS:
- follow the cert-manager pattern from:
  - `projects/research_agent/deploy/azure/cert-manager-letsencrypt-sop.md`
