# Use an official Python runtime as a parent image
FROM python:3.9-slim

ARG TASK
ENV TASK=$TASK
# Set the working directory to /App
WORKDIR /App

# Create the output directory
RUN mkdir /App/output

RUN mkdir /App/output/"$TASK"  # Use single quotes with escape character

RUN mkdir /App/StudentWork

# Copy the run_script.sh file into the App/scripts/ directory
COPY ./run_script.sh scripts/

# Make the script executable
RUN chmod +x scripts/run_script.sh

# Run the script
CMD ["sh", "scripts/run_script.sh"]

