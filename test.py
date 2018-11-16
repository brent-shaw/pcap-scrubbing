import sys
import time
import dpkt
import socket
import datetime
from scrubbable import Scrubbable
from dpkt.compat import compat_ord

def mac_addr(address):
    """Convert a MAC address to a readable/printable string
       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % compat_ord(b) for b in address)

def inet_to_str(inet):
    """Convert inet object to a string
        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)

def show_flow(data):
    eth = dpkt.ethernet.Ethernet(data)

    if not isinstance(eth.data, dpkt.ip.IP):
        pass
    else:
        #ip data
        ip = eth.data
        sourceip = inet_to_str(ip.src)
        destip = inet_to_str(ip.dst)

        print(str(sourceip) + " -> " + str(destip))

subrubbablePCAP = Scrubbable()

with open("test.pcap", 'rb') as f:
    pcap = dpkt.pcap.Reader(f)
    for timestamp, buffer in pcap:
        subrubbablePCAP.append(timestamp, buffer)

print("Scrubber loaded!")

timestamps = list(subrubbablePCAP.timestamps.keys())

# Start at beginning
for i in range(10):
    show_flow(subrubbablePCAP.read().data)

print("---")

# Go back again
for i in range(10):
    show_flow(subrubbablePCAP.readback().data)

# With timestamp
timestamps = list(subrubbablePCAP.timestamps.keys())
aTimestamp = timestamps[1] # get timesamp of 2nd packet
currentData = subrubbablePCAP.get(aTimestamp)
show_flow(currentData)

print("---")

print(str(len(timestamps)))

print("")
x = input("Press 'Enter' to quit")