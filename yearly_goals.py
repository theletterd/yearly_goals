import datetime

from flask import Flask
from flask import jsonify

from trello import Trello

app = Flask(__name__)

@app.route("/")
def current_year():
    current_year = datetime.date.today().year
    return jsonify(Trello.get_yearly_stats(current_year))

@app.route("/<year>")
def year(year):
    return jsonify(Trello.get_yearly_stats(int(year)))

if __name__ == '__main__':
    app.run()
