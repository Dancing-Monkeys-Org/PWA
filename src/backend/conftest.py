import pytest
import os
from flask_sqlalchemy import SQLAlchemy
import pytest_flask_sqlalchemy



# import api
from api import app as _app
from api import db as _db

# @pytest.fixture(scope='session')
# def app(client):
#     yield client.application
#
#
# @pytest.fixture(scope='session')
# def client():
#     api.app.config['TESTING'] = True
#
#     DB_USERNAME = os.environ.get('DB_USERNAME')
#     DB_PASSWORD = os.environ.get('DB_PASSWORD')
#     DB_URL = os.environ.get('DB_URL')
#     DB_NAME = os.environ.get('DB_NAME')
#
#     api.app.config[
#         'SQLALCHEMY_DATABASE_URI'] = "mysql://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_URL + "/" + DB_NAME
#
#     with api.app.test_client() as client:
#         client.application.config[
#         'SQLALCHEMY_DATABASE_URI'] = "mysql://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_URL + "/" + DB_NAME
#
#         yield client
#
#
# # @pytest.fixture(scope='session')
# # def database(client):
# #     '''
# #     Create a Postgres database for the tests, and drop it when the tests are done.
# #     '''
#
#
# @pytest.fixture(scope='session')
# def _db(app):
#     '''
#     Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
#     database connection.
#     '''
#     db = SQLAlchemy(app=app)
#     db.init_app(app)
#     db.create_all()
#     yield db


@pytest.fixture(scope='function')
def client(app):
    """Get a test client for your Flask app"""
    return app.test_client()


@pytest.fixture(scope='function')
def app():
    # DB_USERNAME = os.environ.get('DB_USERNAME')
    # DB_PASSWORD = os.environ.get('DB_PASSWORD')
    # DB_URL = os.environ.get('DB_URL')
    # DB_NAME = os.environ.get('DB_NAME')
    # _app.update(SQLALCHEMY_DATABASE_URI="mysql://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_URL + "/" + DB_NAME)
    with _app.app_context():
        yield _app


@pytest.fixture(scope='function')
def db(app):
    yield _db

