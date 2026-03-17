from abc import ABC, abstractmethod
from ..models.obs_models import LogEntry, MetricEntry, TraceSpan

class IngestionStrategy(ABC):
    @abstractmethod
    def process_log(self, log: LogEntry):
        ...
    
    @abstractmethod
    def process_metric(self, metric: MetricEntry):
        ...
    
    @abstractmethod
    def process_trace(self, trace: TraceSpan):
        ...
