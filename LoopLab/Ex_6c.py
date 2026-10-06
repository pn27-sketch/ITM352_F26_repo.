items = ("hello", 10, "goodbye", 3, "goodnight", 5)
user_input = input("Enter an item to add to the tuple: ")

try:
	items.append(user_input)
except AttributeError as error:
	print(f"An attempt was made to append {user_input!r} to the tuple.")
	print(f"Error: {error}")