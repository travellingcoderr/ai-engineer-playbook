from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.config_manager import KubeConfigManager
from core.resource_manager import KubeResourceManager
import os
import subprocess
import yaml
import tempfile
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

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

class HelmRenderRequest(BaseModel):
    values: Dict[str, Any]

@app.post("/helm/render")
async def render_helm(request: HelmRenderRequest):
    """
    Renders the base-api-chart with provided values.
    """
    # More robust path discovery: Find 'helm-templates' up the directory tree
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chart_path = None
    
    # Search up to 5 levels for the helm-templates directory
    search_dir = current_dir
    for _ in range(5):
        potential_path = os.path.join(search_dir, "helm-templates", "base-api-chart")
        if os.path.exists(potential_path):
            chart_path = potential_path
            break
        search_dir = os.path.dirname(search_dir)
        if search_dir == os.path.dirname(search_dir): # Root reached
            break
    
    if not chart_path:
        # Fallback to the original logic if walking up fails
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        chart_path = os.path.join(base_dir, "helm-templates", "base-api-chart")

    print(f"DEBUG: Rendering Helm chart using path: {chart_path}")
    
    if not os.path.exists(chart_path):
        raise HTTPException(status_code=404, detail=f"Base chart not found at {chart_path}")

    # Use a temporary file for values
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tf:
        yaml.dump(request.values, tf)
        temp_values_path = tf.name

    try:
        # Run helm template
        cmd = ["helm", "template", "preview", chart_path, "-f", temp_values_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"manifests": result.stdout}
    except FileNotFoundError:
        print("ERROR: 'helm' binary not found in system path")
        raise HTTPException(
            status_code=500, 
            detail="Helm not found. Please ensure Helm is installed in the container."
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr or str(e)
        print(f"ERROR: Helm rendering failed: {error_msg}")
        return {"error": error_msg}
    except Exception as e:
        print(f"ERROR: Unexpected rendering error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_values_path):
            os.remove(temp_values_path)

@app.get("/contexts")
async def get_contexts():
    return kube_config.get_contexts()

@app.post("/contexts/switch")
async def switch_context(name: str):
    success = kube_config.switch_context(name)
    if not success:
        raise HTTPException(status_code=400, detail=f"Failed to switch to context: {name}")
    return {"status": "success", "current_context": name}

@app.delete("/contexts/{name}")
async def delete_context(name: str):
    success = kube_config.delete_context(name)
    if not success:
        raise HTTPException(status_code=400, detail=f"Failed to delete context: {name}")
    return {"status": "success", "deleted_context": name}

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
