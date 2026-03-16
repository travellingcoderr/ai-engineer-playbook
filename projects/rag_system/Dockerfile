# Use official Python runtime as a parent image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Install build dependencies (sometimes needed for certain ML packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
# Note: Since the context will be the projects/rag_system directory,
# we need to copy a requirements file. For simplicity, we create one inline
# or copy the global one if run from the project root.
# We will assume this Dockerfile is run from ai-engineer-playbook root
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY projects/rag_system/app /app/projects/rag_system/app

# Set PYTHONPATH so absolute imports like 'app.services.x' work
ENV PYTHONPATH="/app/projects/rag_system"

# Set the port the application should run on (defaults to 8000)
ENV RAG_PORT=8000

# Expose the port the app runs on
EXPOSE ${RAG_PORT}

# Command to run the application using uvicorn
CMD ["sh", "-c", "uvicorn projects.rag_system.app.main:app --host 0.0.0.0 --port ${RAG_PORT}"]
