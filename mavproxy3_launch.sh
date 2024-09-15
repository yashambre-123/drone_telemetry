#!/bin/bash

# Hardcoded IP address for Herelink 2
HERELINK2_IP="192.168.0.103"

# Define the MAVProxy command for Herelink 2
MAVPROXY_COMMAND2="mavproxy.py --master=udpout:$HERELINK2_IP:14552 --out=udp:127.0.0.1:14530"

# Function to handle cleanup when script is interrupted
cleanup() {
    echo "Caught interrupt signal (Ctrl+C). Stopping MAVProxy instance 2..."

    # Kill the MAVProxy process (if it's running)
    pkill -f "$MAVPROXY_COMMAND2"

    # Exit the script
    exit 0
}

# Trap Ctrl+C (SIGINT) and call cleanup
trap cleanup SIGINT

# Start the MAVProxy instance 2 in the foreground
echo "Starting MAVProxy instance 3..."
$MAVPROXY_COMMAND2

# Wait for Ctrl+C to stop the process
echo "MAVProxy instance 3 is running. Press Ctrl+C to stop."

# Keep the script running until interrupted
while true; do
    sleep 1
done
