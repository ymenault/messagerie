import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Vérifier si la clé existe dans le fichier .env
encryption_key = os.getenv("aes_key")

# Initialiser le chiffrement avec la clé
cipher = Fernet(encryption_key.encode())

def encrypt(message):
    return cipher.encrypt(message.encode()).decode()

def decrypt(message):
    return cipher.decrypt(message.encode()).decode()

def get_key():
    return cipher