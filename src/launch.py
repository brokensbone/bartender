
import flask
import logging
import os
import datetime

from . import constants

VERSION = "0.1.0"

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
    