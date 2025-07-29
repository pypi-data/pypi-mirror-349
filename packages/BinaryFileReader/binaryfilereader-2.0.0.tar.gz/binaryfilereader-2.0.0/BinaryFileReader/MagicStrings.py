#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This file process exported strings recursively from binary file.
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

"""
This file process exported strings recursively from binary file.
"""

__version__ = "2.0.0"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This file exports strings from binary file.
"""
__url__ = "https://github.com/mauricelambert/BinaryFileReader"

__all__ = ["MagicStrings", "Result", "main"]

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
    from .Strings import Strings, parse_arguments
except ImportError:
    from Strings import Strings, parse_arguments

from RC6Encryption import RC6Encryption
from RC4Encryption import RC4Encryption
from PegParser import formats

from sys import getrecursionlimit, setrecursionlimit, exit
from typing import Iterator, Tuple, List, Union
from dataclasses import dataclass
from io import BytesIO


@dataclass
class Result:
    """
    This dataclass contains the result for each
    exported and processed strings and matchs.
    """

    string: str
    format: str
    recursive_level: int

    def __str__(self):
        return f"[{self.recursive_level} {self.format}] {self.string}"

    def __repr__(self):
        return f"[{self.recursive_level} {self.format}] {self.string!r}"


class MagicStrings(Strings):
    """
    This class process exported strings recursively from binary file.
    """

    def __init__(
        self,
        *args,
        recursive_level: int = 0,
        keys: List[Tuple[bytes, Union[None, str]]] = [],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.recursive_level = recursive_level
        self.keys = keys
        self._in_bruteforce = False

    def process_strings(self) -> Iterator[Result]:
        """
        This method sends each string to recursive function.
        """

        for string in self.reader():
            yield from self.process_string(string)

    def magic(self) -> Iterator[Result]:
        """
        This method process the file.
        """

        yield from self.process_strings()

        if not hasattr(self.file, "tell") or not hasattr(self.file, "seek"):
            return None

        # if self.file.tell() <= 153600:
        #     self.file.seek(0)
        #     yield from self.process_crypto(self.file.read())

    def new(self, data: bytes) -> Iterator[Result]:
        """
        This method makes a new instance of MagicStrings
        for a in depth string search.
        """

        yield from self.__class__(
            BytesIO(data),
            self.minimum_length,
            self.null_terminated,
            recursive_level=self.recursive_level + 1,
            keys=self.keys,
        ).magic()

    def process_string(self, string: str) -> Iterator[Result]:
        """
        The recursive method to process each string.
        """

        yield Result(string, "string", self.recursive_level)
        string_encoded = string.encode("ascii")

        while len(string_encoded) >= self.minimum_length:
            yield from self.process_decrypted_string(string_encoded)

            # if not self._in_bruteforce:
            #     yield from self.bruteforces(string_encoded, True)
            string_encoded = string_encoded[1:]

    def process_decrypted_string(self, string_encoded: bytes) -> Iterator[Result]:
        """
        The method checks the string for all formats.
        """

        for name, format in formats.items():
            match = format.match(string_encoded)
            if not match:
                continue

            try:
                data = format.decode(match)
            except Exception as e:
                continue
            yield Result(match.decode("ascii"), name, self.recursive_level)
            if data != match and len(data) >= self.minimum_length:
                yield from self.check_length_and_process(data)

    def process_crypto(self, data: bytes) -> Iterator[Result]:
        """
        This method process data with crypto functions.
        """

        for key, cypher in self.keys:
            if cypher is not None:
                yield from self.check_length_and_process(decryptors[cypher](key))
                continue
            for decryptor in decryptors.values():
                yield from self.check_length_and_process(decryptor(key))

        yield from self.bruteforces(data)

    def check_length_and_process(self, data: bytes) -> Iterator[Result]:
        """
        This method checks if data should be processed
        and process it.
        """

        if len(data) >= self.minimum_length:
            yield from self.new(data)

    def bruteforces(
        self, data: bytes, is_string: bool = False
    ) -> Iterator[Result]:
        """
        This method bruteforces one character keys
        for small crypto functions.
        """

        self._in_bruteforce = True
        max = 26 if is_string else 256
        process_function = ((lambda x: self.process_string(x.decode(), "decrypt")) if is_string else self.check_length_and_process)
        print("new")

        for function in (letters_bruteforcer if is_string else bytes_bruteforcer):
            for key in range(max):
                result = function(data, key)
                if result:
                    yield from process_function(result)

        self._in_bruteforce = False


def single_add_bytes(data: bytes, key: int) -> Union[bytes, None]:
    """
    This function encrypts or decrypts single key
    character substitution cypher on all bytes.
    """

    if not key:
        return None

    return bytes([(x + key) & 0xFF for x in data])


def single_add_letters(data: bytes, key: int) -> Union[bytes, None]:
    """
    This function encrypts or decrypts single key
    character substitution cypher on letters only.
    """

    if not key:
        return None

    return bytes([((x + key) % 26) + 97 for x in data])


def single_xor_bytes(data: bytes, key: int) -> Union[bytes, None]:
    """
    This function encrypts or decrypts single key
    character xor cypher.
    """

    if not key:
        return None

    return bytes([(x ^ key) for x in data])


def rc4_decryptor(data: bytes, key: bytes) -> bytes:
    """
    This function is the decryptor for RC4 cypher.
    """

    rc4 = RC4Encryption(key)
    rc4.make_key()
    return rc4.crypt(data)


def rc6_ecb_decryptor(data: bytes, key: bytes) -> bytes:
    """
    This function is the decryptor for RC6 cypher (mode ECB, no IV, not secure).
    """

    rc6 = RC6Encryption(key)
    return rc6.data_decryption_ECB(data)


bytes_bruteforcer = [single_xor_bytes, single_add_bytes]
letters_bruteforcer = [single_add_letters]
decryptors = {
    "rc4": rc4_decryptor,
    "RC4": rc4_decryptor,
    "rc6": rc6_ecb_decryptor,
    "RC6": rc6_ecb_decryptor,
}


def main() -> int:
    """
    This function runs the module from the command line.
    """

    arguments = parse_arguments()

    limit = getrecursionlimit()
    # setrecursionlimit(100000)

    with open(arguments.filename, "rb") as file:
        strings = MagicStrings(
            file,
            minimum_length=arguments.minimum_length,
            null_terminated=not arguments.non_null_terminated,
        )

        for line in strings.magic():
            print(line)

    setrecursionlimit(limit)
    return 0


if __name__ == "__main__":
    exit(main())
