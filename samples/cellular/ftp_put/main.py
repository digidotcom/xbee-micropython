# Copyright (c) 2022, Digi International, Inc.
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
FTP_HOST = "place.holder.ip.address"
FTP_PORT = 21
FTP_USER = "placeholderUsername"
FTP_PASS = "placeholderPassword"

LOCAL_FILE = "2b.txt"

PATH_ROOT = "/flash"
PATH_REMOTE_UPLOAD = "upload"

print(" +----------------------------------------+")
print(" | XBee Micropython FTP PUT Client Sample |")
print(" +----------------------------------------+\n")

cellular = network.Cellular()

# Wait for cellular network connection.
print("- Waiting for the module to connect to the cellular network... ", end="")
while not cellular.isconnected():
    time.sleep(5)
print("[OK]")

# Connect to the FTP server.
print("- Connecting to FTP server... ", end="")
ftp_conn = uftp.FTP(host=FTP_HOST, port=FTP_PORT)
ftp_conn.login(user=FTP_USER, passwd=FTP_PASS)
print("[OK]")

# Upload a file to the upload folder on the FTP server
print("- Uploading file '%s'... " % LOCAL_FILE, end="")
ftp_conn.cwd(PATH_REMOTE_UPLOAD)
start = time.time()
ftp_conn.stor("%s/%s" % (PATH_ROOT, LOCAL_FILE), LOCAL_FILE)
print("[OK]")
print("   * Time taken: %d seconds" % (time.time() - start))

# Close the connection to the FTP server
print("- Closing FTP connection... ", end="")
ftp_conn.cwd("..")
ftp_conn.quit()
print("[OK]")

print("- Done")
