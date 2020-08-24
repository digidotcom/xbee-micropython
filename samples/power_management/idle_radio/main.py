# Copyright (c) 2020, Digi International, Inc.
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
import time
import xbee


def read_sensor():
    """This example uses ATTP to read the internal temperature sensor."""
    return xbee.atcmd("TP")


def handle_rx_packet(rx):
    """Print out any received packets."""
    print("Received:", rx["payload"])


def main():
    module = xbee.XBee()

    # Idle the radio. While the radio is idled, the radio cannot receive
    # transmissions and current draw is reduced.
    xbee.idle_radio(True)

    # register handle_rx_packet to be called whenever a packet is received.
    xbee.receive_callback(handle_rx_packet)

    # Send transmissions to the address configured by DH/DL
    dest_addr = xbee.atcmd("DH") + xbee.atcmd("DL")

    samples = []
    # Since this application spends most of its time asleep, stopping
    # the application through the UART can be difficult. To make the
    # example easier to work with, it will only run for about a minute
    # instead of indefinitely.
    for _ in range(12):
        # Sleep for 5 seconds
        module.sleep_now(5000)

        # Upon waking, take a sample
        sample = read_sensor()
        samples.append(sample)
        print("  Sample: {}".format(sample))

        if len(samples) == 4:
            # Once we have four samples, Send the samples to
            # the coordinator. Note that we don't have to call
            # xbee.idle_radio(True) to be able to do this--the radio is
            # enabled just long enough to send the transmission.
            print("Transmit samples: {}".format(samples))
            xbee.transmit(dest_addr, str(samples))

            # Clear the stored samples
            samples.clear()

            # If the server is ever going to send transmissions to the
            # end device, the end device needs to enable the radio at
            # some point, and the server needs to know when that is. For
            # this example, that is achieved by leaving the radio on for
            # 1 second after transmitting a sample. If this end device
            # never needs to receive transmissions, this can be left
            # out.
            print("Enable the radio for a bit to receive transmissions...")
            xbee.idle_radio(False)
            # Wait 1 second with the radio enabled. This is the only
            # time the radio can receive transmissions.
            time.sleep(1)
            print("Disable the radio again")
            xbee.idle_radio(True)

    print("Example complete, re-enabling radio")
    xbee.idle_radio(False)


main()
