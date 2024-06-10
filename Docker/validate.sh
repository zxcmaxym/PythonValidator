#!/bin/bash

# Check if both task and libraries parameters are provided
if [ -z "$1" ] || [ -z "$2" ]; then
	echo "Both task and libraries parameters are required"
	exit 1
fi

TASK=$1
LIBRARIES=$2

# Define paths
TASK_PATH="./Docker/StudentWork/$TASK"
VALIDATION_PATH="./Docker/StudentValidations/$TASK"

# Ensure the task path exists
if [ ! -d "$TASK_PATH" ]; then
	echo "Task folder does not exist: $TASK_PATH"
	exit 1
fi

# Generate requirements.txt file
echo "$LIBRARIES" | tr ',' '\n' >"$TASK_PATH/requirements.txt"

# Build Docker image
docker build -t validator ./Docker/

# Run Docker container
docker run --name="validator" validator

# Copy student work for the specified task to the container
docker cp "$TASK_PATH" validator:/app/StudentWork

# Start the container
docker start validator

# Wait until the container stops running
while [ "$(docker container inspect -f '{{.State.Running}}' validator)" = "true" ]; do
	sleep 1
done

# Create the task folder in the validation directory
mkdir -p "$VALIDATION_PATH"

# Copy validation results from the container to the host task folder
docker cp validator:/output/. "$VALIDATION_PATH"

# Clean up - remove the container and the image
docker rm validator
docker image rm validator
