from . import auth


def test_not_authorised(client):
    res = client.get("/api/test")
    assert res.status_code == 401
    assert "test_id" not in str(res.json)


def test_no_test_id(client, db):
    # Record to accommodate for foreign key constraints
    # db.session.execute('INSERT INTO drugs () VALUES ("drugUUID", "Drug 1")')
    # Record that should not be returned
    db.session.execute('INSERT INTO standardtests () VALUES ("testUUID", "Blood test 1")')

    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/test", headers={'Authorization': "Bearer " + token})

    assert res.status_code == 400

    assert "name" not in str(res.json)


def test_no_pickups_to_return(client, db):
    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/test", headers={'Authorization': "Bearer " + token},
                     query_string={"test_id": "testUUID"})

    assert "name" not in str(res.json)

    assert res.status_code == 404


def test_id_not_found(client, db):
    # Record to accommodate for foreign key constraints
    db.session.execute('INSERT INTO drugs () VALUES ("drugUUID", "Drug 1")')
    # Record that should not be returned
    db.session.execute('INSERT INTO standardtests () VALUES ("testUUID", "Blood test 1")')

    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/test", headers={'Authorization': "Bearer " + token},
                     query_string={"test_id": "not-test-id"})

    assert "name" not in str(res.json)
    assert res.status_code == 404


def test_retrieve_test(client, db):
    # Record to accommodate for foreign key constraints
    db.session.execute('INSERT INTO drugs () VALUES ("drugUUID", "Drug 1")')
    # Record that should be returned
    db.session.execute('INSERT INTO standardtests () VALUES ("testUUID2", "Blood test 1")')
    # Record that should be returned
    db.session.execute('INSERT INTO standardtests () VALUES ("testUUID", "Blood test 2")')
    # Record that should be returned
    db.session.execute('INSERT INTO standardtests () VALUES ("testUUID1", "Blood test 3")')

    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/test", headers={'Authorization': "Bearer " + token},
                     query_string={"test_id": "testUUID"})

    assert res.status_code == 200

    assert res.json['test_id'] == "testUUID"
    assert res.json['name'] == "Blood test 2"
