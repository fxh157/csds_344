import math
import random

def encrypt_rsa(plain_text, key):
    cipherkey, n = key
    encryptedBlock = [(ord(char) ** cipherkey) % n for char in plain_text]
    return encryptedBlock

def decrypt_rsa(encrypted_text, key):
    cipherkey, n = key
    decryptedBlock = [chr((char ** cipherkey) % n) for char in encrypted_text]
    return ''.join(decryptedBlock)

def create_keys(p, q):
    minLCM = p * q
    randgen = (p - 1) * (q - 1)

    rand = random.randrange(1, randgen)
    gcd = math.gcd(rand, randgen)

    while gcd != 1:
        rand = random.randrange(1, randgen)
        gcd = math.gcd(rand, randgen)

    inverse = multi_Inverse(rand, randgen) 

    return ((rand, minLCM), (inverse, minLCM))

def multi_Inverse(n, m):
 
    for x in range(1, m):
        if (((n % m) * (n % m)) % m == 1):
            return x
    return -1
