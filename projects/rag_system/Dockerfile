FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

COPY projects/rag_system/requirements-rag-system.txt .
COPY pyproject.toml .
COPY packages /app/packages

RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements-rag-system.txt \
    && pip install --no-cache-dir -e .

FROM python:3.12-slim

WORKDIR /app

ENV PATH="/opt/venv/bin:${PATH}"
ENV PYTHONPATH="/app:/app/projects/rag_system"
ENV RAG_PORT=8000

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app/packages /app/packages
COPY --from=builder /app/pyproject.toml /app/pyproject.toml

COPY projects/rag_system/app /app/projects/rag_system/app

EXPOSE ${RAG_PORT}

CMD ["sh", "-c", "uvicorn projects.rag_system.app.main:app --host 0.0.0.0 --port ${RAG_PORT}"]
