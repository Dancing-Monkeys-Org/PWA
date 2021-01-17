from flask import Flask
from flask import Response
from flask import jsonify
from flask import send_from_directory
import flask
import flask_sqlalchemy
import flask_praetorian
import flask_cors
import json
import os


db = flask_sqlalchemy.SQLAlchemy()
guard = flask_praetorian.Praetorian()
cors = flask_cors.CORS()


# A generic user model that might be used by an app powered by flask-praetorian
class User(db.Model):
    userId = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    roles = db.Column(db.String(255))
    # is_active = db.Column(db.Boolean, default=True, server_default='true')

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, userId):
        return cls.query.get(userId)

    @property
    def identity(self):
        return self.userId

    # def is_valid(self):
    #     return self.is_active


app = Flask(__name__, static_url_path='')

app.debug = True
app.config['SECRET_KEY'] = 'top secret'
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

# Initialize the flask-praetorian instance for the app
guard.init_app(app, User)

DB_USERNAME=os.environ.get('DB_USERNAME')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
DB_URL = "pwa-db.cgrwyltiiuin.us-east-2.rds.amazonaws.com"
DB_NAME = "MonkeyDB"

# Initialize a local database for the example
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_URL + "/" + DB_NAME
db.init_app(app)

# Initializes CORS so that the api_tool can talk to the example app
cors.init_app(app)


# Add users for the example
with app.app_context():
    db.create_all()
    if db.session.query(User).filter_by(username='admin').count() < 1:
        db.session.add(User(
            # userId='7211c77d-db69-4b21-bed4-c1bf80023594',
          username='admin',
          password=guard.hash_password('mastermonkey'),
          roles='admin'
            ))
    db.session.commit()


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


@app.route('/api/login', methods=['POST'])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/api/login -X POST \
         -d '{"username":"Yasoob","password":"strongpassword"}'
    """
    req = flask.request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return ret, 200