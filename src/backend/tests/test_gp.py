from . import auth


def test_not_authorised(client):
    res = client.get("/api/gp")
    assert res.status_code == 401
    assert "gp_id" not in str(res.json)


def test_gp_no_gp_id(client, db):
    # Records to accommodate for foreign key constraints
    db.session.execute(
        'INSERT INTO contactdetails () VALUES ("contactDetailUUID", 12345678910, "email1", "addressline11", null,'
        ' "addressline31", "addressline41", "ABC DEF")')

    # Record that should not be returned
    db.session.execute('INSERT INTO gps () VALUES ("gpsUUID", "Gp1", "contactDetailUUID")')

    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/gp", headers={'Authorization': "Bearer " + token})

    assert res.status_code == 400

    assert "name" not in str(res.json)


def test_no_pickups_to_return(client, db):
    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/gp", headers={'Authorization': "Bearer " + token},
                     query_string={"gp_id": "example-gp-id"})

    assert res.status_code == 404
    assert "name" not in str(res.json)


def test_contact_id_not_found(client, db):
    # Records to accommodate for foreign key constraints
    db.session.execute(
        'INSERT INTO contactdetails () VALUES ("contactDetailUUID", 12345678910, "email1", "addressline11", null,'
        ' "addressline31", "addressline41", "ABC DEF")')

    # Record that should not be returned
    db.session.execute('INSERT INTO gps () VALUES ("gpsUUID", "Gp1", "contactDetailUUID")')
    # Record that should not be returned
    db.session.execute('INSERT INTO gps () VALUES ("gpsUUID2", "Gp2", "contactDetailUUID")')
    # Record that should not be returned
    db.session.execute('INSERT INTO gps () VALUES ("gpsUUID3", "Gp3", "contactDetailUUID")')

    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/gp", headers={'Authorization': "Bearer " + token},
                     query_string={"gp_id": "example-gp-id"})

    assert "name" not in str(res.json)
    assert res.status_code == 404


def test_retrieve_gp(client, db):
    # Records to accommodate for foreign key constraints
    db.session.execute(
        'INSERT INTO contactdetails () VALUES ("contactDetailUUID", 12345678910, "email1", "addressline11", null,'
        ' "addressline31", "addressline41", "ABC DEF")')

    # Record that should not be returned
    db.session.execute('INSERT INTO gps () VALUES ("gpsUUID", "Gp1", "contactDetailUUID")')
    # Record that should be returned
    db.session.execute('INSERT INTO gps () VALUES ("gpsUUID2", "Gp2", "contactDetailUUID")')
    # Record that should not be returned
    db.session.execute('INSERT INTO gps () VALUES ("gpsUUID3", "Gp3", "contactDetailUUID")')

    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/gp", headers={'Authorization': "Bearer " + token},
                     query_string={"gp_id": "gpsUUID2"})

    assert res.status_code == 200

    assert res.json['gp_id'] == "gpsUUID2"
    assert res.json['name'] == "Gp2"
    assert res.json['contact_id'] == "contactDetailUUID"
