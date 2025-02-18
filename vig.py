import random

key = "KEY"

def encrypt(message):
    encrypted_message = ""
    for i in range(len(message)):
        if message[i].isalpha():
            ascii_code = ord(message[i])
            if ascii_code >= 65 and ascii_code <= 90:
                ascii_code += ord(key[i % len(key)]) - 65
                if ascii_code > 90:
                    ascii_code -= 26
            elif ascii_code >= 97 and ascii_code <= 122:
                ascii_code += ord(key[i % len(key)]) - 97
                if ascii_code > 122:
                    ascii_code -= 26
            encrypted_message += chr(ascii_code)
        else:
            encrypted_message += message[i]
    return encrypted_message

def decrypt(message):
    decrypted_message = ""
    for i in range(len(message)):
        if message[i].isalpha():
            ascii_code = ord(message[i])
            if ascii_code >= 65 and ascii_code <= 90:
                ascii_code -= ord(key[i % len(key)]) - 65
                if ascii_code < 65:
                    ascii_code += 26
            elif ascii_code >= 97 and ascii_code <= 122:
                ascii_code -= ord(key[i % len(key)]) - 97
                if ascii_code < 97:
                    ascii_code += 26
            decrypted_message += chr(ascii_code)
        else:
            decrypted_message += message[i]
    return decrypted_message