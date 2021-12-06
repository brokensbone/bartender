from src import database, constants, provider
import os
import base64

def test_auth_flow(application):
    data_dir = application.config["DATA_DIR"]
    db_file = os.path.join(data_dir, constants.FILE_DATABASE)
    db = database.Provider(db_file)

    auth = provider.authenticator()

    user = "my_username"
    pw = "very.strong.password"
    creds = {"user" : user, "auth" : pw}

    # Should fail because we're not registered
    assert auth.verify_password(user, pw) == False

    # Do the register
    auth.register(creds)

    # Should fail because we're not approved
    assert auth.verify_password(user, pw) == False

    # Do the approve
    auth.approve(user)

    # Should pass because we're approved
    assert auth.verify_password(user, pw)

    # Should fail because wrong pw
    assert auth.verify_password(user, "not.the.password") == False


def test_auth_flow_client(client):
    data_dir = client.application.config["DATA_DIR"]
    db_file = os.path.join(data_dir, constants.FILE_DATABASE)
    db = database.Provider(db_file)

    auth = provider.authenticator()

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
    auth.approve(user)

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

def test_test_credentials(client, authentication_headers):
    r = client.get("api/testauth", headers=authentication_headers)
    assert r.status_code == 200