#!/bin/bash

# Define the Python script path
PYTHON_SCRIPT1="./drone_telemetry_code/get_attitude_data.py"

# Start the first Python script in the background
echo "Starting Python script 1..."
python3 "$(realpath $PYTHON_SCRIPT1)" &

# Optional: To keep the script running if needed
wait