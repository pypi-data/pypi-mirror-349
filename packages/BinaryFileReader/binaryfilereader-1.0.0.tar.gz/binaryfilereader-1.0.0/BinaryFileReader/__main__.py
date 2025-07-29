#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This package reads binary file to exports strings or prints content as hexadecimal.
"""

###################
#    This package reads binary file to exports strings or prints content as hexadecimal.
#    Copyright (C) 2021, 2025  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

__version__ = "1.0.0"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This module implements a hexadecimal reader.
"""
__url__ = "https://github.com/mauricelambert/BinaryFileReader"

__all__ = ["Strings", "HexaReader", "get_strings", "hexaread"]

__license__ = "GPL-3.0 License"
__copyright__ = """
BinaryFileReader  Copyright (C) 2021, 2025  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
copyright = __copyright__
license = __license__

print(copyright)

try:
    from .Strings import Strings, main as get_strings
    from .HexaReader import HexaReader, main as hexaread
except ImportError:
    from Strings import Strings, main as get_strings
    from HexaReader import HexaReader, main as hexaread

from sys import argv, stderr

help_message = """USAGE: python3 -m BinaryFileReader module filename
    [module] must be "strings" or "hexareader"
    [filename] must be an existing binary file
"""


def main() -> int:
    """
    The main function to run from command line.
    """

    if len(argv) > 1:
        module = argv.pop(1).lower()

        if module == "strings":
            get_strings()
            return 0
        elif module == "hexareader":
            hexaread()
            return 0

    print(help_message, file=stderr)
    return 1


if __name__ == "__main__":
    exit(main())
