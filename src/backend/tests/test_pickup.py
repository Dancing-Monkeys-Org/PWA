from . import auth


def test_not_authorised(client):
    res = client.get("/api/pickup")
    assert res.status_code == 401


def test_pickup_no_pickup_id(client, db):
    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/pickup", headers={'Authorization': "Bearer " + token})

    assert res.status_code == 400


def test_pickup_not_found(client, db):
    token = auth.get_access_token(client, db, "test_user", "test_password", "technician")

    res = client.get("/api/pickup", headers={'Authorization': "Bearer " + token},
                     query_string={"pickup_id": "test-id"})

    assert res.status_code == 404
