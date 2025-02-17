import socket 
import threading

from cesar import encrypt_cesar, decrypt_cesar, cle

IP = "127.0.0.1"
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((IP, PORT))
server.listen(10)

clients = []
pseudos = []

def broadcast(message):
    for client in clients:
        crypted_message = encrypt_cesar(message)
        client.send(bytes(crypted_message, "utf-8"))

def handle_connexion():
    while True:
        client, adress = server.accept()
        print(f"Connection from {adress} has been established!")

        pseudo = client.recv(1024).decode("utf-8")

        clients.append(client)
        pseudos.append(pseudo)

        print(f"{pseudo} has joined the chat!")
        #client.send(bytes("Welcome to the chat ! \n", "utf-8"))
        broadcast(f"{pseudo} has joined the chat ! \n")

        thread_client = threading.Thread(target=handle_client, args=(client, pseudo))
        thread_client.start()

def handle_client(client, pseudo):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            decrypted_message = decrypt_cesar(message)
            broadcast(f"{pseudo} : {decrypted_message}")

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            pseudo = pseudos[index]
            pseudos.remove(pseudo)
            broadcast(f"{pseudo} has left the chat !")
            break

print("Server is listening...")
handle_connexion()