from kubernetes import client
from typing import List, Dict, Any

class KubeResourceManager:
    """
    Class for interacting with Kubernetes resources.
    """
    def __init__(self):
        # We assume config is already loaded by KubeConfigManager
        self.v1 = client.CoreV1Api()
        self.appsv1 = client.AppsV1Api()
        self.custom_api = client.CustomObjectsApi()

    def get_cluster_overview(self) -> Dict[str, Any]:
        """
        Retrieves high-level cluster statistics.
        """
        try:
            # Get Nodes
            nodes = self.v1.list_node()
            total_nodes = len(nodes.items)
            
            # Count Healthy Nodes
            healthy_nodes = 0
            for node in nodes.items:
                for condition in node.status.conditions:
                    if condition.type == 'Ready' and condition.status == 'True':
                        healthy_nodes += 1
                        break
            
            # Get Cluster-wide Pod Health
            all_pods = self.v1.list_pod_for_all_namespaces()
            total_pods = len(all_pods.items)
            running_pods = len([p for p in all_pods.items if p.status.phase == 'Running'])
            pod_health_pct = round((running_pods / total_pods * 100), 1) if total_pods > 0 else 100.0

            # Get K8s Version
            version_api = client.VersionApi()
            version_info = version_api.get_code()
            
            return {
                "total_nodes": total_nodes,
                "healthy_nodes": healthy_nodes,
                "api_version": version_info.git_version,
                "platform": version_info.platform,
                "pod_health_pct": f"{pod_health_pct}%",
                "total_pods": total_pods
            }
        except Exception as e:
            return {"error": f"Failed to get cluster overview: {str(e)}"}

    def get_namespaces(self) -> List[str]:
        try:
            ns_list = self.v1.list_namespace()
            return [ns.metadata.name for ns in ns_list.items]
        except Exception:
            return []

    def get_pods(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            pods = self.v1.list_namespaced_pod(namespace)
            res = []
            for p in pods.items:
                # Extract combined reason and restart count from containers
                restarts = 0
                reason = p.status.phase
                message = ""
                
                if p.status.container_statuses:
                    for cs in p.status.container_statuses:
                        restarts += cs.restart_count
                        if cs.state.waiting:
                            reason = cs.state.waiting.reason
                            message = cs.state.waiting.message or ""
                        elif cs.state.terminated:
                            reason = cs.state.terminated.reason
                            message = cs.state.terminated.message or ""

                res.append({
                    "name": p.metadata.name,
                    "status": p.status.phase,
                    "reason": reason,
                    "message": message,
                    "restarts": restarts,
                    "ip": p.status.pod_ip,
                    "node": p.spec.node_name,
                    "istio_injected": any(c.name == 'istio-proxy' for c in p.spec.containers) if p.spec.containers else False,
                    "creation_timestamp": p.metadata.creation_timestamp
                })
            return res
        except Exception:
            return []

    def get_services(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            svcs = self.v1.list_namespaced_service(namespace)
            return [
                {
                    "name": s.metadata.name,
                    "type": s.spec.type,
                    "cluster_ip": s.spec.cluster_ip,
                    "external_ip": s.status.load_balancer.ingress[0].ip if s.status.load_balancer.ingress else None,
                    "selector": s.spec.selector,
                    "ports": [
                        {
                            "port": p.port,
                            "target_port": p.target_port,
                            "node_port": p.node_port,
                            "protocol": p.protocol
                        } for p in s.spec.ports
                    ] if s.spec.ports else []
                } for s in svcs.items
            ]
        except Exception:
            return []

    def get_deployments(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            deps = self.appsv1.list_namespaced_deployment(namespace)
            return [
                {
                    "name": d.metadata.name,
                    "replicas": d.spec.replicas,
                    "available_replicas": d.status.available_replicas,
                    "image": d.spec.template.spec.containers[0].image if d.spec.template.spec.containers else "N/A",
                    "creation_timestamp": d.metadata.creation_timestamp,
                    "selector": d.spec.selector.match_labels if d.spec.selector else {},
                    "strategy": d.spec.strategy.type if d.spec.strategy else "RollingUpdate"
                } for d in deps.items
            ]
        except Exception:
            return []

    def get_statefulsets(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            ss = self.appsv1.list_namespaced_stateful_set(namespace)
            return [
                {
                    "name": s.metadata.name,
                    "replicas": s.spec.replicas,
                    "ready_replicas": s.status.ready_replicas or 0,
                    "image": s.spec.template.spec.containers[0].image if s.spec.template.spec.containers else "N/A",
                    "creation_timestamp": s.metadata.creation_timestamp
                } for s in ss.items
            ]
        except Exception:
            return []

    def get_daemonsets(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            ds = self.appsv1.list_namespaced_daemon_set(namespace)
            return [
                {
                    "name": s.metadata.name,
                    "desired": s.status.desired_number_scheduled,
                    "current": s.status.current_number_scheduled,
                    "ready": s.status.number_ready,
                    "image": s.spec.template.spec.containers[0].image if s.spec.template.spec.containers else "N/A",
                    "creation_timestamp": s.metadata.creation_timestamp
                } for s in ds.items
            ]
        except Exception:
            return []

    def get_ingresses(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            networking_v1 = client.NetworkingV1Api()
            ings = networking_v1.list_namespaced_ingress(namespace)
            return [
                {
                    "name": i.metadata.name,
                    "hosts": [rule.host for rule in i.spec.rules] if i.spec.rules else [],
                    "address": i.status.load_balancer.ingress[0].ip if i.status.load_balancer.ingress else (i.status.load_balancer.ingress[0].hostname if i.status.load_balancer.ingress and i.status.load_balancer.ingress[0].hostname else None),
                    "creation_timestamp": i.metadata.creation_timestamp,
                    "annotations": i.metadata.annotations or {}
                } for i in ings.items
            ]
        except Exception:
            return []

    def get_network_policies(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            networking_v1 = client.NetworkingV1Api()
            policies = networking_v1.list_namespaced_network_policy(namespace)
            return [
                {
                    "name": p.metadata.name,
                    "pod_selector": p.spec.pod_selector.match_labels if p.spec.pod_selector else {},
                    "policy_types": p.spec.policy_types or [],
                    "creation_timestamp": p.metadata.creation_timestamp
                } for p in policies.items
            ]
        except Exception:
            return []

    def get_pod_logs(self, name: str, namespace: str = "default") -> str:
        try:
            return self.v1.read_namespaced_pod_log(name, namespace, tail_lines=100)
        except Exception as e:
            return f"Error fetching logs: {str(e)}"

    def describe_pod(self, name: str, namespace: str = "default") -> Dict[str, Any]:
        try:
            pod = self.v1.read_namespaced_pod(name, namespace)
            
            # Fetch events for this pod
            events = self.v1.list_namespaced_event(namespace, field_selector=f"involvedObject.name={name}")
            event_list = [
                {
                    "type": e.type,
                    "reason": e.reason,
                    "message": e.message,
                    "last_timestamp": e.last_timestamp
                } for e in events.items
            ]

            return {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "node": pod.spec.node_name,
                "start_time": pod.status.start_time,
                "phase": pod.status.phase,
                "pod_ip": pod.status.pod_ip,
                "containers": [
                    {
                        "name": c.name,
                        "image": c.image,
                        "ready": next((s.ready for s in pod.status.container_statuses if s.name == c.name), False) if pod.status.container_statuses else False,
                        "restart_count": next((s.restart_count for s in pod.status.container_statuses if s.name == c.name), 0) if pod.status.container_statuses else 0
                    } for c in pod.spec.containers
                ],
                "events": event_list
            }
        except Exception as e:
            return {"error": f"Failed to describe pod: {str(e)}"}

    def get_pvcs(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            pvcs = self.v1.list_namespaced_persistent_volume_claim(namespace)
            return [
                {
                    "name": p.metadata.name,
                    "status": p.status.phase,
                    "capacity": p.status.capacity.get("storage") if p.status.capacity else "N/A",
                    "access_modes": p.spec.access_modes,
                    "storage_class": p.spec.storage_class_name,
                    "creation_timestamp": p.metadata.creation_timestamp
                } for p in pvcs.items
            ]
        except Exception:
            return []

    def get_configmaps(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            cms = self.v1.list_namespaced_config_map(namespace)
            return [
                {
                    "name": c.metadata.name,
                    "data_keys": list(c.data.keys()) if c.data else [],
                    "creation_timestamp": c.metadata.creation_timestamp
                } for c in cms.items
            ]
        except Exception:
            return []

    def get_secrets(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            secrets = self.v1.list_namespaced_secret(namespace)
            return [
                {
                    "name": s.metadata.name,
                    "type": s.type,
                    "data_keys": list(s.data.keys()) if s.data else [],
                    "creation_timestamp": s.metadata.creation_timestamp
                } for s in secrets.items
            ]
        except Exception:
            return []

    def get_hpas(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            autoscaling_v1 = client.AutoscalingV1Api()
            hpas = autoscaling_v1.list_namespaced_horizontal_pod_autoscaler(namespace)
            return [
                {
                    "name": h.metadata.name,
                    "min_replicas": h.spec.min_replicas,
                    "max_replicas": h.spec.max_replicas,
                    "current_replicas": h.status.current_replicas,
                    "desired_replicas": h.status.desired_replicas,
                    "current_cpu_utilization": h.status.current_cpu_utilization_percentage,
                    "target_cpu_utilization": h.spec.target_cpu_utilization_percentage,
                    "creation_timestamp": h.metadata.creation_timestamp
                } for h in hpas.items
            ]
        except Exception:
            return []

    def get_service_accounts(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            sa_list = self.v1.list_namespaced_service_account(namespace)
            return [
                {
                    "name": sa.metadata.name,
                    "secrets_count": len(sa.secrets) if sa.secrets else 0,
                    "creation_timestamp": sa.metadata.creation_timestamp
                } for sa in sa_list.items
            ]
        except Exception:
            return []

    def get_roles(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            rbac_v1 = client.RbacAuthorizationV1Api()
            roles = rbac_v1.list_namespaced_role(namespace)
            return [
                {
                    "name": r.metadata.name,
                    "rules_count": len(r.rules) if r.rules else 0,
                    "creation_timestamp": r.metadata.creation_timestamp
                } for r in roles.items
            ]
        except Exception:
            return []

    def get_role_bindings(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            rbac_v1 = client.RbacAuthorizationV1Api()
            bindings = rbac_v1.list_namespaced_role_binding(namespace)
            return [
                {
                    "name": b.metadata.name,
                    "role_ref": b.role_ref.name,
                    "subjects": [{"kind": s.kind, "name": s.name} for s in b.subjects] if b.subjects else [],
                    "creation_timestamp": b.metadata.creation_timestamp
                } for b in bindings.items
            ]
        except Exception:
            return []

    def get_cluster_roles(self) -> List[Dict[str, Any]]:
        try:
            rbac_v1 = client.RbacAuthorizationV1Api()
            roles = rbac_v1.list_cluster_role()
            # Filter system roles to keep UI clean, but return them sorted
            return sorted([
                {
                    "name": r.metadata.name,
                    "rules_count": len(r.rules) if r.rules else 0,
                    "creation_timestamp": r.metadata.creation_timestamp
                } for r in roles.items
            ], key=lambda x: x['name'].startswith('system:'))
        except Exception:
            return []

    def get_cluster_role_bindings(self) -> List[Dict[str, Any]]:
        try:
            rbac_v1 = client.RbacAuthorizationV1Api()
            bindings = rbac_v1.list_cluster_role_binding()
            return sorted([
                {
                    "name": b.metadata.name,
                    "role_ref": b.role_ref.name,
                    "subjects": [{"kind": s.kind, "name": s.name} for s in b.subjects] if b.subjects else [],
                    "creation_timestamp": b.metadata.creation_timestamp
                } for b in bindings.items
            ], key=lambda x: x['name'].startswith('system:'))
        except Exception:
            return []

    def get_certificates(self) -> List[Dict[str, Any]]:
        """
        Retrieves CertificateSigningRequest (CSR) resources and TLS secrets.
        """
        try:
            cert_v1 = client.CertificatesV1Api()
            csrs = cert_v1.list_certificate_signing_request()
            
            res = []
            for c in csrs.items:
                # Determine status
                status = "Pending"
                if c.status.conditions:
                    last_condition = c.status.conditions[-1]
                    status = last_condition.type
                
                res.append({
                    "name": c.metadata.name,
                    "signer_name": c.spec.signer_name,
                    "status": status,
                    "usages": c.spec.usages or [],
                    "creation_timestamp": c.metadata.creation_timestamp,
                    "username": c.spec.username
                })
            return res
        except Exception as e:
            print(f"Error fetching certificates: {str(e)}")
            return []

    def get_istio_virtual_services(self, namespace: str = "default") -> List[Dict[str, Any]]:
        """
        Retrieves Istio VirtualServices.
        """
        try:
            res = self.custom_api.list_namespaced_custom_object(
                group="networking.istio.io",
                version="v1beta1",
                namespace=namespace,
                plural="virtualservices"
            )
            return [
                {
                    "name": i["metadata"]["name"],
                    "hosts": i["spec"].get("hosts", []),
                    "gateways": i["spec"].get("gateways", []),
                    "creation_timestamp": i["metadata"]["creation_timestamp"]
                } for i in res["items"]
            ]
        except Exception:
            return []

    def get_istio_gateways(self, namespace: str = "default") -> List[Dict[str, Any]]:
        """
        Retrieves Istio Gateways.
        """
        try:
            res = self.custom_api.list_namespaced_custom_object(
                group="networking.istio.io",
                version="v1beta1",
                namespace=namespace,
                plural="gateways"
            )
            return [
                {
                    "name": i["metadata"]["name"],
                    "selector": i["spec"].get("selector", {}),
                    "servers": [
                        {
                            "port": s.get("port", {}),
                            "hosts": s.get("hosts", [])
                        } for s in i["spec"].get("servers", [])
                    ],
                    "creation_timestamp": i["metadata"]["creation_timestamp"]
                } for i in res["items"]
            ]
        except Exception:
            return []

    def get_events(self, namespace: str = "default") -> List[Dict[str, Any]]:
        """
        Retrieves recent events from the namespace.
        """
        try:
            events = self.v1.list_namespaced_event(namespace, limit=50)
            res = []
            for e in events.items:
                res.append({
                    "name": e.metadata.name,
                    "reason": e.reason,
                    "message": e.message,
                    "type": e.type, # Normal or Warning
                    "count": e.count,
                    "first_timestamp": e.first_timestamp,
                    "last_timestamp": e.last_timestamp,
                    "object": f"{e.involved_object.kind}/{e.involved_object.name}",
                    "component": e.source.component or "unknown"
                })
            # Sort by last timestamp (most recent first)
            res.sort(key=lambda x: str(x["last_timestamp"] or ""), reverse=True)
            return res
        except Exception:
            return []
