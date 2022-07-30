from django.db import models
from django.utils.translation import gettext_lazy as _

from . import ShortUUID

from typing import Any, Dict, Tuple


class ShortUUIDField(models.CharField):
    description = _("A short UUID field. Without a length parameter, generates a short UUID.  Providing a length, only generates "
    "a random string of the provided length. Not guaranteed universally unique.")

    def __init__(self, *args: Tuple, **kwargs: Dict[str, Any]) -> None:
        """If called without a `length` parameter, generates a `ShortUUID` for the default value.  Guaranteed universally unique.
        Length of the UUID is based on the size of the provided alphabet

        If the `length` parameter is provided, generates a cryptographically secure random string of that length (using os.urandom() internally).
        WARNING: This is NOT guaranteed to be universally unique as it is not a UUID, soley a random string.
        """
        self.length = kwargs.pop("length", None)
        self.prefix = kwargs.pop("prefix", "")
        self.alphabet = kwargs.pop("alphabet", None)

        if self.length is None:  # Generate a UUID
            required_length = self._shortuuid._length + len(self.prefix)
            if "max_length" in kwargs and kwargs["max_length"] < required_length:
                raise Exception(f"max_length too small to fit generated UUID of length {required_length} (including prefix)")
            if "max_length" not in kwargs:
                kwargs["max_length"] = required_length

            kwargs["default"] = self._generate_uuid
        else:  # User provided length, generate a random but not universally unique string
            required_length = self.length + len(self.prefix)
            if "max_length" not in kwargs:
                # If `max_length` was not specified, set it here.
                kwargs["max_length"] = required_length
            elif "max_length" in kwargs and kwargs["max_length"] < required_length:
                raise Exception(f"max_length too small to fit generated random of length {required_length} (including prefix)")

            kwargs["default"] = self._generate_random

        super().__init__(*args, **kwargs)

    def _generate_random(self) -> str:
        """Generate a cryptographically secure random string (using os.urandom() internally)
        WARNING: This is NOT guaranteed to be universally unique as it is not a UUID, soley a cryptographically secure random string.
        """
        return self.prefix + self._shortuuid.random(
            length=self.length
        )

    def _generate_uuid(self) -> str:
        """Generate a uuid"""
        return self.prefix + self._shortuuid.uuid()

    @property
    def _shortuuid(self) -> ShortUUID:
        if not hasattr(self, "__shortuuid"):
            self.__shortuuid = ShortUUID(alphabet=self.alphabet)
        return self.__shortuuid

    def deconstruct(self) -> Tuple[str, str, Tuple, Dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        kwargs["alphabet"] = self.alphabet
        kwargs["length"] = self.length
        kwargs["prefix"] = self.prefix
        kwargs.pop("default", None)
        return name, path, args, kwargs
