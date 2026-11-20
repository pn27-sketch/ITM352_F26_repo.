from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("quiz_mockup_index.html")


@app.route("/quiz")
def take_quiz():
    return render_template("quiz_mockup_question.html")


@app.route("/results")
def results():
    return render_template("quiz_mockup_results.html")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")