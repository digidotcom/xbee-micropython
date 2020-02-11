#!/usr/bin/env python
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

"""
Python script to validate formatting and contents of README.md files
for xbee-micropython samples and libraries.

This script requires Python 3.6+, and the Python-Markdown and lxml libraries,
which can be installed using pip:

    pip install Markdown lxml
    # or
    pip install -r {xbee_micropython}/tools/requirements.txt

"""

import argparse
import traceback
from pathlib import Path
from typing import List

import lxml.etree
import markdown


XPATH_PLATFORMS_LIST = lxml.etree.XPath(
    # Find the second-level heading "Supported platforms".
    # Find its neighboring <ul> (bulleted list).
    # Get all <li> (list items) therein.
    "//h2[text()='Supported platforms']/following-sibling::ul/li")
MIN_FW = "- minimum firmware version:"


def suggest_matches(input_str: str, match_against: List[str]) -> None:
    # Very naive check right now - prefix matching in either direction.
    close_matches = [
        m for m in match_against
        if input_str.startswith(m) or m.startswith(input_str)
    ]

    count = len(close_matches)
    if not count:
        return
    elif count == 1:
        print(f"... did you mean {close_matches[0]!r}?")
    else:
        print(f"... did you mean one of these? {close_matches}")


def scan_readme_file(
    readme: Path,
    recognized_platforms: List[str],
) -> None:
    body = readme.read_text()

    if "Supported platforms" not in body:
        # This README.md does not appear to be for a library or sample.
        return

    as_html = markdown.markdown(body)
    tree = lxml.etree.HTML(as_html)
    supported_platforms = XPATH_PLATFORMS_LIST(tree)
    if not supported_platforms:
        print("ERROR: 'Supported platforms' incorrect heading type?")
        return

    for platform in supported_platforms:
        platform_name, min_version = platform.text.split(MIN_FW, 1)
        name = platform_name.strip()
        if name not in recognized_platforms:
            print(f"ERROR ({readme}): Unrecognized platform: {name}") 

            # See if we can hint at a correction.
            suggest_matches(name, recognized_platforms)

        min_version = min_version.strip()
        min_version_to_parse = min_version
        if min_version.startswith('x'):
            # Wildcard version syntax, e.g. x15.
            min_version_to_parse = '0' + min_version

        try:
            # Check that the minimum version number parses as a hex number.
            int(min_version_to_parse, 16)
        except ValueError:
            print(
                f"ERROR ({readme}): "
                f"Unparseable minimum firmware: {min_version!r}"
            )


def scan_readme_files_in_directory(
    directory: Path,
    recognized_platforms: List[str],
) -> None:
    """
    Check each README.md file in the specified directory, to ensure that
    the file is formatted properly for the Digi XBee MicroPython PyCharm IDE
    plugin.
    """
    if not directory.is_dir():
        raise ValueError(f"{directory} is not a directory")

    for readme in directory.rglob('README.md'):
        try:
            scan_readme_file(readme, recognized_platforms)
        except Exception:
            traceback.print_exc()


def _get_recognized_platforms(platforms_xml: Path) -> List[str]:
    """
    Parse the platforms.xml file and get all platform IDs (names).
    """
    xmltree = lxml.etree.XML(platforms_xml.read_text())
    return [
        # We need the 'id' attribute from each <platform> tag.
        platform.get('id')
        for platform in xmltree.iter('platform')
    ]


if __name__ == "__main__":
    xbee_micropython = Path(__file__).resolve().parent.parent

    parser = argparse.ArgumentParser(
        description=__doc__.format(xbee_micropython=xbee_micropython),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'dirs',
        metavar='directory', nargs='*',
        help=(
            'Library/sample directory to scan. Can be used multiple times. '
            'If no directories are specified, defaults to lib and samples.'
        ),
        type=Path,
        # If no directories are specified at the command line,
        # default to checking the 'lib' and 'samples' directories.
        default=[
            xbee_micropython / 'lib',
            xbee_micropython / 'samples',
        ],
    )
    args = parser.parse_args()

    platforms = _get_recognized_platforms(
        xbee_micropython / 'platforms' / 'platforms.xml'
    )
    # TODO: We could pick up on library names as well,
    # and check the 'Required libraries' list.

    for directory in args.dirs:
        scan_readme_files_in_directory(directory.resolve(), platforms)

