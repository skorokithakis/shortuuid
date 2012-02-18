===========
Description
===========

``shortuuid`` is a simple python library that generates concise, unambiguous,
URL-safe UUIDs.

Often, one needs to use non-sequential IDs in places where users will see them,
but the IDs must be as concise and easy to use as possible. ``shortuuid`` solves
this problem by generating uuids using Python's built-in ``uuid`` module and then
translating them to base57 using lowercase and uppercase letters and digits, and
removing similar-looking characters such as l, 1, I, O and 0.


Installation
------------

To install ``shortuuid`` you need:

* Python 2.5 or later in the 2.x line (3.x not supported, earlier than 2.5 not tested).

If you have the dependencies, you have multiple options of installation:

* With pip (preferred), do ``pip install shortuuid``.
* With setuptools, do ``easy_install shortuuid``.
* To install the source, download it from
  https://github.com/stochastic-technologies/shortuuid/ and do
  ``python setup.py install``.

Usage
-----

To use ``shortuuid``, just import it in your project like so:

>>> import shortuuid

You can then generate a short UUID:

>>> shortuuid.uuid()
'vytxeTZskVKR7C7WgdSP3d'

If you prefer a version 3 UUID, you can pass a URL to the call and it will be used
as a URL namespace for the resulting UUID:

>>> shortuuid.uuid(url="http://example.com/")
'nzcZ3Y648sUBirQ2bwywDP'

To see the alphabet that is being used to generate new UUIDs:

>>> shortuuid.get_alphabet()
'23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

If you want to use your own alphabet to generate UUIDs, use ``set_alphabet()``:

>>> shortuuid.set_alphabet("aaaaabcdefgh1230123")
>>> shortuuid.uuid()
'0agee20aa1hehebcagddhedddc0d2chhab3b'

``shortuuid`` will automatically sort and remove duplicates from your alphabet to
ensure consistency:

>>> shortuuid.get_alphabet()
'0123abcdefgh'

If the default 22 digits are too long for you, you can get shorter IDs by just
truncating the string to the desired length. The IDs won't be universally unique
any longer, but the probability of a collision will still be very low.

License
-------

``shortuuid`` is distributed under the BSD license.
