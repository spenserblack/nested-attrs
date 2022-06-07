from unittest import TestCase

from src.nestedattrs import ngetattr

from .mock import Anything


class NestedGetAttrTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mock = Anything(a=1, nested=Anything(a=2, c=3), b=2)

    def test_get_top_level_attr(self):
        """
        It should get an attribute just like the built-in getattr.
        """
        self.assertEqual(ngetattr(self.mock, "a"), 1)
        self.assertEqual(ngetattr(self.mock, "b"), 2)

    def test_no_top_level_attr_raises(self):
        """
        It should raise an error for an attribute that does not exist.
        """
        with self.assertRaises(AttributeError):
            ngetattr(self.mock, "d")

    def test_get_nested_attr(self):
        self.assertEqual(ngetattr(self.mock, "nested.a"), 2)
        self.assertEqual(ngetattr(self.mock, "nested.c"), 3)

    def test_no_nested_attr_raises(self):
        """
        It should raise an error for an attribute that does not exist.
        """
        with self.assertRaisesRegex(
            AttributeError, r"'Anything.nested' has no attribute 'd'"
        ):
            ngetattr(self.mock, "nested.d")

    def test_get_top_level_attr_with_default(self):
        """
        It should get an attribute or default just like the built-in getattr.
        """
        self.assertEqual(ngetattr(self.mock, "a", 99), 1)
        self.assertEqual(ngetattr(self.mock, "c", 99), 99)

    def test_get_nested_with_default(self):
        self.assertEqual(ngetattr(self.mock, "nested.a", 99), 2)
        self.assertEqual(ngetattr(self.mock, "nested.b", 99), 99)

    def test_fail_extra_args(self):
        """
        It should raise if 4 or more arguments are passed.
        """
        with self.assertRaises(TypeError):
            ngetattr(self.mock, "a", 1, 2)
