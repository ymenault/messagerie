import socket
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from chiffrement.RSA import encrypt, decrypt, load_keys
from database.db_manager import DatabaseManager

IP = "127.0.0.1"
PORT = 55555

server_priv, server_pub = load_keys()
db = DatabaseManager()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(10)

clients = []

def broadcast(message, sender_client):
    encrypted_message = encrypt(message, server_pub)
    for client in clients:
        if client != sender_client:
            client.send(encrypted_message)

def send_recent_messages(client, pseudo):
    """Envoie les messages récents à un nouveau client."""
    recent_messages = db.get_recent_messages(10)  # Récupère les 10 derniers messages
    for username, message, timestamp in recent_messages:
        formatted_message = f"{username}: {message}"
        encrypted_message = encrypt(formatted_message, server_pub)
        client.send(encrypted_message)

def handle_client(client):
    try:
        encrypted_pseudo = client.recv(4096)
        pseudo = decrypt(encrypted_pseudo, server_priv)
        
        # Ajouter l'utilisateur à la base de données
        db.add_user(pseudo)
        
        clients.append(client)
        print(f"{pseudo} a rejoint le chat.")
        
        # Envoyer l'historique des messages récents
        send_recent_messages(client, pseudo)

        while True:
            encrypted_message = client.recv(4096)
            if not encrypted_message:
                break

            message = decrypt(encrypted_message, server_priv)
            print(f"Message reçu: {message}")
            
            # Sauvegarder le message dans la base de données
            sender = message.split(':', 1)[0]
            content = message.split(':', 1)[1].strip()
            db.save_message(sender, content)
            
            broadcast(message, client)
    
    except Exception as e:
        print(f"Erreur avec le client {pseudo}: {str(e)}")
    
    finally:
        if client in clients:
            clients.remove(client)
        client.close()
        print(f"Client {pseudo} déconnecté.")

def accept_clients():
    print("Serveur RSA démarré...")
    print("Base de données initialisée.")
    while True:
        client, addr = server.accept()
        print(f"Nouvelle connexion depuis {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    accept_clients()
