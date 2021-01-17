from flask import Flask
from flask import Response
from flask import jsonify
from flask import send_from_directory
import flask_sqlalchemy
import flask_praetorian
import flask_cors
import json

app = Flask(__name__, static_url_path='')


def get_default_response(body={}):
    res = Response()
    res.headers['Content-type'] = "application/json"
    res.response = json.dumps(body)
    return res


@app.route('/')
def index():
    file = open("index.html", "r")
    return file.read()


@app.route('/swagger/<path:path>')
def send_swagger_files(path):
    return send_from_directory('swagger', path)


@app.route("/spec")
def spec():
    file = open("swagger/index.html", "r")
    return file.read()


@app.route("/test")
def test():
    return get_default_response(body={'message': 'Test successful'})
