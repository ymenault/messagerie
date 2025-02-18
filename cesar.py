import random

key = 5

def encrypt(message):
    encrypted_message = ""
    for letter in message:
        if letter.isalpha():
            ascii_code = ord(letter)
            if ascii_code >= 65 and ascii_code <= 90:
                ascii_code += key
                if ascii_code > 90:
                    ascii_code -= 26
            elif ascii_code >= 97 and ascii_code <= 122:
                ascii_code += key
                if ascii_code > 122:
                    ascii_code -= 26
            encrypted_message += chr(ascii_code)
        else:
            encrypted_message += letter
    return encrypted_message
    
def decrypt(message):
    decrypted_message = ""
    for letter in message:
        if letter.isalpha():
            ascii_code = ord(letter)
            if ascii_code >= 65 and ascii_code <= 90:
                ascii_code -= key
                if ascii_code < 65:
                    ascii_code += 26
            elif ascii_code >= 97 and ascii_code <= 122:
                ascii_code -= key
                if ascii_code < 97:
                    ascii_code += 26
            decrypted_message += chr(ascii_code)
        else:
            decrypted_message += letter
    return decrypted_message

