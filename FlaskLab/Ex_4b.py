from flask import Flask, render_template, request

app = Flask(__name__)

QUESTION = "Who holds the NFL career rushing yards record?"
ANSWERS = ["Walter Payton", "Emmitt Smith", "Barry Sanders", "Frank Gore"]


@app.route("/")
def home():
    return render_template("quiz_app_home.html")


@app.route("/quiz")
def quiz():
    return render_template(
        "quiz_app_question.html",
        question=QUESTION,
        answers=ANSWERS,
    )


@app.route("/results", methods=["GET", "POST"])
def results():
    selected_answer = request.form.get("answer")
    return render_template(
        "quiz_app_results.html",
        selected_answer=selected_answer,
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")