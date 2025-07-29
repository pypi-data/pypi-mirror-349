from setuptools import setup, find_packages

setup(
    name = "BinaryFileReader",
    version = "1.0.0",

    packages = ["BinaryFileReader"],
    install_requires = ["PytonToolsKit==1.2.4"],

    author = "Maurice Lambert", 
    author_email = "mauricelambert434@gmail.com",
    maintainer = "Maurice Lambert",
    maintainer_email = "mauricelambert434@gmail.com",
 
    description = "This package reads binary file to exports strings or prints content as hexadecimal.",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://github.com/mauricelambert/BinaryFileReader',
    download_url="https://mauricelambert.github.io/info/python/security/BinaryFileReader/BinaryFileReader.pyz",
    project_urls={
        "Github": "https://github.com/mauricelambert/BinaryFileReader",
        "Strings Documentation": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/Strings.html",
        "Strings Python Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/Strings.pyz",
        "Strings Windows Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/Strings.exe",
        "HexaReader Documentation": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/HexaReader.html",
        "HexaReader Python Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/HexaReader.pyz",
        "HexaReader Windows Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/HexaReader.exe",
        "Python Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/BinaryFileReader.pyz",
        "Python Windows Executable": "https://mauricelambert.github.io/info/python/security/BinaryFileReader/BinaryFileReader.exe",
    },
 
    classifiers = [
        "Topic :: Security",
        "Environment :: Console",
        "Topic :: System :: Shells",
        "Operating System :: MacOS",
        'Operating System :: POSIX',
        "Natural Language :: English",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Topic :: System :: System Shells",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Microsoft :: Windows",
        "Topic :: System :: Systems Administration",
        "Intended Audience :: System Administrators",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],

    keywords=['strings', 'hexadecimal', 'hexadecimal-reader', 'binary-file', 'reverse', 'binary-reader', 'binary-viewer'],
 
    scripts = [],
    entry_points = {
        'console_scripts': [
            'Strings = BinaryFileReader:get_strings',
            'HexaReader = BinaryFileReader:hexaread',
        ],
    },

    platforms=['Windows', 'Linux', "MacOS"],
    license="GPL-3.0 License",
    python_requires='>=3.8',
)
