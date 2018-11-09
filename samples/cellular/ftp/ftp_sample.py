"""
Copyright (c) 2018, Digi International, Inc.
Sample code released under MIT License.

Instructions:

 - Ensure that the uftp.py module is in the /flash/lib directory
    and the 2b.txt file is in the /flash directory on the XBee module's filesystem
 - Send this code to your XBee module using paste mode (CTRL-E)

"""

import uftp, time, network

conn = network.Cellular()
while not conn.isconnected():
    print("waiting for network connection...")
    time.sleep(4)
print("network connected")

print("Connecting to FTP server...")
f = uftp.FTP(host="speedtest.tele2.net")
f.login(user="anonymous", passwd="anonymous@")

time.sleep(5)

print("Retrieving 1KB.zip...")
start = time.time()
print("File size: %d bytes" % f.size("1KB.zip"))
with open("/flash/1KB.zip", "w") as localfile:
    f.retr("1KB.zip", callback=localfile.write)
print("Time Taken: %d sec" % (time.time() - start))

time.sleep(5)

print("Uploading 2b.txt...")
start = time.time()
f.cwd("upload")
f.stor("/flash/2b.txt", "hamlet.txt")
print("Time Taken: %d sec" % (time.time() - start))

time.sleep(5)

print("Closing FTP connection...")
f.cwd("..")
f.quit()

print("Done")
