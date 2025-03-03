import socket
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

IP = "127.0.0.1"
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(10)

clients = {}  # Associe un socket client à son adresse
public_keys = {}  # Associe un socket client à sa clé publique

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def handle_client(client, addr):
    try:
        # Recevoir et stocker la clé publique du client
        client_pub_key = client.recv(4096)
        public_keys[client] = client_pub_key
        clients[client] = addr

        # Envoyer au nouveau client toutes les clés publiques déjà enregistrées
        for other_client in public_keys:
            if other_client != client:
                client.send(public_keys[other_client])

        # Informer les autres clients de la nouvelle clé publique
        for other_client in clients:
            if other_client != client:
                other_client.send(client_pub_key)

        print(f"Client {addr} connecté et clé publique enregistrée.")

        while True:
            encrypted_message = client.recv(4096)
            if not encrypted_message:
                break
            broadcast(encrypted_message, client)
    except Exception as e:
        print(f"Erreur avec {addr}: {e}")
    finally:
        if client in clients:
            del clients[client]
            del public_keys[client]
        client.close()

def accept_clients():
    print("Server is running...")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr)).start()

accept_clients()
