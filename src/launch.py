
import flask
import logging
import os
import datetime
import sqlite3

from . import constants

VERSION = "0.1.0"
DATABASE_VERSION = 2

def application_factory(extra_config=None):
    
    print("Startup...")
    logging.basicConfig(level=logging.DEBUG)
    flapp = flask.Flask(__name__)

    from .api import bp

    env_data_dir = os.getenv('APPLICATION_DATA')
    flapp.config.from_mapping(
        SECRET_KEY="test_mode",
        DATA_DIR=env_data_dir,
        VERSION=VERSION
    )   

    if extra_config is not None:
        flapp.config.update(extra_config)

    init_data_dir(flapp)    
    flapp.register_blueprint(bp, url_prefix="/api")

    return flapp

def init_data_dir(flapp):
    data_dir = flapp.config["DATA_DIR"]
    logging.info("App data in [{}]".format(data_dir))
    os.makedirs(data_dir, exist_ok=True)

    version_file = os.path.join(data_dir, constants.FILE_VERSION)
    with open(version_file, 'w') as f:
        f.write(flapp.config["VERSION"])
    
    boot_file = os.path.join(data_dir, constants.FILE_BOOTTIME)
    with open(boot_file, 'w') as f:
        now = datetime.datetime.now()
        f.write(now.strftime(constants.ISO8601))
    
    db_file = os.path.join(data_dir, constants.FILE_DATABASE)
    run_db_updates(db_file)


def run_db_updates(db_file):
    if not os.path.exists(db_file):
        upgrade_database(db_file, 0)

    db_version = read_version(db_file)
    while (db_version < DATABASE_VERSION):
        upgrade_database(db_file, db_version+1)
        db_version = read_version(db_file)


def read_version(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT Value FROM Version")
    r = cursor.fetchone()
    conn.close()
    version_number = r[0]
    logging.info("DB VERSION = {}".format(version_number))
    return version_number


def upgrade_database(db_file, db_version):
    sql_script = read_db_script(db_version)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    cursor.execute("UPDATE Version SET Value = ?", (db_version,))
    conn.commit()
    conn.close()


def read_db_script(db_version):
    src_dir = os.path.dirname(__file__)
    target_file = constants.FILE_DATABASE_SCRIPT.format(db_version)
    script_path = os.path.join(src_dir, constants.DIRECTORY_DB, target_file)
    with open(script_path, 'r') as f:
        return f.read()