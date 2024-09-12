from pymavlink import mavutil
import socket
import sys
import time

# Step 1: Get the server address from the command line arguments
if len(sys.argv) < 2:
    print("Usage: python get_attitude_data.py <server_address>")
    sys.exit(1)

server_address = sys.argv[1]  # Get the server address from the shell script
port = 12345

print("THIS IS MY SERVER ADDRESS: ", server_address)

# Set up the socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 2: Connect to the Pixhawk
master = mavutil.mavlink_connection('udp:127.0.0.1:14510')

# Step 3: Wait for a heartbeat from the Pixhawk to ensure the connection is alive
print("Waiting for heartbeat...")
heartbeat = master.wait_heartbeat()

if heartbeat:
    print("Heartbeat received! Connection successful.")
    print(f"Current MAV System ID: {master.target_system}")
else:
    raise TimeoutError("Failed to receive heartbeat from Pixhawk. Connection unsuccessful.")


frequency = 10  # prints 2 times per second
interval = 1 / frequency  # calculate the time interval between prints


# Step 4: Retrieve attitude and GPS data from the Pixhawk
try:
    while True:
        # Step 5: Wait for a HEARTBEAT message
        heartbeat = master.recv_match(type='HEARTBEAT', blocking=True)

        if heartbeat:
            # Step 6: Wait for the ATTITUDE message
            att_msg = master.recv_match(type='ATTITUDE', blocking=True)
            attitude_data = ""
            if att_msg:
                attitude_data = (
                    f"Roll: {att_msg.roll:.4f} rad, "
                    f"Pitch: {att_msg.pitch:.4f} rad, "
                    f"Yaw: {att_msg.yaw:.4f} rad, "
                    f"Roll Speed: {att_msg.rollspeed:.4f} rad/s, "
                    f"Pitch Speed: {att_msg.pitchspeed:.4f} rad/s, "
                    f"Yaw Speed: {att_msg.yawspeed:.4f} rad/s"
                )
            
            # Step 7: Wait for the GPS_RAW_INT message
            gps_msg = master.recv_match(type='GPS_RAW_INT', blocking=True)
            gps_data = ""
            if gps_msg:
                gps_data = (
                    f"Latitude: {gps_msg.lat / 1e7:.6f}°, "
                    f"Longitude: {gps_msg.lon / 1e7:.6f}°, "
                    f"Altitude: {gps_msg.alt / 1e3:.2f} m, "
                    f"Satellites Visible: {gps_msg.satellites_visible}"
                )
            
            # Step 8: Wait for the SYS_STATUS message
            bat_msg = master.recv_match(type='SYS_STATUS', blocking=True)
            battery_data = ""
            if bat_msg:
                battery_data = (
                    f"Battery Voltage: {bat_msg.voltage_battery / 1e3:.2f} V, "
                    f"Current: {bat_msg.current_battery / 1e3:.2f} A, "
                    f"Remaining: {bat_msg.battery_remaining} %"
                )
            
            combined_data = f"Drone_No: {master.target_system}, {attitude_data}, {gps_data}, {battery_data}\n"
            print(combined_data)
            
            time.sleep(interval)
            
            
            # sock.sendall(combined_data.encode('utf-8'))

            # data = sock.recv(1024)
            # print(f"Received response from server: {data.decode('utf-8')}")
        
except KeyboardInterrupt:
    print("Process interrupted by user.")
