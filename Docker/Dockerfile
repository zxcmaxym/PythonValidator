# Use a Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the Python scripts from host to container
COPY ./StudentWork /app/StudentWork

# Create output directory
RUN mkdir -p /output

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Run Python scripts and capture output/errors
CMD find /app/StudentWork -name "*.py" -exec sh -c 'python3 "$1" > "/output/$(basename "$1").out" 2>&1' _ {} \;
