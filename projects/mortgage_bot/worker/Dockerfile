FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY projects/mortgage_bot/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY projects/mortgage_bot/worker/worker.py ./worker.py
COPY projects/mortgage_bot/worker/tasks ./tasks
COPY projects/mortgage_bot/backend/app ./app
COPY packages /app/packages

ENV PYTHONPATH=/app

CMD ["python", "worker.py"]
