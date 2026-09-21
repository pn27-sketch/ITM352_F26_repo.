"""Functions can be passed as arguments because they are first-class objects.

Passing a function is useful when another function needs customizable behavior,
such as a callback that runs after an event or a key function used for sorting.
"""

from HandyMath import apply_function, exponent, max, min


x = 2
y = 3

print(apply_function(x, y, min))
print(apply_function(x, y, max))
print(apply_function(x, y, exponent))
