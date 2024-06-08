# Use a Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the Python scripts from host to container
COPY ./StudentWork /app/StudentWork

# Create output directory
RUN mkdir -p /output

# Copy the shell script to the container
COPY run_scripts.sh /app/run_scripts.sh

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Make the shell script executable
RUN chmod +x /app/run_scripts.sh

# Run the shell script to execute Python scripts
CMD ["/app/run_scripts.sh"]

