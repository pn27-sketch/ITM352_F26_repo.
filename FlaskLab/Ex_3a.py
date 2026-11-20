import requests
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    url = "https://meme-api.com/gimme/wholesomememes"
    response = requests.request("GET", url, timeout=15)
    response.raise_for_status()
    meme = response.json()
    return render_template(
        "meme.html",
        meme_url=meme["url"],
        subreddit=meme["subreddit"],
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")