#import numpy as np

def format_key(input):
    try: key_decimal = int(input, 16)
    except: return False

    return hex(key_decimal), bin(key_decimal)

def format_input(message, key, encrypt):
    #Converts message and key as strings into binary arrays
    #message becomes 2d array, each row is a block
    #key becomes 2d array, each row is a key, in order to be used
    #encrypt is boolean - determines key order

    #Form blocks from message input
    binary = ""
    for char in message:
        char_ascii = bin(ord(char))[2:]
        binary += char_ascii

    n = 64
    blocks = [binary[i:i+n] for i in range(0, len(binary), n)]
    
    #Pad last block with zeros
    while len(blocks[-1]) < 64:
        blocks[-1] += '0'

    #Form round keys from key input
    keys = get_round_keys(key)

    #Invert key order if decrypting
    if not encrypt: 
        keys = keys[::-1]

    return blocks, keys

def format_output(binary):
    output = ''
    n = 7
    chars = [binary[i:i+n] for i in range(0, len(binary), n)]
    for char in chars:
        output += chr(int(char, 2))
    return output.rstrip('\t\r\n\0')


def des_algorithm(input_text, input_key, encrypt):
    blocks, keys = format_input(input_text, input_key, encrypt)
    binary_output = ''

    for block in keys: print (len(block))
    print (len(keys))
    """
    for block in blocks:
        binary_output += encrypt_block(block, keys)

    return output
    """

def encrypt_block(block, keys):
    raise NotImplementedError()

#round-key generation
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
    key_array = [*f'{int(key, 2):064b}']

    new_key = [0] * len(indices)

    for i, index in enumerate(indices):
        new_key[i] = key_array[index]

    output = ''
    for b in new_key:
        output += b

    return output

def circular_shift(binary, n):
    #Since we know every value that uses this function will be 28 bits, we can hardcode that:
    return binary[n:] + binary[:n]

def get_round_keys(key):
    keys = []

    __, key_binary = format_key(key)

    key_binary = reorder_bits(key_binary, pc1)

    left_key = key_binary[0:27]
    right_key = key_binary[28:55]

    for i in range(16):
        keys.append(reorder_bits(left_key + right_key, pc2))

        if len(keys) < 16:
            shift = 1 if i in [0, 1, 8, 15] else 2
            left_key = circular_shift(left_key, shift)
            right_key = circular_shift(right_key, shift)

    return keys

if __name__ == '__main__':
    #Test functions here:
    key = '0c4ba51608cfae10'
    message = 'Here is a message to test encryption functions with'
    des_algorithm(message, key, True)