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

from typing import Any


class sha256(object):
    """
    SHA256 hasher object. The current generation, modern hashing algorithm
    (of SHA2 series). It is suitable for cryptographically-secure purposes.
    """

    def __init__(self, data: Any=None) -> None:
        """
        Class constructor. Instantiates a ``sha256`` hasher object and
        optionally feeds data into it.

        :param data: Initial binary data to add to hash.
        """
        ...

    def update(self, data: Any) -> None:
        """
        Feeds more binary data into hash.

        :param data: Binary data to add to hash.
        """
        ...

    def digest(self) -> bytes:
        """
        Returns hash for all data passed through hash, as a bytes object. After
        this method is called, more data cannot be fed into hash any longer.

        :return: Bytes object with hash for all data passed.
        """
        ...
