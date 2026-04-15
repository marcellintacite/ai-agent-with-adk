# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY src ./src

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Default configuration
ENV PORT=8080
ENV LOG_LEVEL=INFO

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:${PORT}/health || exit 1

EXPOSE ${PORT}

CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT} --workers 4
