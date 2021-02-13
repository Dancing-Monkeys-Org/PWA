from flask import Flask
from flask import Response
from flask import send_from_directory
from flask import request
import flask
import flask_sqlalchemy
import flask_praetorian
# import flask_cors
import json
import os
import uuid
import datetime


statuses = ["unauthorised", "authorised"]

db = flask_sqlalchemy.SQLAlchemy()
guard = flask_praetorian.Praetorian()
# cors = flask_cors.CORS()


class Users(db.Model):
    userId = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(25))

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


class drugs(db.Model):
    drugid = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255))

    @classmethod
    def lookup(cls, drugid):
        return cls.query.filter_by(drugid=drugid).one_or_none()

    @classmethod
    def identify(cls, drugid):
        return cls.query.get(drugid)

    @property
    def identity(self):
        return self.drugid


class contactdetails(db.Model):
    contactdetailid = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    phonenumber = db.Column(db.String(255))
    emailaddress = db.Column(db.String(255))
    addressline1 = db.Column(db.String(255))
    addressline2 = db.Column(db.String(255))
    addressline3 = db.Column(db.String(255))
    addressline4 = db.Column(db.String(255))
    postcode = db.Column(db.String(7))

    @classmethod
    def lookup(cls, contactdetailid):
        return cls.query.filter_by(pickupId=contactdetailid).one_or_none()

    @classmethod
    def identify(cls, contactdetailid):
        return cls.query.get(contactdetailid)

    @property
    def identity(self):
        return self.contactdetailid


class standardtests(db.Model):
    standardtestid = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    testname = db.Column(db.String(255))

    @classmethod
    def lookup(cls, testname):
        return cls.query.filter_by(pickupId=testname).one_or_none()

    @classmethod
    def identify(cls, testname):
        return cls.query.get(testname)

    @property
    def identity(self):
        return self.testname


class patients(db.Model):
    patientid = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    gpid = db.Column(db.String(36))
    sensitivityid = db.Column(db.String(36))
    forename = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    sex = db.Column(db.String(1))
    age = db.Column(db.Integer())
    contactdetailid = db.Column(db.String(36))

    @classmethod
    def lookup(cls, patientid):
        return cls.query.filter_by(pickupId=patientid).one_or_none()

    @classmethod
    def identify(cls, patientid):
        return cls.query.get(patientid)

    @property
    def identity(self):
        return self.patientid


class gps(db.Model):
    gpid = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255))
    contactdetailid = db.Column(db.String(36))

    @classmethod
    def lookup(cls, testid):
        return cls.query.filter_by(pickupId=testid).one_or_none()

    @classmethod
    def identify(cls, testid):
        return cls.query.get(testid)

    @property
    def identity(self):
        return self.testid


class sensitivities(db.Model):
    sensitivityid = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    @classmethod
    def lookup(cls, sensitivityid):
        return cls.query.filter_by(pickupId=sensitivityid).one_or_none()

    @classmethod
    def identify(cls, sensitivityid):
        return cls.query.get(sensitivityid)

    @property
    def identity(self):
        return self.sensitivityid


class requiredtests(db.Model):
    requiredtestid = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    drugid = db.Column(db.String(36))
    standardtestid = db.Column(db.String(36))
    pharmacistdiscretion = db.Column(db.String(255))
    testfrequency = db.Column(db.Integer())

    @classmethod
    def lookup(cls, requiredtestid):
        return cls.query.filter_by(pickupId=requiredtestid).one_or_none()

    @classmethod
    def identify(cls, requiredtestid):
        return cls.query.get(requiredtestid)

    @property
    def identity(self):
        return self.requiredtestid


class patienthistory(db.Model):
    patienthistoryid = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    patientid = db.Column(db.String(36))
    standardtestid = db.Column(db.String(36))
    dateconducted = db.Column(db.Date())
    ispassed = db.Column(db.Boolean())

    @classmethod
    def lookup(cls, patienthistoryid):
        return cls.query.filter_by(pickupId=patienthistoryid).one_or_none()

    @classmethod
    def identify(cls, patienthistoryid):
        return cls.query.get(patienthistoryid)

    @property
    def identity(self):
        return self.patienthistoryid


