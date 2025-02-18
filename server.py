import socket 
import threading

from cesar import encrypt

IP = "127.0.0.1"
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((IP, PORT))
server.listen(10)

clients = []
pseudos = []

def broadcast(message):
    for client in clients:
        client.send(bytes(message, "utf-8"))

def handle_connexion():
    while True:
        client, adress = server.accept()
        print(f"Connection from {adress} has been established!")

        pseudo = client.recv(1024).decode("utf-8")

        clients.append(client)
        pseudos.append(pseudo)

        print(f"{pseudo} has joined the chat!")

        thread_client = threading.Thread(target=handle_client, args=(client, pseudo))
        thread_client.start()

def handle_client(client, pseudo):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            broadcast(f"{pseudo} : {message}")

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            pseudo = pseudos[index]
            pseudos.remove(pseudo)
            break

print("Server is listening...")
handle_connexion()