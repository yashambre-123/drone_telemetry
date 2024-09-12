from pymavlink import mavutil
import socket


server_address = '192.168.1.53'
port = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 1: Connect to the Pixhawk
master = mavutil.mavlink_connection('udp:127.0.0.1:14550')

# Step 2: Wait for a heartbeat from the Pixhawk to ensure the connection is alive
print("Waiting for heartbeat...")
heartbeat = master.wait_heartbeat()  # Timeout in seconds

if heartbeat:
    print("Heartbeat received! Connection successful.")
else:
    raise TimeoutError("Failed to receive heartbeat from Pixhawk. Connection unsuccessful.")

# Step 3: Retrieve attitude and GPS data from the Pixhawk
try:
    sock.connect((server_address, port))

    while True:
        # Step 4: Wait for the ATTITUDE message
        att_msg = master.recv_match(type='ATTITUDE', blocking=True)
        
        if att_msg:
            # Convert attitude data to a string format
            attitude_data = (
                f"Roll: {att_msg.roll:.4f} rad, "
                f"Pitch: {att_msg.pitch:.4f} rad, "
                f"Yaw: {att_msg.yaw:.4f} rad, "
                f"Roll Speed: {att_msg.rollspeed:.4f} rad/s, "
                f"Pitch Speed: {att_msg.pitchspeed:.4f} rad/s, "
                f"Yaw Speed: {att_msg.yawspeed:.4f} rad/s"
            )
            
            # Print the string representation of the attitude data
            # print(attitude_data)

        # print("\n")


        # Step 5: Wait for the GPS_RAW_INT message
        gps_msg = master.recv_match(type='GPS_RAW_INT', blocking=True)

        if gps_msg:
            # Convert GPS data to a string format
            gps_data = (
                f"Latitude: {gps_msg.lat / 1e7:.6f}°, "
                f"Longitude: {gps_msg.lon / 1e7:.6f}°, "
                f"Altitude: {gps_msg.alt / 1e3:.2f} m, "
                f"Satellites Visible: {gps_msg.satellites_visible}"
            )
            
            # Print the string representation of the GPS data
            # print(gps_data)
        
        # print("\n")

        bat_msg = master.recv_match(type='SYS_STATUS', blocking=True)

        if bat_msg:
            # Convert battery data to a string format
            battery_data = (
                f"Battery Voltage: {bat_msg.voltage_battery / 1e3:.2f} V, "
                f"Current: {bat_msg.current_battery / 1e3:.2f} A, "
                f"Remaining: {bat_msg.battery_remaining} %"
            )
        

        combined_data = f"{attitude_data}, {gps_data}, {battery_data}\n"

        print(combined_data)

        sock.sendall(combined_data.encode('utf-8'))

        data = sock.recv(1024)
        print(f"Received response from server: {data.decode('utf-8')}")


except KeyboardInterrupt:
    print("Process interrupted by user.")
