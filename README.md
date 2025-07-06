# Syntactic Cache

![Tests](https://github.com/LeoTurnell-Ritson/syntactic-cache/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/LeoTurnell-Ritson/syntactic-cache/branch/master/graph/badge.svg)](https://codecov.io/gh/leoturnell-ritson/syntactic-cache/)
[![PyPI version](https://img.shields.io/pypi/v/syntactic-cache.svg)](https://pypi.org/project/syntactic-cache)

Syntactic Cache is a Python library that allows you to automatically create cached properties for methods in your classes, using the syntax of the methods to determine which methods should be cached. 

I.e, methods with the `get_` prefix will have a cached property created for them using the method name without the prefix, this allows for easy refactoring of existing code adding cached properties of functions 'for free'. The cache is a simple memory cache linked to each instance of the class. 

## Installation

You can install Syntactic Cache using pip.

```bash
pip install syntactic-cache
```

## Usage

Here's a simple example of how to use Syntactic Cache, curently the library support 'get_' and 'is_' prefixes for methods.

```python
from syntactic_cache import do_not_make_cached_property, make_cached_properties

@make_cached_properties
class MyClass:
    def __init__(self, value):
        self.value = value

    def get_power(self, exponent):
        return self.value ** exponent

    def get_square(self):
        return self.get_power(2)

    @do_not_make_cached_property
    def get_cube(self):
        return self.get_power(3)

    def is_even(self):
        return self.value % 2 == 0

instance = MyClass(3)

print(instance.get_square())  # 9, does not use the cache,
print(instance.get_cube())    # 27, does not use the cache.

print(instance.square)  # 9, sets and uses the cache.
print(instance.cube)    # Raises AttributeError, as making cached properties is disabled.
print(instance.power)  # Raises AttributeError, as will not make cached properties for methods with arguments.

print(instance.is_even())  # False, does not use the cache.
print(instance.even)  # False, sets and uses the cache.
```
