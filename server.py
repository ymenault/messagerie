import socket
import threading

IP = "127.0.0.1"
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(10)

# Matrice stockant les clients sous forme [client_socket, pseudo]
clients_data = []

def broadcast(message):
    for client_info in clients_data:
        client_info[0].send(bytes(message, "utf-8"))

def handle_connexion():
    while True:
        client, adress = server.accept()
        print(f"Connection from {adress} has been established!")

        pseudo = client.recv(1024).decode("utf-8")
        key = client.recv(1024).decode("utf-8")
        clients_data.append([client, pseudo, key])

        print(f"{pseudo} has joined the chat!")

        thread_client = threading.Thread(target=handle_client, args=(client, pseudo, key))
        thread_client.start()

def handle_client(client, pseudo, key):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            broadcast(key)
            broadcast(pseudo)
            print("envoi des informations...")
            broadcast(message)
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

print("Server is listening...")
handle_connexion()