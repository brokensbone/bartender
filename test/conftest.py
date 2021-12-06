import pytest
import tempfile
import shutil
import os
import base64

from src.launch import application_factory, VERSION, read_version, DATABASE_VERSION
from src import constants, provider, database

@pytest.fixture(scope="module")
def credentials():
    return {"user": "the_test_user", "auth" : "the.test.password"}


@pytest.fixture(scope="module")
def authentication_headers(credentials):
    basic_auth = "{}:{}".format(credentials["user"], credentials["auth"])
    valid_credentials = base64.b64encode(basic_auth.encode()).decode()
    return {"Authorization": "Basic " + valid_credentials}


@pytest.fixture(scope="module")
def application(credentials):
    temp_dir = tempfile.mkdtemp()
    app = application_factory({'TESTING': True, "DATA_DIR": temp_dir})
    with app.app_context():
        
        #data_dir = app.config["DATA_DIR"]
        #db_file = os.path.join(data_dir, constants.FILE_DATABASE)
        #db = database.Provider(db_file)
        #authentication.register(db, credentials)
        #authentication.approve(db, credentials["user"])
        auth = provider.authenticator()
        auth.register(credentials)
        auth.approve(credentials["user"])
        yield app

    shutil.rmtree(temp_dir)


@pytest.fixture(scope="module")
def client(application):
    with application.test_client() as client:
        yield client
