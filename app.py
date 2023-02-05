import os

from flask import Flask, render_template

from get_ticker_info import get_ticker_info

app = Flask(__name__)


@app.route("/<tickers>")
def index(tickers):
    return render_template(
        "main.html",
        tickers=get_ticker_info(tickers.upper().split(",")),
    )


@app.route("/github", methods=["POST"])
def github():
    os.system("sudo systemctl restart app")
    return "ok"


if __name__ == "__main__":
    app.run()
