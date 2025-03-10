import socket
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chiffrement.RSA import encrypt, decrypt, load_keys

IP = "127.0.0.1"
PORT = 55555

server_priv, server_pub = load_keys()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(10)

clients = []

def broadcast(message, sender_client):
    encrypted_message = encrypt(message, server_pub)
    for client in clients:
        if client != sender_client:
            client.send(encrypted_message)

def handle_client(client):
    try:
        encrypted_pseudo = client.recv(4096)
        pseudo = decrypt(encrypted_pseudo, server_priv)
        clients.append(client)
        print(f"{pseudo} a rejoint le chat.")

        while True:
            encrypted_message = client.recv(4096)
            if not encrypted_message:
                break

            message = decrypt(encrypted_message, server_priv)
            print(f"Message reçu: {message}")
            broadcast(message, client)
    
    except Exception as e:
        print(f"Erreur avec le client {pseudo}: {str(e)}")
    
    finally:
        if client in clients:
            clients.remove(client)
        client.close()
        print(f"Client {pseudo} déconnecté.")

def start():
    """Fonction de démarrage du serveur."""
    print("Serveur RSA démarré...")
    while True:
        client, addr = server.accept()
        print(f"Nouvelle connexion depuis {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    start()
