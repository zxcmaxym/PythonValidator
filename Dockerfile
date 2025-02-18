# Use an official Python runtime as a parent image
FROM python:3.11-slim
# Set the working directory to /app
WORKDIR /App
# Copy the current directory contents into the container at /app
COPY . /App
# Install the docker client
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl software-properties-common
COPY --from=docker:dind /usr/local/bin/docker /usr/local/bin/
# Run poetry install
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install 
# Make port 80 available to the world outside this container
EXPOSE 4444 
CMD ["python", "hehe.py"]
