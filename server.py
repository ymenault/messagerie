import socket
import threading
import time

IP = "127.0.0.1"
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(10)

clients_data = []

def broadcast(message):
    for client in clients_data:
        client[0].send(bytes(message, "utf-8"))


def handle_connexion():
    while True:
        client, address = server.accept()
        print(f"New connexion from {address}")

        pseudo = client.recv(2048).decode("utf-8")
        key = client.recv(2048).decode("utf-8")
        clients_data.append([client, pseudo, key])

        thread_client = threading.Thread(target=handle_client, args=(client, pseudo, key))
        thread_client.start()

def handle_client(client, pseudo, key):
    while True:
        try:
            message = client.recv(2048).decode("utf-8")
            broadcast(key)
            time.sleep(0.1)
            broadcast(pseudo)
            time.sleep(0.1)
            broadcast(message)
            time.sleep(0.1)

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