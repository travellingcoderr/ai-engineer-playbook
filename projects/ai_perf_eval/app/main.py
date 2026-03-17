import time
import uvicorn
import logging
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.models.eval_models import EvalRequest, LoadTestRequest, EvalType
from packages.core.observability import ObservabilityClient

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-perf-eval")

class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Standardized Audit Log for AI Performance Monitoring
        logger.info(
            f"AUDIT | {request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Duration: {process_time:.3f}s"
        )
        return response

app = FastAPI(title="AI Performance & Evaluation")
app.add_middleware(AuditLogMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Observability
obs = ObservabilityClient("ai_perf_eval")

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ai_perf_eval"}

@app.post("/v1/eval")
async def run_eval(request: EvalRequest, background_tasks: BackgroundTasks):
    """
    Triggers an evaluation run.
    This demonstrates the Phase 4 'Evaluation-as-a-Service' pattern.
    """
    obs.log(f"Received evaluation request: {request.name} for project: {request.project}")
    
    from app.services.eval_factory import EvalFactory
    from app.models.eval_models import CostEvalInput
    
    # Example logic: Perform a cost evaluation immediately for demonstration
    cost_eval = EvalFactory.get_evaluator(EvalType.COST)
    
    # Passing strongly typed input object
    eval_input = CostEvalInput(
        model=request.model,
        input_tokens=1500,
        output_tokens=500
    )
    
    results = cost_eval.evaluate(eval_input)
    
    obs.log(f"Evaluation results for {request.name}: {results}")
    return {"status": "completed", "eval_id": f"eval_{int(time.time())}", "results": results}

@app.post("/v1/load-test")
async def run_load_test(request: LoadTestRequest, background_tasks: BackgroundTasks):
    obs.log(f"Starting load test on target: {request.target_url}")
    # TODO: Implement k6 bridge logic
    return {"status": "starting", "params": request.dict()}

if __name__ == "__main__":
    uvicorn.run("projects.ai_perf_eval.app.main:app", host="0.0.0.0", port=8007, reload=True)
