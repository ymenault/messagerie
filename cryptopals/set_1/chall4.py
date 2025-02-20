from collections import Counter

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

best_overall_score = float('-inf')
best_overall_result = (None, None, None)

with open("data_chall4_cryptopals.txt", "r") as file:
    for line in file:
        hex_data = line.strip()
        if hex_data:
            cipher_bytes = hex_to_bytes(hex_data)
            key, decrypted_text, score = single_byte_xor_crack(cipher_bytes)
            
            if score is not None and score > best_overall_score:
                best_overall_score = score
                best_overall_result = (key, decrypted_text, score)

key, decrypted_text, _ = best_overall_result
if key is not None:
    print(f"Key: {chr(key)} ({key})")
    print(f"Decrypted text: {decrypted_text}")
else:
    print("No valid decryption found.")
