
import flask
import logging
import os


def application_factory(extra_config=None):
    
    print("Startup...")
    logging.basicConfig(level=logging.DEBUG)
    flapp = flask.Flask(__name__)

    #from runapi import bp

    flapp.config.from_mapping(
        SECRET_KEY="test_mode",
    )   

    if extra_config is not None:
        flapp.config.update(extra_config)

    data_dir = os.getenv('APPLICATION_DATA')
    logging.info("App data in [{}]".format(data_dir))

    #flapp.register_blueprint(bp, url_prefix="/run")

    return flapp