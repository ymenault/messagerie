import random

cle = 10

def encrypt_cesar(message,cle):
    message = message.upper()
    message_crypte = ""
    for lettre in message:
        if lettre == " ":
            message_crypte += " "
        else:
            message_crypte += chr((ord(lettre) + cle - 65) % 26 + 65)
    return message_crypte

def decrypt_cesar(message,cle):
    message = message.upper()
    message_decrypte = ""
    for lettre in message:
        if lettre == " ":
            message_decrypte += " "
        else:
            message_decrypte += chr((ord(lettre) - cle - 65) % 26 + 65)
    return message_decrypte