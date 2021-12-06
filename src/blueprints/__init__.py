from .api import bp
from .authentication import bp as bp_auth

def register(flapp):
    flapp.register_blueprint(bp, url_prefix="/api")
    flapp.register_blueprint(bp_auth, url_prefix="/auth")