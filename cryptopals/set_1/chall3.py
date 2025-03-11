from collections import Counter

data = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def hex_to_bytes(hex_str):
    return bytes.fromhex(hex_str)

def xor_decrypt(ciphertext, key):
    return bytes([b ^ key for b in ciphertext])

def score_text(text):
    freq = "ETAOIN SHRDLU"
    return sum(text.upper().count(c) for c in freq)

def single_byte_xor_crack(ciphertext):
    best_score = 0
    best_result = (None, None, None)
    
    for key in range(256):
        plaintext = xor_decrypt(ciphertext, key)
        try:
            decoded_text = plaintext.decode('utf-8')
            score = score_text(decoded_text)
            
            if score > best_score:
                best_score = score
                best_result = (key, decoded_text, score)
        except UnicodeDecodeError:
            continue
    
    return best_result

cipher_bytes = hex_to_bytes(data)
key, decrypted_text, _ = single_byte_xor_crack(cipher_bytes)
print(f"Key: {chr(key)} ({key})")
print(f"Decrypted text: {decrypted_text}")