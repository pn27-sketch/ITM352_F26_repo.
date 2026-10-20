"""Assign two additional requirements to each student."""

from itertools import combinations
import random


class RequirementAssigner:
    def __init__(self, requirements, rng=None):
        if len(requirements) < 2:
            raise ValueError("At least two requirements are needed.")
        if len(set(requirements)) != len(requirements):
            raise ValueError("Requirements must be unique.")

        self._rng = rng if rng is not None else random
        self._all_pairs = list(combinations(requirements, 2))
        self._rng.shuffle(self._all_pairs)
        self._next_pair = 0
        self.assignments = {}

    def assign(self, student):
        """Assign a pair once per student, delaying repeats until necessary."""
        if student in self.assignments:
            return self.assignments[student]

        if self._next_pair == len(self._all_pairs):
            self._rng.shuffle(self._all_pairs)
            self._next_pair = 0

        pair = self._all_pairs[self._next_pair]
        self._next_pair += 1
        self.assignments[student] = pair
        return pair


if __name__ == "__main__":
    additional_requirements = [
        "Requirement 1",
        "Requirement 2",
        "Requirement 3",
        "Requirement 4",
        "Requirement 5",
        "Requirement 6",
        "Requirement 7",
        "Requirement 8",
        "Requirement 9",
        "Requirement 10",
    ]
    assigner = RequirementAssigner(additional_requirements)

    student_name = input("Enter your name or student ID: ").strip()
    if not student_name:
        raise ValueError("A student name or ID is required.")

    assigned_pair = assigner.assign(student_name)
    print("Your assigned requirements are:")
    for requirement in assigned_pair:
        print(f"- {requirement}")

    print("\nInstructor assignment record:")
    for student, pair in assigner.assignments.items():
        print(f"{student}: {', '.join(pair)}")