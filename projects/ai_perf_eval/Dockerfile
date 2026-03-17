FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if any
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from root to leverage monorepo dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the specific project and core packages
COPY projects/ai_perf_eval /app/projects/ai_perf_eval
COPY packages /app/packages

# Set up PYTHONPATH for monorepo imports
ENV PYTHONPATH=/app:/app/projects/ai_perf_eval

EXPOSE 8007

# Run the performance evaluation service
CMD ["python", "projects/ai_perf_eval/app/main.py"]
