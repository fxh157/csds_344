import math
import sys


#predifined rotation amounts
#For each of the 64 opperations there is a specific amount of bit rotations that will rotate the bits
bit_rotations = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]


#predifined input array of hex values used to start (from guidelines)
input_arr = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]




#each of the 512 bit blocks is split into 16 32 bit blocks that are used as inputs at each level. This array varies the input order as required by the algorithm
#This order is then repeated for each block of 512
order = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],[1,6,11,0,5,10,15,4,9,14,3,8,13,2,7,12],[5,8,11,14,1,4,7,10,13,0,3,6,9,12,15,2],[0,7,14,5,12,3,10,1,8,15,6,13,4,11,2,9]]

#takes a string array and outputs string of binary digits representing the string
def str_to_bin(s_arr):
    j = ""
    j = j.join(s_arr) #join all the strings together
    out = int.from_bytes(j.encode(), "big") #econdes the text
    output = bin(out).replace('b','') #convert to binary python adds a b character --> remove it
    tot_len=len(output)
    return output, tot_len


#Don't use this does not account for message length correctly
def split(input, tot_len):
    arr = [input[i:i+447] for i in range(0, len(input), 447)] #splits into chunks at most 447bits
    output = []
    for j in arr:
        #bit_len = (len(j))%2**64
        byte_arr = tot_len.to_bytes(8, byteorder='little') #returns a byte array of 8 length that has the LSB at the front
        len_str = (bin(int.from_bytes(byte_arr)).replace('b','')[-64:])
        temp = j
        temp += '1' #add the one padding digit
        while len(temp) != 448:
            temp += '0' #fill the rest with 0's
        temp += len_str
        output.append(temp)
    return output

#Correct split method:
#1 - append '1' for padding
#2 - append '0's untl the length of the message string is congruent to 448, modulo 512 so we can append length at the end to make devisable by 512
#3 - append length of original message in bits to the end making sure the byteorder is little so the LSB are at the front as is convention for this
def split2(input):
    leng = len(input)
    temp = input
    temp += '1' #add one bit of padding
    #add in 0 padding
    while len(temp)%512 != 448:
        temp += '0'
    byte_arr = leng.to_bytes(8, byteorder='little')  # returns a byte array of 8 length that has the LSB at the front
    len_str = (bin(int.from_bytes(byte_arr, byteorder="big")).replace('b', '')[-64:]) #only returns the 64 lsb if the entry string is really long
    temp += len_str
    output = [temp[i:i+512] for i in range(0, len(temp), 512)] #splits into size 512 chunks
    return output



#medthod described in ietf specifications
def bit_shift(x, amount):
    return ((x << amount) | (x>>(32-amount))) & 0xFFFFFFFF #left bit shift by amount then add the bits shifted to the back end. can't be larger than 32bits


def function(num, b , c, d):
    if num == 1:
        return (b & c) | (~b & d)
    elif num == 2:
        return (d & b) | (~d & c)
    elif num == 3:
        return b ^ c ^ d
    else:
        return c ^ (b | ~d)


#main body of md5 algorithm
def md5(input):
    global input_arr
    for j in input:
        temp = [j[i:i+32] for i in range(0, len(j), 32)]
        m = []
        #splits input into 16 32-bit blocks called "words" each byte individually is bigendian where the words are little endian (msb is last)
        for i in temp:
            raw = int(i,2).to_bytes(4, byteorder="little") #md5 word sections are little endian with bytes per word
            m.append(int.from_bytes(raw, byteorder="big"))
        #loop through the m values for each itteration
        init = input_arr[:]
        cnt = 1
        cons = 0x100000000
        for count,k in enumerate(order): #for each of the 4 operations run function and reset inputs
            for num, m_i in enumerate(k):
                replace = []
                ki = int(abs(math.sin(cnt)) * 2**32) #constant to be added to resulting function. Different constant each time.
                f = function(count+1, init[1], init[2], init[3])
                step_0 = (f + init[0])&0xFFFFFFFF#modular addition of init[0] and result of function
                step_1 = (step_0 + m[m_i]) & 0xFFFFFFFF
                step_2 = (step_1 + ki)&0xFFFFFFFF # Modular addition of k[i] and prev step
                step_3 = bit_shift(step_2, bit_rotations[cnt-1]) #bit shift predetermined amountr
                step_4 = (step_3 + init[1])&0xFFFFFFFF
                replace.extend([init[3],step_4,init[1],init[2]]) #replace A=D, B = Step_4, C=B, D=C
                init = replace
                cnt +=1
        rep = []
        for num in range(len(init)):
            rep.append((init[num]+input_arr[num])&0xFFFFFFFF)#Final modular addition with initial inputs 
        input_arr = rep
    hash = ""
    for entry in input_arr:
        raw = entry.to_bytes(4, byteorder="little")
        hash += '{:08x}'.format(int.from_bytes(raw, byteorder='big'))
    return(hash)


def encrypt_md5(plain_text, key):
    #Process and convert to binary
    raw_input, tot_len = str_to_bin(plain_text)

    #Split into correct sized blocks
    #input = split(raw_input, tot_len)
    input = split2(raw_input)

    #run the md5 algorithm
    return(md5(input))
