# Changelog


## Unreleased

### Features

* Add cli help. [tim]

* Add encode and decode to cli. [tim]

* Use argparse in cli. [tim]

* Add type hinting (#77) [Pablo Collado]

* Add `prefix` and `max_length` to the Django field. [Stavros Korokithakis]

* Add Django ShortUUIDField. [Stavros Korokithakis]

* Added basic input type validation to encode and decode (#49) [Ivan Savov]

* Drop support for Python before 3.5. [Stavros Korokithakis]

* Add simple command-line interface (#43) [Éric Araujo]

* Make int_to_string and string_to_int available globally. [Stavros Korokithakis]

### Fixes

* Fix type annotations. [Stavros Korokithakis]

* Correctly account for length when prefix is used (fixes #71) [Stavros Korokithakis]

* Include the COPYING file in releases. [Stavros Korokithakis]

* Fix compatibility for python versions older than 3.8 (#61) [Adrian Zuber]

* Don't try to get the version from the pyproject.toml, as it's a hassle. [Stavros Korokithakis]

* Fix slow loading times from using pkg_resources (fixes #59) [Stavros Korokithakis]

* Fix the cli interface that the previous release broke. [Stavros Korokithakis]

* Use sys.version_info since sys.version returns string that interprets 3.10 as 3.1 in comparison. (#54) [Karthikeyan Singaravelan]

* Use README as the long description on PyPI. [Stavros Korokithakis]

* Make encode and decode MSB-first (#36) [Keane Nguyen]

* Make the URL check more robust (fixes #32) [Stavros Korokithakis]


