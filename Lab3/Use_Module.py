import HandyMath


number_one = float(input("Enter the first number: "))
number_two = float(input("Enter the second number: "))

print(f"The midpoint is {HandyMath.midpoint(number_one, number_two)}")
print(f"The square root of the square of {number_one} is {HandyMath.squareroot(number_one ** .50)}")
print(f"{number_one} raised to the exponent of {number_two} is {HandyMath.exponent(number_one, number_two)}")
print(f"The maximum is {HandyMath.max(number_one, number_two)}")
print(f"The minimum is {HandyMath.min(number_one, number_two)}")