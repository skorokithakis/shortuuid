# flake8: noqa
import pkg_resources
from shortuuid.main import decode
from shortuuid.main import encode
from shortuuid.main import get_alphabet
from shortuuid.main import random
from shortuuid.main import set_alphabet
from shortuuid.main import ShortUUID
from shortuuid.main import uuid

try:
    __version__ = pkg_resources.get_distribution("shortuuid").version
except pkg_resources.DistributionNotFound:
    __version__ = "0.0.0"
