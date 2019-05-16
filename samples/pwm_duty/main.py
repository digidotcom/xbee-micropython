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

from machine import Pin, PWM
import time

# Pin D0 (AD0/DIO0)
START_BUTTON = "D0"
# Pin P0 (RSSI PWM/DIO10)
PWM_CHANNEL = "P0"

DUTY_CYCLE_MAX = 1023
DUTY_CYCLE_MIN = 0
DUTY_CYCLE_STEP = 25


print(" +----------------------------------------+")
print(" | XBee MicroPython PWM Duty Cycle Sample |")
print(" +----------------------------------------+\n")

current_duty_cycle = DUTY_CYCLE_MIN

# Set up the 'start button' object to check the input value. Configure the
# pin as input and enable the internal pull-up.
start_button = Pin(START_BUTTON, Pin.IN, Pin.PULL_UP)
# Instantiate the PWM object from the corresponding pin. Configure the
# initial duty cycle to the minimum value.
pwm_channel = PWM(PWM_CHANNEL, duty=current_duty_cycle)

while True:
    # Check if the start button is pressed. If so, start the duty cycle
    # sequence.
    if start_button.value() == 0:
        # Increase the duty cycle to the maximum value.
        while current_duty_cycle < DUTY_CYCLE_MAX:
            current_duty_cycle = current_duty_cycle + DUTY_CYCLE_STEP
            if current_duty_cycle > DUTY_CYCLE_MAX:
                current_duty_cycle = DUTY_CYCLE_MAX
            pwm_channel.duty(current_duty_cycle)
            time.sleep(0.1)

        # Keep at maximum 2 seconds.
        time.sleep(2)

        # Decrease the duty cycle to the minimum value.
        while current_duty_cycle > DUTY_CYCLE_MIN:
            current_duty_cycle = current_duty_cycle - DUTY_CYCLE_STEP
            if current_duty_cycle < DUTY_CYCLE_MIN:
                current_duty_cycle = DUTY_CYCLE_MIN
            pwm_channel.duty(current_duty_cycle)
            time.sleep(0.1)
    else:
        time.sleep(0.1)
