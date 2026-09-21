# Get the three name parts as strings.
first_name = input("Enter your first name: ")
middle_initial = input("Enter your middle initial: ")
last_name = input("Enter your last name: ")

# The input() function returns strings, so + joins these strings together.
# Python adds numbers only when both operands are numeric values.
# Do this using a join() method of a list
full_name = " ".join([first_name, middle_initial, last_name])
print(f"The full name is: {full_name}")