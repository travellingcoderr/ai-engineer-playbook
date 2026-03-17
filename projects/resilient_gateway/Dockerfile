FROM python:3.12-slim

WORKDIR /app

# Copy requirements from root if needed, but here we assume monorepo context
# For a standalone build, we'd copy specific files. 
# For now, we'll follow the pattern of other projects in this repo.

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="/app:/app/projects/resilient_gateway"

EXPOSE 8006

CMD ["sh", "-c", "uvicorn projects.resilient_gateway.app.main:app --host 0.0.0.0 --port 8006"]
