
'''
 Copyright 2023, Digi International Inc.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, you can obtain one at http://mozilla.org/MPL/2.0/.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES 
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF 
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR 
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES 
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN 
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF 
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''


DEFAULT_ADDRESS = 0x70  # default i2c address for shtc3 sensor
WAKEUP = [0x35, 0x17]
SLEEP = [0xB098]  # put device to sleep
GET_ID = [0xEFC8]  # get ID from register
SOFTRESET = [0x805D]  # Soft Reset


TEMP_STRETCH = [0x7C, 0xA2]  # temperature first, with clock stretch
TEMP_STRETCH_LOWPOWER = [0x64, 0x58]  # temperature first, with clock stretch and low power
HUMID_STRETCH = [0x5C, 0x24] # humidity first, with clock stretch
HUMID_STRETCH_LOWPOW = [0x44, 0xDE]  # humidity first, with clock stretch and low power
TEMP = [0x78, 0x66]  # temperature first
TEMP_LOWPOW = [0x60, 0x9C]  # temperature first, with low power
HUMID = [0x58, 0xE0]  # humidity first
HUMID_LOWPOW = [0x40, 0x1A]  # humidity first, with low power

class SHTC3():

  def __init__(self, i2c, addr=0x70):
    self.i2c = i2c
    self.addr=addr
    self.set_sleep(False)
    self.set_low_power(False)

  def get_data(self):
    if self.low_power:
      buff=bytearray(TEMP_STRETCH_LOWPOWER)
    else:
      buff=bytearray(TEMP_STRETCH)
    self.i2c.writeto(self.addr, buff)
    buff2=bytearray(bytes(6))
    self.i2c.readfrom_into(self.addr, buff2)
    temp = (buff2[1] | (buff2[0] << 8)) * 175 / 65536.0 - 45.0
    humid = (buff2[4] | (buff2[3] << 8)) * 100 / 65536.0
    return (temp, humid)
  
  def get_temp(self):
    return (self.get_data()[0])
  
  def get_humid(self):
    return (self.get_data()[1])
  
  def set_low_power(self, low_power):
    self.low_power = low_power
  
  def get_low_power(self):
    return self.low_power
  
  def set_sleep(self, sleep):
    if sleep:
      buff=bytearray(WAKEUP)
    else:
      buff=bytearray(SLEEP)
    self.i2c.writeto(self.addr,buff)
    self.sleep = sleep
    return self.sleep
  
  def get_sleep(self):
    return self.sleep

  def reset(self):
    buff=bytearray(SOFTRESET)
    self.i2c.writeto(self.addr, buff)