# Hypothesis: the multiplication expression is split across lines incorrectly,
# and the function call uses undefined names instead of the assigned inputs.
def multiply(x, y):
    result = x * y
    return result


a = 5
b = 6

result = multiply(a, b)
print(result)