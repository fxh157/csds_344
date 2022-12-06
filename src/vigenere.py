# encryption function
def encrypt_vigenere(plain_text, key):
    encryption = ""
    # removes any characters that are not alphabetical
    plain_text = plain_text.replace(" ", "").lower()
    key = key.replace(" ", "").lower() 
    for i in range(len(plain_text)):
        # encrypts message using the key to shift the characters
        encryption += chr((ord(plain_text[i]) + ord(key[i % len(key)])) % 97 % 26 + 97)
    return "".join(encryption)

# decryption function
def decrypt_vigenere(encrypted_text, key):
    decryption = ""
    key = key.replace(" ", "").lower()
    for i in range(len(encrypted_text)):
        # decryps message using the key to derive the original characters
        decryption += chr((ord(encrypted_text[i]) - ord(key[i % len(key)]) + 26) % 26 + 97)
    return "".join(decryption)


if __name__ == "__main__":
    message = "my name is Haywood Jablomi"
    print(message)
    key = "hidden message"
    print(key)
    encrypted_message = encrypt_vigenere(message, key)
    print(encrypted_message)
    decrypted_message = decrypt_vigenere(encrypted_message, key)
    print(decrypted_message)


