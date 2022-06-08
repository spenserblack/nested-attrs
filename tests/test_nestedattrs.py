from unittest import TestCase

from src.nested_attrs import ndelattr, ngetattr, nhasattr, nsetattr

from .mock import Anything


class NestedHasAttrTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mock = Anything(a=1, nested=Anything(a=2, c=3), b=2)

    def test_has_top_level_attr(self):
        """
        It should return True just like the built-in hasattr.
        """
        self.assertTrue(nhasattr(self.mock, "a"))
        self.assertTrue(nhasattr(self.mock, "b"))

    def test_has_not_top_level_attr(self):
        """
        It should return False just like the built-in hasattr.
        """
        self.assertFalse(nhasattr(self.mock, "c"))

    def test_has_nested_attr(self):
        self.assertTrue(nhasattr(self.mock, "nested.a"))
        self.assertTrue(nhasattr(self.mock, "nested.c"))

    def test_has_not_nested_attr(self):
        self.assertFalse(nhasattr(self.mock, "nested.b"))


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
            AttributeError, r"'Anything\.nested' has no attribute 'd'"
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


class NestedSetAttrTests(TestCase):
    def setUp(self):
        super().setUp()
        self.mock = Anything(a=1, nested=Anything(a=2, c=3), b=2)

    def test_set_top_level_attr(self):
        """
        It should set an attribute just like the built-in setattr.
        """
        nsetattr(self.mock, "a", 5)
        self.assertEqual(self.mock.a, 5)
        self.assertEqual(self.mock.b, 2)

    def test_set_nested_attr(self):
        nsetattr(self.mock, "nested.c", 99)
        self.assertEqual(self.mock.nested.c, 99)
        self.assertEqual(self.mock.nested.a, 2)

    def test_no_parent_attr_raises(self):
        """
        It should raise an error for an attribute that does not exist.
        """
        with self.assertRaisesRegex(
            AttributeError, r"'Anything' has no attribute 'notsted'"
        ):
            nsetattr(self.mock, "notsted.c", 4)
        with self.assertRaisesRegex(
            AttributeError, r"'Anything\.nested' has no attribute 'x'"
        ):
            nsetattr(self.mock, "nested.x.d", 4)


class NestedDelAttrTests(TestCase):
    def setUp(self):
        super().setUp()
        self.mock = Anything(a=1, nested=Anything(a=2, c=3), b=2)

    def test_del_top_level_attr(self):
        """
        It should delete an attribute just like the built-in delattr.
        """
        ndelattr(self.mock, "a")
        self.assertFalse(hasattr(self.mock, "a"))
        self.assertTrue(hasattr(self.mock.nested, "a"))

    def test_del_nested_attr(self):
        ndelattr(self.mock, "nested.c")
        self.assertFalse(hasattr(self.mock.nested, "c"))
        self.assertTrue(hasattr(self.mock.nested, "a"))

    def test_no_parent_attr_raises(self):
        """
        It should raise an error for an attribute that does not exist.
        """
        with self.assertRaisesRegex(
            AttributeError, r"'Anything' has no attribute 'notsted'"
        ):
            ndelattr(self.mock, "notsted.c")
        with self.assertRaisesRegex(
            AttributeError, r"'Anything\.nested' has no attribute 'x'"
        ):
            ndelattr(self.mock, "nested.x.d")
