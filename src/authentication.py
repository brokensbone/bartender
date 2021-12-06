import os
import hashlib
from flask import Blueprint, request
from src import database

class Authenticator():
    def __init__(self, database):
        self.database = database

    def verify_password(self, user_name, client_token):
        with self.database.read() as (conn, c):
            c.execute("SELECT Salt, Token FROM user WHERE UserName = ? AND Approved = ? LIMIT 1", (user_name, 1))
            r = c.fetchone()
            if r:
                return self.check_pass(client_token, r[0], r[1])    
        return False

    def check_pass(self, pass_str, salt_str, valid_tok):
        salt_bytes = bytes.fromhex(salt_str)
        pass_bytes = pass_str.encode()
        token = self.salt_and_hash(pass_bytes, salt_bytes)
        return valid_tok == token

    def salt_and_hash(self, pass_bytes, salt_bytes):
        digest = hashlib.pbkdf2_hmac('sha256', pass_bytes, salt_bytes, 10000)
        return digest.hex()

    def register(self, details):
        user_name = details['user']
        pass_bytes = details['auth'].encode()
        salt_bytes = os.urandom(32)
        token = self.salt_and_hash(pass_bytes, salt_bytes)
        
        salt_str = salt_bytes.hex()
        
        with self.database.write() as (conn, c):
            c.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (user_name, token, salt_str, 0))
            return True

    def approve(self, user_name):
        with self.database.write() as (conn, c):
            c.execute("UPDATE User SET Approved = 1 WHERE UserName = ?", (user_name,))