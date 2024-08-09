import socket
import logging

def port_available(port: int):
    status = False
    host = "localhost"

    # Creates a new socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to connect to the given host and port
    if sock.connect_ex((host, port)) == 0:
        logging.info("Port " + str(port) + " is open") # A server is running with this port
    else:
        logging.info("Port " + str(port) + " is closed") # Nothing uses this port
        status = True

    # Close the connection
    sock.close()
    return status
