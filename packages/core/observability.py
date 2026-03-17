import requests
import time
import os
import uuid
from typing import Optional, Dict, Any

class ObservabilityClient:
    def __init__(self, service_name: str, collector_url: str = "http://observability_api:8002"):
        self.service_name = service_name
        self.collector_url = collector_url

    def log(self, message: str, level: str = "INFO", trace_id: Optional[str] = None):
        payload = {
            "service": self.service_name,
            "message": message,
            "level": level,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "trace_id": trace_id or str(uuid.uuid4())
        }
        try:
            requests.post(f"{self.collector_url}/ingest/log", json=payload, timeout=0.5)
        except:
            pass # Fail silently in production, or log to console

    def metric(self, name: str, value: float, unit: str = "count", tags: Optional[Dict[str, str]] = None):
        payload = {
            "service": self.service_name,
            "name": name,
            "value": value,
            "unit": unit,
            "tags": tags or {},
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            requests.post(f"{self.collector_url}/ingest/metric", json=payload, timeout=0.5)
        except:
            pass

    def trace(self, operation: str, start_time: float, end_time: float, trace_id: str, span_id: str):
        payload = {
            "service": self.service_name,
            "operation": operation,
            "trace_id": trace_id,
            "span_id": span_id,
            "start_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(start_time)),
            "end_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(end_time))
        }
        try:
            requests.post(f"{self.collector_url}/ingest/trace", json=payload, timeout=0.5)
        except:
            pass
