# KUUI - Kubernetes User Interface

KUUI is a developer-centric "Hawk-Eye" dashboard for Kubernetes clusters. It provides real-time visibility into your workloads, networking, and diagnostics directly from your local environment.

## 🚀 Getting Started

Ensure you have **Docker** and **Docker Compose** installed.

### 1. Start the Application
Run this from the root of the `projects/kuui` directory:

```bash
docker-compose up --build
```

### 2. Access the Dashboard
- **Frontend**: [http://localhost:3030](http://localhost:3030)
- **Backend API**: [http://localhost:8080](http://localhost:8080)

## 📁 Project Structure

```bash
kuui/
├── frontend/        # Next.js (React) Application
├── backend/         # FastAPI (Python) Service
│   └── core/        # Modular Kube Managers (Singleton)
└── docker-compose.yaml
```

## 🛠️ Key Commands

| Action | Command |
| :--- | :--- |
| **Start Services** | `docker-compose up -d` |
| **Stop Services** | `docker-compose down` |
| **View Logs** | `docker-compose logs -f` |
| **Rebuild** | `docker-compose build --no-cache` |

## 🛡️ Security & Configuration
KUUI mounts your local **`~/.kube/config`** directly into the backend container. 

> [!IMPORTANT]
> To switch clusters, use the Context Switcher in the UI. If you add a new cluster to your host's kubeconfig, restart the containers to refresh the shared volume.

## 📝 Troubleshooting
- **Connection Refused**: Ensure the backend container is healthy and port 8000 is not blocked.
- **Kubeconfig Error**: Verify that `${HOME}/.kube/config` exists on your host machine.
