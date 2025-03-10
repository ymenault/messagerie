import base64

def encrypt_key(key):
    if isinstance(key, int):
        key = str(key)
    key_bytes = key.encode('utf-8')
    encrypted_key = base64.b64encode(key_bytes)
    return encrypted_key.decode('utf-8')

def decrypt_key(encrypted_key):
    encrypted_key_bytes = encrypted_key.encode('utf-8')
    decrypted_key_bytes = base64.b64decode(encrypted_key_bytes)
    decrypted_key = decrypted_key_bytes.decode('utf-8')
    return decrypted_key