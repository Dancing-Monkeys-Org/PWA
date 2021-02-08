from . import auth


def test_not_authorised(client):
    res = client.get("/api/test/items")
    assert res.status_code == 401
    assert "name" not in str(res.json)


def test_no_test_id(client, db):
    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/test/items", headers={'Authorization': "Bearer " + token})

    assert res.status_code == 400

    assert "name" not in str(res.json)


def test_bad_test_id(client, db):
    # Record to accommodate for foreign key constraints
    db.session.execute('INSERT INTO drugs () VALUES ("drugUUID", "Drug 1")')
    db.session.execute('INSERT INTO tests () VALUES ("testUUID2", "drugUUID", "COMPLETE")')
    db.session.execute('INSERT INTO tests () VALUES ("testUUID", "drugUUID", "INCOMPLETE")')
    db.session.execute('INSERT INTO tests () VALUES ("testUUID1", "drugUUID", "COMPLETE")')

    # Records that should not be returned
    db.session.execute('insert into testitems () values ("item1", "testUUID", "blood work 1", "COMPLETE")')
    db.session.execute('insert into testitems () values ("item2", "testUUID", "blood work 2", "INCOMPLETE")')
    db.session.execute('insert into testitems () values ("item3", "testUUID", "blood work 3", "PENDING")')

    # Record that should not be returned
    db.session.execute('insert into testitems () values ("item4", "testUUID2", "blood work 4", "COMPLETE")')

    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/test/items", headers={'Authorization': "Bearer " + token},
                     query_string={"test_id": "testUUID4"})

    assert res.status_code == 404
    assert "name" not in str(res.json)


def test_no_test_items(client, db):
    # Record to accommodate for foreign key constraints
    db.session.execute('INSERT INTO drugs () VALUES ("drugUUID", "Drug 1")')
    db.session.execute('INSERT INTO tests () VALUES ("testUUID2", "drugUUID", "COMPLETE")')
    db.session.execute('INSERT INTO tests () VALUES ("testUUID", "drugUUID", "INCOMPLETE")')
    db.session.execute('INSERT INTO tests () VALUES ("testUUID1", "drugUUID", "COMPLETE")')

    # Records that should not be returned
    db.session.execute('insert into testitems () values ("item1", "testUUID", "blood work 1", "COMPLETE")')
    db.session.execute('insert into testitems () values ("item2", "testUUID", "blood work 2", "INCOMPLETE")')
    db.session.execute('insert into testitems () values ("item3", "testUUID", "blood work 3", "PENDING")')

    # Record that should not be returned
    db.session.execute('insert into testitems () values ("item4", "testUUID2", "blood work 4", "COMPLETE")')

    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/test/items", headers={'Authorization': "Bearer " + token},
                     query_string={"test_id": "testUUID1"})

    assert res.status_code == 200
    assert len(res.json) == 0


def test_return_one(client, db):
    # Record to accommodate for foreign key constraints
    db.session.execute('INSERT INTO drugs () VALUES ("drugUUID", "Drug 1")')
    db.session.execute('INSERT INTO tests () VALUES ("testUUID2", "drugUUID", "COMPLETE")')
    db.session.execute('INSERT INTO tests () VALUES ("testUUID", "drugUUID", "INCOMPLETE")')
    db.session.execute('INSERT INTO tests () VALUES ("testUUID1", "drugUUID", "COMPLETE")')

    # Records that should not be returned
    db.session.execute('insert into testitems () values ("item1", "testUUID", "blood work 1", "COMPLETE")')
    db.session.execute('insert into testitems () values ("item2", "testUUID", "blood work 2", "INCOMPLETE")')
    db.session.execute('insert into testitems () values ("item3", "testUUID", "blood work 3", "PENDING")')

    # Record that should be returned
    db.session.execute('insert into testitems () values ("item4", "testUUID2", "blood work 4", "COMPLETE")')

    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/test/items", headers={'Authorization': "Bearer " + token},
                     query_string={"test_id": "testUUID2"})

    assert res.status_code == 200
    assert len(res.json) == 1

    test_item = res.json[0]

    assert test_item["test_item_id"] == "item4"
    assert test_item["test_id"] == "testUUID2"
    assert test_item["name"] == "blood work 4"
    assert test_item["status"] == "COMPLETE"


def test_return_multiple(client, db):
    # Record to accommodate for foreign key constraints
    db.session.execute('INSERT INTO drugs () VALUES ("drugUUID", "Drug 1")')
    db.session.execute('INSERT INTO tests () VALUES ("testUUID2", "drugUUID", "COMPLETE")')
    db.session.execute('INSERT INTO tests () VALUES ("testUUID", "drugUUID", "INCOMPLETE")')
    db.session.execute('INSERT INTO tests () VALUES ("testUUID1", "drugUUID", "COMPLETE")')

    # Records that should be returned
    db.session.execute('insert into testitems () values ("item1", "testUUID", "blood work 1", "COMPLETE")')
    db.session.execute('insert into testitems () values ("item2", "testUUID", "blood work 2", "INCOMPLETE")')
    db.session.execute('insert into testitems () values ("item3", "testUUID", "blood work 3", "PENDING")')

    # Record that should be not returned
    db.session.execute('insert into testitems () values ("item4", "testUUID2", "blood work 4", "COMPLETE")')

    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/test/items", headers={'Authorization': "Bearer " + token},
                     query_string={"test_id": "testUUID"})

    assert res.status_code == 200
    assert len(res.json) == 3
