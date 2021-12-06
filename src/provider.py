from flask import g, current_app
import os

from . import database as database_module
from . import authentication, constants

"""
A dumping ground for methods that use the current flask app to build other objects.
"""

def database():
    if 'db' not in g:
        data_dir = current_app.config["DATA_DIR"]
        db_file = os.path.join(data_dir, constants.FILE_DATABASE)
        g.db =  database_module.Provider(db_file)
    return g.db 

def authenticator(database_instance=None):
    if database_instance is None:
        database_instance = database()

    return authentication.Authenticator(database_instance)