"""
Copyright (c) 2018, Digi International, Inc.
Sample code released under MIT License.

Test code for CloudFlare's https://auth.pizza page.  For details, see:
    https://blog.cloudflare.com/introducing-tls-client-auth/

Demonstrates use of ussl.wrap_socket() with ca_certs (to only connect
to servers with certificates signed by a single CA) and certfile/keyfile
as the client certificate to authenticate with the server.
    
Instructions:
  - Upload the "pizza" files from ./cert/ to the cert/ directory on your
    XBee Cellular.
  - Upload/run this code on a module connected to the Internet using
    "paste mode".
  - Note that for debugging purposes you can run this script on your
    computer with Python 3 to verify that the certificates are valid.
"""

import sys
if sys.platform == 'xbee-cellular':
    import usocket, ussl
    proto = usocket.IPPROTO_SEC
else:
    import socket as usocket
    import ssl as ussl
    proto = usocket.IPPROTO_TCP

s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM, proto)
w = ussl.wrap_socket(s,
    keyfile='cert/pizza-client.key',
    certfile='cert/pizza-client.pem',
    ca_certs='cert/pizza-ca.pem')
w.connect(('auth.pizza', 443))
w.write(b'GET / HTTP/1.0\r\nHost: auth.pizza\r\nAccept: application/json\r\n\r\n')
print(str(w.read(4096), 'utf-8'))
w.close()
