# Use official Python runtime as a parent image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the core dependencies from root
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the shared core packages and config
COPY pyproject.toml .
COPY packages /app/packages

# Install the shared ai-engineer-packages module
RUN pip install -e .

# Copy the observability source code
COPY projects/observability/app /app/projects/observability/app
COPY projects/observability/api.py /app/projects/observability/api.py

# Set PYTHONPATH so absolute imports work
ENV PYTHONPATH="/app:/app/projects/observability"

# Set the port the application should run on
ENV OBS_PORT=8002

# Expose the port the app runs on
EXPOSE ${OBS_PORT}

# Command to run the application using uvicorn
CMD ["sh", "-c", "uvicorn projects.observability.api:app --host 0.0.0.0 --port ${OBS_PORT}"]
