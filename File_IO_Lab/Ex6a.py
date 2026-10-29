import json
from pathlib import Path

json_file = Path(__file__).resolve().parent / "quiz_questions.json"

with json_file.open("r", encoding="utf-8") as file:
    quiz_questions = json.load(file)

print(json.dumps(quiz_questions, indent=2))