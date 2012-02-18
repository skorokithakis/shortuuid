#!/usr/bin/env python

import sys
assert sys.version >= '2.5', "Requires Python v2.5 or above."
from setuptools import setup

setup(
    name = "shortuuid",
    version = "0.2",
    author = "Stochastic Technologies",
    author_email = "info@stochastictechnologies.com",
    url = "https://github.com/stochastic-technologies/shortuuid/",
	description = "A generator library for concise, unambiguous and URL-safe UUIDs.",
	long_description = "A library that generates short, pretty, unambiguous unique IDs "
                       " by using an extensive, case-sensitive alphabet and omitting "
                       "similar-looking letters and numbers.",
	license = "BSD",
    packages = ["shortuuid"],
)
