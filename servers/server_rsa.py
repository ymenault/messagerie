import socket
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chiffrement.RSA import load_keys

IP = "127.0.0.1"
PORT = 55555

server_priv, server_pub = load_keys()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(10)

clients = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    try:
        encrypted_pseudo = client.recv(4096)
        clients.append(client)
        broadcast(encrypted_pseudo, client)
        
        while True:
            encrypted_message = client.recv(4096)
            if not encrypted_message:
                break
            broadcast(encrypted_message, client)
    except Exception as e:
        print(f"Erreur avec le client: {e}")
    finally:
        if client in clients:
            clients.remove(client)
        client.close()

def accept_clients():
    print("Server is running...")
    while True:
        client, addr = server.accept()
        print(f"New connection from {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()

accept_clients()