from pymavlink import mavutil
import socket
import sys
import time

server_address = '192.168.0.104' # Get the server address from the shell script
port = 12341

print("THIS IS MY SERVER ADDRESS: ", server_address)

# Set up the socket connection (commented as it's unused for now)
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

# Frequency settings for faster data rates (10Hz for attitude, GPS, battery, and speed)
FREQ_ATTITUDE_HZ = 10  # 10 times per second
FREQ_GPS_HZ = 10       # 10 times per second
FREQ_BATTERY_HZ = 10   # 10 times per second
FREQ_SPEED_HZ = 10     # 10 times per second

# Helper function to send message rate commands
def set_message_interval(msg_id, freq_hz):
    interval_us = int(1e6 / freq_hz)  # Convert Hz to microseconds
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
        0,  # Confirmation
        msg_id,  # Message ID
        interval_us,  # Interval in microseconds
        0, 0, 0, 0, 0  # Unused parameters
    )

# Step 4: Set the desired message rates
MSG_ID_ATTITUDE = mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE
MSG_ID_GPS = mavutil.mavlink.MAVLINK_MSG_ID_GPS_RAW_INT
MSG_ID_SYS_STATUS = mavutil.mavlink.MAVLINK_MSG_ID_SYS_STATUS
MSG_ID_VFR_HUD = mavutil.mavlink.MAVLINK_MSG_ID_VFR_HUD  # For speed data

# Set the message rates
set_message_interval(MSG_ID_ATTITUDE, FREQ_ATTITUDE_HZ)
set_message_interval(MSG_ID_GPS, FREQ_GPS_HZ)
set_message_interval(MSG_ID_SYS_STATUS, FREQ_BATTERY_HZ)
set_message_interval(MSG_ID_VFR_HUD, FREQ_SPEED_HZ)

# Step 5: Retrieve attitude, GPS, battery, and speed data at high rates
try:
    sock.connect((server_address, port))
    while True:
        attitude_data = ""
        gps_data = ""
        battery_data = ""
        speed_data = ""

        # Step 6: Retrieve ATTITUDE message
        att_msg = master.recv_match(type='ATTITUDE', blocking=True)
        if att_msg:
            attitude_data = (
                f"Roll: {att_msg.roll:.4f} rad, "
                f"Pitch: {att_msg.pitch:.4f} rad, "
                f"Yaw: {att_msg.yaw:.4f} rad, "
                f"Roll Speed: {att_msg.rollspeed:.4f} rad/s, "
                f"Pitch Speed: {att_msg.pitchspeed:.4f} rad/s, "
                f"Yaw Speed: {att_msg.yawspeed:.4f} rad/s"
            )

        # Step 7: Retrieve GPS_RAW_INT message
        gps_msg = master.recv_match(type='GPS_RAW_INT', blocking=True)  # non-blocking to keep things fast
        if gps_msg:
            gps_data = (
                f"Latitude: {gps_msg.lat / 1e7:.6f}°, "
                f"Longitude: {gps_msg.lon / 1e7:.6f}°, "
                f"Altitude: {gps_msg.alt / 1e3:.2f} m, "
                f"Satellites Visible: {gps_msg.satellites_visible}"
            )

        # Step 8: Retrieve SYS_STATUS message (Battery info)
        bat_msg = master.recv_match(type='SYS_STATUS', blocking=True)
        if bat_msg:
            battery_data = (
                f"Battery Voltage: {bat_msg.voltage_battery / 1e3:.2f} V, "
                f"Current: {bat_msg.current_battery / 1e3:.2f} A, "
                f"Remaining: {bat_msg.battery_remaining} %"
            )

        # Step 9: Retrieve VFR_HUD message (Speed info)
        speed_msg = master.recv_match(type='VFR_HUD', blocking=True)
        if speed_msg:
            speed_data = (
                f"Ground Speed: {speed_msg.groundspeed:.2f} m/s, "
                f"Air Speed: {speed_msg.airspeed:.2f} m/s, "
                f"Heading: {speed_msg.heading}°, "
                f"Throttle: {speed_msg.throttle} %"
            )

        # Combine and print the data
        combined_data = (
            f"Drone_No: {master.target_system}, {attitude_data}, {gps_data}, {battery_data}, {speed_data}\n"
        )
        print(combined_data)
        
        sock.sendall(combined_data.encode('utf-8'))

        data = sock.recv(1024)
        print(f"Received response from server: {data.decode('utf-8')}")

        # time.sleep(interval)  # Control the processing rate if needed

except KeyboardInterrupt:
    print("Process interrupted by user.")
