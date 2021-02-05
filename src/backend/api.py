from flask import Flask
from flask import Response
from flask import send_from_directory
from flask import request
import flask
import flask_sqlalchemy
import flask_praetorian
import flask_cors
import json
import os
import uuid

statuses = ["unauthorised", "authorised"]

db = flask_sqlalchemy.SQLAlchemy()
guard = flask_praetorian.Praetorian()
cors = flask_cors.CORS()


class Users(db.Model):
    userId = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(255))

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


class medicalpickups(db.Model):
    pickupid = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    testid = db.Column(db.String(36))
    patientid = db.Column(db.String(36))
    drugid = db.Column(db.String(36))
    drugquantity = db.Column(db.Integer())
    scheduleddate = db.Column(db.Date())
    reviewdate = db.Column(db.Date())
    isauthorised = db.Column(db.Boolean())
    pickupstatus = db.Column(db.String(25))

    @classmethod
    def lookup(cls, pickupId):
        return cls.query.filter_by(pickupId=pickupId).one_or_none()

    @classmethod
    def identify(cls, pickupId):
        return cls.query.get(pickupId)

    @property
    def identity(self):
        return self.pickupId


class contactdetails(db.Model):
    contactdetailid = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    phonenumber = db.Column(db.String(36))
    emailaddress = db.Column(db.String(36))
    addressline1 = db.Column(db.String(255))
    addressline2 = db.Column(db.String(255))
    addressline3 = db.Column(db.String(255))
    addressline4 = db.Column(db.String(255))
    postcode = db.Column(db.String(255))

    @classmethod
    def lookup(cls, contactdetailid):
        return cls.query.filter_by(pickupId=contactdetailid).one_or_none()

    @classmethod
    def identify(cls, contactdetailid):
        return cls.query.get(contactdetailid)

    @property
    def identity(self):
        return self.contactdetailid


class tests(db.Model):
    testid = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    drugid = db.Column(db.String(36))
    status = db.Column(db.String(36))

    @classmethod
    def lookup(cls, testid):
        return cls.query.filter_by(pickupId=testid).one_or_none()

    @classmethod
    def identify(cls, testid):
        return cls.query.get(testid)

    @property
    def identity(self):
        return self.testid


class patients(db.Model):
    testid = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    drugid = db.Column(db.String(36))
    status = db.Column(db.String(36))

    @classmethod
    def lookup(cls, testid):
        return cls.query.filter_by(pickupId=testid).one_or_none()

    @classmethod
    def identify(cls, testid):
        return cls.query.get(testid)

    @property
    def identity(self):
        return self.testid


def init():
    # Initialize the flask-praetorian instance for the app
    guard.init_app(app, Users)

    # Initialize a local database for the example
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_URL + "/" + DB_NAME
    db.init_app(app)

    # Initializes CORS so that the api_tool can talk to the example app
    cors.init_app(app)

    # Add users for the example
    with app.app_context():
        db.create_all()
        if db.session.query(Users).filter_by(username=DEFAULT_ACCOUNT_USERNAME).count() < 1:
            db.session.add(Users(
              username=DEFAULT_ACCOUNT_USERNAME,
              password=guard.hash_password(DEFAULT_ACCOUNT_PASSWORD),
              role=DEFAULT_ACCOUNT_USERNAME
                ))
        db.session.commit()


# Initialise flask app
app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.debug = True
app.config['SECRET_KEY'] = 'JUIANFuiBfdaukfbeaifuIUBUIB'
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

# Initialize environment variables
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_URL = os.environ.get('DB_URL')
DB_NAME = os.environ.get('DB_NAME')
DEFAULT_ACCOUNT_USERNAME = os.environ.get('DEFAULT_ACCOUNT_USERNAME')
DEFAULT_ACCOUNT_PASSWORD = os.environ.get('DEFAULT_ACCOUNT_PASSWORD')
DEFAULT_ACCOUNT_ROLE = os.environ.get('DEFAULT_ACCOUNT_ROLE')
init()


