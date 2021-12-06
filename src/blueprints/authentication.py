from flask import Blueprint, request
from flask_httpauth import HTTPBasicAuth
from src import provider

bp = Blueprint("auth", __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def api_verify_password(user_name, client_token):
    return provider.authenticator().verify_password(user_name, client_token)

@bp.route("register", methods=["POST"])
def api_reg():
    auth = provider.authenticator()
    details = request.get_json()
    auth.register(details)
    return {"register" : True }

@bp.route("authenticate", methods=["POST"])
def api_auth():
    auth = provider.authenticator()
    details = request.get_json()
    success = auth.verify_password(details["user"], details["auth"])
    return {"authenticate" : success }