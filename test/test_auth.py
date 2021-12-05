from src import database, authentication, constants
import os
import base64

def test_auth_flow(application):
    data_dir = application.config["DATA_DIR"]
    db_file = os.path.join(data_dir, constants.FILE_DATABASE)
    db = database.Provider(db_file)


    user = "my_username"
    pw = "very.strong.password"
    creds = {"user" : user, "auth" : pw}

    # Should fail because we're not registered
    assert authentication.verify_password(db, user, pw) == False

    # Do the register
    authentication.register(db, creds)

    # Should fail because we're not approved
    assert authentication.verify_password(db, user, pw) == False

    # Do the approve
    authentication.approve(db, user)

    # Should pass because we're approved
    assert authentication.verify_password(db, user, pw)

    # Should fail because wrong pw
    assert authentication.verify_password(db, user, "not.the.password") == False


def test_auth_flow_client(client):
    data_dir = client.application.config["DATA_DIR"]
    db_file = os.path.join(data_dir, constants.FILE_DATABASE)
    db = database.Provider(db_file)

    user = "my_next_username"
    pw = "very.strong.password"
    creds = {"user" : user, "auth" : pw}

    # Should fail because we're not registered
    r = client.post("auth/authenticate", json=creds)
    assert r.get_json()["authenticate"] == False

    # Do the register
    client.post("auth/register", json=creds)

    # Should fail because we're not approved
    r = client.post("auth/authenticate", json=creds)
    assert r.get_json()["authenticate"] == False

    # Do the approve
    authentication.approve(db, user)

    # Should pass because we're approved
    r = client.post("auth/authenticate", json=creds)
    assert r.get_json()["authenticate"] == True

    # Should fail because wrong pw
    creds["auth"] = "not.the.password"
    r = client.post("auth/authenticate", json=creds)
    assert r.get_json()["authenticate"] == False

    r = client.get("api/test")
    assert r.status_code == 200

    r = client.get("api/testauth")
    assert r.status_code == 401

    basic_auth = "{}:{}".format(user, pw)
    valid_credentials = base64.b64encode(basic_auth.encode()).decode()
    headers = {"Authorization": "Basic " + valid_credentials}
    r = client.get("api/testauth", headers=headers)
    assert r.status_code == 200
