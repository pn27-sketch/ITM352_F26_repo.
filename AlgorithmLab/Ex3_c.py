"""Assign a pair by indexing a shuffled list of requirement pairs."""

import random


def assign_pair(student_id, requirement_count, rng=None):
    """Return the shuffled pair selected by an eight-digit student ID."""
    student_id = str(student_id).strip()
    if len(student_id) != 8 or not student_id.isdigit():
        raise ValueError("Student ID must be exactly 8 digits.")
    if requirement_count < 2:
        raise ValueError("At least two requirements are needed.")

    pairs = []
    for first in range(1, requirement_count):
        for second in range(first + 1, requirement_count + 1):
            pairs.append((first, second))

    (rng if rng is not None else random).shuffle(pairs)

    index = (int(student_id) - 10_000_000) % len(pairs)
    return pairs[index]


if __name__ == "__main__":
    requirement_count = int(input("Enter the number of requirements: "))
    student_id = input("Enter your 8-digit student ID: ")

    pair = assign_pair(student_id, requirement_count)
    print(f"Assigned requirements: {pair[0]} and {pair[1]}")