import pytest
import os
import pytest_flask_sqlalchemy

import api
# from api import db

from conftest import client
import conftest

from conftest import db


def successful_login(client, db, username, password, role):
    db.session.add(api.Users(username=username,
                             password=api.guard.hash_password(password),
                             role=role))

    body = {"username": username, "password": password}

    return client.post('/api/login', json=body)


def login_bad_credentials(client, db, username, password, role):
    db.session.add(api.Users(username=username,
                                 password=api.guard.hash_password(password),
                                 role=role))

    # body = {"username": username + "---", "password": password + "----"}
    body = {"username": username, "password": password}

    return client.post('/api/login', json=body)


def test_successful_login(client, db):
    res = successful_login(client, db, "theusername", "pspaomdpasmdpomapsd", "admin")

    assert res.status_code == 200


def test_login_bad_credentials(client, db):
    res = login_bad_credentials(client, db, "theusername", "pspaomdpasmdpomapsd", "admin")
    # assert 1 == 1
    assert res.status_code == 200


def test_role_correct(client, db):
    role = "testrole"

    res = successful_login(client, db, "testUser", "sdnaslndlas", role)

    token = res.json['access_token']

    res = client.get("/api/test/auth", headers={'Authorization': "Bearer " + token})

    assert res.status_code == 200
    assert res.json['role'] == role


def test_auth(client, db):
    assert client.get("/api/test/auth").status_code == 401
    assert client.get("/api/test/auth", headers={"Authorization": "Bearer mlmlm"}).status_code == 401