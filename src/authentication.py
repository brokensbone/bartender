from flask_httpauth import HTTPBasicAuth
import os
import hashlib
from flask import Blueprint, request
from src import database

auth = HTTPBasicAuth()
bp = Blueprint("auth", __name__)

@auth.verify_password
def api_verify_password(user_name, client_token):
    return verify_password(database.app_database(), user_name, client_token)

@bp.route("register", methods=["POST"])
def api_reg():
    db = database.app_database()
    details = request.get_json()
    register(db, details)
    return {"register" : True }

@bp.route("authenticate", methods=["POST"])
def api_auth():
    db = database.app_database()
    details = request.get_json()
    success = verify_password(db, details["user"], details["auth"])
    return {"authenticate" : success }

def verify_password(db, user_name, client_token):
    with db.read() as (conn, c):
        c.execute("SELECT Salt, Token FROM user WHERE UserName = ? AND Approved = ? LIMIT 1", (user_name, 1))
        r = c.fetchone()
        if r:
            return check_pass(client_token, r[0], r[1])    
    return False

def check_pass(pass_str, salt_str, valid_tok):
    salt_bytes = bytes.fromhex(salt_str)
    pass_bytes = pass_str.encode()
    token = salt_and_hash(pass_bytes, salt_bytes)
    return valid_tok == token

def salt_and_hash(pass_bytes, salt_bytes):
    digest = hashlib.pbkdf2_hmac('sha256', pass_bytes, salt_bytes, 10000)
    return digest.hex()

def register(db, details):
    user_name = details['user']
    pass_bytes = details['auth'].encode()
    salt_bytes = os.urandom(32)
    token = salt_and_hash(pass_bytes, salt_bytes)
    
    salt_str = salt_bytes.hex()
    
    with db.write() as (conn, c):
        c.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (user_name, token, salt_str, 0))
        return True

def approve(db, user_name):
    with db.write() as (conn, c):
        c.execute("UPDATE User SET Approved = 1 WHERE UserName = ?", (user_name,))