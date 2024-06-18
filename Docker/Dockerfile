# Use an official Python runtime as a parent image
FROM python:3.9-slim

ARG TASK
ENV TASK=$TA
# Set the working directory to /App
WORKDIR /App

# Create directories using the environment variable
RUN mkdir -p /App/output/${TASK}/final \
    && mkdir -p /App/StudentWork
# Copy the run_script.sh file into the App/scripts/ directory
COPY ./run_script.sh scripts/

# Make the script executable
RUN chmod +x scripts/run_script.sh

# Run the script
CMD ["sh", "scripts/run_script.sh"]

