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

import struct

TYPE_UID = 0x00
TYPE_URL = 0x10
TYPE_TLM = 0x20

_DEFAULT_FRAME = (
    b"\x02"      # Flags length
    b"\x01"      # Flags data type value
    b"\x06"      # Flags data
    b"\x03"      # Service UUID length
    b"\x03"      # Service UUID data type value
    b"\xAA\xFE"  # 16-bit Eddystone UUID
    b"\x04"      # Service Data length
    b"\x16"      # Service Data data type value
    b"\xAA\xFE"  # 16-bit Eddystone UUID
)

_LENGTH_INDEX = 7


def _check_for_valid_eddystone(frame, expected_len=None):
    frame_len = len(frame)

    # Verify the length of the advertisement payload.
    # The advertisement contains many length bytes, make sure those lengths add up to the total frame length.
    parse_len = 0
    while True:
        # The length of the field plus the byte for the length of the field
        parse_len += frame[parse_len] + 1

        # The seventh byte is always the eddystone length. Make sure is matches the expected length if specified.
        if expected_len is not None and parse_len == _LENGTH_INDEX and frame[parse_len] != expected_len:
            return False

        # Invalid length bytes in payload
        if parse_len > frame_len:
            return False
        elif parse_len == frame_len:
            # If All is well with this advertisement, continue.
            break

    # All Eddystone advertisements have the same first 12 bytes (excluding the payload length byte)
    if frame[:_LENGTH_INDEX] != _DEFAULT_FRAME[:_LENGTH_INDEX] or frame[8:11] != _DEFAULT_FRAME[8:11]:
        return False

    return True


class _EddystoneGenericFrame(object):
    """
    This class is a generic Advertising frame providing common functions, not to be instantiated.
    """

    def __init__(self, eddystone_type, payload_len):
        self._frame = bytearray()
        self._frame.extend(_DEFAULT_FRAME)
        self._frame.append(eddystone_type)  # Eddystone type
        # Extends the frame to have payload_len number of zero bytes at the end
        self._frame += bytearray(payload_len)
        self._set_payload_length(payload_len)

    def _set_payload_length(self, length):
        self._frame[_LENGTH_INDEX] = 4 + length  # 7th byte specifies the payload len. There are 4 bytes that are used in all frames

    def set_raw_payload(self, payload):
        payload_len = len(payload)
        if payload_len > 19:
            raise TypeError("The payload is too large")

        # Cut off the existing payload (beyond the default frame)
        offset = len(_DEFAULT_FRAME)
        self._frame = self._frame[:offset + 1]
        # Place the new payload at the end
        self._frame.extend(payload)
        self._set_payload_length(payload_len)

    def get_bytes(self) -> bytes:
        """
        Get the advertisement payload. Used to send this frame.
        """
        return bytes(self._frame)

    def _validate_payload(self, expected_len=None):
        return _check_for_valid_eddystone(self._frame, expected_len)

    def validate_payload(self):
        return self._validate_payload(None)

    @property
    def eddystone_type(self):
        if len(self._frame) >= 13 and self._frame[11] in [TYPE_UID, TYPE_URL, TYPE_TLM]:
            return self._frame[11]
        else:
            return None


