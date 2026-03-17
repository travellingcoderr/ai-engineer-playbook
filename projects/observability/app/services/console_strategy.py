from .base import IngestionStrategy
from packages.core.models.observability import LogEntry, MetricEntry, TraceSpan

class ConsoleIngestionStrategy(IngestionStrategy):
    """Simple strategy for local development: Print to console."""
    def process_log(self, log: LogEntry):
        print(f"OBS_LOG: {log.json()}")
        
    def process_metric(self, metric: MetricEntry):
        print(f"OBS_METRIC: {metric.json()}")
        
    def process_trace(self, trace: TraceSpan):
        print(f"OBS_TRACE: {trace.json()}")
