FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from repository root. Build with context set to project root:
#   docker build -f brickstat-app/backend/Dockerfile .
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy backend sources
COPY brickstat-app/backend /app

EXPOSE 5000

CMD ["python", "backend.py"]
