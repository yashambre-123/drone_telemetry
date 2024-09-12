from pymavlink import mavutil
import socket

server_address = '192.168.1.53'
port = 12346

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Specify the MAV system ID of the drone you want to monitor
TARGET_SYSTEM_ID1 = 1  # Replace with the actual MAV system ID of the drone
TARGET_SYSTEM_ID9 = 9

# Step 1: Connect to the Pixhawk
master2 = mavutil.mavlink_connection('udp:127.0.0.1:14570')

# Step 2: Wait for a heartbeat from the Pixhawk to ensure the connection is alive
print("Waiting for heartbeat...")
heartbeat = master2.wait_heartbeat()  # Timeout in seconds

if heartbeat:
    print("Heartbeat received! Connection successful.")
    print(f"Current MAV System ID: {master2.target_system}")

else:
    raise TimeoutError("Failed to receive heartbeat from Pixhawk. Connection unsuccessful.")

# Step 3: Retrieve attitude and GPS data from the Pixhawk
try:
    # sock.connect((server_address, port))

    while True:
        # Step 4: Wait for a HEARTBEAT message to detect if it's from the target drone
        heartbeat = master2.recv_match(type='HEARTBEAT', blocking=True)
        if (heartbeat and (master2.target_system == TARGET_SYSTEM_ID1)):
            # Step 5: Wait for the ATTITUDE message
            att_msg = master2.recv_match(type='ATTITUDE', blocking=True)
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
            
            # Step 6: Wait for the GPS_RAW_INT message
            gps_msg = master2.recv_match(type='GPS_RAW_INT', blocking=True)
            gps_data = ""
            if gps_msg:
                gps_data = (
                    f"Latitude: {gps_msg.lat / 1e7:.6f}°, "
                    f"Longitude: {gps_msg.lon / 1e7:.6f}°, "
                    f"Altitude: {gps_msg.alt / 1e3:.2f} m, "
                    f"Satellites Visible: {gps_msg.satellites_visible}"
                )
            
            # Step 7: Wait for the SYS_STATUS message
            bat_msg = master2.recv_match(type='SYS_STATUS', blocking=True)
            battery_data = ""
            if bat_msg:
                battery_data = (
                    f"Battery Voltage: {bat_msg.voltage_battery / 1e3:.2f} V, "
                    f"Current: {bat_msg.current_battery / 1e3:.2f} A, "
                    f"Remaining: {bat_msg.battery_remaining} %"
                )
            
            combined_data = f"Drone_No: {master2.target_system}, {attitude_data}, {gps_data}, {battery_data}\n"
            print(combined_data)
            # sock.sendall(combined_data.encode('utf-8'))

            # data = sock.recv(1024)
            # print(f"Received response from server: {data.decode('utf-8')}")

        elif (heartbeat and (master2.target_system == TARGET_SYSTEM_ID9)):
            att_msg = master2.recv_match(type='ATTITUDE', blocking=True)
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
            
            # Step 6: Wait for the GPS_RAW_INT message
            gps_msg = master2.recv_match(type='GPS_RAW_INT', blocking=True)
            gps_data = ""
            if gps_msg:
                gps_data = (
                    f"Latitude: {gps_msg.lat / 1e7:.6f}°, "
                    f"Longitude: {gps_msg.lon / 1e7:.6f}°, "
                    f"Altitude: {gps_msg.alt / 1e3:.2f} m, "
                    f"Satellites Visible: {gps_msg.satellites_visible}"
                )
            
            # Step 7: Wait for the SYS_STATUS message
            bat_msg = master2.recv_match(type='SYS_STATUS', blocking=True)
            battery_data = ""
            if bat_msg:
                battery_data = (
                    f"Battery Voltage: {bat_msg.voltage_battery / 1e3:.2f} V, "
                    f"Current: {bat_msg.current_battery / 1e3:.2f} A, "
                    f"Remaining: {bat_msg.battery_remaining} %"
                )
            
            combined_data = f"Drone_No: {master2.target_system}, {attitude_data}, {gps_data}, {battery_data}\n"
            print(combined_data)
            # sock.sendall(combined_data.encode('utf-8'))

            # data = sock.recv(1024)
            # print(f"Received response from server: {data.decode('utf-8')}")
            # If it's not the target drone, skip the message

except KeyboardInterrupt:
    print("Process interrupted by user.")
