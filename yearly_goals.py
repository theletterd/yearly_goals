import datetime

from flask import Flask
from flask import jsonify

from trello import Trello

app = Flask(__name__)


from datetime import timedelta  
from flask import Flask, make_response, request, current_app  
from functools import update_wrapper

# copy-paste, should be temporary
def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):  
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

stats = {}

@app.route("/")
@crossdomain(origin='*')
def current_year():
    current_year = datetime.date.today().year
    if current_year not in stats:
        print(f"Stats for {current_year} not found, hitting API")
        stats[current_year] = Trello.get_yearly_stats(current_year)
    return jsonify(stats[current_year])

@app.route("/year/<year>")
@crossdomain(origin='*')
def year(year):
    year = int(year)
    if year not in stats:
        print(f"Stats for {year} not found, hitting API")
        stats[year] = Trello.get_yearly_stats(year)
    return jsonify(stats[year])

@app.route("/years")
@crossdomain(origin='*')
def available_years():
    return jsonify(Trello.get_available_years())

if __name__ == '__main__':
    app.run(host="0.0.0.0")
