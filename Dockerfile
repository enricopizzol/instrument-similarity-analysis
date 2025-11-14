# Use a lightweight Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed (none for basic pandas/numpy)
# RUN apt-get update && apt-get install -y ...

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables if needed
ENV PYTHONUNBUFFERED=1

# Default command - can be overridden at runtime
CMD ["/bin/bash"]
