items = ("hello", 10, "goodbye", 3, "goodnight", 5)
user_input = input("Enter an item to add to the tuple: ")

appended_tuple = items + (user_input,)
print(appended_tuple)