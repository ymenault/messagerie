from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import os

def generate_keys():
    if not (os.path.exists("private.pem") and os.path.exists("public.pem")):
        key = RSA.generate(2048)
        with open("private.pem", "wb") as priv_file:
            priv_file.write(key.export_key())
        with open("public.pem", "wb") as pub_file:
            pub_file.write(key.publickey().export_key())

def load_keys():
    generate_keys()  # Génère les clés seulement si elles n'existent pas
    private_key = RSA.import_key(open("private.pem").read())
    public_key = RSA.import_key(open("public.pem").read())
    return private_key, public_key

def encrypt(message, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    message_bytes = message.encode()
    chunk_size = 190  # Taille maximale pour RSA 2048 bits avec PKCS1_OAEP
    chunks = [message_bytes[i:i+chunk_size] for i in range(0, len(message_bytes), chunk_size)]
    encrypted_chunks = [cipher.encrypt(chunk) for chunk in chunks]
    # Ajouter la taille de chaque chunk au début pour faciliter le déchiffrement
    result = []
    for chunk in encrypted_chunks:
        result.extend(len(chunk).to_bytes(2, byteorder='big'))
        result.extend(chunk)
    return bytes(result)

def decrypt(encrypted_message, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    # Lire les chunks
    decrypted_parts = []
    i = 0
    while i < len(encrypted_message):
        chunk_size = int.from_bytes(encrypted_message[i:i+2], byteorder='big')
        i += 2
        chunk = encrypted_message[i:i+chunk_size]
        decrypted_parts.append(cipher.decrypt(chunk))
        i += chunk_size
    return b''.join(decrypted_parts).decode()

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

# Ne pas exécuter le code de test lors de l'import
if __name__ == "__main__":
    # Test du chiffrement/déchiffrement
    generate_keys()
    priv, pub = load_keys()
    
    # Test avec un message court
    msg = "salut"
    encrypted_msg = encrypt(msg, pub)
    decrypted_msg = decrypt(encrypted_msg, priv)
    print("Message court déchiffré:", decrypted_msg)
    
    # Test avec un message long
    long_msg = "Ceci est un très long message pour tester le chiffrement RSA par morceaux. " * 10
    encrypted_long = encrypt(long_msg, pub)
    decrypted_long = decrypt(encrypted_long, priv)
    print("Message long déchiffré:", decrypted_long)
    
    # Test de la signature et vérification
    msg_to_sign = "mon message a signer"
    signature = sign(msg_to_sign, priv)
    print(verify(msg_to_sign, signature, pub))
