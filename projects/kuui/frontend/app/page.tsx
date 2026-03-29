'use client'

import React, { useState, useEffect } from 'react'
import { 
  Activity, 
  Box, 
  Cloud, 
  Cpu, 
  Globe, 
  Layout, 
  Search, 
  ShieldCheck, 
  Terminal,
  Server,
  Workflow,
  Info,
  Copy,
  Check,
  ExternalLink,
  AlertTriangle,
  ChevronDown,
  ChevronRight,
  Database,
  FileText,
  Lock,
  Network,
  X,
  FileJson,
  RefreshCcw,
  Download,
  Terminal as TerminalIcon,
  Pencil,
  Zap
} from 'lucide-react'
import mermaid from 'mermaid'

// Mermaid initialization
mermaid.initialize({
  startOnLoad: true,
  theme: 'dark',
  securityLevel: 'loose',
  fontFamily: 'Inter'
})



function TerminalModal({ 
  isOpen, 
  onClose, 
  title, 
  content, 
  loading 
}: { 
  isOpen: boolean, 
  onClose: () => void, 
  title: string, 
  content: string | object, 
  loading: boolean 
}) {
  if (!isOpen) return null

  const formattedContent = typeof content === 'string' ? content : JSON.stringify(content, null, 2);

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-12 animate-in fade-in duration-300">
      <div className="absolute inset-0 bg-kube-dark/80 backdrop-blur-sm" onClick={onClose}></div>
      <div className="bg-[#0b0e14] border border-white/10 w-full max-w-5xl h-[80vh] rounded-2xl shadow-2xl flex flex-col relative overflow-hidden ring-1 ring-white/5">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/5 bg-white/5">
          <div className="flex items-center space-x-3">
            <div className="flex space-x-1.5">
              <div className="w-3 h-3 rounded-full bg-red-500/50"></div>
              <div className="w-3 h-3 rounded-full bg-amber-500/50"></div>
              <div className="w-3 h-3 rounded-full bg-emerald-500/50"></div>
            </div>
            <div className="h-4 w-[1px] bg-white/10 mx-2"></div>
            <h3 className="text-sm font-bold text-white/60 font-mono flex items-center space-x-2 italic">
              <Terminal size={14} className="text-kube-blue" />
              <span>{title}</span>
            </h3>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-white/10 rounded-full transition-colors text-white/40 hover:text-white">
            <X size={20} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-6 font-mono text-sm leading-relaxed selection:bg-kube-blue/30">
          {loading ? (
            <div className="flex flex-col items-center justify-center h-full space-y-4">
              <div className="w-8 h-8 border-2 border-kube-blue border-t-transparent animate-spin rounded-full"></div>
              <p className="text-white/20 animate-pulse">Fetching data from K8s API...</p>
            </div>
          ) : (
            <pre className="text-emerald-400/90 whitespace-pre-wrap whitespace-pre break-all">
              {formattedContent || "No data returned."}
            </pre>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-white/5 bg-black/20 flex justify-between items-center text-[10px] text-white/20 font-bold uppercase tracking-widest">
          <div className="flex items-center space-x-4">
            <span>Lines: {formattedContent.split('\n').length}</span>
            <span>Type: Monospaced</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
            <span>Connected to {title.split(' ')[0]}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

function SidebarCategory({ 
  label, 
  icon, 
  isOpen, 
  onToggle, 
  children 
}: { 
  label: string, 
  icon: React.ReactNode, 
  isOpen: boolean, 
  onToggle: () => void, 
  children: React.ReactNode 
}) {
  return (
    <div className="space-y-1">
      <div 
        onClick={onToggle}
        className="flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer transition-all text-white/40 hover:text-white hover:bg-white/5 font-bold uppercase tracking-widest text-[10px]"
      >
        <div className="flex items-center space-x-2">
          {icon}
          <span>{label}</span>
        </div>
        {isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
      </div>
      {isOpen && <div className="ml-4 space-y-1 animate-in slide-in-from-left-2 duration-200">{children}</div>}
    </div>
  )
}


function CopyButton({ text, label }: { text: string, label?: string }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = (e: React.MouseEvent) => {
    e.stopPropagation()
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <button 
      onClick={handleCopy}
      className="p-1.5 hover:bg-white/10 rounded-md transition-all flex items-center space-x-1 group/copy relative"
      title={label || "Copy to clipboard"}
    >
      {copied ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} className="text-white/40 group-hover/copy:text-white" />}
      {label && <span className="text-[10px] uppercase font-bold text-white/40 group-hover/copy:text-white">{label}</span>}
      
      {copied && (
        <div className="absolute -top-8 left-1/2 -translate-x-1/2 px-2 py-1 bg-emerald-500 text-white text-[10px] rounded shadow-lg animate-in fade-in zoom-in duration-200">
          Copied!
        </div>
      )}
    </button>
  )
}

function EventsTimeline({ events }: { events: any[] }) {
  if (!events || events.length === 0) return <EmptyState resource="Events" />
  
  return (
    <div className="space-y-4">
      {events.map((e, i) => (
        <div key={i} className="group p-4 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all relative overflow-hidden text-left">
          <div className={`absolute left-0 top-0 h-full w-1 ${e.type === 'Warning' ? 'bg-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.5)]' : 'bg-emerald-500/50'}`}></div>
          <div className="flex justify-between items-start">
            <div className="flex items-start space-x-3">
              <div className={`mt-1 w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${e.type === 'Warning' ? 'bg-amber-500/10 border border-amber-500/20' : 'bg-emerald-500/10 border border-emerald-500/20'}`}>
                {e.type === 'Warning' ? <AlertTriangle size={14} className="text-amber-500" /> : <Activity size={14} className="text-emerald-500" />}
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <span className={`text-[10px] font-black uppercase tracking-widest px-1.5 py-0.5 rounded ${e.type === 'Warning' ? 'bg-amber-500/20 text-amber-500' : 'bg-emerald-500/20 text-emerald-500'}`}>
                    {e.reason}
                  </span>
                  <span className="text-[10px] text-white/20 font-mono">{e.object}</span>
                </div>
                <p className="text-xs text-white/70 mt-1 leading-relaxed">{e.message}</p>
                <div className="flex items-center space-x-3 mt-2 text-[10px] text-white/20 font-bold uppercase tracking-tighter">
                  <span>Count: {e.count}</span>
                  <span>•</span>
                  <span>{e.last_timestamp ? new Date(e.last_timestamp).toLocaleString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) : 'N/A'}</span>
                  <span>•</span>
                  <span className="text-white/40">{e.component}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

const resourceDescriptions: Record<string, { title: string, description: string, icon: any }> = {
  'workloads/pods': { 
    title: 'Pods', 
    description: 'The smallest deployable units of computing that you can create and manage in Kubernetes.',
    icon: <Box size={18} className="text-kube-blue" />
  },
  'workloads/deployments': { 
    title: 'Deployments', 
    description: 'Provide declarative updates for Pods and ReplicaSets.',
    icon: <Workflow size={18} className="text-purple-400" />
  },
  'networking/services': { 
    title: 'Services', 
    description: 'An abstract way to expose an application running on a set of Pods as a network service.',
    icon: <Globe size={18} className="text-emerald-400" />
  },
  'storage/pvcs': { 
    title: 'Persistent Volume Claims', 
    description: 'A request for storage by a user, similar to a Pod requesting node resources.',
    icon: <Database size={18} className="text-amber-400" />
  },
  'config/configmaps': { 
    title: 'ConfigMaps', 
    description: 'This is where your application environment variables (app_env) and non-confidential configuration files are stored. Pods inject these at runtime as environment variables or mounted files.',
    icon: <FileText size={18} className="text-blue-400" />
  },
  'config/secrets': { 
    title: 'Secrets', 
    description: 'This is the source for sensitive application variables like database credentials, API keys, and OAuth tokens. They are encoded by default and can be injected into your pods securely.',
    icon: <Lock size={18} className="text-red-400" />
  },
  'mesh/virtualservices': { 
    title: 'Istio VirtualServices', 
    description: 'Define a set of traffic routing rules to apply when a host is addressed.',
    icon: <ShieldCheck size={18} className="text-kube-blue" />
  },
  'mesh/gateways': { 
    title: 'Istio Gateways', 
    description: 'Describe a load balancer operating at the edge of the mesh receiving incoming or outgoing HTTP/TCP connections.',
    icon: <ShieldCheck size={18} className="text-kube-blue" />
  },

  'workloads/statefulsets': { 
    title: 'StatefulSets', 
    description: 'Manages the deployment and scaling of a set of Pods, and provides guarantees about the ordering and uniqueness of these Pods. These are essential for stateful applications like Databases.',
    icon: <Server size={18} className="text-emerald-400" />
  },
  'workloads/daemonsets': { 
    title: 'DaemonSets', 
    description: 'Ensures that all (or some) Nodes run a copy of a Pod. These are typically used for background tasks like logging agents or monitoring systems that must exist on every server.',
    icon: <Activity size={18} className="text-amber-400" />
  },
  'workloads/hpas': { 
    title: 'Horizontal Pod Autoscalers', 
    description: 'Automatically scales the number of Pods in a replication controller, deployment, replica set or stateful set based on observed CPU utilization or other metrics.',
    icon: <Zap size={18} className="text-kube-blue" />
  },
  'networking/ingress': { 
    title: 'Ingress', 
    description: 'An API object that manages external access to the services in a cluster, typically HTTP. Ingress provides load balancing, SSL termination and name-based virtual hosting.',
    icon: <Globe size={18} className="text-kube-blue" />
  },
  'networking/networkpolicies': { 
    title: 'Network Policies', 
    description: 'Specifications of how groups of pods are allowed to communicate with each other and other network endpoints. This is the L3/L4 firewall for your Kubernetes namespace.',
    icon: <ShieldCheck size={18} className="text-amber-400" />
  },
  'rbac/serviceaccounts': { 
    title: 'ServiceAccounts', 
    description: 'Provides an identity for processes that run in a Pod. Applications use these to securely interact with the Kubernetes API server.',
    icon: <Lock size={18} className="text-emerald-400" />
  },
  'rbac/roles': { 
    title: 'Roles', 
    description: 'Contains rules that represent a set of permissions within a namespace. Roles are scope-restricted to the current namespace.',
    icon: <ShieldCheck size={18} className="text-emerald-400" />
  },
  'rbac/rolebindings': { 
    title: 'RoleBindings', 
    description: 'Grants the permissions defined in a role to a user or set of users. Linking a Role to a ServiceAccount is done here.',
    icon: <ShieldCheck size={18} className="text-blue-400" />
  },
  'rbac/clusterroles': { 
    title: 'ClusterRoles', 
    description: 'A cluster-level resource that can be used to grant permissions across the entire cluster. Often used for shared resources like Nodes or across all namespaces.',
    icon: <ShieldCheck size={18} className="text-red-400" />
  },
  'rbac/clusterrolebindings': { 
    title: 'ClusterRoleBindings', 
    description: 'Grants permissions cluster-wide to a user or set of users. This is used for powerful administrative or cross-namespace permissions.',
    icon: <ShieldCheck size={18} className="text-red-500" />
  },
  'infra/certificates': { 
    title: 'Certificates (SSL/TLS Hub)', 
    description: 'A centralized view of Certificate Signing Requests (CSRs). This is where you approve and manage SSL/TLS certificates for secure pod communication.',
    icon: <ShieldCheck size={18} className="text-blue-400" />
  },
  'infra/helm': { 
    title: 'Helm Chart Designer', 
    description: 'Visual architect for defining your infrastructure. Scaffold production-ready charts with Deployments, Services, and Ingress in a standardized way.',
    icon: <Cloud size={18} className="text-purple-400" />
  },
  'observability/traffic': { 
    title: 'Traffic Routing (Live View)', 
    description: 'Real-time visualization of the Istio service mesh traffic. Monitor how requests flow from the Ingress Controller to your Pods.',
    icon: <Globe size={18} className="text-kube-blue" />
  }
};

function ResourceHeader({ title, description, icon }: { title: string, description: string, icon: any }) {
  return (
    <div className="mb-8 p-6 bg-white/5 border border-white/10 rounded-2xl relative overflow-hidden group">
      <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full translate-x-16 -translate-y-16 blur-2xl group-hover:bg-white/10 transition-all"></div>
      <div className="flex items-start space-x-4">
        <div className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center shrink-0">
          {icon}
        </div>
        <div>
          <h2 className="text-xl font-bold text-white mb-1">{title}</h2>
          <p className="text-sm text-white/40 leading-relaxed max-w-2xl">{description}</p>
        </div>
      </div>
    </div>
  );
}

function EmptyState({ resource }: { resource: string }) {
  return (
    <div className="col-span-full py-20 px-6 bg-white/5 border border-dashed border-white/10 rounded-3xl flex flex-col items-center justify-center text-center space-y-4">
      <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center">
        <Box className="text-white/10" size={32} />
      </div>
      <div>
        <h3 className="text-lg font-bold text-white/60">No {resource} found</h3>
        <p className="text-sm text-white/20 max-w-sm mx-auto">Either there are no resources in this namespace, or they haven't been created yet. Check your kubectl context or switch namespaces.</p>
      </div>
    </div>
  );
}

export default function Home() {
  const [pods, setPods] = useState<any[]>([])
  const [services, setServices] = useState<any[]>([])
  const [deployments, setDeployments] = useState<any[]>([])
  const [statefulSets, setStatefulSets] = useState<any[]>([])
  const [daemonSets, setDaemonSets] = useState<any[]>([])
  const [ingresses, setIngresses] = useState<any[]>([])
  const [pvcs, setPvcs] = useState<any[]>([])
  const [configMaps, setConfigMaps] = useState<any[]>([])
  const [secrets, setSecrets] = useState<any[]>([])
  const [networkPolicies, setNetworkPolicies] = useState<any[]>([])
  const [hpas, setHpas] = useState<any[]>([])
  const [serviceAccounts, setServiceAccounts] = useState<any[]>([])
  const [roles, setRoles] = useState<any[]>([])
  const [roleBindings, setRoleBindings] = useState<any[]>([])
  const [clusterRoles, setClusterRoles] = useState<any[]>([])
  const [clusterRoleBindings, setClusterRoleBindings] = useState<any[]>([])
  const [certificates, setCertificates] = useState<any[]>([])
  const [istioVirtualServices, setIstioVirtualServices] = useState<any[]>([])
  const [istioGateways, setIstioGateways] = useState<any[]>([])
  const [events, setEvents] = useState<any[]>([])
  
  const [modalOpen, setModalOpen] = useState(false)
  const [modalTitle, setModalTitle] = useState('')
  const [modalContent, setModalContent] = useState<any>('')
  const [modalLoading, setModalLoading] = useState(false)
  
  const [contexts, setContexts] = useState<any[]>([])
  const [namespaces, setNamespaces] = useState<string[]>([])
  const [selectedNamespace, setSelectedNamespace] = useState<string>('default')
  const [activeContext, setActiveContext] = useState<string>('')
  const [activeTab, setActiveTab] = useState<string>('workloads/pods')
  const [expandedCategories, setExpandedCategories] = useState<string[]>(['workloads', 'networking'])
  const [searchQuery, setSearchQuery] = useState('')
  const [clusterOverview, setClusterOverview] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [switchingNamespace, setSwitchingNamespace] = useState(false)
  const [isClient, setIsClient] = useState(false)
  const [kconfigModalOpen, setKconfigModalOpen] = useState(false)

  // Derived cluster info
  const currentContextObj = contexts.find(c => c.name === activeContext) || null;
  const activeCluster = currentContextObj?.cluster || 'Searching...';
  const activeServer = currentContextObj?.server || 'Loading...';
  
  // Helm Designer State
  const [helmConfig, setHelmConfig] = useState({
    name: 'my-app',
    image: 'nginx:latest',
    replicas: 1,
    port: 80,
    ingress: false,
    pvc: false,
    secret: false
  })

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

  const fetchData = async (ns: string = selectedNamespace) => {
    setLoading(true)
    try {
      const endpoints = [
        { key: 'pods', url: 'pods' },
        { key: 'services', url: 'services' },
        { key: 'deployments', url: 'deployments' },
        { key: 'statefulsets', url: 'statefulsets' },
        { key: 'daemonsets', url: 'daemonsets' },
        { key: 'ingresses', url: 'ingresses' },
        { key: 'pvcs', url: 'pvcs' },
        { key: 'configmaps', url: 'configmaps' },
        { key: 'secrets', url: 'secrets' },
        { key: 'networkpolicies', url: 'networkpolicies' }
      ];

      const results = await Promise.all(
        endpoints.map(e => fetch(`${apiUrl}/resources/${e.url}?namespace=${ns}`).then(r => r.json()))
      );

      setPods(results[0] || []);
      setServices(results[1] || []);
      setDeployments(results[2] || []);
      setStatefulSets(results[3] || []);
      setDaemonSets(results[4] || []);
      setIngresses(results[5] || []);
      setPvcs(results[6] || []);
      setConfigMaps(results[7] || []);
      setSecrets(results[8] || []);
      setNetworkPolicies(results[9] || []);

      // Batch 2: Scaling & RBAC
      const batch2Endpoints = [
        { key: 'hpas', url: 'hpas' },
        { key: 'serviceaccounts', url: 'serviceaccounts' },
        { key: 'roles', url: 'roles' },
        { key: 'rolebindings', url: 'rolebindings' },
        { key: 'clusterroles', url: 'clusterroles' },
        { key: 'clusterrolebindings', url: 'clusterrolebindings' }
      ];

      const batch2Results = await Promise.all(
        batch2Endpoints.map(e => fetch(`${apiUrl}/resources/${e.url}?namespace=${ns}`).then(r => r.json()))
      );

      setHpas(batch2Results[0] || []);
      setServiceAccounts(batch2Results[1] || []);
      setRoles(batch2Results[2] || []);
      setRoleBindings(batch2Results[3] || []);
      setClusterRoles(batch2Results[4] || []);
      setClusterRoleBindings(batch2Results[5] || []);

      const batch3Res = await fetch(`${apiUrl}/resources/certificates`)
      const certData = await batch3Res.json()
      setCertificates(certData || [])

      // Batch 4: Istio (Service Mesh)
      const istioEndpoints = [
        { key: 'virtualservices', url: 'istio/virtualservices' },
        { key: 'gateways', url: 'istio/gateways' }
      ];
      
      const istioResults = await Promise.all(
        istioEndpoints.map(e => fetch(`${apiUrl}/resources/${e.url}?namespace=${ns}`).then(r => r.json()))
      );
      
      setIstioVirtualServices(istioResults[0] || []);
      setIstioGateways(istioResults[1] || []);

      // Batch 5: Events
      const eventsRes = await fetch(`${apiUrl}/resources/events?namespace=${ns}`)
      const eventsData = await eventsRes.json()
      setEvents(eventsData || [])

      // Fetch Cluster Overview (Global)
      const overviewRes = await fetch(`${apiUrl}/cluster/overview`)
      const overviewData = await overviewRes.json()
      setClusterOverview(overviewData)
    } catch (err) {
      console.error("Failed to fetch cluster data", err)
    } finally {
      setLoading(false)
    }
  }

  const fetchContexts = async () => {
    try {
      const res = await fetch(`${apiUrl}/contexts`)
      const data = await res.json()
      setContexts(data.contexts || [])
      setActiveContext(data.current_context || '')
      
      // Also fetch namespaces for the current context
      fetchNamespaces()
    } catch (err) {
      console.error("Failed to fetch contexts", err)
    }
  }

  const fetchNamespaces = async () => {
    try {
      const res = await fetch(`${apiUrl}/resources/namespaces`)
      const data = await res.json()
      setNamespaces(data || ['default'])
    } catch (err) {
      console.error("Failed to fetch namespaces", err)
    }
  }

  const handleSwitchContext = async (contextName: string) => {
    if (contextName === activeContext) return
    
    try {
      const res = await fetch(`${apiUrl}/contexts/switch?name=${contextName}`, { method: 'POST' })
      if (res.ok) {
        setActiveContext(contextName)
        fetchNamespaces() // Refresh namespaces for new cluster
        fetchData() // Refresh data for new context
      }
    } catch (err) {
      console.error("Failed to switch context", err)
    }
  }

  const handleNamespaceChange = async (ns: string) => {
    setSwitchingNamespace(true)
    setSelectedNamespace(ns)
    await fetchData(ns)
    setSwitchingNamespace(false)
  }

  const handleFetchLogs = async (podName: string) => {
    setModalTitle(`Logs: ${podName}`)
    setModalOpen(true)
    setModalLoading(true)
    try {
      const res = await fetch(`${apiUrl}/resources/pods/${podName}/logs?namespace=${selectedNamespace}`)
      const data = await res.json()
      setModalContent(data.logs || "No logs found.")
    } catch (err) {
      setModalContent("Failed to fetch logs.")
    } finally {
      setModalLoading(false)
    }
  }

  const handleDescribePod = async (podName: string) => {
    setModalTitle(`Describe: ${podName}`)
    setModalOpen(true)
    setModalLoading(true)
    try {
      const res = await fetch(`${apiUrl}/resources/pods/${podName}/describe?namespace=${selectedNamespace}`)
      const data = await res.json()
      setModalContent(data)
    } catch (err) {
      setModalContent("Failed to fetch pod description.")
    } finally {
      setModalLoading(false)
    }
  }

  useEffect(() => {
    fetchContexts()
    fetchData()
    setIsClient(true)
  }, [])

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    if (activeTab === 'observability/traffic' && isClient) {
      setTimeout(() => {
        mermaid.contentLoaded();
        // Force a re-render if needed
        const mermaidDiv = document.querySelector('.mermaid');
        if (mermaidDiv instanceof HTMLElement) {
          mermaid.init(undefined, mermaidDiv);
        }
      }, 100);
    }
  }, [activeTab, isClient]);

  useEffect(() => {
    mermaid.contentLoaded()
  }, [pods, activeContext])

  const filteredPods = pods.filter(pod => 
    pod.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    pod.status.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (pod.ip && pod.ip.includes(searchQuery))
  ).sort((a, b) => {
    const aIsUnhealthy = a.status !== 'Running' || a.restarts > 0;
    const bIsUnhealthy = b.status !== 'Running' || b.restarts > 0;
    if (aIsUnhealthy && !bIsUnhealthy) return -1;
    if (!aIsUnhealthy && bIsUnhealthy) return 1;
    return a.name.localeCompare(b.name);
  })

  const filteredServices = services.filter(svc => 
    svc.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    svc.type.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (svc.cluster_ip && svc.cluster_ip.includes(searchQuery))
  )

  const filteredDeployments = deployments.filter(dep => 
    dep.name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="flex flex-col min-h-screen">
      {/* Navbar */}
      <header className="h-16 border-b border-white/10 bg-kube-dark/80 backdrop-blur-md flex items-center justify-between px-6 sticky top-0 z-50">
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 rounded-xl bg-kube-blue/10 border border-kube-blue/20 flex items-center justify-center">
            <Layout className="text-white" size={24} />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">KUUI <span className="text-kube-blue font-black italic">MASTER</span></h1>
            <div className="flex items-center space-x-1.5 -mt-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="text-[10px] font-bold text-white/20 uppercase tracking-widest leading-none">Cluster API Active</span>
            </div>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          {/* Context/Cluster Selector */}
          <div className="flex items-center space-x-2 px-3 py-1.5 bg-white/5 border border-white/10 rounded-lg group relative hover:border-kube-blue/30 transition-all">
            <span className="text-[10px] uppercase font-bold text-white/40 absolute -top-2 left-2 bg-kube-dark px-1">Cluster / Context</span>
            <Activity size={16} className="text-purple-400" />
            <select 
              value={activeContext} 
              onChange={(e) => handleSwitchContext(e.target.value)}
              className="bg-transparent text-sm font-medium border-none focus:ring-0 cursor-pointer outline-none min-w-[150px]"
            >
              {contexts.map(ctx => (
                <option key={ctx.name} value={ctx.name} className="bg-kube-dark text-white">
                  {ctx.cluster} ({ctx.name})
                </option>
              ))}
            </select>
            <button 
              onClick={() => setKconfigModalOpen(true)}
              className="ml-2 p-1 hover:bg-white/10 rounded transition-colors"
              title="View KubeConfig Details"
            >
              <Info size={14} className="text-white/40" />
            </button>
          </div>

          {/* Namespace Selector */}
          <div className="flex items-center space-x-2 px-3 py-1.5 bg-white/5 border border-white/10 rounded-lg group relative hover:border-kube-blue/30 transition-all">
            <span className="text-[10px] uppercase font-bold text-white/40 absolute -top-2 left-2 bg-kube-dark px-1">Namespace</span>
            <Box size={16} className="text-kube-blue" />
            <select 
              value={selectedNamespace} 
              onChange={(e) => handleNamespaceChange(e.target.value)}
              className="bg-transparent text-sm font-medium border-none focus:ring-0 cursor-pointer outline-none min-w-[100px]"
            >
              {namespaces.map(ns => <option key={ns} value={ns} className="bg-kube-dark text-white">{ns}</option>)}
            </select>
          </div>

          <div className="relative group">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-white/40 group-focus-within:text-kube-blue transition-colors" size={18} />
            <input 
              type="text" 
              placeholder="Search resources..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-full text-sm focus:outline-none focus:border-kube-blue/50 focus:ring-1 focus:ring-kube-blue/20 transition-all w-64"
            />
          </div>
          <button className="p-2 hover:bg-white/5 rounded-lg transition-colors border border-white/10">
            <Globe size={20} className="text-white/60" />
          </button>
        </div>
      </header>

      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-64 border-r border-white/10 p-4 space-y-6 hidden md:block overflow-y-auto">
          <nav className="space-y-4">
            <SidebarCategory 
              label="Workloads" 
              icon={<Server size={14} />} 
              isOpen={expandedCategories.includes('workloads')}
              onToggle={() => setExpandedCategories(prev => prev.includes('workloads') ? prev.filter(c => c !== 'workloads') : [...prev, 'workloads'])}
            >
              <SidebarItem label="Pods" active={activeTab === 'workloads/pods'} onClick={() => setActiveTab('workloads/pods')} />
              <SidebarItem label="Deployments" active={activeTab === 'workloads/deployments'} onClick={() => setActiveTab('workloads/deployments')} />
              <SidebarItem label="StatefulSets" active={activeTab === 'workloads/statefulsets'} onClick={() => setActiveTab('workloads/statefulsets')} />
              <SidebarItem label="DaemonSets" active={activeTab === 'workloads/daemonsets'} onClick={() => setActiveTab('workloads/daemonsets')} />
              <SidebarItem label="HPA (Scaling)" active={activeTab === 'workloads/hpas'} onClick={() => setActiveTab('workloads/hpas')} />
            </SidebarCategory>

            <SidebarCategory 
              label="Networking" 
              icon={<Network size={14} />} 
              isOpen={expandedCategories.includes('networking')}
              onToggle={() => setExpandedCategories(prev => prev.includes('networking') ? prev.filter(c => c !== 'networking') : [...prev, 'networking'])}
            >
              <SidebarItem label="Services" active={activeTab === 'networking/services'} onClick={() => setActiveTab('networking/services')} />
              <SidebarItem label="Ingress" active={activeTab === 'networking/ingress'} onClick={() => setActiveTab('networking/ingress')} />
              <SidebarItem label="Network Policies" active={activeTab === 'networking/networkpolicies'} onClick={() => setActiveTab('networking/networkpolicies')} />
            </SidebarCategory>

            <SidebarCategory 
              label="RBAC & Security" 
              icon={<ShieldCheck size={14} />} 
              isOpen={expandedCategories.includes('rbac')}
              onToggle={() => setExpandedCategories(prev => prev.includes('rbac') ? prev.filter(c => c !== 'rbac') : [...prev, 'rbac'])}
            >
              <SidebarItem label="ServiceAccounts" active={activeTab === 'rbac/serviceaccounts'} onClick={() => setActiveTab('rbac/serviceaccounts')} />
              <SidebarItem label="Roles" active={activeTab === 'rbac/roles'} onClick={() => setActiveTab('rbac/roles')} />
              <SidebarItem label="RoleBindings" active={activeTab === 'rbac/rolebindings'} onClick={() => setActiveTab('rbac/rolebindings')} />
              <SidebarItem label="ClusterRoles" active={activeTab === 'rbac/clusterroles'} onClick={() => setActiveTab('rbac/clusterroles')} />
              <SidebarItem label="ClusterRoleBindings" active={activeTab === 'rbac/clusterrolebindings'} onClick={() => setActiveTab('rbac/clusterrolebindings')} />
            </SidebarCategory>

            <SidebarCategory 
              label="Storage" 
              icon={<Database size={14} />} 
              isOpen={expandedCategories.includes('storage')}
              onToggle={() => setExpandedCategories(prev => prev.includes('storage') ? prev.filter(c => c !== 'storage') : [...prev, 'storage'])}
            >
              <SidebarItem label="Persistent Volume Claims" active={activeTab === 'storage/pvcs'} onClick={() => setActiveTab('storage/pvcs')} />
            </SidebarCategory>

            <SidebarCategory 
              label="Configuration" 
              icon={<FileText size={14} />} 
              isOpen={expandedCategories.includes('config')}
              onToggle={() => setExpandedCategories(prev => prev.includes('config') ? prev.filter(c => c !== 'config') : [...prev, 'config'])}
            >
              <SidebarItem label="ConfigMaps" active={activeTab === 'config/configmaps'} onClick={() => setActiveTab('config/configmaps')} />
              <SidebarItem label="Secrets" active={activeTab === 'config/secrets'} onClick={() => setActiveTab('config/secrets')} />
            </SidebarCategory>

            <SidebarCategory 
              label="Infrastructure & Automation" 
              icon={<Cloud size={14} />} 
              isOpen={expandedCategories.includes('infra')}
              onToggle={() => setExpandedCategories(prev => prev.includes('infra') ? prev.filter(c => c !== 'infra') : [...prev, 'infra'])}
            >
              <SidebarItem label="Certificates (SSL Hub)" active={activeTab === 'infra/certificates'} onClick={() => setActiveTab('infra/certificates')} />
              <SidebarItem label="Helm Designer" active={activeTab === 'infra/helm'} onClick={() => setActiveTab('infra/helm')} />
            </SidebarCategory>

            <SidebarCategory 
              label="Service Mesh (Istio)" 
              icon={<ShieldCheck size={14} className="text-kube-blue" />} 
              isOpen={expandedCategories.includes('mesh')}
              onToggle={() => setExpandedCategories(prev => prev.includes('mesh') ? prev.filter(c => c !== 'mesh') : [...prev, 'mesh'])}
            >
              <SidebarItem label="VirtualServices" active={activeTab === 'mesh/virtualservices'} onClick={() => setActiveTab('mesh/virtualservices')} />
              <SidebarItem label="Gateways" active={activeTab === 'mesh/gateways'} onClick={() => setActiveTab('mesh/gateways')} />
            </SidebarCategory>

            <SidebarCategory 
              label="Observability" 
              icon={<Zap size={14} className="text-amber-400" />} 
              isOpen={expandedCategories.includes('observability')}
              onToggle={() => setExpandedCategories(prev => prev.includes('observability') ? prev.filter(c => c !== 'observability') : [...prev, 'observability'])}
            >
              <SidebarItem label="Live Traffic" active={activeTab === 'observability/traffic'} onClick={() => setActiveTab('observability/traffic')} />
            </SidebarCategory>
          </nav>

        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8 space-y-8 overflow-y-auto">
          {/* Stats Bar */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard icon={<Cpu className="text-kube-blue" />} label="Nodes" value={clusterOverview?.total_nodes || '0'} subValue={`${clusterOverview?.healthy_nodes || 0} Healthy`} />
            <StatCard icon={<Server className="text-purple-400" />} label="API Version" value={clusterOverview?.api_version || 'N/A'} subValue={clusterOverview?.platform || 'K8s Cluster'} />
            <StatCard icon={<Box className="text-emerald-400" />} label="Avg Pod Health" value={clusterOverview?.pod_health_pct || '0%'} subValue={`Across ${clusterOverview?.total_pods || 0} total pods`} />
            <StatCard icon={<Globe className="text-amber-400" />} label="Active Cluster" value={activeCluster} subValue={activeServer} />
          </div>

          {switchingNamespace ? (
            <div className="flex-1 flex flex-col items-center justify-center min-h-[60vh] animate-in fade-in duration-700">
               <div className="relative group">
                 <div className="absolute inset-0 bg-kube-blue/20 blur-3xl rounded-full group-hover:bg-kube-blue/30 transition-all duration-700"></div>
                 <img 
                   src="/loading.png" 
                   alt="Loading..." 
                   className="w-48 h-48 relative z-10 animate-spin-slow drop-shadow-[0_0_20px_rgba(6,182,212,0.5)]"
                 />
               </div>
               <div className="mt-8 space-y-2 text-center">
                 <h2 className="text-2xl font-bold tracking-tight text-white/80 animate-pulse">Switching Namespace...</h2>
                 <p className="text-white/30 text-sm font-medium uppercase tracking-[0.2em]">Synchronizing {selectedNamespace} resources</p>
               </div>
            </div>
          ) : (
            <>
              {activeTab === 'workloads/pods' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <ResourceHeader {...resourceDescriptions[activeTab]} />
              <div className="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-3 gap-6">
                {(loading ? Array(6).fill(0) : pods).length > 0 ? (loading ? Array(6).fill(0) : pods).map((pod: any, i: number) => (
                  loading ? <LoadingSkeleton key={i} /> : 
                  <PodCard 
                    key={pod.name} 
                    {...pod} 
                    onLogs={() => handleFetchLogs(pod.name)}
                    onDescribe={() => handleDescribePod(pod.name)}
                  />
                )) : <EmptyState resource="Pods" />}
              </div>
            </div>
          )}

          {activeTab === 'workloads/deployments' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : deployments.length > 0 ? deployments.map((dep: any) => (
                  <DeploymentCard key={dep.name} {...dep} namespace={selectedNamespace} />
                )) : <EmptyState resource="Deployments" />}
              </div>
            </div>
          )}

          {activeTab === 'workloads/statefulsets' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : statefulSets.length > 0 ? statefulSets.map((ss: any) => (
                  <StatefulSetCard key={ss.name} {...ss} namespace={selectedNamespace} />
                )) : <EmptyState resource="StatefulSets" />}
              </div>
            </div>
          )}

          {activeTab === 'workloads/daemonsets' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : daemonSets.length > 0 ? daemonSets.map((ds: any) => (
                  <DaemonSetCard key={ds.name} {...ds} namespace={selectedNamespace} />
                )) : <EmptyState resource="DaemonSets" />}
              </div>
            </div>
          )}

          {activeTab === 'workloads/hpas' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : hpas.length > 0 ? hpas.map((h: any) => (
                  <HPACard key={h.name} {...h} namespace={selectedNamespace} />
                )) : <EmptyState resource="HPAs" />}
              </div>
            </div>
          )}

          {activeTab === 'networking/services' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : services.length > 0 ? services.map((svc: any) => (
                  <ServiceCard key={svc.name} {...svc} namespace={selectedNamespace} />
                )) : <EmptyState resource="Services" />}
              </div>
            </div>
          )}

          {activeTab === 'networking/ingress' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : ingresses.length > 0 ? ingresses.map((ing: any) => (
                  <IngressCard key={ing.name} {...ing} namespace={selectedNamespace} />
                )) : <EmptyState resource="Ingress" />}
              </div>
            </div>
          )}

          {activeTab === 'networking/networkpolicies' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : networkPolicies.length > 0 ? networkPolicies.map((p: any) => (
                  <NetworkPolicyCard key={p.name} {...p} namespace={selectedNamespace} />
                )) : <EmptyState resource="Network Policies" />}
              </div>
            </div>
          )}

          {activeTab === 'rbac/serviceaccounts' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : serviceAccounts.length > 0 ? serviceAccounts.map((sa: any) => (
                  <RBACCard key={sa.name} {...sa} type="SERVICEACCOUNT" namespace={selectedNamespace} />
                )) : <EmptyState resource="ServiceAccounts" />}
              </div>
            </div>
          )}

          {activeTab === 'rbac/roles' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : roles.length > 0 ? roles.map((r: any) => (
                  <RBACCard key={r.name} {...r} type="ROLE" namespace={selectedNamespace} />
                )) : <EmptyState resource="Roles" />}
              </div>
            </div>
          )}

          {activeTab === 'rbac/rolebindings' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : roleBindings.length > 0 ? roleBindings.map((rb: any) => (
                  <RBACCard key={rb.name} {...rb} type="ROLEBINDING" namespace={selectedNamespace} />
                )) : <EmptyState resource="RoleBindings" />}
              </div>
            </div>
          )}

          {activeTab === 'rbac/clusterroles' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : clusterRoles.length > 0 ? clusterRoles.map((cr: any) => (
                  <RBACCard key={cr.name} {...cr} type="CLUSTERROLE" namespace={selectedNamespace} />
                )) : <EmptyState resource="ClusterRoles" />}
              </div>
            </div>
          )}

          {(activeTab === 'rbac/clusterrolerolebindings' || activeTab === 'rbac/clusterrolebindings') && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions['rbac/clusterrolebindings']} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : clusterRoleBindings.length > 0 ? clusterRoleBindings.map((crb: any) => (
                  <RBACCard key={crb.name} {...crb} type="CLUSTERROLEBINDING" namespace={selectedNamespace} />
                )) : <EmptyState resource="ClusterRoleBindings" />}
              </div>
            </div>
          )}

          {activeTab === 'storage/pvcs' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : pvcs.length > 0 ? pvcs.map((pvc: any) => (
                  <PVCCard key={pvc.name} {...pvc} namespace={selectedNamespace} />
                )) : <EmptyState resource="Persistent Volume Claims" />}
              </div>
            </div>
          )}

          {activeTab === 'config/configmaps' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : configMaps.length > 0 ? configMaps.map((cm: any) => (
                  <DataResourceCard key={cm.name} {...cm} type="CONFIGMAP" namespace={selectedNamespace} />
                )) : <EmptyState resource="ConfigMaps" />}
              </div>
            </div>
          )}

          {activeTab === 'config/secrets' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : secrets.length > 0 ? secrets.map((sec: any) => (
                  <DataResourceCard key={sec.name} {...sec} type="SECRET" namespace={selectedNamespace} />
                )) : <EmptyState resource="Secrets" />}
              </div>
            </div>
          )}

          {activeTab === 'infra/certificates' && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <ResourceHeader {...resourceDescriptions[activeTab]} />
              <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold flex items-center space-x-3">
                  <ShieldCheck className="text-blue-400" />
                  <span>Certificate Hub (SSL/TLS)</span>
                </h2>
                <div className="flex items-center space-x-2 text-[10px] uppercase font-bold text-white/40 bg-white/5 px-3 py-1 rounded-full border border-white/10">
                  <RefreshCcw size={10} className="animate-spin-slow" />
                  <span>Auto-Refreshing CSRs</span>
                </div>
              </div>

              <SSLGuide />

              <div className="space-y-6">
                <h3 className="text-sm font-bold text-white/40 uppercase tracking-widest flex items-center space-x-2">
                  <Activity size={14} className="text-blue-400" />
                  <span>Certificate Signing Requests (CSR)</span>
                </h3>
                <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                  {loading ? <LoadingSkeleton /> : certificates.length > 0 ? certificates.map((cert: any) => (
                    <CertCard key={cert.name} {...cert} />
                  )) : (
                    <div className="col-span-full p-12 bg-white/5 border border-dashed border-white/10 rounded-3xl flex flex-col items-center justify-center text-center space-y-4">
                      <div className="w-12 h-12 bg-white/5 rounded-full flex items-center justify-center">
                        <FileJson className="text-white/20" size={24} />
                      </div>
                      <div>
                        <p className="text-white/60 font-bold">No active CSRs found</p>
                        <p className="text-xs text-white/20">Generate a workload CSR to see it appear here for approval.</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              <div className="space-y-6">
                <h3 className="text-sm font-bold text-white/40 uppercase tracking-widest flex items-center space-x-2">
                  <Lock size={14} className="text-emerald-400" />
                  <span>TLS Secrets (Ready to Use)</span>
                </h3>
                <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                  {loading ? <LoadingSkeleton /> : secrets.filter(s => s.type === 'kubernetes.io/tls').map((sec: any) => (
                    <DataResourceCard key={sec.name} {...sec} type="SECRET" namespace={selectedNamespace} />
                  ))}
                  {secrets.filter(s => s.type === 'kubernetes.io/tls').length === 0 && (
                     <div className="col-span-full p-8 bg-white/5 border border-dashed border-white/10 rounded-2xl text-center text-xs text-white/20">
                        No signed TLS secrets found in this namespace.
                     </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'infra/helm' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold flex items-center space-x-3">
                  <Cloud className="text-purple-400" />
                  <span>Helm Chart Designer</span>
                </h2>
                <div className="px-4 py-2 bg-purple-500/10 border border-purple-500/20 rounded-xl text-[10px] font-bold text-purple-400 uppercase tracking-widest">
                  Enterprise Scaffolder
                </div>
              </div>
              <p className="text-sm text-white/40 max-w-2xl">
                Design your infrastructure visually. Toggle modules like Ingress, Storage, and Secrets to generate a standardized production-ready Helm chart.
              </p>
              
              <HelmDesigner config={helmConfig} setConfig={setHelmConfig} />
            </div>
          )}

          {activeTab === 'mesh/virtualservices' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <ResourceHeader {...resourceDescriptions[activeTab]} />
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold flex items-center space-x-3">
                  <ShieldCheck className="text-kube-blue" />
                  <span>Istio VirtualServices</span>
                </h2>
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : istioVirtualServices.length > 0 ? istioVirtualServices.map((vs: any) => (
                  <IstioCard key={vs.name} {...vs} type="VIRTUALSERVICE" namespace={selectedNamespace} />
                )) : (
                  <div className="col-span-full p-12 bg-white/5 border border-dashed border-white/10 rounded-3xl text-center text-white/20">
                    No VirtualServices found in this namespace.
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'mesh/gateways' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <ResourceHeader {...resourceDescriptions[activeTab]} />
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold flex items-center space-x-3">
                  <ShieldCheck className="text-kube-blue" />
                  <span>Istio Gateways</span>
                </h2>
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-6">
                {loading ? <LoadingSkeleton /> : istioGateways.length > 0 ? istioGateways.map((gw: any) => (
                  <IstioCard key={gw.name} {...gw} type="GATEWAY" namespace={selectedNamespace} />
                )) : (
                  <div className="col-span-full p-12 bg-white/5 border border-dashed border-white/10 rounded-3xl text-center text-white/20">
                    No Istio Gateways found in this namespace.
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'observability/traffic' && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
               <ResourceHeader {...resourceDescriptions[activeTab]} />
               <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold flex items-center space-x-3">
                  <Globe className="text-kube-blue" />
                  <span>Traffic Routing (Live View)</span>
                </h2>
                <div className="px-4 py-2 bg-kube-blue/10 border border-kube-blue/20 rounded-xl text-[10px] font-bold text-kube-blue uppercase tracking-widest flex items-center space-x-2">
                  <Activity size={12} className="animate-pulse" />
                  <span>Real-Time Mesh Monitoring</span>
                </div>
              </div>

              <div className="grid grid-cols-1 2xl:grid-cols-3 gap-8">
                <div className="2xl:col-span-2 p-1.5 bg-white/5 border border-white/10 rounded-3xl relative overflow-hidden group">
                  <div className="absolute top-0 right-0 w-64 h-64 bg-kube-blue/10 rounded-full translate-x-32 -translate-y-32 blur-3xl group-hover:bg-kube-blue/20 transition-all duration-700"></div>
                  <div className="bg-black/40 backdrop-blur-sm rounded-[22px] border border-white/10 p-12 overflow-x-auto min-h-[600px] flex items-center justify-center">
                    {isClient && (
                      <div className="mermaid min-w-[1000px] flex justify-center scale-110">
                        {`
                        graph LR
                          Internet([Internet]) --> LB(Load Balancer)
                          LB --> ING{Ingress Controller}
                          ING --> |/api| SVC_API[API Service]
                          ING --> |/ui| SVC_UI[UI Service]
                          SVC_API --> Pod_1[Pod A]
                          SVC_API --> Pod_2[Pod B]

                          style Internet fill:#432A61,stroke:#6366f1,color:#fff
                          style LB fill:#1E293B,stroke:#6366f1,color:#fff
                          style ING fill:#1E293B,stroke:#6366f1,color:#fff
                          style SVC_API fill:#0F172A,stroke:#10b981,color:#fff
                          style Pod_1 fill:#0F172A,stroke:#6366f1,stroke-dasharray: 5 5,color:#fff
                          style Pod_2 fill:#0F172A,stroke:#6366f1,color:#fff
                        `}
                      </div>
                    )}
                  </div>
                </div>

                <div className="space-y-6">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-black uppercase tracking-widest text-white/40 flex items-center space-x-2">
                      <Activity size={14} className="text-amber-400" />
                      <span>Meaningful Events</span>
                    </h3>
                    <span className="text-[10px] text-white/10 font-bold uppercase tracking-tighter">Last 50</span>
                  </div>
                  <div className="max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
                    <EventsTimeline events={events} />
                  </div>
                </div>
              </div>
            </div>
          )}
            </>
          )}
        </main>
      </div>

      <TerminalModal 
        isOpen={modalOpen} 
        onClose={() => setModalOpen(false)} 
        title={modalTitle} 
        content={modalContent} 
        loading={modalLoading}
      />

      <KconfigModal 
        isOpen={kconfigModalOpen}
        onClose={() => setKconfigModalOpen(false)}
        contexts={contexts}
        activeContext={activeContext}
        onSwitch={handleSwitchContext}
      />
    </div>
  )
}

function KconfigModal({ isOpen, onClose, contexts, activeContext, onSwitch }: { isOpen: boolean, onClose: () => void, contexts: any[], activeContext: string, onSwitch: (name: string) => void }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-kube-dark/80 backdrop-blur-md" onClick={onClose}></div>
      <div className="relative w-full max-w-4xl bg-[#111] border border-white/10 rounded-3xl overflow-hidden shadow-2xl animate-in fade-in zoom-in duration-300">
        <div className="p-8 border-b border-white/10 flex items-center justify-between bg-white/[0.02]">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 rounded-2xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
              <Cloud size={24} />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white tracking-tight">KubeConfig <span className="text-purple-400">Audit</span></h2>
              <p className="text-sm text-white/40">Inspect all available Kubernetes cluster connections and environments.</p>
            </div>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-white/10 rounded-xl transition-colors text-white/40 hover:text-white">
            <X size={24} />
          </button>
        </div>

        <div className="p-8 overflow-y-auto max-h-[60vh] custom-scrollbar">
          <div className="space-y-4">
            {contexts.map((ctx) => (
              <div 
                key={ctx.name}
                onClick={() => { onSwitch(ctx.name); onClose(); }}
                className={`p-6 rounded-2xl border transition-all cursor-pointer group relative overflow-hidden ${
                  ctx.name === activeContext 
                    ? 'bg-kube-blue/5 border-kube-blue/30 shadow-[0_0_20px_rgba(6,182,212,0.1)]' 
                    : 'bg-white/5 border-white/5 hover:bg-white/10 hover:border-white/20'
                }`}
              >
                {ctx.name === activeContext && (
                  <div className="absolute top-0 right-0 px-4 py-1.5 bg-kube-blue text-[10px] font-black uppercase tracking-widest rounded-bl-xl text-kube-dark">
                    Active Environment
                  </div>
                )}
                
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <div className="flex items-center space-x-3">
                      <h3 className="text-lg font-bold text-white group-hover:text-kube-blue transition-colors">{ctx.cluster}</h3>
                      <span className="text-[10px] font-black uppercase tracking-widest text-white/20 px-2 py-0.5 border border-white/10 rounded-full">
                        {ctx.user}
                      </span>
                    </div>
                    <p className="text-xs text-white/40 font-mono tracking-tighter">{ctx.server}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-[10px] uppercase font-bold text-white/20 tracking-widest mb-1">Context Identifier</p>
                    <p className="text-xs font-bold text-white/60">{ctx.name}</p>
                  </div>
                </div>

                <div className="mt-4 flex items-center space-x-6">
                  <div className="flex items-center space-x-2">
                    <div className={`w-2 h-2 rounded-full ${ctx.name === activeContext ? 'bg-kube-blue' : 'bg-white/10'}`}></div>
                    <span className="text-[10px] font-bold uppercase tracking-widest text-white/40">Status: {ctx.name === activeContext ? 'Connected' : 'Available'}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Globe size={12} className="text-white/20" />
                    <span className="text-[10px] font-bold uppercase tracking-widest text-white/40">Region: Global</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="p-6 bg-white/[0.02] border-t border-white/10 flex items-center justify-between text-[10px] font-bold text-white/20 uppercase tracking-[0.2em]">
          <span>Enriched with Kubernetes Context Discovery v1.0</span>
          <span>Security Managed via local KubeConfig</span>
        </div>
      </div>
    </div>
  );
}

function SidebarItem({ label, active = false, onClick }: { label: string, active?: boolean, onClick?: () => void }) {
  return (
    <div 
      onClick={onClick}
      className={`px-3 py-1.5 rounded-lg cursor-pointer text-sm transition-all border ${active ? 'bg-kube-blue/10 text-kube-blue border-kube-blue/20 shadow-inner' : 'text-white/40 hover:text-white hover:bg-white/5 border-transparent'}`}
    >
      <span>{label}</span>
    </div>
  )
}

function LoadingSkeleton() {
  return (
    <>
      {Array(6).fill(0).map((_, i) => <div key={i} className="h-48 bg-white/5 animate-pulse rounded-2xl border border-white/10"></div>)}
    </>
  )
}

function ContextItem({ label, active = false, onClick }: { label: string, active?: boolean, onClick: () => void }) {
  return (
    <div 
      onClick={onClick}
      className={`flex items-center space-x-2 px-3 py-1.5 rounded-md cursor-pointer text-sm transition-all ${active ? 'text-kube-blue bg-kube-blue/10 border border-kube-blue/20' : 'text-white/40 hover:text-white/60 hover:bg-white/5'}`}
    >
      <div className={`w-2 h-2 rounded-full ${active ? 'bg-kube-blue animate-pulse' : 'bg-white/20'}`}></div>
      <span>{label}</span>
    </div>
  )
}

function StatCard({ icon, label, value, subValue }: { icon: React.ReactNode, label: string, value: string, subValue: string }) {
  const tooltipContent = {
    "Nodes": "Physical or virtual machines in your cluster that run containerized applications.",
    "API Version": "The specific version of the Kubernetes API server running on the control plane.",
    "Avg Pod Health": "Percentage of pods currently in the 'Running' or 'Succeeded' phase across all namespaces.",
    "Active Context": "The current kube-config context being used by the KUUI backend proxy."
  }[label] || "Cluster resource information."

  return (
    <div className="p-5 bg-white/5 border border-white/10 rounded-2xl space-y-2 hover:border-white/20 transition-all group relative">
      {/* Tooltip */}
      <div className="absolute top-full left-0 w-48 mt-2 p-2 bg-kube-blue text-[10px] rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-20 shadow-xl shadow-black/50 border border-white/10">
        <div className="flex items-start space-x-2">
          <Info size={12} className="mt-0.5 shrink-0" />
          <span>{tooltipContent}</span>
        </div>
        <div className="absolute -top-1 left-4 w-2 h-2 bg-kube-blue rotate-45"></div>
      </div>

      <div className="flex items-center justify-between">
        <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center group-hover:bg-white/10 transition-colors">
          {icon}
        </div>
        <div className="text-xs text-white/40 bg-white/5 px-2 py-1 rounded-full group-hover:text-white/60 transition-colors uppercase tracking-widest font-bold">Live</div>
      </div>
      <div>
        <p className="text-sm text-white/40 font-medium tracking-wide uppercase leading-relaxed">{label}</p>
        <p className="text-2xl font-bold tracking-tight text-white/90">{value}</p>
      </div>
      <p className="text-xs text-white/30 italic group-hover:text-white/50 transition-colors">{subValue}</p>
    </div>
  )
}

function PodCard({ 
  name, 
  status, 
  reason, 
  message, 
  restarts, 
  ip, 
  node, 
  creation_timestamp, 
  namespace, 
  context, 
  onLogs, 
  onDescribe, 
  istio_injected 
}: { 
  name: string, 
  status: string, 
  reason: string, 
  message: string, 
  restarts: number, 
  ip: string, 
  node: string, 
  creation_timestamp: string, 
  namespace: string, 
  context: string, 
  onLogs: () => void, 
  onDescribe: () => void, 
  istio_injected?: boolean 
}) {
  const isRunning = status === 'Running'
  const isHealthy = isRunning && restarts === 0
  const kubectlCmd = `kubectl get pod ${name} -n ${namespace}`
  
  return (
    <div 
      className={`group p-6 bg-white/5 border rounded-2xl transition-all cursor-pointer relative overflow-hidden flex flex-col justify-between h-full ${!isHealthy ? 'border-red-500/30 bg-red-500/5 shadow-lg shadow-red-500/10' : 'border-white/10 hover:bg-white/10 hover:border-white/20'}`}
    >
      <div className={`absolute top-0 left-0 w-1 h-full ${isHealthy ? 'bg-kube-blue shadow-lg shadow-kube-blue/20' : 'bg-red-500 animate-pulse-slow shadow-lg shadow-red-500/40'}`}></div>
      
      {/* Istio Badge */}
      {istio_injected && (
        <div className="absolute top-2 right-2 flex items-center space-x-1 px-2 py-0.5 bg-kube-blue/10 border border-kube-blue/20 rounded-md text-[8px] font-black text-kube-blue uppercase tracking-widest animate-in fade-in zoom-in duration-500">
          <ShieldCheck size={10} />
          <span>Istio Proxy</span>
        </div>
      )}

      {/* Diagnostic Tooltip for errors */}
      {(!isHealthy || message) && (
        <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity z-10 pointer-events-none">
          <div className="bg-black/90 backdrop-blur-md px-3 py-2 rounded-lg border border-red-500/30 text-[10px] max-w-[200px] shadow-2xl">
            <p className="font-bold text-red-400 mb-1 flex items-center space-x-1">
              <AlertTriangle size={10} />
              <span>{reason || status}</span>
            </p>
            <p className="text-white/60 leading-tight italic">"{message || `Pod is in ${status} state.`}"</p>
          </div>
        </div>
      )}

      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center space-x-3">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center transition-all shadow-inner border ${!isHealthy ? 'bg-red-500/10 border-red-500/20 group-hover:scale-110' : 'bg-kube-blue/10 border-kube-blue/20 group-hover:scale-110'}`}>
            <Box className={!isHealthy ? 'text-red-400' : 'text-kube-blue'} size={24} />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className={`font-bold text-base leading-tight transition-colors break-all ${!isHealthy ? 'text-red-400 group-hover:text-red-300' : 'group-hover:text-kube-blue'}`}>{name}</h3>
              <CopyButton text={kubectlCmd} label="kubectl" />
            </div>
            <div className="flex items-center space-x-2 text-[10px] font-mono font-bold tracking-widest text-white/40">
              <span>{ip || '0.0.0.0'}</span>
              <span>•</span>
              <span className="truncate max-w-[80px]">{node}</span>
            </div>
          </div>
        </div>
        <div className={`px-2 py-1 rounded-md text-[10px] font-black uppercase tracking-widest border transition-colors ${isRunning ? 'text-emerald-400/80 border-emerald-400/20 bg-emerald-400/5' : 'text-red-400/80 border-red-400/20 bg-red-400/5'}`}>
          {reason || status}
        </div>
      </div>
      
      {restarts > 0 && (
        <div className="mb-4">
          <div className="flex items-center justify-between text-[10px] mb-1">
            <span className="text-white/20 uppercase font-bold tracking-widest">Restart Count</span>
            <span className="text-red-400 font-bold">{restarts}</span>
          </div>
          <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
            <div className="h-full bg-red-400/50" style={{ width: `${Math.min(restarts * 10, 100)}%` }}></div>
          </div>
        </div>
      )}

      <div className="flex space-x-2 pt-2 opacity-100 group-hover:translate-y-0 translate-y-2 transition-all">
        <button onClick={(e) => { e.stopPropagation(); onLogs(); }} className="flex-1 px-3 py-1.5 bg-white/5 rounded-lg text-[10px] font-black uppercase tracking-tighter hover:bg-white/10 border border-white/5 transition-all hover:text-kube-blue">Logs</button>
        <button onClick={(e) => { e.stopPropagation(); onDescribe(); }} className="flex-1 px-3 py-1.5 bg-white/5 rounded-lg text-[10px] font-black uppercase tracking-tighter hover:bg-white/10 border border-white/5 transition-all hover:text-kube-blue">Describe</button>
      </div>
    </div>
  )
}

function DeploymentCard({ name, replicas, available_replicas, image, creation_timestamp, strategy, namespace }: { name: string, replicas: number, available_replicas: number, image: string, creation_timestamp: string, strategy: string, namespace: string }) {
  const isHealthy = replicas === available_replicas && replicas > 0
  const kubectlCmd = `kubectl get deployment ${name} -n ${namespace}`
  
  return (
    <div className="p-6 bg-white/5 border border-white/10 rounded-2xl space-y-4 hover:bg-white/10 transition-all cursor-pointer relative group overflow-hidden">
      <div className={`absolute top-0 left-0 w-1 h-full ${isHealthy ? 'bg-emerald-500 shadow-lg shadow-emerald-500/20' : 'bg-red-500 animate-pulse'}`}></div>
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-purple-500/10 border border-purple-500/20 group-hover:scale-110 transition-transform">
            <Workflow size={24} className="text-purple-400" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold text-base leading-tight break-all">{name}</h3>
              <CopyButton text={kubectlCmd} label="kubectl" />
            </div>
            <p className="text-[10px] text-white/40 font-mono font-bold tracking-widest uppercase truncate max-w-[150px]">{image}</p>
          </div>
        </div>
      </div>
      <p className="text-[10px] text-white/20 uppercase font-black">{strategy}</p>
      <div className="flex items-center justify-between text-xs pt-1">
        <span className="text-white/40">Ready: <span className={`font-bold ${isHealthy ? 'text-emerald-400' : 'text-red-400'}`}>{available_replicas} / {replicas}</span></span>
      </div>
    </div>
  )
}

function ServiceCard({ name, type, cluster_ip, external_ip, ports, namespace }: { name: string, type: string, cluster_ip: string, external_ip?: string, ports: any[], namespace: string }) {
  const kubectlCmd = `kubectl get svc ${name} -n ${namespace}`
  
  return (
    <div className="p-6 bg-white/5 border border-white/10 rounded-2xl space-y-4 hover:bg-white/10 transition-all cursor-pointer relative group overflow-hidden">
      <div className="absolute top-0 left-0 w-1 h-full bg-emerald-500 shadow-lg shadow-emerald-500/20"></div>
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-emerald-500/10 border border-emerald-500/20 group-hover:scale-110 transition-transform shadow-inner">
            <Globe className="text-emerald-400" size={24} />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold text-base leading-tight break-all">{name}</h3>
              <CopyButton text={kubectlCmd} label="kubectl" />
            </div>
            <p className="text-[10px] text-white/40 font-mono font-bold tracking-widest uppercase">{type}</p>
          </div>
        </div>
      </div>
      <div className="space-y-2">
        <p className="text-[10px] text-white/40 font-mono uppercase">IP: <span className="text-white">{cluster_ip || external_ip || 'None'}</span></p>
        <div className="flex flex-wrap gap-1.5 pt-1">
          {ports.map((p, i) => (
            <div key={i} className="px-2 py-0.5 bg-white/5 rounded border border-white/10 text-[9px] font-mono text-emerald-400/80">
              {p.port}:{p.target_port} <span className="text-white/20 text-[8px] uppercase">{p.protocol}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function StatefulSetCard({ name, replicas, ready_replicas, image, namespace }: { name: string, replicas: number, ready_replicas: number, image: string, namespace: string }) {
  const isHealthy = replicas === ready_replicas && replicas > 0
  const kubectlCmd = `kubectl get statefulset ${name} -n ${namespace}`
  
  return (
    <div className="p-6 bg-white/5 border border-white/10 rounded-2xl space-y-4 hover:bg-white/10 transition-all cursor-pointer relative group overflow-hidden">
      <div className={`absolute top-0 left-0 w-1 h-full ${isHealthy ? 'bg-emerald-500 shadow-lg shadow-emerald-500/20' : 'bg-amber-500 animate-pulse'}`}></div>
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-emerald-500/10 border border-emerald-500/20 group-hover:scale-110 transition-transform">
            <Server className="text-emerald-400" size={24} />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold text-base leading-tight break-all">{name}</h3>
              <CopyButton text={kubectlCmd} label="kubectl" />
            </div>
            <p className="text-[10px] text-white/40 font-mono font-bold tracking-widest uppercase truncate max-w-[150px]">{image}</p>
          </div>
        </div>
      </div>
      <div className="flex items-center justify-between text-xs pt-2">
        <span className="text-white/40">Ready: <span className={`font-bold ${isHealthy ? 'text-emerald-400' : 'text-amber-400'}`}>{ready_replicas} / {replicas}</span></span>
      </div>
    </div>
  )
}

function DaemonSetCard({ name, desired, current, ready, image, namespace }: { name: string, desired: number, current: number, ready: number, image: string, namespace: string }) {
  const isHealthy = desired === ready && desired > 0
  const kubectlCmd = `kubectl get ds ${name} -n ${namespace}`
  
  return (
    <div className="p-6 bg-white/5 border border-white/10 rounded-2xl space-y-4 hover:bg-white/10 transition-all cursor-pointer relative group overflow-hidden">
      <div className={`absolute top-0 left-0 w-1 h-full ${isHealthy ? 'bg-emerald-500 shadow-lg shadow-emerald-500/20' : 'bg-red-500 animate-pulse'}`}></div>
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-amber-500/10 border border-amber-500/20 group-hover:scale-110 transition-transform">
            <Activity className="text-amber-400" size={24} />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold text-base leading-tight break-all">{name}</h3>
              <CopyButton text={kubectlCmd} label="kubectl" />
            </div>
            <p className="text-[10px] text-white/40 font-mono font-bold tracking-widest uppercase truncate max-w-[150px]">{image}</p>
          </div>
        </div>
      </div>
      <div className="flex items-center justify-between text-xs pt-2">
        <span className="text-white/40">Healthy: <span className={`font-bold ${isHealthy ? 'text-emerald-400' : 'text-red-400'}`}>{ready} / {desired}</span></span>
      </div>
    </div>
  )
}

function HPACard({ name, min_replicas, max_replicas, current_replicas, desired_replicas, current_cpu_utilization, target_cpu_utilization, namespace }: { name: string, min_replicas: number, max_replicas: number, current_replicas: number, desired_replicas: number, current_cpu_utilization?: number, target_cpu_utilization?: number, namespace: string }) {
  const isHealthy = current_replicas === desired_replicas
  const cpuPct = current_cpu_utilization || 0
  const targetPct = target_cpu_utilization || 0
  const isTargetMet = cpuPct <= targetPct
  const kubectlCmd = `kubectl get hpa ${name} -n ${namespace}`

  return (
    <div className="p-6 bg-white/5 border border-white/10 rounded-2xl space-y-4 hover:bg-white/10 transition-all cursor-pointer relative group overflow-hidden">
      <div className={`absolute top-0 left-0 w-1 h-full ${isTargetMet ? 'bg-kube-blue shadow-lg' : 'bg-amber-500 animate-pulse'}`}></div>
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-kube-blue/10 border border-kube-blue/20 group-hover:scale-110 transition-transform">
            <Activity className="text-kube-blue" size={24} />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold text-base leading-tight break-all">{name}</h3>
              <CopyButton text={kubectlCmd} label="kubectl" />
            </div>
            <p className="text-[10px] text-white/40 font-mono font-bold tracking-widest uppercase">Target: {targetPct}% CPU</p>
          </div>
        </div>
      </div>
      
      <div className="space-y-3 pt-1">
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/40 uppercase font-black">Replicas</span>
          <span className="font-bold text-white/80">{current_replicas} / {desired_replicas} <span className="text-[10px] text-white/20">(max {max_replicas})</span></span>
        </div>
        
        <div className="space-y-1">
          <div className="flex items-center justify-between text-[10px]">
            <span className="text-white/20 uppercase font-bold">CPU Utilization</span>
            <span className={`font-bold ${cpuPct > targetPct ? 'text-amber-500' : 'text-kube-blue'}`}>{cpuPct}%</span>
          </div>
          <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden border border-white/5">
            <div 
              className={`h-full transition-all duration-1000 ${cpuPct > targetPct ? 'bg-amber-500/50' : 'bg-kube-blue/50'}`} 
              style={{ width: `${Math.min((cpuPct / (targetPct || 100)) * 100, 100)}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  )
}

function RBACCard({ name, type, rules_count, secrets_count, role_ref, subjects, namespace }: { name: string, type: 'SERVICEACCOUNT' | 'ROLE' | 'ROLEBINDING' | 'CLUSTERROLE' | 'CLUSTERROLEBINDING', rules_count?: number, secrets_count?: number, role_ref?: string, subjects?: any[], namespace: string }) {
  const isClusterWide = type.startsWith('CLUSTER')
  const kubectlCmd = `kubectl get ${type.toLowerCase().replace('_', '')} ${name} ${isClusterWide ? '' : `-n ${namespace}`}`
  
  const icon = {
    'SERVICEACCOUNT': <Lock className="text-emerald-400" size={24} />,
    'ROLE': <ShieldCheck className="text-emerald-400" size={24} />,
    'ROLEBINDING': <ShieldCheck className="text-blue-400" size={24} />,
    'CLUSTERROLE': <ShieldCheck className="text-red-400" size={24} />,
    'CLUSTERROLEBINDING': <ShieldCheck className="text-red-500" size={24} />
  }[type]

  const colorClass = {
    'SERVICEACCOUNT': 'border-emerald-500/50',
    'ROLE': 'border-emerald-500/50',
    'ROLEBINDING': 'border-blue-500/50',
    'CLUSTERROLE': 'border-red-500/50',
    'CLUSTERROLEBINDING': 'border-red-500/50'
  }[type]

  return (
    <div className={`p-6 bg-white/5 border rounded-2xl space-y-4 hover:bg-white/10 transition-all cursor-pointer relative group overflow-hidden ${name.startsWith('system:') ? 'opacity-50 grayscale hover:grayscale-0 transition-all' : 'border-white/10'}`}>
      <div className={`absolute top-0 left-0 w-1 h-full bg-current ${colorClass.replace('border-', 'bg-')}`}></div>
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-white/5 border border-white/10 group-hover:scale-110 transition-transform">
            {icon}
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold text-base leading-tight break-all">{name}</h3>
              <CopyButton text={kubectlCmd} label="kubectl" />
            </div>
            <p className="text-[10px] text-white/40 font-mono font-bold tracking-widest uppercase">{type.replace(/_/g, ' ')}</p>
          </div>
        </div>
      </div>

      <div className="pt-2 border-t border-white/5 space-y-2">
        {type === 'SERVICEACCOUNT' && (
          <p className="text-[10px] text-white/40 uppercase font-bold">Secrets: <span className="text-white">{secrets_count || 0}</span></p>
        )}
        {(type === 'ROLE' || type === 'CLUSTERROLE') && (
          <p className="text-[10px] text-white/40 uppercase font-bold">Rules: <span className="text-white">{rules_count || 0}</span></p>
        )}
        {(type === 'ROLEBINDING' || type === 'CLUSTERROLEBINDING') && (
          <>
            <p className="text-[10px] text-white/40 uppercase font-bold">Ref: <span className="text-blue-400">{role_ref}</span></p>
            <div className="flex flex-wrap gap-1 pt-1">
              {subjects?.map((s, i) => (
                <div key={i} className="px-2 py-0.5 bg-white/5 rounded border border-white/10 text-[9px] font-mono text-white/60">
                  <span className="text-white/20 mr-1">{s.kind}:</span>{s.name}
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  )
}

function IngressCard({ name, hosts, address, annotations, namespace }: { name: string, hosts: string[], address?: string, annotations: any, namespace: string }) {
  const kubectlCmd = `kubectl get ingress ${name} -n ${namespace}`
  
  return (
    <div className="p-6 bg-white/5 border border-white/10 rounded-2xl space-y-4 hover:bg-white/10 transition-all cursor-pointer relative group overflow-hidden">
      <div className="absolute top-0 left-0 w-1 h-full bg-kube-blue shadow-lg shadow-kube-blue/20"></div>
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-kube-blue/10 border border-kube-blue/20 group-hover:scale-110 transition-transform">
            <Network className="text-kube-blue" size={24} />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold text-base leading-tight break-all">{name}</h3>
              <CopyButton text={kubectlCmd} label="kubectl" />
            </div>
            <p className="text-[10px] text-white/40 font-mono font-bold tracking-widest uppercase">{address || 'No IP Assigned'}</p>
          </div>
        </div>
      </div>
      <div className="space-y-3">
        <div className="flex flex-wrap gap-2">
          {hosts.map((h, i) => (
            <div key={i} className="px-2 py-1 bg-white/5 rounded text-[10px] font-mono text-kube-blue border border-white/5">{h}</div>
          ))}
        </div>
        
        {/* Annotations Preview */}
        {Object.keys(annotations).length > 0 && (
          <div className="pt-2 border-t border-white/5">
            <p className="text-[8px] uppercase font-bold text-white/20 mb-1">Top Annotations</p>
            <div className="flex flex-wrap gap-1">
              {Object.entries(annotations).slice(0, 3).map(([k, v], i) => (
                <div key={i} className="text-[9px] text-white/40 truncate w-full flex items-center space-x-1">
                  <span className="text-kube-blue shrink-0">●</span>
                  <span className="truncate">{k.split('/').pop()}: {String(v)}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

function NetworkPolicyCard({ name, pod_selector, policy_types, namespace }: { name: string, pod_selector: any, policy_types: string[], namespace: string }) {
  const kubectlCmd = `kubectl get netpol ${name} -n ${namespace}`
  
  return (
    <div className="p-6 bg-white/5 border border-white/10 rounded-2xl space-y-4 hover:bg-white/10 transition-all cursor-pointer relative group overflow-hidden">
      <div className="absolute top-0 left-0 w-1 h-full bg-amber-500 shadow-lg shadow-amber-500/20"></div>
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-amber-500/10 border border-amber-500/20 group-hover:scale-110 transition-transform">
            <ShieldCheck className="text-amber-400" size={24} />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold text-base leading-tight break-all">{name}</h3>
              <CopyButton text={kubectlCmd} label="kubectl" />
            </div>
            <p className="text-[10px] text-white/40 font-mono font-bold tracking-widest uppercase">{policy_types.join(' & ')}</p>
          </div>
        </div>
      </div>
      
      <div className="pt-2 border-t border-white/5">
        <p className="text-[8px] uppercase font-bold text-white/20 mb-1">Target Pods</p>
        <div className="flex flex-wrap gap-1">
          {Object.entries(pod_selector).length > 0 ? Object.entries(pod_selector).map(([k, v], i) => (
            <div key={i} className="px-2 py-0.5 bg-white/5 rounded border border-white/10 text-[9px] font-mono text-amber-400/80">
              {k}={String(v)}
            </div>
          )) : <span className="text-[10px] italic text-white/20">Matches all pods (allow)</span>}
        </div>
      </div>
    </div>
  )
}

function PVCCard({ name, status, capacity, storage_class, namespace }: { name: string, status: string, capacity: string, storage_class: string, namespace: string }) {
  const isBound = status === 'Bound'
  const kubectlCmd = `kubectl get pvc ${name} -n ${namespace}`
  
  return (
    <div className="p-6 bg-white/5 border border-white/10 rounded-2xl space-y-4 hover:bg-white/10 transition-all cursor-pointer relative group overflow-hidden">
      <div className={`absolute top-0 left-0 w-1 h-full ${isBound ? 'bg-emerald-500 shadow-lg shadow-emerald-500/20' : 'bg-amber-500 animate-pulse'}`}></div>
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-amber-500/10 border border-amber-500/20 group-hover:scale-110 transition-transform">
            <Database className="text-amber-400" size={24} />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold text-base leading-tight break-all">{name}</h3>
              <CopyButton text={kubectlCmd} label="kubectl" />
            </div>
            <p className="text-[10px] text-white/40 font-mono font-bold tracking-widest uppercase">{storage_class}</p>
          </div>
        </div>
        <div className={`px-2 py-1 rounded-md text-[10px] font-black uppercase tracking-widest border ${isBound ? 'text-emerald-400/80 border-emerald-400/20 bg-emerald-400/5' : 'text-amber-400/80 border-amber-400/20 bg-amber-400/5'}`}>
          {status}
        </div>
      </div>
      <div className="text-xs text-white/60">Capacity: <span className="text-white font-bold">{capacity}</span></div>
    </div>
  )
}

function DataResourceCard({ name, data_keys, type, namespace }: { name: string, data_keys: string[], type: 'CONFIGMAP' | 'SECRET', namespace: string }) {
  const kubectlCmd = `kubectl get ${type.toLowerCase()} ${name} -n ${namespace}`
  const isSecret = type === 'SECRET'
  
  return (
    <div className="p-6 bg-white/5 border border-white/10 rounded-2xl space-y-4 hover:bg-white/10 transition-all cursor-pointer relative group overflow-hidden">
      <div className={`absolute top-0 left-0 w-1 h-full ${isSecret ? 'bg-red-400 shadow-lg shadow-red-400/20' : 'bg-blue-400 shadow-lg shadow-blue-400/20'}`}></div>
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center border group-hover:scale-110 transition-transform ${isSecret ? 'bg-red-400/10 border-red-400/20' : 'bg-blue-400/10 border-blue-400/20'}`}>
            {isSecret ? <Lock className="text-red-400" size={24} /> : <FileText className="text-blue-400" size={24} />}
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold text-base leading-tight break-all">{name}</h3>
              <CopyButton text={kubectlCmd} label="kubectl" />
            </div>
            <p className="text-[10px] text-white/40 font-mono font-bold tracking-widest uppercase">{type}</p>
          </div>
        </div>
      </div>
      <div className="flex flex-wrap gap-1.5 pt-2">
        {data_keys.map((k, i) => (
          <div key={i} className="px-2 py-0.5 bg-white/5 rounded border border-white/5 text-[9px] font-mono text-white/60">{k}</div>
        ))}
        {data_keys.length === 0 && <span className="text-[10px] italic text-white/20">No data entries.</span>}
      </div>
    </div>
  )
}

function IstioCard({ name, type, hosts, gateways, selector, servers, namespace }: { name: string, type: 'VIRTUALSERVICE' | 'GATEWAY', hosts?: string[], gateways?: string[], selector?: any, servers?: any[], namespace: string }) {
  const kubectlCmd = `kubectl get ${type.toLowerCase()} ${name} -n ${namespace}`
  const isVS = type === 'VIRTUALSERVICE'

  return (
    <div className="p-6 bg-white/5 border border-white/10 rounded-2xl space-y-4 hover:bg-white/10 transition-all cursor-pointer relative group overflow-hidden">
      <div className={`absolute top-0 left-0 w-1 h-full bg-kube-blue shadow-lg shadow-kube-blue/20`}></div>
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-kube-blue/10 border border-kube-blue/20 group-hover:scale-110 transition-transform">
            <ShieldCheck size={24} className="text-kube-blue" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold text-base leading-tight break-all">{name}</h3>
              <CopyButton text={kubectlCmd} label="kubectl" />
            </div>
            <p className="text-[10px] text-white/40 font-mono font-bold tracking-widest uppercase">{type}</p>
          </div>
        </div>
      </div>

      <div className="space-y-3 pt-2">
        {isVS ? (
          <>
            <div className="space-y-1">
              <p className="text-[8px] uppercase font-bold text-white/20">Hosts</p>
              <div className="flex flex-wrap gap-1">
                {hosts?.map((h, i) => (
                  <div key={i} className="px-2 py-0.5 bg-white/5 rounded border border-white/10 text-[9px] font-mono text-kube-blue">
                    {h}
                  </div>
                ))}
              </div>
            </div>
            <div className="space-y-1">
              <p className="text-[8px] uppercase font-bold text-white/20">Gateways</p>
              <div className="flex flex-wrap gap-1">
                {gateways?.map((g, i) => (
                  <div key={i} className="px-2 py-0.5 bg-white/5 rounded border border-white/10 text-[9px] font-mono text-white/40">
                    {g}
                  </div>
                ))}
              </div>
            </div>
          </>
        ) : (
          <>
             <div className="space-y-1">
              <p className="text-[8px] uppercase font-bold text-white/20">Selector</p>
              <div className="flex flex-wrap gap-1">
                {Object.entries(selector || {}).map(([k, v], i) => (
                  <div key={i} className="px-2 py-0.5 bg-white/5 rounded border border-white/10 text-[9px] font-mono text-emerald-400/80">
                    {k}={String(v)}
                  </div>
                ))}
              </div>
            </div>
            <div className="space-y-1">
              <p className="text-[8px] uppercase font-bold text-white/20">Servers</p>
              <div className="space-y-1">
                 {servers?.map((s, i) => (
                   <div key={i} className="p-2 bg-white/5 rounded border border-white/10 text-[9px] font-mono">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-white/60">{s.port?.name}</span>
                        <span className="text-kube-blue font-bold">{s.port?.number}/{s.port?.protocol}</span>
                      </div>
                      <div className="text-white/20 truncate">{s.hosts?.join(', ')}</div>
                   </div>
                 ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
function CertCard({ name, status, usages, signer_name, creation_timestamp }: { name: string, status: string, usages: string[], signer_name: string, creation_timestamp: string }) {
  const isApproved = status === 'Approved'
  const isPending = status === 'Pending'
  const kubectlCmd = `kubectl get csr ${name}`

  return (
    <div className="p-6 bg-white/5 border border-white/10 rounded-2xl space-y-4 hover:bg-white/10 transition-all cursor-pointer relative group overflow-hidden">
      <div className={`absolute top-0 left-0 w-1 h-full ${isApproved ? 'bg-emerald-500 shadow-lg' : isPending ? 'bg-amber-500 animate-pulse' : 'bg-red-500'}`}></div>
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-blue-500/10 border border-blue-500/20 group-hover:scale-110 transition-transform">
            <Lock className="text-blue-400" size={24} />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold text-base leading-tight break-all">{name}</h3>
              <CopyButton text={kubectlCmd} label="kubectl" />
            </div>
            <p className="text-[10px] text-white/40 font-mono font-bold tracking-widest uppercase">{signer_name.split('/').pop()}</p>
          </div>
        </div>
        <div className={`px-2 py-1 rounded-md text-[10px] font-black uppercase tracking-widest border ${isApproved ? 'text-emerald-400/80 border-emerald-400/20 bg-emerald-400/5' : 'text-amber-400/80 border-amber-400/20 bg-amber-400/5'}`}>
          {status}
        </div>
      </div>
      <div className="flex flex-wrap gap-1.5 pt-2">
        {usages.map((u, i) => (
          <div key={i} className="px-2 py-0.5 bg-white/5 rounded border border-white/5 text-[9px] font-mono text-white/60">{u}</div>
        ))}
      </div>
    </div>
  )
}

function SSLGuide() {
  const [show, setShow] = useState(false)
  
  return (
    <div className="space-y-4">
      <div 
        onClick={() => setShow(!show)}
        className="p-4 bg-kube-blue/10 border border-kube-blue/30 rounded-xl cursor-pointer hover:bg-kube-blue/20 transition-all flex items-center justify-between group"
      >
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 rounded-full bg-kube-blue flex items-center justify-center shadow-lg shadow-kube-blue/20">
            <Info className="text-white" size={20} />
          </div>
          <div>
            <h3 className="font-bold text-white">SSL/TLS Flow Guide</h3>
            <p className="text-xs text-white/60">Learn how to create keys, CSRs, and sign certificates for Ingress.</p>
          </div>
        </div>
        <div className="px-4 py-2 bg-kube-blue/20 rounded-lg text-xs font-bold uppercase tracking-widest group-hover:bg-kube-blue/40 transition-all">
          {show ? 'Close' : 'View Guide'}
        </div>
      </div>

      {show && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 p-8 bg-black/40 border border-white/10 rounded-3xl animate-in fade-in slide-in-from-top-4 duration-500">
          <div className="space-y-6">
            <h4 className="text-lg font-bold text-kube-blue flex items-center space-x-2">
              <TerminalIcon size={18} />
              <span>Step-by-Step Security Flow</span>
            </h4>
            
            <div className="space-y-8 relative">
              <div className="absolute left-4 top-2 bottom-2 w-[1px] bg-gradient-to-b from-kube-blue/50 via-purple-500/50 to-transparent"></div>
              
              <div className="relative pl-10">
                <div className="absolute left-0 top-0 w-8 h-8 rounded-full bg-kube-dark border-2 border-kube-blue flex items-center justify-center text-[10px] font-bold">1</div>
                <h5 className="font-bold text-white/90">Generate Private Key</h5>
                <p className="text-xs text-white/50 mb-2">Create a 2048-bit RSA key for your workload.</p>
                <div className="bg-black/60 rounded-lg p-3 border border-white/5 font-mono text-[10px] text-emerald-400 group">
                  openssl genrsa -out server.key 2048
                  <div className="mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <CopyButton text="openssl genrsa -out server.key 2048" label="Copy Cmd" />
                  </div>
                </div>
              </div>

              <div className="relative pl-10">
                <div className="absolute left-0 top-0 w-8 h-8 rounded-full bg-kube-dark border-2 border-purple-500 flex items-center justify-center text-[10px] font-bold">2</div>
                <h5 className="font-bold text-white/90">Create CSR</h5>
                <p className="text-xs text-white/50 mb-2">Generate a Certificate Signing Request to be signed by the K8s CA.</p>
                <div className="bg-black/60 rounded-lg p-3 border border-white/5 font-mono text-[10px] text-emerald-400 group">
                  openssl req -new -key server.key -out server.csr -subj "/CN=myapp.default"
                  <div className="mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <CopyButton text='openssl req -new -key server.key -out server.csr -subj "/CN=myapp.default"' label="Copy Cmd" />
                  </div>
                </div>
              </div>

              <div className="relative pl-10">
                <div className="absolute left-0 top-0 w-8 h-8 rounded-full bg-kube-dark border-2 border-emerald-500 flex items-center justify-center text-[10px] font-bold">3</div>
                <h5 className="font-bold text-white/90">Signing in K8s</h5>
                <p className="text-xs text-white/50 mb-2">Apply the CSR to K8s and approve it.</p>
                <div className="bg-black/60 rounded-lg p-3 border border-white/5 font-mono text-[10px] text-emerald-400 group">
                  kubectl certificate approve my-csr-name
                  <div className="mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <CopyButton text="kubectl certificate approve my-csr-name" label="Copy Cmd" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h4 className="text-lg font-bold text-purple-400 flex items-center space-x-2">
              <Activity size={18} />
              <span>Flow Architecture</span>
            </h4>
            <div className="bg-black/60 rounded-2xl border border-white/5 p-6 flex items-center justify-center min-h-[300px]">
              <div className="mermaid">
                {`
                graph TD
                  A[Private Key] --> B[CSR]
                  B --> C{K8s CSR API}
                  C --> D[Approved Cert]
                  D --> E[TLS Secret]
                  E --> F[Ingress Controller]
                  F --> G((Browser))
                  
                  style A fill:#1E293B,stroke:#6366f1,color:#fff
                  style C fill:#432A61,stroke:#6366f1,color:#fff
                  style E fill:#0F172A,stroke:#10b981,color:#fff
                  style F fill:#0F172A,stroke:#10b981,color:#fff
                `}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function HelmDesigner({ config, setConfig }: { config: any, setConfig: any }) {
  const [activeView, setActiveView] = useState<'config' | 'preview'>('config')

  const generateYaml = () => {
    return `
# values.yaml for ${config.name}
nameOverride: ""
fullnameOverride: ""

replicaCount: ${config.replicas}

image:
  repository: ${config.image.split(':')[0]}
  pullPolicy: IfNotPresent
  tag: "${config.image.split(':')[1] || 'latest'}"

service:
  type: ClusterIP
  port: ${config.port}

ingress:
  enabled: ${config.ingress}
  className: "nginx"
  annotations:
    ${config.ingress ? 'kubernetes.io/ingress.class: nginx\n    cert-manager.io/cluster-issuer: letsencrypt-prod' : ''}
  hosts:
    - host: ${config.name}.local
      paths:
        - path: /
          pathType: ImplementationSpecific

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi
    `.trim()
  }

  const generateDeployment = () => {
    return `
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "${config.name}.fullname" . }}
  labels:
    {{- include "${config.name}.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "${config.name}.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "${config.name}.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
    `.trim()
  }

  return (
    <div className="bg-white/5 border border-white/10 rounded-3xl overflow-hidden shadow-2xl">
      <div className="flex border-b border-white/10 bg-white/5">
        <button 
          onClick={() => setActiveView('config')}
          className={`px-8 py-4 text-xs font-bold uppercase tracking-widest transition-all ${activeView === 'config' ? 'bg-kube-blue text-white shadow-lg' : 'text-white/40 hover:text-white hover:bg-white/5'}`}
        >
          1. Design Architecture
        </button>
        <button 
          onClick={() => setActiveView('preview')}
          className={`px-8 py-4 text-xs font-bold uppercase tracking-widest transition-all ${activeView === 'preview' ? 'bg-purple-500 text-white shadow-lg' : 'text-white/40 hover:text-white hover:bg-white/5'}`}
        >
          2. Code Preview
        </button>
      </div>

      <div className="p-8">
        {activeView === 'config' ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <div className="space-y-8">
              <div className="space-y-4">
                <h4 className="text-sm font-bold text-white/40 uppercase tracking-widest flex items-center space-x-2">
                  <Pencil size={14} />
                  <span>Basic Configuration</span>
                </h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-[10px] text-white/20 uppercase font-black">Release Name</label>
                    <input 
                      type="text" 
                      value={config.name} 
                      onChange={(e) => setConfig({...config, name: e.target.value})}
                      className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-kube-blue transition-all"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] text-white/20 uppercase font-black">Image</label>
                    <input 
                      type="text" 
                      value={config.image} 
                      onChange={(e) => setConfig({...config, image: e.target.value})}
                      className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-kube-blue transition-all"
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-[10px] text-white/20 uppercase font-black">Replicas ({config.replicas})</label>
                    <input 
                      type="range" 
                      min="1" 
                      max="10" 
                      value={config.replicas} 
                      onChange={(e) => setConfig({...config, replicas: parseInt(e.target.value)})}
                      className="w-full accent-kube-blue h-2 bg-white/5 rounded-full appearance-none cursor-pointer"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] text-white/20 uppercase font-black">Port</label>
                    <input 
                      type="number" 
                      value={config.port} 
                      onChange={(e) => setConfig({...config, port: parseInt(e.target.value)})}
                      className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-kube-blue transition-all"
                    />
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="text-sm font-bold text-white/40 uppercase tracking-widest flex items-center space-x-2">
                  <Workflow size={14} />
                  <span>Modules & Features</span>
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div 
                    onClick={() => setConfig({...config, ingress: !config.ingress})}
                    className={`p-4 rounded-2xl border cursor-pointer transition-all flex items-center space-x-3 ${config.ingress ? 'bg-kube-blue/10 border-kube-blue' : 'bg-white/5 border-white/10 opacity-60 hover:opacity-100'}`}
                  >
                    <Network size={20} className={config.ingress ? 'text-kube-blue' : 'text-white/40'} />
                    <div>
                      <h5 className="text-xs font-bold">Ingress Controller</h5>
                      <p className="text-[10px] text-white/40">Exposed via Domain</p>
                    </div>
                  </div>
                  <div 
                    onClick={() => setConfig({...config, secret: !config.secret})}
                    className={`p-4 rounded-2xl border cursor-pointer transition-all flex items-center space-x-3 ${config.secret ? 'bg-red-500/10 border-red-500' : 'bg-white/5 border-white/10 opacity-60 hover:opacity-100'}`}
                  >
                    <Lock size={20} className={config.secret ? 'text-red-400' : 'text-white/40'} />
                    <div>
                      <h5 className="text-xs font-bold">Secret Management</h5>
                      <p className="text-[10px] text-white/40">Opaque Environment</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-kube-blue/5 to-purple-500/5 rounded-3xl -z-10 blur-xl"></div>
              <div className="p-8 bg-black/40 rounded-3xl border border-white/10 h-full flex flex-col justify-center items-center text-center space-y-6">
                <div className="w-20 h-20 bg-kube-blue/10 border border-kube-blue/20 rounded-2xl flex items-center justify-center">
                  <Server className="text-kube-blue animate-pulse" size={32} />
                </div>
                <div>
                  <h3 className="text-lg font-bold">Ready to Scaffold</h3>
                  <p className="text-sm text-white/40 max-w-xs mx-auto">Your configuration will be automatically bundled into a production-ready Helm chart structure.</p>
                </div>
                <div className="flex space-x-4">
                  <div className="px-4 py-2 bg-white/5 border border-white/10 rounded-full text-[10px] font-bold uppercase tracking-widest text-white/60">
                    Deployment
                  </div>
                  <div className="px-4 py-2 bg-white/5 border border-white/10 rounded-full text-[10px] font-bold uppercase tracking-widest text-white/60">
                    Service
                  </div>
                  {config.ingress && <div className="px-4 py-2 bg-kube-blue/20 border border-kube-blue/20 rounded-full text-[10px] font-bold uppercase tracking-widest text-kube-blue">Ingress</div>}
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-6 animate-in fade-in zoom-in duration-300">
            <div className="flex justify-between items-center">
              <h4 className="text-sm font-bold text-white/40 uppercase tracking-widest">Generated Chart Scaffolding</h4>
              <button className="flex items-center space-x-2 px-4 py-2 bg-kube-blue rounded-lg text-xs font-bold hover:bg-kube-blue/80 transition-all">
                <Download size={14} />
                <span>Download .tgz</span>
              </button>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between px-2">
                  <span className="text-[10px] font-mono text-white/20 uppercase font-black">values.yaml</span>
                  <CopyButton text={generateYaml()} label="Copy" />
                </div>
                <pre className="bg-black/60 rounded-2xl p-6 border border-white/10 font-mono text-xs text-blue-300 overflow-auto h-[400px]">
                  {generateYaml()}
                </pre>
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between px-2">
                  <span className="text-[10px] font-mono text-white/20 uppercase font-black">templates/deployment.yaml</span>
                  <CopyButton text={generateDeployment()} label="Copy" />
                </div>
                <pre className="bg-black/60 rounded-2xl p-6 border border-white/10 font-mono text-xs text-purple-300 overflow-auto h-[400px]">
                  {generateDeployment()}
                </pre>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
