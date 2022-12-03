import re

# encryption function
def encrypt_vigenere(plain_text, key):
	encryption = ""
    # removes any characters that are not alphabetical
	regex = re.compile('[^a-zA-Z]')
	plain_text = list(regex.sub("", plain_text))
	key = list(key)
	for i in range(len(plain_text)):
        # encrypts message using the key to shift the characters
		encryption += chr((ord(plain_text[i]) + ord(key[i % len(key)])) % 97 % 26 + 97)
	return "".join(encryption)

# decryption function
def decrypt_vigenere(encrypted_text, key):
	decryption = ""
	encrypted_text = list(encrypted_text)
	key = list(key)
	for i in range(len(encrypted_text)):
        # decryps message using the key to derive the original characters
		decryption += chr((ord(encrypted_text[i]) - ord(key[i % len(key)]) + 26) % 26 + 97)
	return "".join(decryption)

