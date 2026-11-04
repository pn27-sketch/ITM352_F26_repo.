import pandas as pd

ages = [25, 30, 22, 35, 28, 40, 50, 18, 60, 45]

names = [
    "Joe",
    "Jaden",
    "Max",
    "Sidney",
    "Evgeni",
    "Taylor",
    "Pia",
    "Luis",
    "Blanca",
    "Cyndi",
]

gender = ["M", "M", "M", "F", "M", "F", "F", "M", "F", "F"]

age_gender = list(zip(ages, gender))
individuals = pd.DataFrame(
    age_gender,
    index=names,
    columns=["Age", "Gender"],
)

print("Individuals:")
print(individuals)

print("\nDataFrame summary:")
print(individuals.describe())

print("\nAverage age by gender:")
print(individuals.groupby("Gender")["Age"].mean())