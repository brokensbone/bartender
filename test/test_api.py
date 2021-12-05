import pytest
import tempfile
import shutil
import os

from src.launch import application_factory, VERSION, read_version, DATABASE_VERSION
from src import constants

@pytest.fixture
def application():
    temp_dir = tempfile.mkdtemp()
    app = application_factory({'TESTING': True, "DATA_DIR": temp_dir})
    with app.app_context():
        pass
    yield app

    shutil.rmtree(temp_dir)

@pytest.fixture
def client(application):
    with application.test_client() as client:
        yield client

def test_test(client):
    rv = client.get("api/test")
    assert rv.status_code == 200

def test_version(application):
    data_dir = application.config["DATA_DIR"]
    version_file = os.path.join(data_dir, constants.FILE_VERSION)
    with open(version_file, 'r') as f:
        written = f.read()
        assert written == VERSION

def test_db_verson(application):
    data_dir = application.config["DATA_DIR"]
    db_file = os.path.join(data_dir, constants.FILE_DATABASE)
    assert read_version(db_file) == DATABASE_VERSION