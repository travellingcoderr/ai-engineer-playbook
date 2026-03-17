from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class EvalType(str, Enum):
    COST = "cost"
    ACCURACY = "accuracy"
    LATENCY = "latency"

class EvalRequest(BaseModel):
    name: str = Field(..., description="Name of the evaluation run")
    project: str = Field(..., description="Project to evaluate (e.g., rag_system)")
    model: str = Field("gpt-4o", description="Model to use for evaluation")
    dataset_path: Optional[str] = None

class EvalResult(BaseModel):
    eval_id: str
    status: str
    scores: Dict[str, float]
    details: Optional[Dict[str, Any]] = None

class LoadTestRequest(BaseModel):
    target_url: str = Field("http://resilient_gateway:8006/v1/complete", description="URL to stress test")
    vus: int = Field(10, description="Number of virtual users")
    duration: str = Field("30s", description="Duration of the test (e.g., 30s, 1m)")
