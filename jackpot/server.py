from flask import Flask
from jackpot.database import Jackpotdb

app = Flask(__name__)


@app.route("/")
def jackpot():
    return "Jackpot!"


@app.route('/<game_name>/lucky_combination')
def show_lucky_combination(game_name):
    return db.get_latest_lucky_combination(game_name)


@app.route('/<game_name>/extras')
def show_extras(game_name):
    return db.get_latest_extras(game_name)


if __name__ == "__main__":
    db = Jackpotdb()
    app.run()
