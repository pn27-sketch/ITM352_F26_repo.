...
#Write Python code that uses the Python while statement to create a list of elements that are even numbers from 1 to 50.
...
even_numbers = [2]
while even_numbers[-1] <= 50:
    next_number = even_numbers[-1] + 2
    if next_number > 50:
        break
    even_numbers.append(next_number)
print(even_numbers)