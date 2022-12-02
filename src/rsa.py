import math
import random
import sympy

def encrypt_rsa(plain_text, key):
    pkey, n = key
    cipher = [(ord(char) ** pkey) % n for char in plain_text]
    return cipher

def decrypt_rsa(cipher_text, key):
    pkey, n = key
    cipher = [chr((char ** pkey) % n) for char in cipher_text]
    return ''.join(cipher)

def generate_keypair(p, q):
    minLCM = p * q
    randgen = (p - 1) * (q - 1)

    rand = random.randrange(1, randgen)
    gcd = math.gcd(rand, randgen)

    while gcd != 1:
        rand = random.randrange(1, randgen)
        gcd = math.gcd(rand, randgen)

    inverse = multi_Inverse(rand, randgen) 

    return ((rand, minLCM), (inverse, minLCM))

def multi_Inverse(Y, M):
 
    for X in range(1, M):
        if (((Y % M) * (X % M)) % M == 1):
            return X
    return -1

p = sympy.randprime(1, 100)
q = sympy.randprime(1, 100)

public, private = generate_keypair(p, q)

message = input("Enter message you wish to encrypt: ")

encrypt_message = encrypt_rsa(message, public)
print(encrypt_message)

decrypt_message = decrypt_rsa(encrypt_message, private)

print("Decrypted Message: " + decrypt_rsa(encrypt_message, private))