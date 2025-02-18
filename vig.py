import random

def encrypt(message, key):
    message = message.lower()
    encrypted_message = ""
    for i in range(len(message)):
        if message[i].isalpha():
            ascii_code = ord(message[i])
            ascii_code += ord(key[i % len(key)]) - 97
            if ascii_code > 122:
                ascii_code -= 26
            encrypted_message += chr(ascii_code)
        else:
            encrypted_message += message[i]
    return encrypted_message

def decrypt(message, key):
    message = message.lower()
    decrypted_message = ""
    for i in range(len(message)):
        if message[i].isalpha():
            ascii_code = ord(message[i])
            ascii_code -= ord(key[i % len(key)]) - 97
            if ascii_code < 97:
                ascii_code += 26
            decrypted_message += chr(ascii_code)
        else:
            decrypted_message += message[i]
    return decrypted_message


def generate_random_string(length):
    letters = "abcdefghijklmnopqrstuvwxyz"
    return ''.join(random.choice(letters) for _ in range(length))