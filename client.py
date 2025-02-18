import socket
import threading

from cesar import encrypt, decrypt

IP = "127.0.0.1"
PORT = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((IP, PORT))

pseudo = input("Choose a pseudo : ")
encrypted_pseudo = encrypt(pseudo)
client.send(bytes(encrypted_pseudo, "utf-8"))

def send_message():
    while True:
        message = input()
        crypted_message = encrypt(message)
        client.send(bytes(crypted_message, "utf-8"))

def receive_message():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            decrypted_message = decrypt(message)
            print(decrypted_message)
        except:
            print("An error occured!")
            client.close()
            break

thread_send = threading.Thread(target=send_message)
thread_receive = threading.Thread(target=receive_message)

thread_send.start()
thread_receive.start()