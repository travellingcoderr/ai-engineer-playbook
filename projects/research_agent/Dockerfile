# Builder stage: install dependencies into a dedicated virtualenv.
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

# Copy only the files required to install Python dependencies.
COPY projects/research_agent/requirements-research-agent.txt .
COPY pyproject.toml .
COPY packages /app/packages

RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements-research-agent.txt \
    && pip install --no-cache-dir -e .

# Runtime stage: keep only the runtime interpreter, virtualenv, and app code.
FROM python:3.12-slim

WORKDIR /app

ENV PATH="/opt/venv/bin:${PATH}"
ENV PYTHONPATH="/app:/app/projects/research_agent"
ENV RESEARCH_PORT=8003

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app/packages /app/packages
COPY --from=builder /app/pyproject.toml /app/pyproject.toml

COPY projects/research_agent/app /app/projects/research_agent/app
COPY projects/research_agent/agent.py /app/projects/research_agent/agent.py

EXPOSE ${RESEARCH_PORT}

CMD ["sh", "-c", "uvicorn projects.research_agent.app.main:app --host 0.0.0.0 --port ${RESEARCH_PORT}"]
