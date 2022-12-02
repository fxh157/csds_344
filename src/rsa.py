import math
import random

def encrypt_rsa(plain_text, key):
    ciphtext, n = key
    cipher = [(ord(char) ** ciphtext) % n for char in plain_text]
    return cipher

def decrypt_rsa(cipher_text, key):
    ciphtext, n = key
    cipher = [chr((char ** ciphtext) % n) for char in cipher_text]
    return ''.join(cipher)

def create_keys(p, q):
    randgen = (p - 1) * (q - 1)

    rand = random.randrange(1, randgen)
    gcd = math.gcd(rand, randgen)

    while gcd != 1:
        rand = random.randrange(1, randgen)
        gcd = math.gcd(rand, randgen)

    inverse = multi_Inverse(rand, randgen) 
    return ((rand, p * q), (inverse, p * q))

def multi_Inverse(n, m):
 
    for x in range(1, m):
        if (((n % m) * (x % m)) % m == 1):
            return x

    return -1

