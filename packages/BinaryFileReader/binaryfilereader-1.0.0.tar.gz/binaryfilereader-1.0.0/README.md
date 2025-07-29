![BinaryFileReader Logo](https://mauricelambert.github.io/info/python/security/BinaryFileReader/small.png "BinaryFileReader logo")

# BinaryFileReader

## Description

This package reads binary file to exports strings or prints content as hexadecimal.

> By default the `Strings` command print only null terminated strings (*unicode (Windows, utf-16-le)* and ascii *(Linux, latin-1)*) and support non-null termined strings with option `-t`.
> `HexaReader` is colored and support custom coloration.

## Requirements

This package require:

 - python3
 - python3 Standard Library
 - PythonToolsKit==1.2.4

## Installation

### Pip

```bash
pip install BinaryFileReader
```

### Git

```bash
git clone "https://github.com/mauricelambert/BinaryFileReader.git"
cd "BinaryFileReader"
python3 -m pip install .
```

### Wget

```bash
wget https://github.com/mauricelambert/BinaryFileReader/archive/refs/heads/main.zip
unzip main.zip
cd BinaryFileReader-main
python3 -m pip install .
```

### cURL

```bash
curl -O https://github.com/mauricelambert/BinaryFileReader/archive/refs/heads/main.zip
unzip main.zip
cd BinaryFileReader-main
python3 -m pip install .
```

## Usages

## Command line

```bash
Strings                                 # Using CLI package executable
HexaReader                              # Using CLI package executable
python3 -m BinaryFileReader strings     # Using python module
python3 -m BinaryFileReader.Strings     # Using python module
python3 -m BinaryFileReader hexareader  # Using python module
python3 -m BinaryFileReader.HexaReader  # Using python module
python3 BinaryFileReader.pyz strings    # Using python executable
python3 BinaryFileReader.pyz hexareader # Using python executable
python3 Strings.pyz                     # Using python executable
python3 HexaReader.pyz                  # Using python executable
Strings.exe                             # Using python Windows executable
HexaReader.exe                          # Using python Windows executable

Strings -h                              # get help message
Strings test.bin                        # exports null terminated strings from test.bin
Strings -n 7 -t test.dump               # exports strings with minimum length of 7 characters
HexaReader test.bin                     # Read test.bin as hexadecimal and ascii printable
HexaReader -c -s 25 test.bin            # Read test.bin as hexadecimal and ascii printable without colors and with 25 characters by line
```

### Python script

```python
from BinaryFileReader import Strings, HexaReader

with open("test.bin", 'rb') as file:
    hexareader = HexaReader(file)
    for line in hexareader.reader():
        print(line)

with open("test.bin", 'rb') as file:
    strings = Strings(file, minimum_length=5, null_terminated=True)
    for line in strings.reader():
        print(line)

with open("test.bin", 'rb') as file:
    hexa_reader = HexaReader(
        file,
        size=16,
        ascii=True,
        colors={  # color names can be found from PythonToolsKit.Terminal.COLORS (BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, GRAY)
            "abcdefghijklmnopqrstuvwxyzABCDEFIJKLMNOPQRSTUVWXYZ": "GREEN",
            "0123456789": "CYAN",
            " !\"#$%&'()*+,-./:;<=>?[\\]^_{|}~`": "YELLOW",
        },
    )
    for line in hexareader.reader():
        print(line)
```

## Links

 - [Pypi package](https://pypi.org/project/BinaryFileReader/)
 - [Github Page](https://github.com/mauricelambert/BinaryFileReader/)
 - [Strings Documentation](https://mauricelambert.github.io/info/python/security/BinaryFileReader/Strings.html)
 - [Strings Python executable](https://mauricelambert.github.io/info/python/security/BinaryFileReader/Strings.pyz)
 - [Strings Python Windows executable](https://mauricelambert.github.io/info/python/security/BinaryFileReader/Strings.exe)
 - [HexaReader Documentation](https://mauricelambert.github.io/info/python/security/BinaryFileReader/HexaReader.html)
 - [HexaReader Python executable](https://mauricelambert.github.io/info/python/security/BinaryFileReader/HexaReader.pyz)
 - [HexaReader Python Windows executable](https://mauricelambert.github.io/info/python/security/BinaryFileReader/HexaReader.exe)
 - [Python executable](https://mauricelambert.github.io/info/python/security/BinaryFileReader/BinaryFileReader.pyz)
 - [Python Windows executable](https://mauricelambert.github.io/info/python/security/BinaryFileReader/BinaryFileReader.exe)

## Licence

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
