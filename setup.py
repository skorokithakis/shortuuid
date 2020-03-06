#!/usr/bin/env python
import sys

from setuptools import setup

from shortuuid import __version__

assert sys.version >= "2.5", "Requires Python v2.5 or above."

classifiers = [
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setup(
    name="shortuuid",
    version=__version__,
    author="Stochastic Technologies",
    author_email="info@stochastictechnologies.com",
    url="https://github.com/stochastic-technologies/shortuuid/",
    description="A generator library for concise, " "unambiguous and URL-safe UUIDs.",
    long_description="A library that generates short, pretty, "
    "unambiguous unique IDs "
    "by using an extensive, case-sensitive alphabet and omitting "
    "similar-looking letters and numbers.",
    license="BSD",
    classifiers=classifiers,
    packages=["shortuuid"],
    test_suite="shortuuid.tests",
    tests_require=[],
)
