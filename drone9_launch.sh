#!/bin/bash

# Define the Python script path
PYTHON_SCRIPT2="./drone_telemetry_code/get_complex.py"

# Start the second Python script in the background
echo "Starting Python script 2..."
python3 "$(realpath $PYTHON_SCRIPT2)" &

# Optional: To keep the script running if needed
wait
