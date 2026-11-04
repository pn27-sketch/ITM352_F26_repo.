import numpy as np

household_income_percentiles = [
    (10, 14629),
    (20, 25600),
    (30, 37002),
    (40, 50000),
    (50, 63179),
    (60, 79542),
    (70, 100162),
    (80, 130000),
    (90, 184292),
]

household_income_array = np.array(household_income_percentiles)

print("Array dimensions:", household_income_array.shape)
print("Number of elements:", household_income_array.size)
print("\nPercentile\tHousehold Income")
for percentile, income in household_income_array:
    print(f"{percentile}\t\t{income:,}")