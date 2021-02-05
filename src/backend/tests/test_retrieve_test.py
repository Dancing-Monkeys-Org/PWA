from . import auth


def test_not_authorised(client):
    res = client.get("/api/test")
    assert res.status_code == 401
    assert "test_id" not in str(res.json)


def test_no_test_id(client, db):
    # Record to accommodate for foreign key constraints
    db.session.execute('INSERT INTO drugs () VALUES ("drugUUID", "Drug 1")')
    # Record that should not be returned
    db.session.execute('INSERT INTO tests () VALUES ("testUUID", "drugUUID", "INCOMPLETE")')

    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/test", headers={'Authorization': "Bearer " + token})

    assert res.status_code == 400

    assert "drug_id" not in str(res.json)


def test_no_pickups_to_return(client, db):
    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/test", headers={'Authorization': "Bearer " + token},
                     query_string={"test_id": "testUUID"})

    assert "drug_id" not in str(res.json)

    assert res.status_code == 404


def test_id_not_found(client, db):
    # Record to accommodate for foreign key constraints
    db.session.execute('INSERT INTO drugs () VALUES ("drugUUID", "Drug 1")')
    # Record that should not be returned
    db.session.execute('INSERT INTO tests () VALUES ("testUUID", "drugUUID", "INCOMPLETE")')

    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/test", headers={'Authorization': "Bearer " + token},
                     query_string={"test_id": "not-test-id"})

    assert "drug_id" not in str(res.json)
    assert res.status_code == 404


def test_retrieve_test(client, db):
    # Record to accommodate for foreign key constraints
    db.session.execute('INSERT INTO drugs () VALUES ("drugUUID", "Drug 1")')
    # Record that should be returned
    db.session.execute('INSERT INTO tests () VALUES ("testUUID2", "drugUUID", "COMPLETE")')
    # Record that should be returned
    db.session.execute('INSERT INTO tests () VALUES ("testUUID", "drugUUID", "INCOMPLETE")')
    # Record that should be returned
    db.session.execute('INSERT INTO tests () VALUES ("testUUID1", "drugUUID", "COMPLETE")')

    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/test", headers={'Authorization': "Bearer " + token},
                     query_string={"test_id": "testUUID"})

    assert res.status_code == 200

    assert res.json['test_id'] == "testUUID"
    assert res.json['drug_id'] == "drugUUID"
    assert res.json['status'] == "INCOMPLETE"
