from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class LogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    level: str = "INFO"
    service: str
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    trace_id: Optional[str] = None

class MetricEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    service: str
    name: str
    value: float
    unit: str = "count"
    labels: Dict[str, str] = Field(default_factory=dict)

class TraceSpan(BaseModel):
    service: str
    operation: str
    trace_id: str
    span_id: str
    parent_id: Optional[str] = None
    start_time: datetime
    end_time: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)
