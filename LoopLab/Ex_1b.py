...
#Write Python code that uses a Python for-statement to create a list of elements that are the odd numbers between 1 and 50. Use range() and an if-statement in a “traditional” for loop
#Use range() and the fact an odd number is 2*num + 1
...

odd_numbers = []
for n in range(25):	
	odd_numbers.append(2*n + 1)
print(odd_numbers)