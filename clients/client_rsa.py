import socket
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chiffrement.RSA import encrypt, decrypt, load_keys

IP = "127.0.0.1"
PORT = 55555

# Charger la clé publique du serveur pour chiffrer les messages
_, server_pub = load_keys()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

pseudo = input("Choose a pseudo : ")
client.send(encrypt(pseudo, server_pub))  # Envoi du pseudo chiffré

def send_message():
    while True:
        message = input()
        client.send(encrypt(message, server_pub))  # Envoi du message chiffré

def receive_message():
    while True:
        try:
            encrypted_data = client.recv(4096)
            if not encrypted_data:
                break

            message = decrypt(encrypted_data, private_key)
            print(message)
        except:
            print("Connexion perdue.")
            client.close()
            break

thread_send = threading.Thread(target=send_message)
thread_receive = threading.Thread(target=receive_message)

thread_send.start()
thread_receive.start()
