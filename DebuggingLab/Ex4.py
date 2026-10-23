# Hypothesis: the second call requests index 5, but a five-item list ends at index 4.
def get_element(items, index):
    return items[index]


my_list = [1, 2, 3, 4, 5]
print(get_element(my_list, 2))
print(get_element(my_list, 4))