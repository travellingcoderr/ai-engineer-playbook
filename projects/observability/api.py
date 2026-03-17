from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.models.obs_models import LogEntry, MetricEntry, TraceSpan
from app.services.factory import ObservabilityFactory
import time
import json
import os

app = FastAPI(title="Observability Collector Service", version="0.1.0")

# Initialize strategy (in corporate apps, this would be env-driven)
strategy = ObservabilityFactory.get_strategy("file")
LOG_FILE = "observability.log"

@app.middleware("http")
async def audit_logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    # Internal audit of the ingestion service itself
    log_entry = {
        "path": request.url.path,
        "status_code": response.status_code,
        "latency": f"{duration:.4f}s",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    # We print to console, but we could also ship to our own strategy!
    print(f"OBS_AUDIT: {json.dumps(log_entry)}")
    return response

@app.post("/ingest/log")
async def ingest_log(log: LogEntry):
    strategy.process_log(log)
    return {"status": "ingested"}

@app.post("/ingest/metric")
async def ingest_metric(metric: MetricEntry):
    strategy.process_metric(metric)
    return {"status": "ingested"}

@app.post("/ingest/trace")
async def ingest_trace(trace: TraceSpan):
    strategy.process_trace(trace)
    return {"status": "ingested"}

@app.get("/api/telemetry")
async def get_telemetry():
    if not os.path.exists(LOG_FILE):
        return {"logs": [], "metrics": [], "traces": []}
    
    data = {"logs": [], "metrics": [], "traces": []}
    with open(LOG_FILE, "r") as f:
        # Get last 100 lines
        lines = f.readlines()[-100:]
        for line in lines:
            try:
                entry = json.loads(line)
                entry_type = entry.get("type")
                if entry_type == "log":
                    data["logs"].append(entry)
                elif entry_type == "metric":
                    data["metrics"].append(entry)
                elif entry_type == "trace":
                    data["traces"].append(entry)
            except:
                continue
    return data

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Observability Dashboard</title>
        <style>
            body { font-family: 'Inter', system-ui, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
            .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 10px; margin-bottom: 20px; }
            .grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
            .card { background: #1e293b; border-radius: 8px; padding: 15px; border: 1px solid #334155; }
            .card h2 { margin-top: 0; font-size: 1.2rem; color: #38bdf8; display: flex; justify-content: space-between; }
            .log-list, .metric-list, .trace-list { height: 500px; overflow-y: auto; font-family: monospace; font-size: 0.85rem; }
            .log-item, .trace-item { padding: 8px; border-bottom: 1px solid #334155; }
            .log-item.ERROR { color: #f87171; }
            .log-item.INFO { color: #34d399; }
            .metric-item { display: flex; justify-content: space-between; padding: 8px; background: #0f172a; margin-bottom: 5px; border-radius: 4px; }
            .tag { font-size: 0.7rem; background: #334155; padding: 2px 6px; border-radius: 4px; margin-right: 5px; }
            .refresh-btn { background: #38bdf8; color: #0f172a; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; }
            .trace-id { color: #94a3b8; font-size: 0.75rem; }
            .duration { color: #fbbf24; font-weight: bold; float: right; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Observability Collector</h1>
            <button class="refresh-btn" onclick="fetchData()">🔄 Refresh</button>
        </div>
        <div class="grid">
            <div class="card">
                <h2>Recent Logs <span id="log-count">0</span></h2>
                <div id="logs" class="log-list"></div>
            </div>
            <div class="card">
                <h2>Metrics Summary <span id="metric-count">0</span></h2>
                <div id="metrics" class="metric-list"></div>
            </div>
            <div class="card">
                <h2>Distributed Traces <span id="trace-count">0</span></h2>
                <div id="traces" class="trace-list"></div>
            </div>
        </div>

        <script>
            // Get service from URL query param
            const urlParams = new URLSearchParams(window.location.search);
            const serviceFilter = urlParams.get('service');
            
            if (serviceFilter) {
                document.querySelector('h1').innerText += ` - ${serviceFilter}`;
            }

            async function fetchData() {
                try {
                    const res = await fetch('/api/telemetry');
                    const data = await res.json();
                    
                    // Apply filtering if serviceFilter is present
                    let logs = data.logs;
                    let metrics = data.metrics;
                    let traces = data.traces;

                    if (serviceFilter) {
                        logs = logs.filter(l => l.service === serviceFilter);
                        metrics = metrics.filter(m => m.service === serviceFilter);
                        traces = traces.filter(t => t.service === serviceFilter);
                    }
                    
                    // Update Logs
                    const logContainer = document.getElementById('logs');
                    document.getElementById('log-count').innerText = logs.length;
                    logContainer.innerHTML = logs.slice().reverse().map(l => `
                        <div class="log-item ${l.level}">
                            <span class="tag">${l.service}</span>
                            [${l.level}] ${l.message}
                            <div style="font-size: 0.7rem; opacity: 0.5;">${l.timestamp} | Trace: ${l.trace_id || 'N/A'}</div>
                        </div>
                    `).join('');

                    // Update Metrics
                    const metricContainer = document.getElementById('metrics');
                    document.getElementById('metric-count').innerText = metrics.length;
                    metricContainer.innerHTML = metrics.slice().reverse().map(m => `
                        <div class="metric-item">
                            <span><span class="tag">${m.service}</span> ${m.name}</span>
                            <span style="color: #fbbf24; font-weight: bold;">${m.value} ${m.unit}</span>
                        </div>
                    `).join('');

                    // Update Traces
                    const traceContainer = document.getElementById('traces');
                    document.getElementById('trace-count').innerText = traces.length;
                    traceContainer.innerHTML = traces.slice().reverse().map(t => {
                        const start = new Date(t.start_time);
                        const end = new Date(t.end_time);
                        const duration = (end - start) / 1000;
                        return `
                            <div class="trace-item">
                                <span class="tag">${t.service}</span>
                                <strong>${t.operation}</strong>
                                <span class="duration">${duration.toFixed(3)}s</span>
                                <div class="trace-id">ID: ${t.trace_id} | Span: ${t.span_id}</div>
                            </div>
                        `;
                    }).join('');
                } catch (e) {
                    console.error("Failed to fetch telemetry:", e);
                }
            }
            fetchData();
            setInterval(fetchData, 5000); // Auto refresh every 5s
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
def health():
    return {"status": "ok", "ingestion_strategy": type(strategy).__name__}
