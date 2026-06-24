from machine import I2C
import sys
import time

# CONSTANTS
I3G4250D_ADDR = 0X68

# REGISTER ADDRESSES

REG_WHO_AM_I = 0x0F
CTRL_REG_1 = 0x20
CTRL_REG_2 = 0x21
CTRL_REG_3 = 0x22
CTRL_REG_4 = 0x23
CTRL_REG_5 = 0x24
REG_TEMP = 0x26
STATUS = 0X27
FIFO_CTRL_REG = 0x2E

OUT_X_LSB = 0x28  # X low - Output register
OUT_X_MSB = 0x29  # X high - Output register
OUT_Y_LSB = 0x2A  # Y low - Output register
OUT_Y_MSB = 0x2B  # Y high - Output register
OUT_Z_LSB = 0x2C  # Z low - Output register
OUT_Z_MSB = 0x2D  # Z high - Output register


# Measurement range set by user (by default measurement range is 2000 dps)
def gyro_meas_range(meas_range=2000):
    if meas_range == 245:
        scale_const = 8.75
    elif meas_range == 500:
        scale_const = 17.5
    else:
        scale_const = 70.0

    return scale_const


# Transform to degrees per second based on measurement range setting
def transform_meas(data1, data2, meas_range):
    data = to_signed_2b(data2 << 8 | data1)

    scale_const = gyro_meas_range(meas_range)
    return data * scale_const / 1000.0


# Transforms a 2-bytes value into signed
def to_signed_2b(n):
    n = n & 0xFFFF
    return n | (-(n & 0x8000))


# Transforms a 1-byte value into signed
def to_signed_1b(n):
    n = n & 0xFF
    return n | (-(n & 0x80))


class I3G4250D:
    # We initialize the process
    def __init__(self, i2c, I3G4250D_ADDR):
        devices = i2c.scan()  # Scans several devices and makes a list of the ones who respond
        print(devices)

        # In case the slave address is not contained in the list, shows the error message
        if I3G4250D_ADDR not in devices:
            print("Couldn't find the sensor")
            sys.exit(1)

        # Assign the variables to self
        self.i2c = i2c
        self.address = I3G4250D_ADDR

    # ---------------------------------------------------------- #
    #                      Helping methods                       #
    # ---------------------------------------------------------- #

    def read_from_reg(self, register, n_bytes):
        time.sleep_ms(100)
        self.i2c.writeto(self.address, bytearray([register]))
        time.sleep_ms(100)
        data = self.i2c.readfrom(self.address, n_bytes)
        return data

    def data_update(self, register, n_hex):
        time.sleep_ms(100)
        data = bytearray(2)
        data[0] = register
        data[1] = n_hex
        self.i2c.writeto(self.address, data)
        time.sleep_ms(100)

    # -----------------------------------------------------------#

    def who_am_i(self):
        """
        Checks if the identity of the sensor is correct

        :return: boolean
        """
        data = self.read_from_reg(REG_WHO_AM_I, 1)
        data = int.from_bytes(data, "big")
        print(data)
        if data == 0xD3:
            return True
        else:
            return False

    def gyro_setting(self):
        """
        Sets the basic configuration in the control registers
        """
        # Enables all the axis and sets a frequency of 200 Hz with a cutoff of 12.5
        self.data_update(CTRL_REG_1, 0x4F)
        time.sleep_ms(100)

        # Filter mode and filter cutoff freq configuration
        self.data_update(CTRL_REG_2, 0x39)
        time.sleep_ms(100)

        # Interrupt configuration
        self.data_update(CTRL_REG_3, 0xA8)
        time.sleep_ms(100)

        # Scale selection
        self.data_update(CTRL_REG_4, 0x30)
        time.sleep_ms(100)

        # High pass filter enable and out selection config
        self.data_update(CTRL_REG_5, 0x1F)
        time.sleep_ms(100)

        # Set bypass mode
        self.data_update(FIFO_CTRL_REG, 0x00)
        time.sleep_ms(100)

    def read_x(self, meas_range):
        """
        Reads the x axis and applies a sensitivity factor

        :param meas_range: measurement range (user selectable) -245-500-2000-
        """
        data1 = self.read_from_reg(OUT_X_LSB, 1)[0]
        data2 = self.read_from_reg(OUT_X_MSB, 1)[0]

        return transform_meas(data1, data2, meas_range)

    def read_y(self, meas_range):
        """
        Reads the y axis and applies a sensitivity factor

        :param meas_range: measurement range (user selectable) -245-500-2000-
        """
        data1 = self.read_from_reg(OUT_Y_LSB, 1)[0]
        data2 = self.read_from_reg(OUT_Y_MSB, 1)[0]

        return transform_meas(data1, data2, meas_range)

    def read_z(self, meas_range):
        """
        Reads the z axis and applies a sensitivity factor

        :param meas_range: measurement range (user selectable) -245-500-2000-
        """
        data1 = self.read_from_reg(OUT_Z_LSB, 1)[0]
        data2 = self.read_from_reg(OUT_Z_MSB, 1)[0]

        return transform_meas(data1, data2, meas_range)

    def read_temp(self):
        """
        Reads the temperature
        """
        data = self.read_from_reg(REG_TEMP, 1)
        data = to_signed_1b(int.from_bytes(data, "big"))

        return data

    def gyro_status(self):
        """
        Checks the status of the axis (which are enabled and receiving data)

        Recommended: If 255 then is **everything enabled**
        """
        data = self.read_from_reg(STATUS, 1)
        data = int.from_bytes(data, "big")

        return data
