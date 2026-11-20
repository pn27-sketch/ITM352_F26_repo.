import json
import random
import secrets
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

QUESTIONS_FILE = Path(__file__).resolve().parent.parent / "Assignment#1" / "questions.json"
LABELS = "ABCD"


def load_questions():
    with QUESTIONS_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def render_question(questions, error=None):
    question_index = session["question_index"]
    question_id = session["question_order"][question_index]
    question = questions[question_id]
    answer_order = session["answer_orders"][question_id]
    choices = [
        {"label": LABELS[position], "text": question["answers"][answer_index]["text"]}
        for position, answer_index in enumerate(answer_order)
    ]
    return render_template(
        "quiz_question.html",
        question=question["question"],
        choices=choices,
        question_number=question_index + 1,
        question_count=len(questions),
        error=error,
    )


@app.route("/")
def home():
    return render_template("quiz_start.html")


@app.route("/start", methods=["POST"])
def start_quiz():
    questions = load_questions()
    question_order = list(range(len(questions)))
    random.shuffle(question_order)

    answer_orders = []
    for question in questions:
        answers = question["answers"]
        if not answers or len(answers) > len(LABELS):
            raise ValueError("A question must have between 1 and 4 answers")
        answer_order = list(range(len(answers)))
        random.shuffle(answer_order)
        answer_orders.append(answer_order)

    session["question_order"] = question_order
    session["answer_orders"] = answer_orders
    session["question_index"] = 0
    session["score"] = 0
    return redirect(url_for("show_question"))


@app.route("/question")
def show_question():
    if "question_order" not in session:
        return redirect(url_for("home"))

    questions = load_questions()
    if session["question_index"] >= len(questions):
        return render_template(
            "quiz_result.html",
            score=session["score"],
            question_count=len(questions),
        )
    return render_question(questions)


@app.route("/answer", methods=["POST"])
def submit_answer():
    if "question_order" not in session:
        return redirect(url_for("home"))

    questions = load_questions()
    question_index = session["question_index"]
    if question_index >= len(questions):
        return redirect(url_for("show_question"))

    question_id = session["question_order"][question_index]
    question = questions[question_id]
    answer_order = session["answer_orders"][question_id]
    choice = request.form.get("choice", "").strip().upper()
    valid_labels = LABELS[:len(answer_order)]
    if choice not in valid_labels:
        return render_question(questions, "Please choose one of the listed labels.")

    answer_index = answer_order[valid_labels.index(choice)]
    if question["answers"][answer_index]["correct"]:
        session["score"] += 1
    session["question_index"] += 1
    return redirect(url_for("show_question"))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")