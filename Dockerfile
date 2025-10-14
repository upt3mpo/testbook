# Multi-stage build for Testbook
# Stage 1: Build frontend
FROM node:20-alpine AS frontend-build
ENV CI=1

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN --mount=type=cache,target=/root/.npm npm ci --ignore-scripts
COPY frontend/ ./
RUN npm run build

# Stage 2: Final image with backend and frontend
FROM python:3.11-slim-bookworm

# Speed up Python and keep images small
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:${PATH}" \
    VIRTUAL_ENV="/app/.venv"

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv for faster package installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files for reproducible builds
COPY pyproject.toml uv.lock ./

# Install dependencies using uv sync (faster and uses lockfile)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Copy backend code
COPY backend/ ./

# Copy built frontend to backend static directory
COPY --from=frontend-build /app/frontend/dist ./frontend-dist

# Create necessary directories
RUN mkdir -p static/images static/videos

# Copy image generation script
COPY setup_images.py ./

# Generate placeholder images
RUN python3 setup_images.py

# Expose port
EXPOSE 8000


# Run seed and start server
CMD python3 -c "from seed import seed_database; seed_database()" && \
    uvicorn main:app --host 0.0.0.0 --port 8000
