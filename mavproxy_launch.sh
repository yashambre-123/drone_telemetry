#!/bin/bash

# Hardcoded IP addresses
HERELINK1_IP="192.168.0.103"
HERELINK2_IP="192.168.0.100"

# Define the MAVProxy commands with hardcoded Herelink IPs
MAVPROXY_COMMAND1="mavproxy.py --master=udpout:$HERELINK1_IP:14552 --out=udp:127.0.0.1:14510"
MAVPROXY_COMMAND2="mavproxy.py --master=udpout:$HERELINK2_IP:14552 --out=udp:127.0.0.1:14520"

# Function to handle cleanup when script is interrupted
cleanup() {
    echo "Caught interrupt signal (Ctrl+C). Stopping MAVProxy instances..."

    # Kill all background MAVProxy processes
    pkill -f "$MAVPROXY_COMMAND1"
    pkill -f "$MAVPROXY_COMMAND2"

    # Exit the script
    exit 0
}

# Trap Ctrl+C (SIGINT) and call cleanup
trap cleanup SIGINT

# Start the first MAVProxy instance in the background
echo "Starting MAVProxy instance 1..."
$MAVPROXY_COMMAND1 &

# Start the second MAVProxy instance in the background
echo "Starting MAVProxy instance 2..."
$MAVPROXY_COMMAND2 &

# Wait for Ctrl+C to stop the processes
echo "MAVProxy instances are running. Press Ctrl+C to stop."

# Keep the script running until interrupted
while true; do
    sleep 1
done
