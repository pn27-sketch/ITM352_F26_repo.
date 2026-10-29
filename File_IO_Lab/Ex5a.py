import json
from pathlib import Path

assignment_questions = (
    Path(__file__).resolve().parents[1] / "Assignment#1" / "questions.json"
)
output_file = Path(__file__).resolve().parent / "quiz_questions.json"

with assignment_questions.open("r", encoding="utf-8") as file:
    quiz_questions = json.load(file)

with output_file.open("w", encoding="utf-8") as file:
    json.dump(quiz_questions, file, indent=2)

print(f"Quiz questions saved to {output_file.name}")