import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os



salt = os.urandom(16)

def encrypt(msg, pwd):


    if isinstance(msg, str):
        msg = msg.encode()

    # Derive key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(pwd.encode())

    # Encrypt message
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_msg = encryptor.update(msg) + encryptor.finalize()

    return base64.b64encode(iv + encrypted_msg)

def decrypt(encrypted_msg, pwd):

    encrypted_msg = base64.b64decode(encrypted_msg)
    iv = encrypted_msg[:16]
    encrypted_msg = encrypted_msg[16:]

    # Derive key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(pwd.encode())

    # Decrypt message
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_msg = decryptor.update(encrypted_msg) + decryptor.finalize()

    return decrypted_msg.decode()

# Example usage
if __name__ == "__main__":
    password = "mysecretpassword"
    message = "This is a secret message."

    encrypted = encrypt(password, message)
    print(f"Encrypted: {encrypted}")

    decrypted = decrypt(password, encrypted)
    print(f"Decrypted: {decrypted}")