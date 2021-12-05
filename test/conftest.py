import pytest
import tempfile
import shutil
import os

from src.launch import application_factory, VERSION, read_version, DATABASE_VERSION
from src import constants

@pytest.fixture(scope="module")
def application():
    temp_dir = tempfile.mkdtemp()
    app = application_factory({'TESTING': True, "DATA_DIR": temp_dir})
    with app.app_context():
        pass
    yield app

    shutil.rmtree(temp_dir)

@pytest.fixture(scope="module")
def client(application):
    with application.test_client() as client:
        yield client