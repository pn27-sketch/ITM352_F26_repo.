respondent_ids = (1012, 1035, 1021, 1053)

# A tuple does not have an append() method. Catch the error so the rest of
# the example can still run.
try:
	respondent_ids.append(1011)
except AttributeError as error:
	print(f"The append() attempt fails: {error}")

# The + operator creates a new tuple containing the original values and 1011.
respondent_ids = respondent_ids + (1011,)
print(respondent_ids)