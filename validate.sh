#!/bin/bash

# Build Docker image
docker build -t validator ./Docker/

# Run Docker container
docker run --name="validator" validator

# Copy student work to container
docker cp ./Docker/StudentWork validator:/app/StudentWork

# Start the container
docker start validator

# Wait until the container stops running
while [ "$(docker container inspect -f '{{.State.Running}}' validator)" = "true" ]; do
	sleep 1
done

# Copy validation results from container to host
docker cp validator:/output/. ./Docker/StudentValidations/

# Clean up - remove the container
docker rm validator
docker image rm validator
