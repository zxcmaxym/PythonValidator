#!/bin/sh

# Find and execute all Python scripts, capturing output and errors
find /app/StudentWork -name "*.py" | while read -r script; do
	output_file="/output/$(basename "$script").out"
	if ! python3 "$script" >"$output_file" 2>&1; then
		echo "Failed" >>"$output_file"
	fi
done
