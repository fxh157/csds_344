import math

#returns the encrypted cipher
def encrypt_rsa(plain_text, key):
    ciphtext, x = key
    encryptedCiph = [(ord(char) ** ciphtext) % x for char in plain_text]
    return encryptedCiph

#returns the decrypted cipher
def decrypt_rsa(cipher_text, key):
    ciphtext, x = key
    decryptedCiph = [chr((char ** ciphtext) % x) for char in cipher_text]
    return ''.join(decryptedCiph)

#Calculates the public and private keys
#I use 65357 here because it's an extremely commonly used and reliable large prime number for RSA algorithms
def create_keys(x, y):
    randgen = (x - 1) * (y - 1)

    greatest_com_denom = math.gcd(65357, randgen)

    while greatest_com_denom != 1:
        greatest_com_denom = math.gcd(65357, randgen)

    inverse = multi_Inverse(65357, randgen) 
    return ((65357, x * y), (inverse, x * y))

#calculates the multiplicative inverse for the key creation algorithm
def multi_Inverse(n, m):
 
    for x in range(1, m):
        if (((n % m) * (x % m)) % m == 1):
            return x

    return -1

