#!/bin/bash

# Hardcoded IP addresses
HERELINK1_IP="192.168.0.103"
HERELINK2_IP="192.168.0.100"

# Define the Python scripts
PYTHON_SCRIPT1="./drone_telemetry_code/get_attitude_data.py"
PYTHON_SCRIPT2="./drone_telemetry_code/get_complex.py"

# Define the MAVProxy commands with hardcoded Herelink IPs
MAVPROXY_COMMAND1="mavproxy.py --master=udpout:$HERELINK1_IP:14552 --out=udp:127.0.0.1:14510"
MAVPROXY_COMMAND2="mavproxy.py --master=udpout:$HERELINK2_IP:14552 --out=udp:127.0.0.1:14520"

# Function to handle cleanup when script is interrupted
cleanup() {
    echo "Caught interrupt signal (Ctrl+C). Cleaning up..."

    # Kill all Python and MAVProxy processes
    pkill -f "python3 $PYTHON_SCRIPT1"
    pkill -f "python3 $PYTHON_SCRIPT2"
    pkill -f "$MAVPROXY_COMMAND1"
    pkill -f "$MAVPROXY_COMMAND2"

    # Exit the script
    exit 0
}

# Trap Ctrl+C (SIGINT) and call cleanup
trap cleanup SIGINT

# Start the first Python script in a new GNOME terminal window
echo "Starting Python script 1 in a new terminal..."
gnome-terminal -- bash -c "python3 $(realpath $PYTHON_SCRIPT1); exec bash"

# Start the second Python script in a new GNOME terminal window
echo "Starting Python script 2 in a new terminal..."
gnome-terminal -- bash -c "python3 $(realpath $PYTHON_SCRIPT2); exec bash"

# Start the first MAVProxy instance in a new GNOME terminal window
echo "Starting MAVProxy instance 1 in a new terminal..."
gnome-terminal -- bash -c "$MAVPROXY_COMMAND1; exec bash"

# Start the second MAVProxy instance in a new GNOME terminal window
echo "Starting MAVProxy instance 2 in a new terminal..."
gnome-terminal -- bash -c "$MAVPROXY_COMMAND2; exec bash"

# Wait for the processes to run indefinitely until interrupted
echo "All instances are running in separate terminals. Press Ctrl+C to stop."

# Keep the script running until interrupted by Ctrl+C
while true; do
    sleep 1
done