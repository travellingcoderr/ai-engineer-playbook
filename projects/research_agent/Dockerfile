# Use official Python runtime as a parent image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
# We will assume this Dockerfile is run from ai-engineer-playbook root
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the shared core packages and config
COPY pyproject.toml .
COPY packages /app/packages

# Install the shared ai-engineer-packages module
RUN pip install -e .

# Copy the current directory contents into the container at /app
COPY projects/research_agent/app /app/projects/research_agent/app
COPY projects/research_agent/agent.py /app/projects/research_agent/agent.py

# Set PYTHONPATH so absolute imports work
ENV PYTHONPATH="/app:/app/projects/research_agent"

# Set the port the application should run on (defaults to 8003)
ENV RESEARCH_PORT=8003

# Expose the port the app runs on
EXPOSE ${RESEARCH_PORT}

# Command to run the application using uvicorn
CMD ["sh", "-c", "uvicorn projects.research_agent.app.main:app --host 0.0.0.0 --port ${RESEARCH_PORT}"]
