import socket
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chiffrement.AES import encrypt, decrypt


IP = "127.0.0.1"
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(10)

clients_data = []

def broadcast(message):
    message = encrypt(message)
    for client in clients_data:
        client[0].send(bytes(message.encode("utf-8")))


def handle_connexion():
    while True:
        client, address = server.accept()
        print(f"New connexion from {address}")

        pseudo = decrypt(client.recv(2048).decode("utf-8"))
        clients_data.append([client, pseudo])

        thread_client = threading.Thread(target=handle_client, args=(client, pseudo))
        thread_client.start()

def handle_client(client, pseudo):
    while True:
        try:
            message = decrypt(client.recv(2048).decode("utf-8"))
            formatted_message = f"{pseudo}: {message}"
            broadcast(formatted_message)
        except:
            remove_client(client)
            break

def remove_client(client):
    for client_info in clients_data:
        if client_info[0] == client:
            clients_data.remove(client_info)
            client.close()
            print(f"{client_info[1]} has left the chat! \n")
            break

print("Server is running...")
handle_connexion()