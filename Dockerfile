FROM python:3.12-slim

# Install system dependencies: ffmpeg for media merging/clipping and curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Set environment defaults
ENV HOST=0.0.0.0
ENV PORT=8000
ENV RENDER=true

EXPOSE 8000

# Start server
CMD ["python", "main.py"]
