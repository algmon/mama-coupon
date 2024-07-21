import base64
import hashlib

def get_developer_by_key(mama_api_key: str, db: object):
    # TODO: Hash the provided API key using SHA-256
    # hashed_mama_api_key = hashlib.sha256(mama_api_key.encode()).hexdigest()
    mama_api_key_bytes = mama_api_key.encode('utf-8')
    mama_api_key_base64 = base64.b64encode(mama_api_key_bytes)
    db.execute("SELECT * FROM developers WHERE mama_api_key = %s",
               (mama_api_key_base64,))
    userInfo = db.fetchone() # Fetch the result
    return userInfo