import math
import sys

#predifined rotation amounts
bit_rotations = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]


#predifined input array of hex values used to start
input_arr = [0x01234567,0x89abcdef, 0xfedcba98,0x76543210]

#each of the 512 bit blocks is split into 16 32 bit blocks that are used as inputs at each level. This array varies the input order as required by the algorithm
order = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],[1,6,11,0,5,10,15,4,9,14,3,8,13,2,7,12],[5,8,11,14,1,4,7,10,13,0,3,6,9,12,15,2],[0,7,14,5,12,3,10,1,8,15,6,13,4,11,2,9]]

#takes a string and outputs binary
def str_to_bin(s_arr):
    print(bit_rotations[16])
    j = ""
    j = j.join(s_arr)
    out = int.from_bytes(j.encode(), "big") #econdes the text
    output = bin(out).replace('b','') #convert to binary python adds a b character --> remove it
    return output

#
def split(input):
    og_len = len(input)
    arr = [input[i:i+447] for i in range(0, len(input), 447)] #splits into chunks 176 bits in length
    output = []
    for j in arr:
        bin_len = bin(len(j)).replace('b','')
        temp = j
        temp += '1' #add the one padding digit
        while len(temp) != 448:
            temp += '0' #fill the rest with 0's
        length = bin_len[len(bin_len) - 64:]
        while len(length) != 64:
            length = '0' + length
        temp = temp + length
        output.append(temp)
    return output


def bit_shift(x, amount):
    return ((x << amount) | (x>>(32-amount))) & 0xFFFFFFFF #left bit shift by amount then add the bits shifted to the back end


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
        #splits input into 16 32-bit blocks
        for i in temp:
            m.append(int(i,2))
        #loop through the m values for each itteration
        #init = [hex(int(z)) for z in input_arr]
        init = []
        init = input_arr
        cnt = 1
        cons = 0x100000000
        for count,k in enumerate(order): #for each of the 4 operations run function and reset inputs
            for m_i in k:
                replace = []
                print(count+1)
                ki = int(abs(math.sin(cnt)) * 2**32) #constant to be added to resulting function. Different constant each time.
                f = function(count+1, init[1], init[2], init[3])
                step_0 = (f + init[0])&0xFFFFFFFF#modular addition of init[0] and result of function
                step_1 = (step_0 + m[m_i])&0xFFFFFFFF # modular addition of section of input message and function output
                step_2 = (step_1 + ki)&0xFFFFFFFF # Modular addition...
                step_3 = bit_shift(step_2, bit_rotations[cnt-1])
                step_4 = (step_3 + init[1])&0xFFFFFFFF
                replace.extend([init[3],step_4,init[1],init[2]])
                init = replace
                cnt +=1
        rep = []
        for num in range(len(init)):
            rep.append((init[num]+input_arr[num])&0xFFFFFFFF)
        input_arr = rep
        print(input_arr)
    final_hash = [hex(int(z)) for z in input_arr]
    print(final_hash)
    hash = ""
    for x in final_hash:
        hash += x[2:]
    return(hash)



#Designing this to read text from a file
#might need to play around with inputs for other things
def main():
    #Process and convert to binary
    args = sys.argv[1:]
    with open(args[0], "r") as file:  # how do i get it to input a line
        lines = file.readlines()
    s = []
    for l in lines:
        s.append(l)
    raw_input = str_to_bin(s)

    #Split into correct sized blocks
    input = split(raw_input)

    #run the md5 algorithm
    print(md5(input))



if __name__ == '__main__':
    main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
