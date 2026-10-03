...
#Write Python code that uses a Python for-statement to create a list of elements that are the odd numbers between 1 and 50. Use range() and an if-statement in a “traditional” for loop
#Use range() and the fact an odd number is 2*num + 1
#Use range() with a step and no if-statement or using 2*num + 1
...

odd_numbers = []
for n in range(1, 50, 2):	
	odd_numbers.append(n)
print(odd_numbers)