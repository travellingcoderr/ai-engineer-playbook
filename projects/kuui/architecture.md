# KUUI Architecture: Kubernetes Master UI

This document provides a technical overview of how KUUI maps physical Kubernetes concepts to its internal logic and user interface.

## 🏗️ System Components

KUUI is a containerized, decoupled application designed for local and production-grade cluster management:

1. **Frontend (Next.js)**: A premium, React-based dashboard using TailwindCSS and Lucide-React for low-latency cluster visualization.
2. **Backend (FastAPI)**: A modular Python service that acts as a secure proxy to the Kubernetes API.
3. **Orchestration (Docker Compose)**: Manages local lifecycle and mounts the host's `~/.kube/config` into the backend for zero-touch configuration.

---

## 🔗 Kubernetes Concept Mapping

### 1. Clusters & Contexts
A **Cluster** is a group of nodes. A **Context** (stored in `kubeconfig`) is a specific connection profile (Cluster + User + Namespace).
- **KUUI Implementation**: The sidebar displays all available contexts. Switching contexts in the UI triggers a global reload of the `kubernetes-python` client in the backend.

### 2. Nodes & Resources
Nodes are the physical/virtual machines. Resources (Pods, Services, Deployments) are the workloads.
- **KUUI Implementation**: 
  - **Stats Bar**: Aggregates node health and cluster-wide capacity.
  - **Resource Manager**: Decouples logic for fetching pods/services into dedicated modular handlers.

### 3. Networking (Ingress & Services)
- **Services (ClusterIP/LoadBalancer)**: Internal/External entry points.
- **Ingress**: Traffic routing from external domains (like `api.purpletechllc.com`) to internal services.
- **KUUI Implementation**: KUUI aims to provide a **"Hawk-Eye View"** of traffic flow, which will eventually be visualized using Mermaid.js diagrams.

---

## 📡 Data Flow

1. **User Action**: Selecting a new cluster in the Sidebar.
2. **API Request**: `POST /contexts/switch?name=aks-cluster`.
3. **Backend Logic**:
   - `KubeConfigManager` (Singleton) reloads the config with the new context.
   - All subsequent calls to `CoreV1Api` or `AppsV1Api` now point to the new cluster.
4. **UI Update**: Next.js state refreshes, fetching new pod/node lists.

---

## 🔒 Security Principles
- **Read-Only by Default**: Most operations are GET-based for safe cluster inspection.
- **Host Isolation**: KUUI runs in Docker but only interacts with the mounted `~/.kube/config`, strictly honoring your local RBAC permissions.
