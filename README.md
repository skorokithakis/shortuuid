Description
===========

`shortuuid` is a simple python library that generates concise, unambiguous, URL-safe
UUIDs.

Often, one needs to use non-sequential IDs in places where users will see them, but the
IDs must be as concise and easy to use as possible.  `shortuuid` solves this problem by
generating uuids using Python's built-in `uuid` module and then translating them to
base57 using lowercase and uppercase letters and digits, and removing similar-looking
characters such as l, 1, I, O and 0.

[![image](https://travis-ci.org/skorokithakis/shortuuid.svg?branch=master)](https://travis-ci.org/skorokithakis/shortuuid)


Installation
------------

To install `shortuuid` you need:

-   Python 3.x.

If you have the dependencies, you have multiple options of installation:

-   With pip (preferred), do `pip install shortuuid`.
-   With setuptools, do `easy_install shortuuid`.
-   To install the source, download it from
    https://github.com/stochastic-technologies/shortuuid and run `python setup.py
    install`.


Usage
-----

To use `shortuuid`, just import it in your project like so:

```python
>>> import shortuuid
```

You can then generate a short UUID:

```python
>>> shortuuid.uuid()
'vytxeTZskVKR7C7WgdSP3d'
```

If you prefer a version 5 UUID, you can pass a name (DNS or URL) to the call and it will
be used as a namespace (`uuid.NAMESPACE_DNS` or `uuid.NAMESPACE_URL`) for the resulting
UUID:

```python
>>> shortuuid.uuid(name="example.com")
'exu3DTbj2ncsn9tLdLWspw'

>>> shortuuid.uuid(name="<http://example.com>")
'shortuuid.uuid(name="<http://example.com>")'
```

You can also generate a cryptographically secure random string (using `os.urandom()`
internally) with:

```python
>>> shortuuid.ShortUUID().random(length=22)
'RaF56o2r58hTKT7AYS9doj'
```

To see the alphabet that is being used to generate new UUIDs:

```python
>>> shortuuid.get_alphabet()
'23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
```

If you want to use your own alphabet to generate UUIDs, use `set_alphabet()`:

```python
>>> shortuuid.set_alphabet("aaaaabcdefgh1230123")
>>> shortuuid.uuid()
'0agee20aa1hehebcagddhedddc0d2chhab3b'
```

`shortuuid` will automatically sort and remove duplicates from your alphabet to ensure
consistency:

```python
>>> shortuuid.get_alphabet()
'0123abcdefgh'
```

If the default 22 digits are too long for you, you can get shorter IDs by just
truncating the string to the desired length. The IDs won't be universally unique any
longer, but the probability of a collision will still be very low.

To serialize existing UUIDs, use `encode()` and `decode()`:

```python
>>> import uuid
>>> u = uuid.uuid4()
>>> u
UUID('6ca4f0f8-2508-4bac-b8f1-5d1e3da2247a')

>>> s = shortuuid.encode(u)
>>> s
'MLpZDiEXM4VsUryR9oE8uc'

>>> shortuuid.decode(s) == u
True

>>> short = s[:7]
>>> short
'MLpZDiE'

>>> h = shortuuid.decode(short)
UUID('00000000-0000-0000-0000-009a5b27f8b9')

>>> shortuuid.decode(shortuuid.encode(h)) == h
True
```


Class-based usage
-----------------

If you need to have various alphabets per-thread, you can use the `ShortUUID` class,
like so:

```python
>>> su = shortuuid.ShortUUID(alphabet="01345678")
>>> su.uuid()
'034636353306816784480643806546503818874456'

>>> su.get_alphabet()
'01345678'

>>> su.set_alphabet("21345687654123456")
>>> su.get_alphabet()
'12345678'
```


Command-line usage
------------------

`shortuuid` provides a simple way to generate a short UUID in a terminal:

```bash
$ shortuuid
fZpeF6gcskHbSpTgpQCkcJ
```


Django field
------------

`shortuuid` includes a Django field that generates random short UUIDs by default, for
your convenience:

```python
from shortuuid.django_fields import ShortUUIDField

class MyModel(models.Model):
    # A primary key ID with a short alphabet.
    # When ShortUUIDField is not provided with length, a uuid is generated
    id = ShortUUIDField(
        max_length=40,
        prefix="id_",
        alphabet="abcdefg1234",
        primary_key=True,
    )
    # When ShortUUIDField is provided with a length parameter, a cryptographically secure 
    # random but NOT universally unique string is generated
    random_field = ShortUUIDField(
        length=16,
        max_length=40,
        prefix="id_",
        alphabet="abcdefg1234",
        primary_key=True,
    )

    # A short cryptographically secure random string of length 22 and the default alphabet.
    api_key = ShortUUIDField(length=22) 
```

The field is the same as the `CharField`, with a `length` argument (the length of the
ID for cryptographically secure random strings), an `alphabet` argument, and the `default` 
argument removed. Everything else is exactly the same, e.g. `index`, `help_text`, `max_length`, 
etc.

If you do not provide a `length` parameter, the field will generate a default value using
`ShortUUID.uuid` which will be universally unique.

However, if you provide a `length` parameter, the field will genrate a default value using
`ShortUUID.random` which WILL NOT BE universally unique.



Compatibility note
------------------

Versions of ShortUUID prior to 1.0.0 generated UUIDs with their MSB last, i.e. reversed.
This was later fixed, but if you have some UUIDs stored as a string with the old method,
you need to pass `legacy=True` to `decode()` when converting your strings back to UUIDs.

That option will go away in the future, so you will want to convert your UUIDs to
strings using the new method. This can be done like so:

```python
>>> new_uuid_str = encode(decode(old_uuid_str, legacy=True))
```

License
-------

`shortuuid` is distributed under the BSD license.
