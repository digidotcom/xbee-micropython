# Copyright (c) 2019, Digi International, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import network
import time
import uftp

# Constants
FTP_HOST = "speedtest.tele2.net"
FTP_USER = "anonymous"
FTP_PASS = "anonymous@"

REMOTE_FILE = "1KB.zip"
LOCAL_FILE = "2b.txt"

PATH_ROOT = "/flash"
PATH_REMOTE_UPLOAD = "upload"


print(" +------------------------------------+")
print(" | XBee MicroPython FTP Client Sample |")
print(" +------------------------------------+\n")

cellular = network.Cellular()

print("- Waiting for the module to be connected to the cellular network... ",
      end="")
while not cellular.isconnected():
    time.sleep(5)
print("[OK]")

# Connect to the FTP server.
print("- Connecting to FTP server... ", end="")
ftp_conn = uftp.FTP(host=FTP_HOST)
ftp_conn.login(user=FTP_USER, passwd=FTP_PASS)
print("[OK]")

# Download a file from the FTP.
print("- Retrieving file '%s' (%d bytes)... " % (REMOTE_FILE,
                                                 ftp_conn.size(REMOTE_FILE)),
      end="")
start = time.time()
with open("%s/%s" % (PATH_ROOT, REMOTE_FILE), "w") as local_file:
    ftp_conn.retr(REMOTE_FILE, callback=local_file.write)
print("[OK]")
print("   * Time taken: %d seconds" % (time.time() - start))

# Upload a file to the 'update' folder of the FTP.
print("- Uploading file '%s'... " % LOCAL_FILE, end="")
ftp_conn.cwd(PATH_REMOTE_UPLOAD)
start = time.time()
ftp_conn.stor("%s/%s" % (PATH_ROOT, LOCAL_FILE), LOCAL_FILE)
print("[OK]")
print("   * Time taken: %d seconds" % (time.time() - start))

# Close connection.
print("- Closing FTP connection... ", end="")
ftp_conn.cwd("..")
ftp_conn.quit()
print("[OK]")

print("- Done")
