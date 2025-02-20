def repeating_key_xor(plaintext, key):
    key_len = len(key)
    ciphertext = []

    for i, char in enumerate(plaintext):
        key_byte = key[i % key_len]
        ciphertext.append(chr(char ^ ord(key_byte)))
    
    return ''.join(ciphertext)

plaintext = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = "ICE"

plaintext_bytes = plaintext.encode('utf-8')

ciphertext = repeating_key_xor(plaintext_bytes, key)

ciphertext_hex = ciphertext.encode('utf-8').hex()
print(ciphertext_hex)

result = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
if ciphertext_hex == result:
    print("Test passed !")