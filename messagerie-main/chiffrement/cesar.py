def encrypt(message, key):
    key = int(key)
    encrypted_message = ""
    for char in message:
        ascii_code = ord(char)
        if ascii_code >= 32 and ascii_code <= 126:  # Caractères imprimables ASCII
            ascii_code = ((ascii_code - 32 + key) % 95) + 32
        encrypted_message += chr(ascii_code)
    return encrypted_message
    
def decrypt(message, key):
    key = int(key)
    decrypted_message = ""
    for char in message:
        ascii_code = ord(char)
        if ascii_code >= 32 and ascii_code <= 126:  # Caractères imprimables ASCII
            ascii_code = ((ascii_code - 32 - key) % 95) + 32
        decrypted_message += chr(ascii_code)
    return decrypted_message