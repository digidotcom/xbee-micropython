import network
import time

print(" +------------------------------------+")
print(" | XBee MicroPython Tower Scan Sample |")
print(" +------------------------------------+\n")

cellular = network.Cellular()

print("Waiting for the module to be connected to the cellular network...")

# Wait until the module is connected to the cellular network.
while not cellular.isconnected():
    time.sleep(1)

print("Gathering cell information:")
# This is a blocking call that will return a list containing tower information
towers = cellular.scan()

for tower in towers:
    print(tower)
print("")

# Define a callback function that will be called with the list of tower information
scan_complete = False
def scan_callback(towers):
    global scan_complete
    for tower in towers:
        print(tower)
    scan_complete = True


print("Gathering cell information via callback:")
# When a callback function is provided, scan() is a non-blocking call
cellular.scan(callback=scan_callback)

while not scan_complete:
    # Other tasks can be completed while the scan runs in the background
    time.sleep(1)
