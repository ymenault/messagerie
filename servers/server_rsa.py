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
        print(f"{pseudo} has joined the chat.")

        while True:
            encrypted_message = client.recv(4096)
            if not encrypted_message:
                break

            message = decrypt(encrypted_message, server_priv)
            print(f"{pseudo}: {message}")
            broadcast(f"{pseudo}: {message}", client)
    
    except:
        print(f"Client {pseudo} déconnecté.")
    
    finally:
        clients.remove(client)
        client.close()

def accept_clients():
    print("Server is running...")
    while True:
        client, addr = server.accept()
        print(f"New connection from {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()

accept_clients()
