import socket
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def data_gen(sock):
    """
    Continuously receive data from the socket, buffer it, and yield (time, sensor) tuples.
    Each message is expected to be in the format: "<sensor_data>, <time_data>\n"
    """
    buffer = ""
    while True:
        try:
            # Receive data from the socket
            chunk = sock.recv(1024)
            if not chunk:
                # No data received, wait a little and try again
                time.sleep(0.1)
                continue

            # Append received data to the buffer (decode from bytes)
            buffer += chunk.decode('utf-8')

            # Process complete lines (terminated by newline)
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line.strip():
                    continue  # Skip empty lines
                parts = line.split(",")
                if len(parts) < 2:
                    print("Not enough values in line, skipping:", line)
                    continue
                try:
                    # Parse sensor and time values
                    sensor_data = float(parts[0].strip())
                    time_data = int(parts[1].strip())
                    yield time_data, sensor_data
                except Exception as conv_err:
                    print("Conversion error:", conv_err, "in line:", line)
                    continue
        except Exception as e:
            print("Error receiving data:", e)
            time.sleep(0.1)
            continue

def main():
    HOST = "192.168.4.1"  # Pico's access point IP address
    PORT = 1234
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    
    # Set up the plot
    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'b-', label='Sensor Data')
    ax.set_xlabel('Time')
    ax.set_ylabel('Sensor Data')
    ax.set_title('Live Sensor Data')
    ax.legend()
    ax.grid(True)
    
    # Data containers for plotting
    xdata, ydata = [], []
    
    def update(data):
        """Update the plot with new data."""
        t, s = data
        xdata.append(t)
        ydata.append(s)
        line.set_data(xdata, ydata)
        ax.relim()             # Recalculate axis limits
        ax.autoscale_view()    # Adjust the view to include new data
        return line,
    
    # Create the animation.
    ani = animation.FuncAnimation(
        fig,
        update,
        frames=data_gen(sock),
        interval=100,
        blit=True,
        cache_frame_data=False,
        save_count=50
    )
    
    plt.show()

if __name__ == "__main__":
    main()
