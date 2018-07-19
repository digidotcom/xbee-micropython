"""
Copyright (c) 2018, Digi International, Inc.
Sample code released under MIT License.

Demonstration code for reporting on changes to ATAI until cellular modem is
online.  Useful for troubleshooting connectivity issues.

Instructions:
  - Upload/run this code on a module connected to the Internet using
    "paste mode".
  - After uploading once, you can just type watch_ai() to re-run the code.
"""

import time, xbee


ai_desc = {
    0x00: 'CONNECTED',
    0x22: 'REGISTERING_TO_NETWORK',
    0x23: 'CONNECTING_TO_INTERNET',
    0x24: 'RECOVERY_NEEDED',
    0x25: 'NETWORK_REG_FAILURE',
    0x2A: 'AIRPLANE_MODE',
    0x2B: 'USB_DIRECT',
    0x2C: 'PSM_DORMANT',
    0x2F: 'BYPASS_MODE_ACTIVE',
    0xFF: 'MODEM_INITIALIZING',
}


def watch_ai():
    old_ai = -1
    while old_ai != 0x00:
        new_ai = xbee.atcmd('AI')
        if new_ai != old_ai:
            print("ATAI=0x%02X (%s)" % (new_ai, ai_desc.get(new_ai, 'UNKNOWN')))
            old_ai = new_ai
        else:
            time.sleep(0.01)


watch_ai()
