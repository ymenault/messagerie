import socket
import threading
import sys
import os
from Crypto.PublicKey import RSA
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chiffrement.RSA import encrypt, decrypt, generate_keys, load_keys

IP = "127.0.0.1"
PORT = 55555

# Générer ou charger la paire de clés
generate_keys()
client_priv, client_pub = load_keys()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

# Envoyer sa clé publique au serveur
client.send(client_pub.export_key())

# Dictionnaire des clés publiques des autres clients
public_keys = {}

def receive_messages():
    while True:
        try:
            encrypted_data = client.recv(4096)
            if not encrypted_data:
                break

            # Vérifier si c'est une clé publique
            if encrypted_data.startswith(b"-----BEGIN PUBLIC KEY-----"):
                new_pub_key = RSA.import_key(encrypted_data)
                public_keys[encrypted_data] = new_pub_key  # Stocker la clé
                print("Un utilisateur est arrivé")
            else:
                # Déchiffrer si possible
                message = decrypt(encrypted_data, client_priv)
                print(f"Message reçu: {message}")

        except Exception as e:
            print(f"Erreur réception: {e}")
            break

def send_message():
    while True:
        if not public_keys:
            print("Attente d'un autre utilisateur...")
            while not public_keys:
                pass  # Boucle d'attente active jusqu'à réception d'une clé publique

        message = input()
        
        # Sélectionner une clé publique (ici, on prend la première disponible)
        dest_pub_key = list(public_keys.values())[0]  # Exemple simple : 1er contact
        encrypted_msg = encrypt(message, dest_pub_key)
        client.send(encrypted_msg)

thread_receive = threading.Thread(target=receive_messages)
thread_send = threading.Thread(target=send_message)

thread_receive.start()
thread_send.start()
