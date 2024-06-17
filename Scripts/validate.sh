#!/bin/bash

# Function to check for log message and copy file
check_and_copy() {
	task_name="$1"
	file_name="$2"

	# Escape special characters in the log message for grep

	# Check if log contains the completion message
	if docker logs "$task_name" 2>&1 | grep -q "$file_name is done"; then
		# Create output directory if it doesn't exist
		mkdir -p "./output/$task_name"

		# Copy the file with progress indicator
		docker cp "$task_name:/App/output/$task_name/$file_name.py.out" "./output/$task_name/$file_name.py.out" && echo "File copied successfully!" || echo "Error copying file!"

		# Exit the script after successful copy
		return 0
	fi
}

# Get task and file name from arguments
task_name="$1"
file_name="$2"

# Check for missing arguments
if [ -z "$task_name" ] || [ -z "$file_name" ]; then
	echo "Usage: $0 <task_name> <file_name>"
	exit 1
fi

# Loop until file is copied or an error occurs
while true; do
	# Call the check_and_copy function
	result=$(check_and_copy "$task_name" "$file_name")

	# Exit the loop if successful (return value of 0 from check_and_copy)
	if [[ $result == 0 ]]; then
		break
		echo "Done"
	fi

	# Print message and sleep before next iteration
	echo "No matching message found in logs. Waiting for completion..."
	sleep 1 # Adjust sleep time as needed
done
