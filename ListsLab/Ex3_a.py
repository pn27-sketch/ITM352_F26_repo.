responses = [5, 7, 3, 8]
responses.append(0)
responses.insert(2, 6)
print(responses)

# The same changes using list slicing and the + operator.
sliced_responses = [5, 7, 3, 8]
sliced_responses = sliced_responses + [0]
sliced_responses = sliced_responses[:2] + [6] + sliced_responses[2:]
print(sliced_responses)