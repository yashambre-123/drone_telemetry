#!/bin/bash

# IP addresses for Herelink 1 and Herelink 2
HERELINK1_IP="192.168.0.103"
HERELINK2_IP="192.168.0.100"

# MAVProxy commands for Herelink 1 and Herelink 2
MAVPROXY_COMMAND1="mavproxy.py --master=udpout:$HERELINK1_IP:14552 --out=udp:127.0.0.1:14510"
MAVPROXY_COMMAND2="mavproxy.py --master=udpout:$HERELINK2_IP:14552 --out=udp:127.0.0.1:14520"

# Python script paths
PYTHON_SCRIPT1="./drone_telemetry_code/get_attitude_data.py"
PYTHON_SCRIPT2="./drone_telemetry_code/get_complex.py"

# Function to handle cleanup when the script is interrupted
cleanup() {
    echo "Caught interrupt signal (Ctrl+C). Stopping all processes..."

    # Kill the MAVProxy instances
    pkill -f "$MAVPROXY_COMMAND1"
    pkill -f "$MAVPROXY_COMMAND2"

    # Kill the Python scripts
    pkill -f "$(realpath $PYTHON_SCRIPT1)"
    pkill -f "$(realpath $PYTHON_SCRIPT2)"

    # Exit the script
    exit 0
}

# Trap Ctrl+C (SIGINT) and call cleanup
trap cleanup SIGINT

# Start the MAVProxy instance for Herelink 1 in the background
echo "Starting MAVProxy instance 1..."
$MAVPROXY_COMMAND1 &

# Start the MAVProxy instance for Herelink 2 in the background
echo "Starting MAVProxy instance 2..."
$MAVPROXY_COMMAND2 &

# Start the first Python script in the background
echo "Starting Python script 1..."
python3 "$(realpath $PYTHON_SCRIPT1)" &

# Start the second Python script in the background
echo "Starting Python script 2..."
python3 "$(realpath $PYTHON_SCRIPT2)" &

# Wait for Ctrl+C to stop all processes
echo "All instances are running. Press Ctrl+C to stop."

# Keep the script running until interrupted
while true; do
    sleep 1
done
