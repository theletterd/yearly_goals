.DEFAULT_GOAL := run-dev

run-dev:
	FLASK_APP=yearly_goals.py python -m flask run --host=0.0.0.0
