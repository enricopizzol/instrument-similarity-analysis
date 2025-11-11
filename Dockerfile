# Use a lightweight Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed (none for basic pandas/numpy)
# RUN apt-get update && apt-get install -y ...

# Install Python dependencies
# Using --no-cache-dir to keep image size down
RUN pip install --no-cache-dir pandas numpy

COPY run_correlation_job.sh .

# Make script executable
RUN chmod +x run_correlation_job.sh

# Set environment variables if needed
ENV PYTHONUNBUFFERED=1

# Define default command to run the bash script wrapper
# Usage: docker run -v ... my-image /input.csv /data /output.csv
ENTRYPOINT ["./run_correlation_job.sh"]

# Default arguments (can be overridden)
CMD []
