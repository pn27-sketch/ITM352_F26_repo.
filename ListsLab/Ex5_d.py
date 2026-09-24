email = input("Enter an email address: ")

# Parse the email address using split().
username, domain = email.split("@", 1)
print("Using split():")
print("Username:", username)
print("Domain:", domain)

# Parse the email address using index() and slicing.
at_index = email.index("@")
username = email[:at_index]
domain = email[at_index + 1:]
print("Using index() and slicing:")
print("Username:", username)
print("Domain:", domain)