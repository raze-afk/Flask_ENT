import flask
from flask import request, jsonify
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '<h1>Distant Reading Archive</h1>'

app.run()
