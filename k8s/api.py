import os
from fastapi import FastAPI
from prometheus_client import make_asgi_app, Counter

app = FastAPI(title="K8s API Service")

# Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

REQUEST_COUNT = Counter("api_requests_total", "Total count of requests", ["endpoint"])

@app.get("/")
async def root():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return {"message": "Welcome to the K8s API Service!", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/secret")
async def get_secret():
    REQUEST_COUNT.labels(endpoint="/secret").inc()
    # In a real app, this would be injected via K8s Secret
    secret_value = os.getenv("APP_SECRET", "default_secret_not_set")
    return {"secret_key": "APP_SECRET", "value": secret_value}

@app.get("/env")
async def get_env():
    REQUEST_COUNT.labels(endpoint="/env").inc()
    # In a real app, this would be injected via K8s ConfigMap
    env_value = os.getenv("APP_ENV_VAR", "default_env_not_set")
    return {"env_var": "APP_ENV_VAR", "value": env_value}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
