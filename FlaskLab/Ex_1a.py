from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to Patrick Nguyen's web site!"


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")