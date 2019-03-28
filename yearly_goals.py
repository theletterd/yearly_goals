from flask import Flask
from flask import jsonify
from flask import render_template

from trello import Trello


app = Flask(__name__)


#stats = {}

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/year/<year>")
def year(year):
    stats = {}
    year = int(year)
    if year not in stats:
        print(f"Stats for {year} not found, hitting API")
        stats[year] = Trello.get_yearly_stats(year)
    return jsonify(stats[year])

@app.route("/years")
def available_years():
    return jsonify(Trello.get_available_years())

if __name__ == '__main__':
    app.run()


