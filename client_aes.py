import socket
import threading

from chiffrement.AES import encrypt, decrypt, get_key

IP = "127.0.0.1"
PORT = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

pseudo = input("Choose a pseudo : ")
client.send(encrypt(pseudo).encode("utf-8"))

def send_message():
    while True:
        message = input()
        client.send(encrypt(message).encode("utf-8"))

def receive_message():
    while True:
            pseudo = decrypt(client.recv(2048).decode("utf-8"))
            message = decrypt(client.recv(2048).decode("utf-8"))
            print(f"{pseudo} : {message}")

thread_send = threading.Thread(target=send_message)
thread_receive = threading.Thread(target=receive_message)

thread_send.start()
thread_receive.start()