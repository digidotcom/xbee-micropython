from umachine import ADC, Pin
import time

# PINS
ADC_PIN_ID = "D2"
DIO_PIN_INT = "D4"

# CONSTANTS
THRESHOLD = 50

# 12 bits --> 4096 values
adc_pin = ADC(ADC_PIN_ID)
int_pin_in = Pin(DIO_PIN_INT, Pin.IN)
int_pin_out = Pin(DIO_PIN_INT, Pin.OUT)


class noiseClick:

    def __init__(self, THRESHOLD):
        self.THRESHOLD = THRESHOLD
        int_pin_in.value(0)

    def noise_command_value(self):
        """
        Sets the **interruption value** to 1 if the noise level is above the threshold, otherwise is set to 0
        """
        if self.noise_read() > self.THRESHOLD:
            int_pin_in.value(1)

        else:
            int_pin_in.value(0)

    def check_int_pin(self):
        """
        Returns the value of the interruption pin

        :return: returns the value of the interruption pin
        """
        return int_pin_out.value()

    def noise_read(self):
        """
        Returns the value of the noise level

        :return: returns the value of the noise level
        """
        return adc_pin.read()

    def set_threshold(self, value):
        """
        Sets a new threshold
        """
        self.THRESHOLD = value

