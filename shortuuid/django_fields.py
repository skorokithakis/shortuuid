from django.db import models
from django.utils.translation import gettext_lazy as _

from . import ShortUUID


class ShortUUIDField(models.CharField):
    description = _("A short UUID field.")

    def __init__(self, *args, **kwargs):
        self.length = kwargs.pop("length", 22)
        self.prefix = kwargs.pop("prefix", "")

        if "max_length" not in kwargs:
            # If `max_length` was not specified, set it here.
            kwargs["max_length"] = self.length + len(self.prefix)

        self.alphabet = kwargs.pop("alphabet", None)
        kwargs["default"] = self._generate_uuid

        super().__init__(*args, **kwargs)

    def _generate_uuid(self):
        """Generate a short random string."""
        return self.prefix + ShortUUID(alphabet=self.alphabet).random(
            length=self.length
        )

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["alphabet"] = self.alphabet
        kwargs["length"] = self.length
        kwargs["prefix"] = self.prefix
        kwargs.pop("default", None)
        return name, path, args, kwargs
