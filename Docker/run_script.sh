#!/bin/bash

echo "Starting script"

process_scripts() {
    echo "Processing scripts"
    find /App/StudentWork -name "*.py" | while read -r script; do
        output_file="/App/output/$TASK/$(basename "$script").out"
        if python3 "$script" >"$output_file" 2>&1; then
            echo "Success" >>"$output_file"
        else
            echo "Failed" >>"$output_file"
        fi
        base_name=$(basename "$script" .py)
        echo "$base_name is done"
        rm "$script"
    done
}

SECONDS=0
WATCHED_FOLDER="/App/StudentWork"
DURATION=$((500)) # Duration in seconds
END_TIME=$((SECONDS + DURATION))
initial_files=$(ls "$WATCHED_FOLDER")

echo $SECONDS
while [ $SECONDS -lt $END_TIME ]; do
	current_files=$(ls "$WATCHED_FOLDER")
	if [ "$initial_files" != "$current_files" ]; then
		echo "Found new Files, Evaluating"
		process_scripts
		initial_files=$(ls "$WATCHED_FOLDER") # Update initial_files
		END_TIME=$((SECONDS + DURATION))
	fi
	sleep 1
	SECONDS=$((SECONDS + 1))
done
