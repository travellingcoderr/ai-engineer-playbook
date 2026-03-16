FROM python:3.11-slim

WORKDIR /app

# Upgrade pip and install core system deps if any exist
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

# We expect the unified requirements file to be injected via root context
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# The code will be mounted at run-time for hot-reloading in dev.
CMD ["uvicorn", "projects.multi_agent.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
