"""
Copyright (c) 2018, Digi International, Inc.
Sample code released under MIT License.

Instructions:

 - Ensure that the SSL certificate files are in the /flash/cert directory
   on the XBee Filesystem
    - "ssl_params" shows which ssl parameters are required, and gives
     examples for referencing the files
    - If needed, replace the file paths to match the certificates you're using
 - The policy attached to the SSL certificates must allow for
   connecting, and getting a Thing's Shadow
 - The host, region, and thing_name params need to be filled in to create a valid
   AWS endpoint to connect to
 - Send this code to your XBee module using paste mode (CTRL-E)

"""

import usocket, ussl, time, network

# AWS endpoint parameters
host = b'FILL_ME_IN'  # ex: b'abcdefg1234567'
region = b'FILL_ME_IN'  # ex: b'us-east-1'
thing_name = b'FILL_ME_IN'  #ex: b'IMEI_12345'

aws_endpoint = b'%s.iot.%s.amazonaws.com' % (host, region)
ssl_params = {'keyfile': "/flash/cert/aws.key",
              'certfile': "/flash/cert/aws.crt",
              'ca_certs': "/flash/cert/aws.ca"}  # ssl certs

conn = network.Cellular()
while not conn.isconnected():
    print("waiting for network connection...")
    time.sleep(4)
print("network connected")

def https_test(hostname=aws_endpoint, sslp=ssl_params):
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM, usocket.IPPROTO_SEC)
    s.setblocking(False)
    w = ussl.wrap_socket(s, **ssl_params)
    print("connecting...")
    w.connect((hostname, 8443))
    print("connected")
    print("sending request")
    w.write(b'GET /things/%s/shadow HTTP/1.0\r\nHost: %s\r\n\r\n' % (thing_name, hostname))
    print("waiting for data...")
    while True:
        data = w.read(1024)
        if data:
            print(str(data, 'utf-8'))
            break
    w.close()
    print("DONE")

https_test()
