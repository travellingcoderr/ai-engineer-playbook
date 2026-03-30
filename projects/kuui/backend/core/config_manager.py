from kubernetes import config
from typing import Dict, Any

class KubeConfigManager:
    """
    Singleton for managing Kubernetes configuration.
    """
    _instance = None
    _config_loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KubeConfigManager, cls).__new__(cls)
        return cls._instance

    def load_config(self) -> str:
        """
        Loads the kubeconfig from the standard location or environment variable.
        """
        try:
            config.load_kube_config()
            self._config_loaded = True
            return "Kubeconfig loaded successfully."
        except Exception as e:
            self._config_loaded = False
            return f"Error loading kubeconfig: {str(e)}"

    def get_contexts(self) -> Dict[str, Any]:
        """
        Retrieves all contexts enriched with cluster details.
        """
        if not self._config_loaded:
            self.load_config()
            
        try:
            contexts, current_context = config.list_kube_config_contexts()
            
            # Manually load kubeconfig to get cluster server URLs
            import yaml
            import os
            kube_path = os.getenv("KUBECONFIG") or os.path.expanduser("~/.kube/config")
            
            cluster_map = {}
            if os.path.exists(kube_path):
                with open(kube_path, 'r') as f:
                    cfg = yaml.safe_load(f)
                    for c in cfg.get('clusters', []):
                        cluster_map[c['name']] = c['cluster'].get('server', 'unknown')
            
            result_contexts = []
            for c in contexts:
                cluster_name = c['context']['cluster']
                result_contexts.append({
                    "name": c['name'],
                    "cluster": cluster_name,
                    "user": c['context'].get('user', 'unknown'),
                    "server": cluster_map.get(cluster_name, "unknown"),
                    "is_current": c['name'] == current_context['name'] if current_context else False
                })

            return {
                "contexts": result_contexts,
                "current_context": current_context['name'] if current_context else None
            }
        except Exception as e:
            return {"error": f"Failed to list contexts: {str(e)}"}

    def switch_context(self, context_name: str) -> bool:
        """
        Switches the current active context.
        """
        try:
            config.load_kube_config(context=context_name)
            return True
        except Exception:
            return False

    def delete_context(self, context_name: str) -> bool:
        """
        Deletes a context from the kubeconfig file.
        """
        import yaml
        import os
        kube_path = os.getenv("KUBECONFIG") or os.path.expanduser("~/.kube/config")
        
        if not os.path.exists(kube_path):
            return False
            
        try:
            with open(kube_path, 'r') as f:
                cfg = yaml.safe_load(f)
            
            # Filter out the context
            original_len = len(cfg.get('contexts', []))
            cfg['contexts'] = [c for c in cfg.get('contexts', []) if c['name'] != context_name]
            
            if len(cfg['contexts']) == original_len:
                return False # Context not found
                
            # Save back to file
            with open(kube_path, 'w') as f:
                yaml.dump(cfg, f, default_flow_style=False)
                
            # Re-initialize the kubernetes client
            self.load_config()
            return True
        except Exception:
            return False
