from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.config_manager import KubeConfigManager
from core.resource_manager import KubeResourceManager
import os

app = FastAPI(title="KUUI API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Managers
kube_config = KubeConfigManager()
kube_config.load_config()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/contexts")
async def get_contexts():
    return kube_config.get_contexts()

@app.post("/contexts/switch")
async def switch_context(name: str):
    success = kube_config.switch_context(name)
    if not success:
        raise HTTPException(status_code=400, detail=f"Failed to switch to context: {name}")
    return {"status": "success", "current_context": name}

@app.get("/cluster/overview")
async def get_cluster_overview():
    resource_manager = KubeResourceManager()
    return resource_manager.get_cluster_overview()

@app.get("/resources/namespaces")
async def get_namespaces():
    resource_manager = KubeResourceManager()
    return resource_manager.get_namespaces()

@app.get("/resources/pods")
async def get_pods(namespace: str = "default"):
    resource_manager = KubeResourceManager()
    return resource_manager.get_pods(namespace)

@app.get("/resources/services")
async def get_services(namespace: str = "default"):
    resource_manager = KubeResourceManager()
    return resource_manager.get_services(namespace)

@app.get("/resources/deployments")
async def get_deployments(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_deployments(namespace)

@app.get("/resources/statefulsets")
async def get_statefulsets(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_statefulsets(namespace)

@app.get("/resources/daemonsets")
async def get_daemonsets(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_daemonsets(namespace)

@app.get("/resources/ingresses")
async def get_ingresses(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_ingresses(namespace)

@app.get("/resources/networkpolicies")
async def get_network_policies(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_network_policies(namespace)

@app.get("/resources/pods/{name}/logs")
async def get_pod_logs(name: str, namespace: str = "default"):
    manager = KubeResourceManager()
    return {"logs": manager.get_pod_logs(name, namespace)}

@app.get("/resources/pods/{name}/describe")
async def describe_pod(name: str, namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.describe_pod(name, namespace)

@app.get("/resources/pvcs")
async def get_pvcs(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_pvcs(namespace)

@app.get("/resources/configmaps")
async def get_configmaps(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_configmaps(namespace)

@app.get("/resources/secrets")
async def get_secrets(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_secrets(namespace)

@app.get("/resources/hpas")
async def get_hpas(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_hpas(namespace)

@app.get("/resources/serviceaccounts")
async def get_service_accounts(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_service_accounts(namespace)

@app.get("/resources/roles")
async def get_roles(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_roles(namespace)

@app.get("/resources/rolebindings")
async def get_role_bindings(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_role_bindings(namespace)

@app.get("/resources/clusterroles")
async def get_cluster_roles():
    manager = KubeResourceManager()
    return manager.get_cluster_roles()

@app.get("/resources/clusterrolebindings")
async def get_cluster_role_bindings():
    manager = KubeResourceManager()
    return manager.get_cluster_role_bindings()

@app.get("/resources/certificates")
async def get_certificates():
    manager = KubeResourceManager()
    return manager.get_certificates()

@app.get("/resources/istio/virtualservices")
async def get_istio_virtual_services(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_istio_virtual_services(namespace)

@app.get("/resources/istio/gateways")
async def get_istio_gateways(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_istio_gateways(namespace)

@app.get("/resources/events")
async def get_events(namespace: str = "default"):
    manager = KubeResourceManager()
    return manager.get_events(namespace)

from core.constants import PORT_BACKEND

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT_BACKEND)
