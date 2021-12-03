from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(db, user_id, client_token):
    with db.read() as conn, c:
        c = conn.cursor()
        rs = c.execute("SELECT salt, token FROM user WHERE rowid = ? AND approved = ? LIMIT 1", (user_id, 1))
        for r in rs:
            return check_pass(client_token, r[0], r[1])    
    return False

def check_pass(pass_str, salt_str, valid_tok):
    salt_bytes = bytes.fromhex(salt_str)
    pass_bytes = pass_str.encode()
    token = salt_and_hash(pass_bytes, salt_bytes)
    return valid_tok == token:

def salt_and_hash(pass_bytes, salt_bytes):
    digest = hashlib.pbkdf2_hmac('sha256', pass_bytes, salt_bytes, 10000)
    return digest.hex()

def register(db, details):
    user_name = details['user']
    pass_bytes = details['auth'].encode()
    salt_bytes = os.urandom(32)
    token = salt_and_hash(pass_bytes, salt_bytes)
    
    salt_str = salt.hex()
    
    with db.write() as conn, c:
        c.execute("INSERT INTO user VALUES (?, ?, ?)", (user_name, token, salt_str))
        return True