from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

key = b"YELLOW SUBMARINE"

def decrypt_aes_ecb(base64_encrypted_data):

    ciphertext = base64.b64decode(base64_encrypted_data)
    cipher = AES.new(key, AES.MODE_ECB)

    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return decrypted_data.decode('utf-8')

def decrypt_file(file_path):
    with open(file_path, 'r') as f:
        encoded_data = f.read().strip()

    decrypted_message = decrypt_aes_ecb(encoded_data)
    return decrypted_message

file_path = "data_chall7_cryptopals.txt"
decrypted_message = decrypt_file(file_path)
print(decrypted_message)
