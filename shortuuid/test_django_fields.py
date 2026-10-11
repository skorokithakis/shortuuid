import unittest
from unittest.mock import patch

from django.db.migrations.writer import MigrationWriter

from shortuuid.django_fields import ShortUUIDField


class ShortUUIDFieldTest(unittest.TestCase):
    def test_clone_preserves_unsorted_alphabet(self):
        field = ShortUUIDField(
            alphabet="cba", dont_sort_alphabet=True, length=4, prefix="id_"
        )
        clone = field.clone()

        with patch("shortuuid.main.secrets.choice", side_effect=lambda chars: chars[0]):
            self.assertEqual(field.get_default(), "id_cccc")
            self.assertEqual(clone.get_default(), "id_cccc")

    def test_migration_preserves_unsorted_alphabet(self):
        field = ShortUUIDField(alphabet="cba", dont_sort_alphabet=True)
        serialized, imports = MigrationWriter.serialize(field)
        namespace = {}
        exec("\n".join(imports), namespace)
        restored = eval(serialized, namespace)

        self.assertTrue(restored.dont_sort_alphabet)
        self.assertEqual(restored.alphabet, "cba")

    def test_default_sorting_is_omitted_from_migrations(self):
        for options in ({}, {"dont_sort_alphabet": False}):
            with self.subTest(options=options):
                field = ShortUUIDField(alphabet="cba", **options)
                self.assertNotIn("dont_sort_alphabet", field.deconstruct()[3])
                self.assertFalse(field.clone().dont_sort_alphabet)
