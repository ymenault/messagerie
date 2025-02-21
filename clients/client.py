import random
import socket
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from chiffrement.cesar import encrypt, decrypt
from chiffrement.vig import encrypt, decrypt, generate_random_string
from chiffrement.handle_key import encrypt_key, decrypt_key

IP = "127.0.0.1"
PORT = 55555

# key = random.randint(1, 25)
key = generate_random_string(16)
encrypted_key = encrypt_key(key)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

pseudo = input("Choose a pseudo : ")
client.send(bytes(encrypt(pseudo, key), "utf-8"))
client.send(encrypted_key.encode("utf-8"))

def send_message():
    while True:
        message = input()
        client.send(bytes(encrypt(message, key), "utf-8"))

def receive_message():
    while True:
        try:
            key = decrypt_key(client.recv(2048).decode("utf-8"))
            pseudo = decrypt(client.recv(2048).decode("utf-8"), key)
            message = decrypt(client.recv(2048).decode("utf-8"), key)
            print(f"{pseudo} : {message}")
        except:
            print("An error occurred!")
            client.close()
            break

thread_send = threading.Thread(target=send_message)
thread_receive = threading.Thread(target=receive_message)

thread_send.start()
thread_receive.start()
