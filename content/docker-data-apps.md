---
title: "Containerizing Data Apps with Docker"
date: "2026-04-15"
category: "Software Engineering"
excerpt: "A practical walkthrough of Dockerizing Streamlit and FastAPI applications for reproducible, deployable data projects."
---

# Containerizing Data Apps with Docker

Docker eliminates the "it works on my machine" problem. For data applications with complex dependency chains — Python packages, system libraries, ML models — containerization is essential for reproducibility and deployment.

## Why Containerize Data Apps?

Data applications have unique packaging challenges:

- **Native dependencies**: Libraries like PyMuPDF, NumPy, and Pandas require compiled binaries
- **Model artifacts**: ML models can be gigabytes — they need to be bundled or mounted
- **Environment parity**: Development, staging, and production must use identical dependencies
- **Scaling**: Containers make horizontal scaling with orchestration tools straightforward

## A Production Dockerfile

Here's a Dockerfile for a Streamlit-based data application:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for native packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Multi-Stage Builds for ML Apps

When bundling ML models, use multi-stage builds to keep image sizes manageable:

```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim AS runtime
COPY --from=builder /root/.local /root/.local
COPY model.pkl /app/model.pkl
COPY src/ /app/src
ENV PATH=/root/.local/bin:$PATH
```

This pattern reduces final image size by separating build-time and runtime dependencies.

## Docker Compose for Multi-Service Apps

For applications with multiple services — a Streamlit frontend, FastAPI backend, and PostgreSQL database — Docker Compose orchestrates everything:

```yaml
version: "3.9"
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: portfolio
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://app:${DB_PASSWORD}@db:5432/portfolio

  app:
    build: .
    ports:
      - "8501:8501"
    depends_on:
      - api
    environment:
      API_URL: http://api:8000

volumes:
  postgres_data:
```

## Best Practices

1. **Pin base image versions**: Never use `latest` — specify `python:3.11-slim` precisely
2. **Use `.dockerignore`**: Exclude `__pycache__`, `.git`, `venv`, and test files
3. **Layer caching**: Order RUN commands from least to most frequently changing
4. **Minimize layers**: Combine related RUN commands with `&&`
5. **Non-root user**: Run applications as a non-root user for security
6. **Health checks**: Always define HEALTHCHECK for orchestration tools

## Conclusion

Containerization turns data applications from fragile scripts into robust, deployable products. Docker's learning curve is shallow, but its impact on reproducibility and deployment confidence is profound. Every data project worth building is worth containerizing.
