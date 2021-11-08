# Changelog


## Unreleased

### Features

* Add `prefix` and `max_length` to the Django field. [Stavros Korokithakis]


## v1.0.6 (2021-11-08)

### Fixes

* Fix compatibility for python versions older than 3.8 (#61) [Adrian Zuber]


## v1.0.5 (2021-11-08)

### Fixes

* Don't try to get the version from the pyproject.toml, as it's a hassle. [Stavros Korokithakis]

* Fix slow loading times from using pkg_resources (fixes #59) [Stavros Korokithakis]


## v1.0.4 (2021-11-08)

### Fixes

* Fix the cli interface that the previous release broke. [Stavros Korokithakis]


## v1.0.3 (2021-11-08)

### Features

* Add Django ShortUUIDField. [Stavros Korokithakis]


## v1.0.2 (2021-11-08)

### Features

* Added basic input type validation to encode and decode (#49) [Ivan Savov]

### Fixes

* Use sys.version_info since sys.version returns string that interprets 3.10 as 3.1 in comparison. (#54) [Karthikeyan Singaravelan]


## v1.0.1 (2020-03-06)

### Features

* Drop support for Python before 3.5. [Stavros Korokithakis]

### Fixes

* Use README as the long description on PyPI. [Stavros Korokithakis]


## v1.0.0 (2020-03-05)

### Features

* Add simple command-line interface (#43) [Éric Araujo]

### Fixes

* Make encode and decode MSB-first (#36) [Keane Nguyen]

* Make the URL check more robust (fixes #32) [Stavros Korokithakis]


## v0.5.0 (2017-02-19)

### Features

* Make int_to_string and string_to_int available globally. [Stavros Korokithakis]


