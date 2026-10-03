LOWER_LIMIT = 5
UPPER_LIMIT = 10


def describe_list(values):
	item_count = len(values)

	if item_count < LOWER_LIMIT:
		return "The list has fewer than 5 elements."
	elif LOWER_LIMIT <= item_count <= UPPER_LIMIT:
		return "The list has between 5 and 10 elements, inclusive."
	else:
		return "The list has more than 10 elements."


sample_list = ["apple", 42, 3.14, True, None, "pear"]
print(describe_list(sample_list))

test_values = ["red", 7, 2.5, True, None, "blue", 9, False, "green", 0, "gold"]
test_lengths = (0, LOWER_LIMIT - 1, LOWER_LIMIT, UPPER_LIMIT, UPPER_LIMIT + 1)
test_cases = [test_values[:size] for size in test_lengths]

for test_list in test_cases:
	print(f"Length {len(test_list)}: {describe_list(test_list)}")