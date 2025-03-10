def xor_buffers(buf1, buf2):
    if len(buf1) != len(buf2):
        raise ValueError("Les tampons doivent avoir la même longueur.")
    return bytes(a ^ b for a, b in zip(buf1, buf2))

def hex_xor(hex1, hex2):
    buf1 = bytes(int(hex1[i:i+2], 16) for i in range(0, len(hex1), 2))
    buf2 = bytes(int(hex2[i:i+2], 16) for i in range(0, len(hex2), 2))
    return xor_buffers(buf1, buf2).hex()

hex1 = "1c0111001f010100061a024b53535009181c"
hex2 = "686974207468652062756c6c277320657965"
result = hex_xor(hex1, hex2)
print("XOR Result :", result)

rep = '746865206b696420646f6e277420706c6179'
if result == rep:
    print("Chall 2 passed")