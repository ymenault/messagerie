from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import os

def generate_keys():
    if not os.path.exists("private.pem") or not os.path.exists("public.pem"):
        key = RSA.generate(2048)
        with open("private.pem", "wb") as priv_file:
            priv_file.write(key.export_key())
        with open("public.pem", "wb") as pub_file:
            pub_file.write(key.publickey().export_key())

def load_keys():
    private_key = RSA.import_key(open("private.pem").read())
    public_key = RSA.import_key(open("public.pem").read())
    return private_key, public_key

def encrypt(message, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(message.encode())

def decrypt(encrypted_message, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(encrypted_message).decode()

def sign(message, private_key):
    hash_obj = SHA256.new(message.encode())
    return pkcs1_15.new(private_key).sign(hash_obj)

def verify(message, signature, public_key):
    hash_obj = SHA256.new(message.encode())
    try:
        pkcs1_15.new(public_key).verify(hash_obj, signature)
        return "La signature est valide"
    except (ValueError, TypeError):
        return "La signature est invalide"

# Générer et charger les clés
generate_keys()
priv, pub = load_keys()


# # Chiffrement et déchiffrement
# msg = "salut"
# encrypted_msg = encrypt(msg, pub)
# decrypted_msg = decrypt(encrypted_msg, priv)
# print("Message déchiffré:", decrypted_msg)

# # Signature et vérification
# msg_to_sign = "mon message a signer"
# signature = sign(msg_to_sign, priv)
# print(verify(msg_to_sign, signature, pub))
