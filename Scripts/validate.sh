#!/bin/bash

TASK=$1
NAME=$2

# Ensure TASK and NAME are provided
if [ -z "$TASK" ] || [ -z "$NAME" ]; then
	echo "Usage: $0 <task> <name>"
	exit 1
fi

# Ensure the output directory exists
OUTPUT_DIR="./Output/$TASK"
FINAL_DIR="./Output/$TASK/final/"
mkdir -p "$FINAL_DIR"
TASK_FILE="./Tasks/$TASK/$NAME.py"

docker cp $TASK_FILE $TASK:/App/StudentWork/
# Function to monitor Docker logs and copy the file
monitor_logs_and_copy() {
	while true; do
		# Check Docker logs for the specific message
		if docker logs "$TASK" 2>&1 | grep -q "$NAME is done"; then
			# Perform the docker cp command
			docker cp "$TASK:/App/output/$NAME.py.out" "$OUTPUT_DIR"
			docker cp "$TASK:/App/output/final/$NAME.final" "$FINAL_DIR"
			echo "File copied to $OUTPUT_DIR"
			break
		fi
		# Sleep for a short duration to avoid busy-waiting
		sleep 5
	done
}

# Start monitoring logs
monitor_logs_and_copy
