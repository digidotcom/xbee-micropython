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

from typing import Union, Optional, TypeVar

_WriteBufT = TypeVar('_WriteBufT', bytearray, memoryview)


MODE_ECB: int = ...
MODE_CBC: int = ...
MODE_CTR: int = ...


class aes:
    def __init__(self,
                 key: Union[str, bytes],
                 mode: int,
                 IV: Optional[Union[str, bytes]] = None) -> None:
        """Initialize cipher object, suitable for encryption/decryption. Note:
        after initialization, cipher object can be use only either for
        encryption or decryption. Running decrypt() operation after
        encrypt() or vice versa is not supported.

        **Note:** This is only available on XBee and XBee 3 Cellular products
        with firmware ending in 15 or newer.

        Parameters are:

        :param key:
                An encryption/decryption key (bytes-like).

        :param mode:
            1 (or ucryptolib.MODE_ECB) for Electronic Code Book (ECB).
            2 (or ucryptolib.MODE_CBC) for Cipher Block Chaining (CBC).
            6 (or ucryptolib.MODE_CTR) for Counter mode (CTR).

        :param IV:
            For CBC mode, an initialization vector.
            For Counter mode, the initial value for the counter.
        """
        ...

    def encrypt(self,
                in_buf: Union[str, bytes, bytearray, memoryview],
                out_buf: Optional[_WriteBufT] = None) -> Union[bytes, _WriteBufT]:
        """Encrypt ``in_buf``.

        If no ``out_buf`` is given result is returned as a newly
        allocated bytes object. Otherwise, result is written into
        mutable buffer ``out_buf``. ``in_buf`` and ``out_buf`` can
        also refer to the same mutable buffer, in which case data is
        encrypted in-place.

        """
        ...

    def decrypt(self,
                in_buf: Union[str, bytes, bytearray, memoryview],
                out_buf: Optional[_WriteBufT] = None) -> Union[bytes, _WriteBufT]:
        """Decrypt ``in_buf``.

        If no ``out_buf`` is given result is returned as a newly
        allocated bytes object. Otherwise, result is written into
        mutable buffer ``out_buf``. ``in_buf`` and ``out_buf`` can
        also refer to the same mutable buffer, in which case data is
        encrypted in-place

        """
        ...
