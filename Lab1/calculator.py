# Basic calculator program

print("Welcome to the calculator!")

while True:
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        continue

    print("Choose an operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    operation = input("Enter your choice (1-4): ")

    if operation == "1":
        result = num1 + num2
        print(f"Result: {num1} + {num2} = {result}")
    elif operation == "2":
        result = num1 - num2
        print(f"Result: {num1} - {num2} = {result}")
    elif operation == "3":
        result = num1 * num2
        print(f"Result: {num1} * {num2} = {result}")
    elif operation == "4":
        if num2 == 0:
            print("Error: Division by zero is not allowed.")
        else:
            result = num1 / num2
            print(f"Result: {num1} / {num2} = {result}")
    else:
        print("Invalid operation. Please choose a number from 1 to 4.")

    again = input("Would you like to perform another calculation? (y/n): ").lower()
    if again != "y":
        print("Goodbye!")
        break
