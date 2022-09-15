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

import socket
import uselect

echo_server = ('52.43.121.77', 9001)

conns = []

# Create the sockets
for i in range(2):
    print("Creating socket {}".format(i))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(echo_server)
    conns.append(s)

# Prime them with data
for i in range(2):
    conns[i].send("Data for socket {}".format(i))
    conns[i].send(str(i) * 2048)

# Wait for data from each connection, or timeout
while True:
    rlist, wlist, xlist = uselect.select(conns, [], [], 10)

    if len(rlist) == 0:
        # timed out
        break

    # Can read without blocking if in rlist
    for i in range(2):
        if conns[i] in rlist:
            data = conns[i].recv(1024)
            print("Data from connection {}: {}".format(i, data))
