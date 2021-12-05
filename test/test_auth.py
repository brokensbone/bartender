from src import database, authentication, constants
import os

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
