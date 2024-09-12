#!/bin/bash

# Use Zenity to pop up a dialog for inputting two Herelink transmitter IP addresses
USER_INPUT=$(zenity --forms --title="Input Required" \
  --text="Enter the server and Herelink transmitter IP addresses:" \
  --add-entry="Server address" \
  --add-entry="Herelink 1 IP" \
  --add-entry="Herelink 2 IP")

# Check if input was canceled or empty
if [ -z "$USER_INPUT" ]; then
    echo "No input provided. Exiting..."
    exit 1
fi

# Split the user input into separate variables (Server, Herelink1, Herelink2)
SERVER_IP=$(echo "$USER_INPUT" | cut -d '|' -f 1)
HERELINK1_IP=$(echo "$USER_INPUT" | cut -d '|' -f 2)
HERELINK2_IP=$(echo "$USER_INPUT" | cut -d '|' -f 3)

# Define the Python scripts
PYTHON_SCRIPT1="./drone_telemetry_code/get_attitude_data.py"
PYTHON_SCRIPT2="./drone_telemetry_code/get_complex.py"

# Define the MAVProxy commands with user-provided Herelink IPs
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

    # Close all gnome-terminal windows that were opened
    pkill -f gnome-terminal

    # Exit the script
    exit 0
}

# Trap Ctrl+C (SIGINT) and call cleanup
trap cleanup SIGINT

# Start the first MAVProxy instance in a new terminal
echo "Starting MAVProxy instance 1 in a new terminal..."
gnome-terminal -- bash -c "$MAVPROXY_COMMAND1; exec bash" &

# Start the second MAVProxy instance in a new terminal
echo "Starting MAVProxy instance 2 in a new terminal..."
gnome-terminal -- bash -c "$MAVPROXY_COMMAND2; exec bash" &

# Start the first Python script in a new terminal and pass the input as an argument
echo "Starting Python script 1 in a new terminal with server address $SERVER_IP..."
gnome-terminal -- bash -c "python3 $PYTHON_SCRIPT1 $SERVER_IP; exec bash" &

# Start the second Python script in a new terminal and pass the input as an argument
echo "Starting Python script 2 in a new terminal with server address $SERVER_IP..."
gnome-terminal -- bash -c "python3 $PYTHON_SCRIPT2 $SERVER_IP; exec bash" &

# Wait for the processes to run indefinitely until interrupted
echo "All instances are running. Press Ctrl+C to stop and close all terminals."

# Keep the script running until interrupted by Ctrl+C
while true; do
    sleep 1
done
