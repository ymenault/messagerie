import base64

def hamming_distance(str1, str2):
    assert len(str1) == len(str2), "Les chaînes comparées doivent être de la même taille"
    return sum(bin(byte1 ^ byte2).count('1') for byte1, byte2 in zip(str1, str2))

def normalized_hamming_distance(ciphertext, keysize):
    distances = []
    for i in range(0, len(ciphertext) - keysize, keysize):
        block1 = ciphertext[i:i+keysize]
        block2 = ciphertext[i+keysize:i+2*keysize]
        if len(block1) == len(block2):
            dist = hamming_distance(block1, block2)
            distances.append(dist / keysize)
    return sum(distances) / len(distances) if distances else float('inf')

def find_best_keysize(ciphertext):
    best_keysize = None
    best_distance = float('inf')
    for keysize in range(2, 41):
        distance = normalized_hamming_distance(ciphertext, keysize)
        if distance < best_distance:
            best_distance = distance
            best_keysize = keysize
    return best_keysize

def transpose_blocks(ciphertext, keysize):
    blocks = [bytearray() for _ in range(keysize)]
    for i in range(len(ciphertext)):
        blocks[i % keysize].append(ciphertext[i])
    return blocks

def score_text(text):
    freq = "ETAOIN SHRDLU"
    return sum(text.upper().count(c) for c in freq)

def single_byte_xor_decrypt(block):
    best_score = float('-inf')
    best_text = None
    best_key = None
    for key in range(256):
        decrypted_text = bytes([b ^ key for b in block])
        score = score_text(decrypted_text.decode(errors='ignore'))
        if score > best_score:
            best_score = score
            best_text = decrypted_text
            best_key = key
    return best_key, best_text

def decrypt_repeating_key_xor(ciphertext):
    keysize = find_best_keysize(ciphertext)
    print(f"Best KEYSIZE: {keysize}")
    blocks = transpose_blocks(ciphertext, keysize)
    key = []
    for block in blocks:
        key_byte, _ = single_byte_xor_decrypt(block)
        key.append(key_byte)
    print(f"Key: {bytes(key).decode('utf-8')}")
    decrypted_text = bytes([ciphertext[i] ^ key[i % keysize] for i in range(len(ciphertext))])
    return decrypted_text.decode(errors='ignore')

def decrypt_file(file_path):
    with open(file_path, 'r') as f:
        encoded_data = f.read().strip()
    ciphertext = base64.b64decode(encoded_data)
    decrypted_text = decrypt_repeating_key_xor(ciphertext)
    return decrypted_text

file_path = "data_chall6_cryptopals.txt"
decrypted_message = decrypt_file(file_path)
print(decrypted_message)
