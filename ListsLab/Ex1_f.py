# Get the three name parts as strings.
first_name = input("Enter your first name: ")
middle_initial = input("Enter your middle initial: ")
last_name = input("Enter your last name: ")

# The input() function returns strings, so + joins these strings together.
# Python adds numbers only when both operands are numeric values.
# Do this using the format() method for a string but unpacking the list as the argument
full_name = [first_name, middle_initial, last_name]
print("The full name is: {} {} {}".format(*full_name))