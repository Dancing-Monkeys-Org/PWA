import pytest

from api import app as _app
from api import db as _db


@pytest.fixture(scope='function')
def client(app):
    """Get a test client for your Flask app"""
    return app.test_client()


@pytest.fixture(scope='function')
def app():
    with _app.app_context():
        yield _app


@pytest.fixture(scope='function')
def db(app):
    yield _db

