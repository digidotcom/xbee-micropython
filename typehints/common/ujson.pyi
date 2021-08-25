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

from typing import Any, Union


def dump(obj: Any, stream: Any) -> None:
    """
    Serialises ``obj`` to a JSON string, writing it to the given ``stream``.

    :param obj: Object to serialise to a JSON string.
    :param stream: Destination stream to write the serialised object (a
        .write()-supporting file-like object)
    """
    ...

def dumps(obj: Any) -> str:
    """
    Returns object ``obj`` represented as a JSON string.

    :param obj: Object to serialise to a JSON string.

    :return: Object ``obj`` represented as a JSON string.
    """
    ...

def load(stream: Any) -> Any:
    """
    Parses the given stream, interpreting it as a JSON string and deserialising
    the data to a Python object. The resulting object is returned.

    Parsing continues until end-of-file is encountered. A ValueError is raised
    if the data in stream is not correctly formed.

    :param stream: Source stream to read the JSON string to deserialise (a
        .read()-supporting text file or binary file containing a JSON document)

    :return: A Python object corresponding to the read JSON string.
    """
    ...

def loads(json_string: Union[str, bytes, bytearray, memoryview]) -> Any:
    """
    Parses the given JSON string and returns a Python object. Raises
    ``ValueError`` if the string is not correctly formed.

    **Note:** In MicroPython versions v1.11 and earlier, the ``json_string``
    parameter is required to be of type ``str``. In newer version of
    MicroPython, it must implement the buffer protocol (i.e. it must be
    of type ``str``, ``bytes``, ``bytearray`` or ``memoryview``).
    (The MicroPython version is visible in the banner displayed at the REPL,
    using the **ATPYV** command, and as the second item in the
    ``sys.implementation`` tuple.)

    :param json_string: String containing the JSON document to deserialise.

    :return: A Python object corresponding to the given JSON string.
    """
    ...
