# This script tests getting a IP address for use in the API
import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Your hostname is " + hostname)
print("Your IP address is " + IPAddr)
