"""Choose two distinct requirements using the student's ID digits."""


def choose_requirements(student_id, requirements):
    """Return the two requirements selected by the Ex3_b flowchart."""
    student_id = str(student_id).strip()
    if not student_id or not student_id.isdigit():
        raise ValueError("Student ID must contain digits only.")
    if len(requirements) < 2:
        raise ValueError("At least two requirements are needed.")

    digits = [int(digit) for digit in student_id]
    requirement_count = len(requirements)

    first_number = sum(digits) % requirement_count + 1

    nonzero_product = 1
    for digit in digits:
        if digit != 0:
            nonzero_product *= digit
    second_number = nonzero_product % requirement_count + 1

    while second_number == first_number:
        second_number = second_number % requirement_count + 1

    return requirements[first_number - 1], requirements[second_number - 1]


if __name__ == "__main__":
    additional_requirements = [
        "Requirement 1",
        "Requirement 2",
        "Requirement 3",
        "Requirement 4",
        "Requirement 5",
        "Requirement 6",
        "Requirement 7",
    ]
    student_id = input("Enter your student ID: ").strip()
    assigned_pair = choose_requirements(student_id, additional_requirements)

    print("Your assigned requirements are:")
    for requirement in assigned_pair:
        print(f"- {requirement}")