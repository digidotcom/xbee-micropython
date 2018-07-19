"""
Copyright (c) 2018, Digi International, Inc.
Sample code released under MIT License.

Test code for CloudFlare's https://auth.pizza page.  For details, see:
    https://blog.cloudflare.com/introducing-tls-client-auth/

This is a version of the auth_pizza.py sample that uses urequests to handle
the HTTP client work.  Demonstrates use of requests parameters "verify" (to
only connect to servers with certificates signed by a given CA) and
"cert" as the client certificate to authenticate with the server.

Note that unlike the full Python Requests module, urequests.py only supports
a tuple of (cert, key) for the "cert" parameter.
    
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
    import urequests
else:
    import requests as urequests

r = urequests.get('https://auth.pizza',
                  headers={'Accept': 'application/json'},
                  verify='cert/pizza-ca.pem',
                  cert=('cert/pizza-client.pem', 'cert/pizza-client.key'))
print(r.text)
