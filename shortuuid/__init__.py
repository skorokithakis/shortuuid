""" Concise UUID generation. """

import uuid as _uu

# Define our alphabet.
_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def encode(uuid):
    """
    Encodes a UUID into a string (LSB first) according to the alphabet
    If leftmost (MSB) bits 0, string might be shorter
    """
    unique_id = uuid.int
    alphabet_length = len(_ALPHABET)
    output = ""
    while unique_id > 0:
        digit = unique_id % alphabet_length
        output += _ALPHABET[digit]
        unique_id = int(unique_id / alphabet_length)
    return output

def decode(string):
    """
    Decodes a string according to the current alphabet into a UUID
    Raises ValueError when encountering illegal characters or too long string
    If string too short, fills leftmost (MSB) bits with 0.
    """
    number = 0
    for char in string[::-1]:
        value = _ALPHABET.index(char)
        number = number * len(_ALPHABET) + value
    return _uu.UUID(int = number)

def uuid(name=None):
    """
    Generate and return a UUID.

    If the name parameter is provided, set the namespace to the provided
    name and generate a UUID.
    """
    # If no name is given, generate a random UUID.
    if name is None:
        uuid = _uu.uuid4()
    elif not "http" in name:
        uuid = _uu.uuid5(_uu.NAMESPACE_DNS, name)
    else:
        uuid = _uu.uuid5(_uu.NAMESPACE_URL, name)
    return encode(uuid)

def get_alphabet():
    """Return the current alphabet used for new UUIDs."""
    return _ALPHABET

def set_alphabet(alphabet):
    """Set the alphabet to be used for new UUIDs."""
    global _ALPHABET

    try:
       set
    except NameError:
       from sets import Set as set

    # Turn the alphabet into a set and sort it to prevent duplicates
    # and ensure reproducibility.
    new_alphabet = "".join(sorted(set(alphabet)))
    if len(new_alphabet) > 1:
        _ALPHABET = new_alphabet
    else:
        raise ValueError("Alphabet with more than one unique symbols required.")
