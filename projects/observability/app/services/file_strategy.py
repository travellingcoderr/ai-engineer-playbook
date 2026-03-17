import json
from typing import Dict, Any
from .base import IngestionStrategy
from ..models.obs_models import LogEntry, MetricEntry, TraceSpan

class FileIngestionStrategy(IngestionStrategy):
    """Corporate pattern: Buffer to file for later log-shipper (FluentBit/Filebeat) digestion."""
    def __init__(self, filename: str = "observability.log"):
        self.filename = filename

    def _write(self, data: Dict[str, Any]):
        with open(self.filename, "a") as f:
            f.write(json.dumps(data) + "\n")

    def process_log(self, log: LogEntry):
        self._write({"type": "log", **json.loads(log.json())})

    def process_metric(self, metric: MetricEntry):
        self._write({"type": "metric", **json.loads(metric.json())})

    def process_trace(self, trace: TraceSpan):
        self._write({"type": "trace", **json.loads(trace.json())})
