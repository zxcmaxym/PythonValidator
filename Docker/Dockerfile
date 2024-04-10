FROM python:3

# Set working directory
WORKDIR /app

# Copy all .py files from /app/StudentWork into the container
COPY ./StudentWork/*.py /app/StudentWork/

# Create a directory to store output files
RUN mkdir /output

# Run each Python script in /app/StudentWork and redirect output and error to corresponding text files
CMD ["bash", "-c", "for script in /app/StudentWork/*.py; do python3 $script > /output/$(basename $script .py).txt 2>&1; done"]

