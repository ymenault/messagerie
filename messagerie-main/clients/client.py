import random
import socket
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chiffrement.cesar import encrypt, decrypt

IP = "127.0.0.1"
PORT = 55555

key = random.randint(1, 25)
print(f"Clé de chiffrement: {key}")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

pseudo = input("Choose a pseudo : ")

# Test du chiffrement
print("Test de chiffrement:")
test_message = "Hello"
encrypted_test = encrypt(test_message, key)
print(f"Message original: {test_message}")
print(f"Message chiffré: {encrypted_test}")
print(f"Message déchiffré: {decrypt(encrypted_test, key)}")

# Envoyer le pseudo chiffré
encrypted_pseudo = encrypt(pseudo, key)
print(f"Pseudo chiffré envoyé: {encrypted_pseudo}")
client.send(encrypted_pseudo.encode())

def send_message():
    while True:
        try:
            message = input()
            if message:
                # Chiffrer et afficher pour vérification
                encrypted_message = encrypt(message, key)
                print(f"Message envoyé (chiffré): {encrypted_message}")
                client.send(encrypted_message.encode())
        except Exception as e:
            print(f"Erreur d'envoi: {e}")
            break

def receive_message():
    while True:
        try:
            encrypted_message = client.recv(2048).decode()
            if encrypted_message:
                # Déchiffrer et afficher
                decrypted_message = decrypt(encrypted_message, key)
                print(f"Message reçu (chiffré): {encrypted_message}")
                print(f"Message déchiffré: {decrypted_message}")
        except Exception as e:
            print(f"Erreur de réception: {e}")
            break

thread_send = threading.Thread(target=send_message)
thread_receive = threading.Thread(target=receive_message)

thread_send.start()
thread_receive.start()
