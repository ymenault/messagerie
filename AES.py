import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Dérive une clé de 256 bits à partir d'un mot de passe et d'un sel en utilisant PBKDF2.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256
        salt=salt,
        iterations=100_000,  # Sécurité renforcée
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt(password: str, plaintext: str) -> bytes:
    """
    Chiffre un message avec AES-GCM.
    - Génère un sel aléatoire (16 octets).
    - Génère un IV aléatoire (12 octets, recommandé pour AES-GCM).
    - Retourne un message contenant le sel + IV + tag + texte chiffré, encodé en base64.
    """
    salt = os.urandom(16)  # 16 octets pour le sel
    key = derive_key(password, salt)

    iv = os.urandom(12)  # 12 octets pour l'IV (Nonce)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    tag = encryptor.tag  # Tag d'authentification (16 octets)

    return base64.b64encode(salt + iv + tag + ciphertext)  # On concatène tout

def decrypt(password: str, encrypted_data: bytes) -> str:
    """
    Déchiffre un message chiffré avec AES-GCM.
    - Extrait le sel (16 octets), l'IV (12 octets), le tag (16 octets) et le texte chiffré.
    - Vérifie l'intégrité grâce au tag GCM.
    """
    encrypted_data = base64.b64decode(encrypted_data)

    salt = encrypted_data[:16]
    iv = encrypted_data[16:28]
    tag = encrypted_data[28:44]
    ciphertext = encrypted_data[44:]

    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    return decryptor.update(ciphertext) + decryptor.finalize()

password = "monMotDePasseSecurise"
message = "Ceci est un message secret."

encrypted_msg = encrypt(password, message)
print(f"🔐 Message chiffré : {encrypted_msg}")

decrypted_msg = decrypt(password, encrypted_msg)
print(f"🔓 Message déchiffré : {decrypted_msg}")