class EddystoneURLFrame(_EddystoneGenericFrame):
    """
    Eddystone-URL frame broadcasts ranging data and a URL using a compressed encoding format.
    See https://github.com/google/eddystone/tree/master/eddystone-url for format details.
    """
    # The ordering of the elements in both of the following list are significant for encoding them.
    _EXTENSIONS = [
        ".com/", ".org/", ".edu/", ".net/", ".info/", ".biz/", ".gov/",
        ".com", ".org", ".edu", ".net", ".info", ".biz", ".gov",
    ]

    _SCHEMES = [
        "http://www.",
        "https://www.",
        "http://",
        "https://",
    ]

    def __init__(self, ranging_data, url):
        super().__init__(eddystone_type=TYPE_URL, payload_len=3)
        self.ranging_data = ranging_data
        self.url = url

    @property
    def ranging_data(self) -> int:
        """
        Get or set the ranging data, specified in decibel-milliwatts (dBm). Defined as the calibrated Tx power at 0 m.
        """
        return struct.unpack('>b', self._frame[12:13])[0]

    @ranging_data.setter
    def ranging_data(self, ranging_data: int):
        if ranging_data < -100 or ranging_data > 20:
            raise ValueError("ranging_data is out of range")

        tx_power_byte = struct.pack('>b', ranging_data)
        self._frame = self._frame[:12] + tx_power_byte + self._frame[13:]

    def __find_scheme_id(self, input_url):
        for i in range(len(self._SCHEMES)):
            if input_url.startswith(self._SCHEMES[i]):
                return i, len(self._SCHEMES[i])
        else:
            raise ValueError("The URL does not use a supported prefix scheme")

    def __find_extension_id(self, input_url, pos):
        # Check if this matches a supported extension
        for ext_id in range(len(self._EXTENSIONS)):
            extension = self._EXTENSIONS[ext_id]
            if input_url.startswith(extension, pos):
                return ext_id
        return None

    @property
    def url(self) -> str:
        """
        Get or set the URL. Encoded internally as defined by RFC 1738.
        """
        url = self._frame[13:]
        if len(url) == 0:
            return str()

        if url[0] >= len(self._SCHEMES):
            raise ValueError("Invalid URL scheme")

        decoded_url = self._SCHEMES[url[0]]
        extension_index_max = len(self._EXTENSIONS) - 1
        for c in url[1:]:
            if c <= extension_index_max:  # If this is one of the extensions
                decoded_url += self._EXTENSIONS[c]
            elif 0x21 <= c < 0x7F:
                decoded_url += chr(c)
            else:
                raise ValueError("Invalid URL")

        return decoded_url

    @url.setter
    def url(self, input_url: str):
        encoded_url = bytearray()

        scheme_id, scheme_len = self.__find_scheme_id(input_url)
        encoded_url.append(scheme_id)

        # Start processing after the scheme
        pos = scheme_len
        while pos < len(input_url):
            ext_id = self.__find_extension_id(input_url, pos)
            if ext_id is not None:
                encoded_url += struct.pack('>b', ext_id)
                pos += len(self._EXTENSIONS[ext_id])
            else:
                # Just write the character if a shortened extension wasn't found.
                encoded_url.append(ord(input_url[pos]))
                pos += 1

        # Set the url into the frame
        self._frame = self._frame[:13] + encoded_url
        # Set the length of the payload, +1 for ranging data
        self._set_payload_length(len(encoded_url) + 1)


class EddystoneUIDFrame(_EddystoneGenericFrame):
    """
    Eddystone-UID frame broadcasts ranging data and
    an unique 16-byte Beacon ID composed of a 10-byte namespace and a 6-byte instance.
    See https://github.com/google/eddystone/tree/master/eddystone-uid for format details.
    """

    def __init__(self, ranging_data, uid):
        super().__init__(eddystone_type=TYPE_UID, payload_len=19)
        # A minimum viable UID frame is 19 bytes of zeros
        self.ranging_data = ranging_data
        self.uid = uid

    @property
    def ranging_data(self) -> int:
        """
        Get or set the ranging data, specified in decibel-milliwatts (dBm). Defined as the calibrated Tx power at 0 m.
        """
        return struct.unpack('>b', self._frame[12:13])[0]

    @ranging_data.setter
    def ranging_data(self, ranging_data: int):
        if ranging_data < -100 or ranging_data > 20:
            raise ValueError("ranging_data is out of range")

        ranging_data_byte = struct.pack('>b', ranging_data)
        self._frame = self._frame[:12] + ranging_data_byte + self._frame[13:]

    @property
    def uid(self) -> bytes:
        """
        Get or set the UID. An Eddystone-UID beacon ID is 16 bytes long, consisting of a 10-byte namespace component and
        a 6-byte instance component.
        """
        return bytes(self._frame[13:29])

    @uid.setter
    def uid(self, uid: bytes):
        if len(uid) != 16:
            raise ValueError("The UID field is an incorrect size, expected 16 bytes")

        # Insert UID with an extra zeroed two bytes at the end that are reserved for future use.
        self._frame = self._frame[:13] + uid + self._frame[29:]

    def validate_payload(self):
        # All UUID fields are of the same length: 23 bytes
        return self._validate_payload(23)


