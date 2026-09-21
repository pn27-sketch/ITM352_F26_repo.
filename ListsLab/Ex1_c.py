# Get the three name parts as strings.
first_name = input("Enter your first name: ")
middle_initial = input("Enter your middle initial: ")
last_name = input("Enter your last name: ")

# The input() function returns strings, so + joins these strings together.
# Python adds numbers only when both operands are numeric values.
# Do this using the % Operator
print("The full name is: %s %s %s" % (first_name, middle_initial, last_name))