def get_default_response(body={}):
    res = Response()
    res.headers['Content-type'] = "application/json"
    res.data = json.dumps(body)
    return res


@app.route('/')
def index():
    file = open("index.html", "r")
    return file.read()


@app.route('/api/swagger/<path:path>')
def send_swagger_files(path):
    return send_from_directory('swagger', path)


# Returns YAML documentation
@app.route("/api/spec")
def spec():
    file = open("swagger/index.html", "r")
    return file.read()


@app.route('/api/login', methods=['POST'])
def login():
    req = flask.request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return ret, 200


# Endpoint for unit tests to verify roles are working as expected
@app.route('/api/test/auth', methods=['GET'])
@flask_praetorian.auth_required
def test_auth():
    role = flask_praetorian.current_user().role
    return get_default_response({"role": role})


@app.route('/api/refresh', methods=['POST'])
def refresh():
    print("refresh request")
    old_token = flask.request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200


@app.route('/api/pickups', methods=['GET'])
@flask_praetorian.auth_required
def get_pickups():
    arr = []
    with app.app_context():
        for instance in db.session.query(medicalpickups):
            arr.append({"pickup_id": instance.pickupid,
                        "drug_quantity": instance.drugquantity,
                        "scheduled_date": str(instance.scheduleddate),
                        "review_date": str(instance.reviewdate),
                        "is_authorised": statuses[instance.isauthorised],
                        "pickup_status": instance.pickupstatus})
        return get_default_response(arr)


@app.route('/api/pickup', methods=['GET'])
@flask_praetorian.auth_required
def get_pickup():
    if request.args.get("pickup_id") is None:
        return get_default_response({"message": "Parameter required: pickup_id",
                                     "status_code": 400}), 400

    query = db.session.query(medicalpickups).filter_by(pickupid=request.args.get("pickup_id"))

    if query.count() < 1:
        return get_default_response({"message": "No pick up with that ID could be found",
                                     "status_code": 404}), 404

    instance = query.first()

    return_value = {"pickup_id": instance.pickupid,
                    "test_id": instance.testid,
                    "patient_id": instance.patientid,
                    "drug_id": instance.drugid,
                    "drug_quantity": instance.drugquantity,
                    "scheduled_date": str(instance.scheduleddate),
                    "review_date": str(instance.reviewdate),
                    "is_authorised": statuses[instance.isauthorised],
                    "pickup_status": instance.pickupstatus}

    return get_default_response(return_value)


@app.route('/api/test', methods=['GET'])
@flask_praetorian.auth_required
def get_test():
    if request.args.get("test_id") is None:
        return get_default_response({"message": "Parameter required: test_id",
                                     "status_code": 400}), 400

    query = db.session.query(tests).filter_by(testid=request.args.get("test_id"))

    if query.count() < 1:
        return get_default_response({"message": "No test with that ID could be found",
                                     "status_code": 404}), 404

    instance = query.first()

    return_value = {
                    "test_id": instance.testid,
                    "drug_id": instance.drugid,
                    "status": instance.status,
    }

    return get_default_response(return_value)


@app.route('/api/contact', methods=['GET'])
@flask_praetorian.auth_required
def get_contact():
    if request.args.get("contact_id") is None:
        return get_default_response({"message": "Parameter required: contact_id",
                                     "status_code": 400}), 400

    query = db.session.query(contactdetails).filter_by(contactdetailid=request.args.get("contact_id"))

    if query.count() < 1:
        return get_default_response({"message": "No contact with that ID could be found",
                                     "status_code": 404}), 404

    instance = query.first()

    return_value = {
        "contact_id": instance.contactdetailid,
        "phone_number": instance.phonenumber,
        "email_address": instance.emailaddress,
        "address_line_1": instance.addressline1,
        "address_line_2": instance.addressline2,
        "address_line_3": instance.addressline3,
        "address_line_4": instance.addressline4,
        "postcode": instance.postcode,
    }

    return get_default_response(return_value)
