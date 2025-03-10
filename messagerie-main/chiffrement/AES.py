import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Vérifier si la clé existe dans le fichier .env
encryption_key = os.getenv("aes_key")

# Si la clé n'existe pas, en générer une nouvelle
if not encryption_key:
    encryption_key = Fernet.generate_key().decode()
    # Créer ou mettre à jour le fichier .env avec la nouvelle clé
    with open('.env', 'a') as f:
        f.write(f"\naes_key={encryption_key}")

# Initialiser le chiffrement avec la clé
cipher = Fernet(encryption_key.encode())

def encrypt(message):
    return cipher.encrypt(message.encode()).decode()

def decrypt(message):
    return cipher.decrypt(message.encode()).decode()

def get_key():
    return cipher