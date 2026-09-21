def midpoint(x, y):
    return (x + y) / 2


def squareroot(n):
    return n**0.5


def exponent(base, exponent):
    return base**exponent


def max(x, y):
    return x if x >= y else y


def min(x, y):
    return x if x <= y else y


def apply_function(x, y, function):
    return f"The function {function.__name__} {x},{y} = {function(x, y)}"