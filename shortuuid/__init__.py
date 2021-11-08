# flake8: noqa
import importlib.metadata

from shortuuid.main import decode
from shortuuid.main import encode
from shortuuid.main import get_alphabet
from shortuuid.main import random
from shortuuid.main import set_alphabet
from shortuuid.main import ShortUUID
from shortuuid.main import uuid


try:
    _DISTRIBUTION_METADATA = importlib.metadata.metadata("shortuuid")
    __version__ = _DISTRIBUTION_METADATA["Version"]
except Exception:
    __version__ = "0.0.0"
