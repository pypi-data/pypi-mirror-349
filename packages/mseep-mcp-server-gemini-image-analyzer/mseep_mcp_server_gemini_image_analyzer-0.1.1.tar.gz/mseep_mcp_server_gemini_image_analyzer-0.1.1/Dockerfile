FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with specific order to handle conflicts
RUN pip install --no-cache-dir google-generativeai>=0.3.0 && \
    pip uninstall -y google && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
ENV HOST=0.0.0.0
ENV LOG_LEVEL=INFO

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "-m", "fastmcp", "dev", "server.py"] 