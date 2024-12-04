from machine import I2C
import sys
import time

# CONSTANTS
LIS3DSH_ADDR = 0x1D  # (Slave Address) // In case it is connected to a voltage supply it is 0x1D

# REGISTER ADDRESSES
OFF_X = 0x10
OFF_Y = 0x11
OFF_Z = 0x12

STATUS = 0x27
OUT_X_LSB = 0x28  # X low - Output register
OUT_X_MSB = 0x29  # X high - Output register
OUT_Y_LSB = 0x2A  # Y low - Output register
OUT_Y_MSB = 0x2B  # Y high - Output register
OUT_Z_LSB = 0x2C  # Z low - Output register
OUT_Z_MSB = 0x2D  # Z high - Output register

FIFO_CTRL = 0x2E
REG_TEMP = 0x0C
REG_WHO_AM_I = 0x0F
REG_INFO_1 = 0x0D
REG_INFO_2 = 0x0E
CTRL_REG_3 = 0x23
CTRL_REG_4 = 0x20
CTRL_REG_5 = 0x24
CTRL_REG_6 = 0x25

# SDA Pin 6      SCL Pin 4      SEL Pin 7


# Transforms a 2-bytes value into signed
def to_signed_2b(n):
    n = n & 0xFFFF
    return n | (-(n & 0x8000))


# Transforms a 1-byte value into signed
def to_signed_1b(n):
    n = n & 0xFF
    return n | (-(n & 0x80))


class LIS3DSH:
    # We initialize the process
    def __init__(self, i2c, LIS3DSH_ADDR):
        devices = i2c.scan()  # Scans several devices and makes a list of the ones who respond
        print(devices)

        # In case the slave address is not contained in the list, shows the error message
        if LIS3DSH_ADDR not in devices:
            print("Couldn't find the sensor")
            sys.exit(1)

        # Assign the variables to self
        self.i2c = i2c
        self.address = LIS3DSH_ADDR

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

    def accel_info(self):
        """
        Read-Only information registers (it shows if the sensor is working correctly)

        :return: boolean
        """
        data1 = self.read_from_reg(REG_INFO_1, 1)
        time.sleep_ms(100)
        data2 = self.read_from_reg(REG_INFO_2, 1)
        # print("info 1: ", data1, " info 2: ", data2)
        if (data1 == b'!') and (data2 == b'\x00'):
            return True
        else:
            return False

    def check_id(self):
        """
        Checks if the identity of the sensor is correct

        :return: boolean
        """
        data = self.read_from_reg(REG_WHO_AM_I, 1)
        # print("id: ", data)
        if data == b'?':
            return True
        else:
            return False

    def off_corr(self, axis_x=False, axis_y=False, axis_z=False):
        """
        Offset correction registers

        Makes an offset of each axis, depending if it is selected as true

        :param axis_x: Must be set to True to activate
        :param axis_y: Must be set to True to activate
        :param axis_z: Must be set to True to activate
        """
        reg_num = 0x00
        if axis_x:
            self.data_update(OFF_X, reg_num)
            time.sleep_ms(100)
        if axis_y:
            self.data_update(OFF_Y, reg_num)
            time.sleep_ms(100)
        if axis_z:
            self.data_update(OFF_Z, reg_num)

    def accel_setting(self):
        """
        Sets the basic configuration in the control registers
        """
        # Enables all the axis and sets a frecuency of 400 Hz
        self.data_update(CTRL_REG_4, 0x77)
        time.sleep_ms(100)

        # DRDY signal enable to INT1,  INT1/DRDY signal enabled  and  interrupt signals active HIGH
        self.data_update(CTRL_REG_3, 0xC8)

    def fifo_disable(self):
        """
        Bypass mode (FIFO turned off)
        """
        self.data_update(FIFO_CTRL, 0x00)

    #
    def fifo_enable(self):
        """
        Enables FIFO and activates stream mode (if FIFO full, new samples overwrites older ones)
        """
        # FIFO enable
        self.data_update(CTRL_REG_6, 0x40)

        # Stream mode
        self.data_update(FIFO_CTRL, 0xE0)

    def read_x_axis(self):
        """
        Reads the x axis

        :return: signed value
        """
        data1 = self.read_from_reg(OUT_X_LSB, 1)[0]
        data2 = self.read_from_reg(OUT_X_MSB, 1)[0]

        data = to_signed_2b(data2 << 8 | data1)
        return data

    def read_y_axis(self):
        """
        Reads the y axis

        :return: signed value
        """
        data1 = self.read_from_reg(OUT_Y_LSB, 1)[0]
        data2 = self.read_from_reg(OUT_Y_MSB, 1)[0]

        data = to_signed_2b(data2 << 8 | data1)
        return data

    def read_z_axis(self):
        """
        Reads the z axis

        :return: signed value
        """
        data1 = self.read_from_reg(OUT_Z_LSB, 1)[0]
        data2 = self.read_from_reg(OUT_Z_MSB, 1)[0]

        data = to_signed_2b(data2 << 8 | data1)
        return data

    def read_temp(self):
        """
        Reads the temperature

        :return: signed value
        """
        data = self.read_from_reg(REG_TEMP, 1)
        data = to_signed_1b(int.from_bytes(data, "big"))

        return data

    def accel_status(self):
        """
        Checks the status of the axis (which are enabled and receiving data)

        Recommended: If 255 then is **everything enabled**
        """
        data = self.read_from_reg(STATUS, 1)
        data = int.from_bytes(data, "big")
        return data

    def update_status(self):
        """
        Updates the status of the axis
        """
        self.data_update(STATUS, 0xFF)
