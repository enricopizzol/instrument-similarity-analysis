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

COPY run_correlation_job.sh .

# Make script executable
RUN chmod +x run_correlation_job.sh

# Set environment variables if needed
ENV PYTHONUNBUFFERED=1

# Default command (can be overridden easily)
# We use CMD instead of ENTRYPOINT to allow flexible command execution (e.g., bash -c "...")
CMD ["./run_correlation_job.sh"]
