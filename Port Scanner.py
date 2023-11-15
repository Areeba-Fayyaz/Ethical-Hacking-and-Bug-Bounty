import socket
from datetime import datetime

# Prompting the user to enter the target IP address or hostname
target = input("Enter the target IP address or hostname: ")

# Define the port scanning function
def port_scan(target):
    try:
        # Resolving the hostname to an IP address
        ip = socket.gethostbyname(target)

        # Printing header for the scan results
        print("-" * 50)
        print("Scanning target:", ip)
        print("Time started:", datetime.now())
        print("-" * 50)

        # Scanning ports in the range 1 to 65535
        for port in range(1, 90):
            # Creating a new socket for each port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Setting a timeout for the connection attempt

            # Connecting to the port, checking if it is open
            result = sock.connect_ex((ip, port))
            if result == 0:
                print("Port {}: Open".format(port))  # Port is open
            sock.close()  # Closing the socket

    except socket.gaierror:
        print("Hostname could not be resolved.")  # Hostname resolution failed
    except socket.error:
        print("Could not connect to the server.")  # Connection to server failed

# Calling the port scan function with the user input
port_scan(target)
