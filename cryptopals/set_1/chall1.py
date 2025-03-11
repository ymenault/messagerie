def hex_to_base64(hex_str):

    if len(hex_str) % 2 != 0:
        raise ValueError("Chaîne hexadécimale invalide.")
    
    bytes_data = bytes(int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2))
    
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    base64_str = ""
    
    padding = (3 - len(bytes_data) % 3) % 3
    bytes_data += b'\x00' * padding
    
    for i in range(0, len(bytes_data), 3):
        combined = (bytes_data[i] << 16) | (bytes_data[i+1] << 8) | bytes_data[i+2]
        base64_str += base64_chars[(combined >> 18) & 0x3F]
        base64_str += base64_chars[(combined >> 12) & 0x3F]
        base64_str += base64_chars[(combined >> 6) & 0x3F]
        base64_str += base64_chars[combined & 0x3F]
    
    if padding:
        base64_str = base64_str[:-padding] + "=" * padding
    
    return base64_str

hex_input = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
try:
    base64_output = hex_to_base64(hex_input)
    print("Base64 :", base64_output)
    rep = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
    if rep == base64_output:
        print("Test passed")

except ValueError:
    print("Erreur : Chaîne hexadécimale invalide.")