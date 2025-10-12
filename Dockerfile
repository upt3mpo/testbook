# Multi-stage build for Testbook
# Stage 1: Build frontend
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Final image with backend and frontend
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install uv for faster package installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy backend requirements and install with uv (fallback to pip)
# Use --only-binary to avoid compilation (no gcc needed)
COPY backend/requirements.txt ./
RUN uv pip install --system --no-cache --only-binary :all: -r requirements.txt || \
    pip install --no-cache-dir --only-binary :all: -r requirements.txt || \
    (apt-get update && apt-get install -y gcc && \
     uv pip install --system --no-cache -r requirements.txt)

# Copy backend code
COPY backend/ ./

# Copy built frontend to backend static directory
COPY --from=frontend-build /app/frontend/dist ./frontend-dist

# Create necessary directories
RUN mkdir -p static/images static/videos

# Copy image generation script
COPY setup_images.py ./

# Generate placeholder images
RUN pip install Pillow && python3 setup_images.py

# Expose port
EXPOSE 8000

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Run seed and start server
CMD python3 -c "from seed import seed_database; seed_database()" && \
    uvicorn main:app --host 0.0.0.0 --port 8000

