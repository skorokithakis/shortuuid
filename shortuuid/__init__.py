""" Concise UUID generation. """

import uuid as _uu

# Define our alphabet.
_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def uuid(url=None):
    """
    Generate and return a UUID.

    If the url parameter is provided, set the namespace to the provided
    URL and generate a UUID.
    """
    # If no URL is given, generate a random UUID.
    if url is None:
        unique_id = _uu.uuid4().int
    else:
        unique_id = _uu.uuid3(_uu.NAMESPACE_URL, url).int

    alphabet_length = len(_ALPHABET)
    output = ""
    while unique_id > 0:
        digit = unique_id % alphabet_length
        output += _ALPHABET[digit]
        unique_id = int(unique_id / alphabet_length)
    return output   

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

