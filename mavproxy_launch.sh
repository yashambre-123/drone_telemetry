#!/bin/bash

# Hardcoded IP addresses
HERELINK1_IP="192.168.0.103"
HERELINK2_IP="192.168.0.100"

# Define the MAVProxy commands with hardcoded Herelink IPs
MAVPROXY_COMMAND1="mavproxy.py --master=udpout:$HERELINK1_IP:14552 --out=udp:127.0.0.1:14510"
MAVPROXY_COMMAND2="mavproxy.py --master=udpout:$HERELINK2_IP:14552 --out=udp:127.0.0.1:14520"

# Start the first MAVProxy instance in the background
echo "Starting MAVProxy instance 1..."
$MAVPROXY_COMMAND1 &

# Start the second MAVProxy instance in the background
echo "Starting MAVProxy instance 2..."
$MAVPROXY_COMMAND2 &

# Optional: To keep the script running if needed
wait
