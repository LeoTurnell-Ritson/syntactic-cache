import functools


def _cached_property(func):
    """Decorator to create a cached property.

    This decorator will cache the result of the function on the instance
    so that subsequent accesses do not recompute the value.

    Returns:
        property: A property that caches the result of the function.

    """
    @functools.wraps(func)
    def wrapper(self):
        if not hasattr(self, '_cached_properties'):
            self._cached_properties = {}
        if func.__name__ not in self._cached_properties:
            self._cached_properties[func.__name__] = func(self)
        return self._cached_properties[func.__name__]

    return property(wrapper)


def make_cached_properties(*args):
    """Decorator create cached properties for methods.

    This decorator will convert methods that start with the specified prefixes
    into cached properties. It will skip methods that are not callable or have
    the @do_not_make_cached_property decorator applied, as well as methods that
    take positional arguments other than 'self'.

    Properties will have the prefix removed, so a method named 'get_value' will
    become a cached property named 'value' etc.

    Args:
        args (List[str]): A list of prefixes to match method names against.

    Returns:
        class: The class with methods converted to cached properties.

    """
    def decorator(cls):
        initial = cls.__dict__.copy()
        for arg in args:
            if not isinstance(arg, str):
                raise TypeError(f"Expected string argument, got {type(arg).__name__}")

        effective_args = [arg + '_' if not arg.endswith('_') else arg for arg in args]
        for name, method in initial.items():  # avoid modifying dict during iteration
            prefix = next((p for p in effective_args if name.startswith(p)), None)
            if (
                not callable(method)
                or not prefix
                or getattr(method, '_do_not_make_cached_property', False)
                or method.__code__.co_argcount > 1
            ):
                continue

            if hasattr(cls, name[len(prefix):]):
                msg = (
                    f"Cannot convert method '{name}' to cached property "
                    f"because '{name[len(prefix):]}' already exists in class. "
                    "Consider marking this method with the "
                    "@do_not_make_cached_property decorator to skip "
                    "this conversion."
                )
                raise ValueError(msg)

            setattr(
                cls,
                name[len(prefix):],
                _cached_property(method)
            )

        return cls

    return decorator


def do_not_make_cached_property(func):
    """Decorator to skip making a method a cached property.

    Returns:
        func [callable]: The original function with a flag set to
            skip generating a cached property.

    """
    func._do_not_make_cached_property = True
    return func
