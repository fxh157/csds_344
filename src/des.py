#import numpy as np
from sbox import sbox

def format_key(input):
    try: key_decimal = int(input, 16)
    except: return False,

    return hex(key_decimal), f'{key_decimal:064b}'

def format_input(message, key, encrypt):
    #Converts message and key as strings into binary arrays
    #message becomes 2d array, each row is a block
    #key becomes 2d array, each row is a key, in order to be used
    #encrypt is boolean - determines key order

    # Pad message to fit 64-bit block format
    while len(message) * 7 % 64 != 0:
        message += '\0'

    #Form blocks from message input
    binary = ""
    for char in message:
        char_ascii = f'{ord(char):07b}'
        binary += char_ascii

    n = 64
    blocks = [binary[i:i+n] for i in range(0, len(binary), n)]

    #Form round keys from key input
    keys = get_round_keys(key)

    #Invert key order if decrypting
    if not encrypt: keys = keys[::-1]

    return blocks, keys

def format_output(binary):
    output = ''
    n = 7
    chars = [binary[i:i+n] for i in range(0, len(binary), n)]
    for char in chars:
        output += chr(int(char, 2))
    return output.rstrip('\t\r\n\0')


#round-key generation
#note: all index arrays are 1-indexed; decrement is applied in reorder()
pc1 = [
  57,49,41,33,25,17,9, 
  1,58,50,42,34,26,18, 
  10,2,59,51,43,35,27, 
  19,11,3,60,52,44,36,           
  63,55,47,39,31,23,15, 
  7,62,54,46,38,30,22, 
  14,6,61,53,45,37,29, 
  21,13,5,28,20,12,4 
]
pc2 = [
  14,17,11,24,1,5, 
  3,28,15,6,21,10, 
  23,19,12,4,26,8, 
  16,7,27,20,13,2, 
  41,52,31,37,47,55, 
  30,40,51,45,33,48, 
  44,49,39,56,34,53, 
  46,42,50,36,29,32 
]

def reorder_bits(key, indices):
    key_array = [*f'{int(key, 2):0{len(key)}b}']

    new_key = [0] * len(indices)

    for i, index in enumerate(indices):
        new_key[i] = key_array[index - 1]

    output = ''
    for b in new_key:
        output += b

    return output

def circular_shift(binary, n):
    return binary[n:] + binary[:n]

def get_round_keys(key):
    keys = []

    __, key_binary = format_key(key)

    key_binary = reorder_bits(key_binary, pc1)

    left_key = key_binary[:28]
    right_key = key_binary[28:]

    for i in range(16):
        keys.append(reorder_bits(left_key + right_key, pc2))

        if len(keys) < 16:
            shift = 1 if i in [0, 1, 8, 15] else 2
            left_key = circular_shift(left_key, shift)
            right_key = circular_shift(right_key, shift)

    return keys

initial_permutation = [
    58,50,42,34,26,18,10,2, 
    60,52,44,36,28,20,12,4, 
    62,54,46,38,30,22,14,6, 
    64,56,48,40,32,24,16,8, 
    57,49,41,33,25,17,9,1, 
    59,51,43,35,27,19,11,3, 
    61,53,45,37,29,21,13,5, 
    63,55,47,39,31,23,15,7
]
final_permutation = [
    40,8,48,16,56,24,64,32,
    39,7,47,15,55,23,63,31,
    38,6,46,14,54,22,62,30,
    37,5,45,13,53,21,61,29,
    36,4,44,12,52,20,60,28,
    35,3,43,11,51,19,59,27,
    34,2,42,10,50,18,58,26,
    33,1,41,9,49,17,57,25
]
expansion_table = [
  32,1,2,3,4,5,4,5, 
  6,7,8,9,8,9,10,11, 
  12,13,12,13,14,15,16,17, 
  16,17,18,19,20,21,20,21, 
  22,23,24,25,24,25,26,27, 
  28,29,28,29,30,31,32,1 
]
permutation_table = [
    16,7,20,21,29,12,28,17, 
    1,15,23,26,5,18,31,10, 
    2,8,24,14,32,27,3,9, 
    19,13,30,6,22,11,4,25 
]

def xor(bin1, bin2):
    if (len(bin1) != len(bin2)):
        print("ERR: inputs to xor are differing lengths")
        print(len(bin1))
        print(len(bin2))

    output = ''
    for i in range(len(bin1)):
        output += '0' if bin1[i] == bin2[i] else '1'
    return output


def encrypt_block(block, keys):
    # Initial Permutation
    block = reorder_bits(block, initial_permutation)
    # Split into left and right parts
    left, right = block[:32], block[32:]

    for key in keys:
        expanded = reorder_bits(right, expansion_table)
        expanded = xor(expanded, key)
        expanded = sbox(expanded)
        expanded = reorder_bits(expanded, permutation_table)
        expanded = xor(expanded, left)
        left = right
        right = expanded


    # Final Permutation
    output = reorder_bits(right + left, final_permutation)
    
    return output

def des_algorithm(input_text, input_key, encrypt):
    blocks, keys = format_input(input_text, input_key, encrypt)
    binary_output = ''

    
    for block in blocks:
        binary_output += encrypt_block(block, keys)

    output = format_output(binary_output)
    return output

if __name__ == '__main__':
    #Test functions here:
    key = '0c4ba51608cfae10'
    plain_text = 'This is a random test message.'
    print(f'message: {plain_text}')
    cipher_text = des_algorithm(plain_text, key, True)
    print()
    print(f'cipher: {cipher_text}')
    print()
    result = des_algorithm(cipher_text, key, False)
    print (f'output: {result}')