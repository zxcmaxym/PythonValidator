#!/bin/bash

# Build Docker image
docker build -t my-python-app ./testenv/.

# Run Docker container
docker run my-python-app
