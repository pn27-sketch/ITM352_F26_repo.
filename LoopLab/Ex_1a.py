...
#Write Python code that uses a Python for-statement to create a list of elements that are the odd numbers between 1 and 50. Use range() and an if-statement in a “traditional” for loop
...

odd_numbers = []
for n in range(1, 50):
	if n % 2 == 1:
		odd_numbers.append(n)
print(odd_numbers)