class EddystoneTLMFrame(_EddystoneGenericFrame):
    """
    Eddystone-TLM frame broadcasts telemetry information about the beacon itself such as battery voltage,
    device temperature, and counts of broadcast packets.
    See https://github.com/google/eddystone/blob/master/eddystone-tlm/tlm-plain.md for format details.
    """

    def __init__(self, advertisement_count, time_sec, beacon_temperature=-128, battery_voltage=0):
        super().__init__(eddystone_type=TYPE_TLM, payload_len=13)
        self.battery_voltage = battery_voltage
        self.beacon_temperature = beacon_temperature
        self.advertisement_count = advertisement_count
        self.time_sec = time_sec

    @staticmethod
    def __to_fixed88(fl):
        """
        Convert from a float to a fixed point 8.8
        """
        # limited to Q 8.8 fixed point range. valid range: -2^7 < temperature < 2^7 - 2^-8
        if fl < -128 or fl > 127.9961:
            raise ValueError("Out of range of representable values")
        return struct.pack('>h', int(fl * (2 ** 8)))

    @staticmethod
    def __from_fixed88(fp):
        """
        Convert from fixed point 8.8 to a float
        """
        return float(struct.unpack('>h', fp)[0] * (2 ** -8))

    @property
    def battery_voltage(self) -> float:
        """
        Get or set the battery voltage, specified in volts with a resolution of mV.
        """
        b = self._frame[13:15]
        return float(struct.unpack('>H', b)[0]) / 1000

    @battery_voltage.setter
    def battery_voltage(self, voltage: float):
        voltage = int(voltage * 1000)
        if voltage & ~0xFFFF:
            raise ValueError("Voltage is out of range")

        voltage_bytes = struct.pack('>H', voltage)

        self._frame = self._frame[:13] + voltage_bytes + self._frame[15:]

    @property
    def beacon_temperature(self) -> float:
        """
        Get or set the temperature, specified in Celsius.
        """
        return self.__from_fixed88(bytes(self._frame[15:17]))

    @beacon_temperature.setter
    def beacon_temperature(self, temperature: float):
        temperature_bytes = self.__to_fixed88(temperature)
        self._frame = self._frame[:15] + temperature_bytes + self._frame[17:]

    @property
    def advertisement_count(self) -> int:
        """
        Get or set the running count of advertisement frames emitted by the beacon since power-on.
        """
        return struct.unpack('>I', self._frame[17:21])[0]

    @advertisement_count.setter
    def advertisement_count(self, count: int):
        if count >= 1 << 32:
            raise ValueError("Advertisement count is out of range of representable values")
        count_bytes = struct.pack('>I', count)
        self._frame = self._frame[:17] + count_bytes + self._frame[21:]

    @property
    def time_sec(self) -> float:
        """
        Get or set the time since power-on, specified in seconds with a resolution of tenths of seconds.
        """
        return struct.unpack('>I', self._frame[21:25])[0] / 10.0

    @time_sec.setter
    def time_sec(self, time_sec: float):
        count = int(time_sec * 10)
        if count >= 1 << 32:
            raise ValueError("Time stamp out of range")
        count_bytes = struct.pack('>I', count)
        self._frame = self._frame[:21] + count_bytes

    def validate_payload(self):
        # All TLM fields are of the same size: 17 bytes
        return super()._validate_payload(17)


def parse(frame: bytes):
    """
    Parses a raw advertisement frame, returning a parsed Eddystone frame.
    :param frame: The raw advertisement to be parsed.
    :return: The type of the frame and a parsed Eddystone frame of that type:
        int, (EddystoneUIDFrame or EddystoneURLFrame or EddystoneTLMFrame).
    """
    if not _check_for_valid_eddystone(frame):
        raise TypeError("Incoming Eddystone frame is invalid")

    eddy_type = struct.unpack('>b', frame[11:12])[0]
    eddy_len = struct.unpack('>b', frame[_LENGTH_INDEX:_LENGTH_INDEX + 1])[0]
    # Setup a default empty frame to parse the values into
    if eddy_type == TYPE_URL:
        eddy_frame = EddystoneURLFrame(ranging_data=0, url='http://.com')
    elif eddy_type == TYPE_UID:
        eddy_frame = EddystoneUIDFrame(ranging_data=0, uid=bytearray(16))
    elif eddy_type == TYPE_TLM:
        eddy_frame = EddystoneTLMFrame(advertisement_count=0, time_sec=0)
    else:
        raise TypeError("Eddystone type is not supported: {}".format(eddy_type))

    # Place values into frame, Do not need to replace common 4 bytes at start
    eddy_frame.set_raw_payload(frame[(8 + 4):(12 + eddy_len - 4)])

    # Validate the eddystone frame
    if not eddy_frame.validate_payload():
        raise TypeError("Eddystone Payload is invalid")

    return eddy_type, eddy_frame
