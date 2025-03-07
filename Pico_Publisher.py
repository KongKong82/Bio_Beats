import network
import socket
import time
import random
import math

# ---------------------------
# Step 1: Set up AP Mode
# ---------------------------

# Create and activate the AP interface
ap = network.WLAN(network.AP_IF)
ap.active(True)

# Set SSID and password
ssid = "PicoDataAP"
password = "YourStrongPassword"
# Configure AP without explicitly specifying auth mode (defaults to WPA2-PSK if password length >= 8)
ap.config(essid=ssid, password=password)

# Optionally, set a static IP configuration:
# Format: ('IP address', 'netmask', 'gateway', 'DNS server')
ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))

# Wait until AP is active
while not ap.active():
    pass

print("Access Point active")
print("AP Configuration:", ap.ifconfig())

# ---------------------------
# Step 2: Create TCP Server
# ---------------------------

# Set up a TCP server on port 1234
addr = socket.getaddrinfo("0.0.0.0", 1234)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
print("TCP server listening on", addr)

while True:
    cl, client_addr = s.accept()
    print("Client connected from", client_addr)
    try:
        while True:
            # Replace the following with your sensor data reading code:
            sensor_data = int(random.randint(0,2) + (20*math.sin(time.ticks_ms()))*math.exp(-6*time.ticks_ms))
            time_data = int(time.time())
            message = f"{sensor_data}, {time_data}\n"
            cl.send(message.encode())
            # Adjust delay for your sampling rate requirements:
            time.sleep(0.1)
    except Exception as e:
        print("Connection error:", e)
    finally:
        cl.close()
        print("Client disconnected")
