...
#Write Python code that uses the input built-in function to ask the user to enter a temperature in the Fahrenheit temperature scale. The input function always returns a string value, so use the float built-in function to convert the value entered to a float data type and determine the equivalent temperature in the Celsius temperature scale (use the conversion factor °C = (°F – 32) × (5/9)). Print a message to the user stating the temperature in Fahrenheit that they entered and the equivalent temperature in Celsius. 
...

def fahrenheit_to_celsius(fahrenheit):
	return (fahrenheit - 32) * (5 / 9)


assert fahrenheit_to_celsius(32) == 0

fahrenheit = float(input("Please enter a temperature in the Fahrenheit temperature scale: "))
celsius = fahrenheit_to_celsius(fahrenheit)
print("You entered the temperature in Fahrenheit: " + str(fahrenheit) + " which is equivalent to: " + str(celsius) + " in Celsius.")