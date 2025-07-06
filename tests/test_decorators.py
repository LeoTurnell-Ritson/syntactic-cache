import unittest

from syntactic_cache import do_not_make_cached_property, make_cached_properties


class TestDecorators(unittest.TestCase):
    """Test suite for decorators in syntactic_cache module."""

    def test_make_cached_properties(self):
        """Test that make_cached_properties create a property from get prefix."""

        @make_cached_properties
        class TestClass:

            def __init__(self, value):
                self._value = value
                self.call_count = 0

            def get_square(self):
                self.call_count += 1
                return self._value ** 2

        instance = TestClass(2)
        self.assertEqual(instance.get_square(), 4)
        self.assertEqual(instance.call_count, 1)

        # Check that the property cache is created.
        self.assertFalse(hasattr(instance, "_cached_properties"))
        self.assertEqual(instance.square, 4)
        self.assertTrue(hasattr(instance, "_cached_properties"))

        # Check that the get_square method has been evaluated again.
        self.assertEqual(instance.call_count, 2)

        # Check that the cached property is stored in the instance.
        self.assertEqual(instance._cached_properties, {"get_square": 4})

        # Check that the cached property can be accessed directly, and no
        # additional calls to the original method are made.
        _ = instance.square
        self.assertEqual(instance.call_count, 2)

    def test_make_cached_properties_does_not_cache_calls_to_original_method(self):
        """Test that make_cached_properties does not cache existing methods."""
        @make_cached_properties
        class TestClass:
            def __init__(self, value):
                self._value = value

            def get_square(self):
                return self._value ** 2

        instance = TestClass(2)
        self.assertEqual(instance.get_square(), 4)
        self.assertFalse(hasattr(instance, "_cached_properties"))

    def test_make_cached_properties_skips_decorated_methods(self):
        """Test that make_cached_properties skips decorated methods."""
        @make_cached_properties
        class TestClass:
            def __init__(self, value):
                self._value = value

            @do_not_make_cached_property
            def get_square(self):
                return self._value ** 2

        instance = TestClass(2)
        self.assertEqual(instance.get_square(), 4)
        with self.assertRaises(AttributeError):
            _ = instance.square

    def test_make_cached_properties_skips_not_syntax(self):
        """Test that make_cached_properties skips methods with alt. prefix."""
        @make_cached_properties
        class TestClass:
            def __init__(self, value):
                self._value = value

            def make_square(self):
                return self._value ** 2

        instance = TestClass(2)
        self.assertEqual(instance.make_square(), 4)
        with self.assertRaises(AttributeError):
            _ = instance.square

    def test_make_cached_properties_raises_value_error_if_clash(self):
        """Test that make_cached_properties raises ValueError if a clash occurs."""
        with self.assertRaises(ValueError):
            @make_cached_properties
            class TestClass:
                square = None

                def get_square(self):
                    pass

    def test_make_cached_properties_skip_methods_with_multiple_arguments(self):
        """Test that make_cached_properties skips methods with multiple arguments."""
        @make_cached_properties
        class TestClass:
            def __init__(self, value):
                self._value = value

            def get_power(self, power):
                return self._value ** power

        instance = TestClass(2)
        self.assertEqual(instance.get_power(2), 4)
        with self.assertRaises(AttributeError):
            _ = instance.square