class testrequests(db.Model):
    testrequestid = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    daterequested = db.Column(db.Date())
    standardtestid = db.Column(db.String(36))
    patientid = db.Column(db.String(36))
    gpid = db.Column(db.String(36))

    @classmethod
    def lookup(cls, testrequestid):
        return cls.query.filter_by(testrequestid=testrequestid).one_or_none()

    @classmethod
    def identify(cls, testrequestid):
        return cls.query.get(testrequestid)

    @property
    def identity(self):
        return self.testrequestid


def init():
    # Initialize the flask-praetorian instance for the app
    guard.init_app(app, Users)

    # Initialize a local database for the example
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_URL + "/" + DB_NAME
    db.init_app(app)

    # Initializes CORS so that the api_tool can talk to the example app
    # cors.init_app(app)

    # Add users for the example
    with app.app_context():
        db.create_all()
        if db.session.query(Users).filter_by(username=DEFAULT_ACCOUNT_USERNAME).count() < 1:
            db.session.add(Users(
              username=DEFAULT_ACCOUNT_USERNAME,
              password=guard.hash_password(DEFAULT_ACCOUNT_PASSWORD),
              role=DEFAULT_ACCOUNT_ROLE
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
                        "patient_id": instance.patientid,
                        "drug_id": instance.drugid,
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
                    "patient_id": instance.patientid,
                    "drug_id": instance.drugid,
                    "drug_quantity": instance.drugquantity,
                    "scheduled_date": str(instance.scheduleddate),
                    "review_date": str(instance.reviewdate),
                    "is_authorised": statuses[instance.isauthorised],
                    "pickup_status": instance.pickupstatus}

    return get_default_response(return_value)


@app.route('/api/pickup/status', methods=['PATCH'])
@flask_praetorian.auth_required
def update_pickup_status():
    valid_pickup_states = ["AWAITING_PHARMACIST_AUTHORISATION",
                           "AWAITING_CONFIRMATION",
                           "AWAITING_ASSEMBLY",
                           "AWAITING_COLLECTION",
                           "COLLECTED"]

    if flask_praetorian.current_user().role != "pharmacist":
        return get_default_response({"message": "Pharmacist role required to update pickup status",
                                     "status_code": 401}), 401

    if request.args.get("pickup_id") is None:
        return get_default_response({"message": "Parameter required: pickup_id",
                                     "status_code": 400}), 400

    pickup_id = request.args.get("pickup_id")

    if request.json is None:
        return get_default_response({"message": "JSON body required",
                                     "status_code": 400}), 400

    if "status" not in request.json:
        return get_default_response({"message": "Field required in JSON body: status",
                                     "status_code": 400}), 400

    if request.json['status'] not in valid_pickup_states:
        return get_default_response({"message": request.json['status'] + " Is not a valid status. This list of valid "
                                                                         "status are " + str(valid_pickup_states),
                                     "status_code": 400}), 400

    query = db.session.query(medicalpickups).filter_by(pickupid=pickup_id)
    pickup = query.first()
    if query.count() < 1:
        return get_default_response({"message": "No pickup with that ID could be found",
                                     "status_code": 404}), 404
    print(pickup.pickupstatus)
    if pickup.pickupstatus == "AWAITING_PHARMACIST_AUTHORISATION":
        authorised = json.loads(is_authorised(pickup_id).data)
        if not authorised['is_authorised']:
            return get_default_response({"message": "Cannot update status as pickup has unmet requirements",
                                         "status_code": 400}), 400

    pickup.pickupstatus = request.json['status']
    db.session.commit()
    return get_default_response({"message": "Successfully updated pickup status"})


@app.route('/api/drug', methods=['GET'])
@flask_praetorian.auth_required
def get_drug():
    if request.args.get("drug_id") is None:
         return get_default_response({"message": "Parameter required: drug_id",
                                     "status_code": 400}), 400
    query = db.session.query(drugs).filter_by(drugid=request.args.get("drug_id"))
    if query.count() < 1:
        return get_default_response({"message": "No drug with that ID could be found",
                                     "status_code": 404}), 404
    instance = query.first()
    return_value = {"drug_id": instance.drugid,
                    "name": instance.name}
    return get_default_response(return_value)


@app.route('/api/test', methods=['GET'])
@flask_praetorian.auth_required
def get_test():
    if request.args.get("test_id") is None:
        return get_default_response({"message": "Parameter required: test_id",
                                     "status_code": 400}), 400

    query = db.session.query(standardtests).filter_by(standardtestid=request.args.get("test_id"))

    if query.count() < 1:
        return get_default_response({"message": "No test with that ID could be found",
                                     "status_code": 404}), 404

    instance = query.first()

    return_value = {
                    "test_id": instance.standardtestid,
                    "name": instance.testname,
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


@app.route('/api/gp', methods=['GET'])
@flask_praetorian.auth_required
def get_gp():
    if request.args.get("gp_id") is None:
        return get_default_response({"message": "Parameter required: gp_id",
                                     "status_code": 400}), 400

    query = db.session.query(gps).filter_by(gpid=request.args.get("gp_id"))

    if query.count() < 1:
        return get_default_response({"message": "No gp with that ID could be found",
                                     "status_code": 404}), 404

    instance = query.first()

    return_value = {
        "gp_id": instance.gpid,
        "name": instance.name,
        "contact_id": instance.contactdetailid
    }

    return get_default_response(return_value)


@app.route('/api/patient', methods=['GET'])
@flask_praetorian.auth_required
def get_patient():
    if request.args.get("patient_id") is None:
        return get_default_response({"message": "Parameter required: patient_id",
                                     "status_code": 400}), 400

    query = db.session.query(patients).filter_by(patientid=request.args.get("patient_id"))

    if query.count() < 1:
        return get_default_response({"message": "No patient with that ID could be found",
                                     "status_code": 404}), 404

    instance = query.first()

    return_value = {
        "patient_id": instance.patientid,
        "gp_id": instance.gpid,
        "sensitivity_id": instance.sensitivityid,
        "forename": instance.forename,
        "surname": instance.surname,
        "sex": instance.sex,
        "age": instance.age,
        "contact_id": instance.contactdetailid,
    }

    return get_default_response(return_value)


@app.route('/api/sensitivity', methods=['GET'])
@flask_praetorian.auth_required
def get_sensitivity():
    if request.args.get("sensitivity_id") is None:
        return get_default_response({"message": "Parameter required: sensitivity_id",
                                     "status_code": 400}), 400

    query = db.session.query(sensitivities).filter_by(sensitivityid=request.args.get("sensitivity_id"))

    if query.count() < 1:
        return get_default_response({"message": "No sensitivity with that ID could be found",
                                     "status_code": 404}), 404

    instance = query.first()

    return_value = {
        "sensitivity_id": instance.sensitivityid,
        "name": instance.name,
        "description": instance.description
    }

    return get_default_response(return_value)


def is_authorised(pickup_id):
    if pickup_id is None:
        return get_default_response({"message": "Parameter required: pickup_id",
                                     "status_code": 400}), 400

    query = db.session.query(medicalpickups).filter_by(pickupid=pickup_id)

    if query.count() < 1:
        return get_default_response({"message": "No pick up with that ID could be found",
                                     "status_code": 404}), 404

    pickup = query.first()

    drug_id = pickup.drugid
    patient_id = pickup.patientid
    scheduled_date = pickup.scheduleddate

    requirements = []

    authorised = True

    # Loops through all test requirements
    for requirement in db.session.query(requiredtests).filter_by(drugid=drug_id):
        minimum_last_test_date = scheduled_date - datetime.timedelta(days=requirement.testfrequency)

        # Queries the database for tests in the patients medical history that would match the requirements for the drug
        query2 = db.session.query(patienthistory).filter(patienthistory.patientid == patient_id,
                                                         patienthistory.standardtestid == requirement.standardtestid,
                                                         patienthistory.dateconducted > minimum_last_test_date)
        if query2.count() > 0:
            requirement_met = "Yes"
        else:
            requirement_met = "No"
            # If pharmacist has discretion to authorise pickup without test then requirements is considered to be met
            if requirement.pharmacistdiscretion == "non":
                # If any of the requirements are not met then the pharmacist cannot authorise the pickup
                authorised = False

        requirements.append({"requirement_id": requirement.requiredtestid,
                             "drug_id": requirement.drugid,
                             "test_id": requirement.standardtestid,
                             "pharmacist_discretion": requirement.pharmacistdiscretion,
                             "minimum_last_test_date": str(minimum_last_test_date),
                             "requirement_met": requirement_met})

    return get_default_response({"is_authorised": authorised, "requirements": requirements})


@app.route('/api/pickup/authorised', methods=['GET'])
@flask_praetorian.auth_required
def get_pickup_authorised():
    return is_authorised(request.args.get("pickup_id"))
