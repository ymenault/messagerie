import socket
import threading
import random

from handle_key import encrypt_key, decrypt_key
#from cesar import encrypt, decrypt
#from vig import encrypt, decrypt, generate_random_string
from AES import encrypt, decrypt, generate_random_string

#key = random.randint(1, 25) # Cesar key
key = generate_random_string(16) # Vigenere key

IP = "127.0.0.1"
PORT = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((IP, PORT))

pseudo = input("Choose a pseudo : ")
client.send(bytes(encrypt(pseudo, key), "utf-8"))

client.send(bytes(encrypt_key(key), "utf-8"))

def send_message():
    while True:
        message = input()
        crypted_message = encrypt(message, key)
        client.send(bytes(crypted_message, "utf-8"))

def receive_message():
    while True:
        try:
            key = decrypt_key(client.recv(1024).decode("utf-8"))
            pseudo = client.recv(1024).decode("utf-8")
            message = client.recv(1024).decode("utf-8")
            print(f"{decrypt(pseudo, key)} : {decrypt(message, key)}")
        except:
            print("An error occured!")
            client.close()
            break

thread_send = threading.Thread(target=send_message)
thread_receive = threading.Thread(target=receive_message)

thread_send.start()
thread_receive.start()