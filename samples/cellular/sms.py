"""
Copyright (c) 2018, Digi International, Inc.
Sample code released under MIT License.

Demonstration code for using network.Cellular() class's sms_receive() method.

Instructions:
  - Upload/run this code on a module connected to the Internet using
    "paste mode".
  - You can use c.isconnected() to see if the Cellular Modem has established
    a connection.
  - Type wait_for_sms() in the REPL to wait for an SMS to arrive and then
    print it out.
"""

import network, time, xbee

c = network.Cellular()

def timestamp(t = None):
    return "%04u-%02u-%02uT%02u:%02u:%02u" % time.localtime(t)[0:6]

def check_sms():
    msg = c.sms_receive()
    if msg:
        print('SMS at %s from %s:\n%s' % (timestamp(msg['timestamp']),
              msg['sender'], msg['message']))
    return msg

def wait_for_sms():
    print('Waiting for SMS to', xbee.atcmd('PH'))
    while not check_sms():
        time.sleep_ms(100)

wait_for_sms()
