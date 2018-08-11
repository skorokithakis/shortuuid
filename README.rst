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

.. image:: https://travis-ci.org/skorokithakis/shortuuid.svg?branch=master
    :target: https://travis-ci.org/skorokithakis/shortuuid

Installation
------------

To install ``shortuuid`` you need:

* Python 2.5 or later in the 2.x line (earlier than 2.6 not tested).

If you have the dependencies, you have multiple options of installation:

* With pip (preferred), do ``pip install shortuuid``.
* With setuptools, do ``easy_install shortuuid``.
* To install the source, download it from
  https://github.com/stochastic-technologies/shortuuid and do
  ``python setup.py install``.

Usage
-----

To use ``shortuuid``, just import it in your project like so:

>>> import shortuuid

You can then generate a short UUID:

>>> shortuuid.uuid()
'vytxeTZskVKR7C7WgdSP3d'

If you prefer a version 5 UUID, you can pass a name (DNS or URL) to the call and
it will be used as a namespace (uuid.NAMESPACE_DNS or uuid.NAMESPACE_URL) for the
resulting UUID:

>>> shortuuid.uuid(name="example.com")
'wpsWLdLt9nscn2jbTD3uxe'
>>> shortuuid.uuid(name="http://example.com")
'c8sh5y9hdSMS6zVnrvf53T'

You can also generate a cryptographically secure random string (using 
`os.urandom()`, internally) with:

>>> shortuuid.ShortUUID().random(length=22)
'RaF56o2r58hTKT7AYS9doj'


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

To serialize existing UUIDs, use ``encode()`` and ``decode()``:

>>> import uuid ; u = uuid.uuid4() ; u
UUID('6ca4f0f8-2508-4bac-b8f1-5d1e3da2247a')
>>> s = shortuuid.encode(u) ; s
'cu8Eo9RyrUsV4MXEiDZpLM'
>>> shortuuid.decode(s) == u
True
>>> short = s[:7] ; short
'cu8Eo9R'
>>> h = shortuuid.decode(short)
UUID('00000000-0000-0000-0000-00b8c0b9f952')
>>> shortuuid.decode(shortuuid.encode(h)) == h
True

Class-based usage
-----------------

If you need to have various alphabets per-thread, you can use the `ShortUUID` class, like so:

>>> su = shortuuid.ShortUUID(alphabet="01345678")
>>> su.uuid()
'034636353306816784480643806546503818874456'
>>> su.get_alphabet()
'01345678'
>>> su.set_alphabet("21345687654123456")
>>> su.get_alphabet()
'12345678'


Compatibility note
------------------

Earlier versions of ShortUUID generated UUIDs with their MSB last, i.e. reversed. This was later fixed, but if you have some UUIDs stored as a string in the old way, you need to pass `legacy=True` to `decode()` when converting your strings back to ints.

That option will go away in the future, so you will want to convert your UUIDs to strings using the new way, with:

>>> uuid = encode(decode(uuid))


License
-------

``shortuuid`` is distributed under the BSD license.
