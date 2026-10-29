import csv
import os

file_path = "my_custom_sheet.csv.csv"
salaries = []

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
elif not os.access(file_path, os.R_OK):
    print(f"File is not readable: {file_path}")
else:
    print(f"File size: {os.path.getsize(file_path)} bytes")

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            salary = row.get("Annual_Salary")
            if salary:
                salaries.append(float(salary))

    average_salary = sum(salaries) / len(salaries)
    maximum_salary = max(salaries)
    minimum_salary = min(salaries)

    print(f"Average Annual Salary: ${average_salary:,.2f}")
    print(f"Maximum Annual Salary: ${maximum_salary:,.2f}")
    print(f"Minimum Annual Salary: ${minimum_salary:,.2f}")