import binascii

def detect_aes_ecb(hex_ciphertext):

    ciphertext = binascii.unhexlify(hex_ciphertext.strip())

    block_size = 16
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]

    seen_blocks = set()
    for block in blocks:
        if block in seen_blocks:
            return True
        seen_blocks.add(block)
    
    return False

def detect_ecb_in_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if detect_aes_ecb(line):
                print("Possible AES-ECB encryption detected in line:")
                print(line)
                break

file_path = "data_chall8_cryptopals.txt"
detect_ecb_in_file(file_path)
