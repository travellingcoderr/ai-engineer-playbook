# Global Helm Charts

This folder contains reusable Helm charts shared across projects in this repository.

Recommended pattern:
- project-specific infrastructure and scripts live under each project
- reusable Kubernetes packaging lives here
- each project keeps its own values file next to its deployment scripts

Current reusable charts:
- `charts/fastapi-service`: generic FastAPI chart for AKS deployments with ingress, TLS, probes, and optional Key Vault CSI secret sync
