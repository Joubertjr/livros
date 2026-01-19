# Base image
FROM python:3.11-slim

# Ensure deterministic I/O
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Workdir
WORKDIR /app

# System deps (optional but good for wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# App source
COPY src /app/src

# Copy Makefile
COPY Makefile /app/Makefile

# Copy and setup entrypoint
COPY src/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create necessary directories
RUN mkdir -p /app/volumes /app/EVIDENCIAS /app/volumes/temp

# Expose port for Web UI
EXPOSE 8000

# Use entrypoint for dual-mode (CLI + Web)
ENTRYPOINT ["/app/entrypoint.sh"]

# Default mode: Web UI
CMD ["web"]
