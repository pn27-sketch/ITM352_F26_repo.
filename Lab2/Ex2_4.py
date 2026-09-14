...
"Write Python code that uses the input built-in function to ask the user to enter a decimal formatted number between 1 and 100."
...

number = float(input("Please enter a decimal formatted number between 1 and 100: "))

# Square the number using the exponentiation operator
#add a rounding feature to round the squared number to 2 decimal places
squared = round(number ** 2, 2)

print("You entered the number: " + str(number)+ " is: " + str(squared))
