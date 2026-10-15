import json
import random

#Load questions from a JSON file
def load_questions():
    with open("questions.json") as file:
        return json.load(file)

#Present questions to the user and return the score, with optional parameters for random number generator, input function, output function, and maximum attempts
def present_question(
    questions, rng=random, input_fn=input, output_fn=print, max_attempts=1
):
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    questions = questions.copy()
    rng.shuffle(questions)
    score = 0

    output_fn("Welcome to the quiz!")
    for number, question in enumerate(questions, start=1):
        output_fn(f"Question {number} of {len(questions)}")
        answers = question["answers"].copy()
        rng.shuffle(answers)
        labels = "ABCD"
        if not answers or len(answers) > len(labels):
            raise ValueError("A question must have between 1 and 4 answers")

        output_fn(question["question"])
        for answer_number, answer in enumerate(answers):
            output_fn(f"{labels[answer_number]}. {answer['text']}")

        correct_labels = {
            labels[answer_number]
            for answer_number, answer in enumerate(answers)
            if answer["correct"]
        }

        valid_labels = labels[:len(answers)]
        attempts = 0
        while True:
            choice = input_fn(
                f"Choose an answer ({'/'.join(valid_labels)}): "
            ).strip().upper()

            if choice not in valid_labels:
                output_fn("Please choose one of the listed labels.")
                continue

            attempts += 1
            if choice in correct_labels:
                output_fn("Correct!")
                score += 1
                break

            if attempts == max_attempts:
                output_fn(
                    f"Incorrect. The correct answer was "
                    f"{' or '.join(sorted(correct_labels))}."
                )
                break

#Give a message to the user about their score at the end of the quiz
    output_fn(
        f"\nQuiz complete! You answered {score} of "
        f"{len(questions)} questions correctly."
    )
    return score

if __name__ == "__main__":
    present_question(load_questions())