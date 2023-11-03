from sklearn.utils import murmurhash3_32
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random

random.seed(42)

def twoUniHash(a, x, b):
    return ((a * x + b) % P) % 1024

def threeUniHash(a,x,b,c):
    return ((a * x ** 2 + b * x + c) % P) % 1024

def fourUniHash(a,x,b,c,d):
    return ((a * x ** 3 + b * x ** 2 + c * x + d) % P) % 1024

def decimalToBinary(n):
    return format(n, '010b')

def decimalToBinary2(n):
    return format(n, '031b')

def binaryToDecimal(n):
    return int(n,2)

a = random.randrange(1, 1048573)
b = random.randrange(1, 1048573)
c = random.randrange(1, 1048573)
d = random.randrange(1, 1048573)
P = 1048573
two_uni_mat = []
three_uni_mat= []
four_uni_mat = []
murmur_uni_mat = []
mat_list = [two_uni_mat, three_uni_mat, four_uni_mat]


for i in range(10):
    temp = []
    temp1= []
    temp2 = []
    temp3 = []
    for j in range(31):
        temp.append(0)
        temp1.append(0)
        temp2.append(0)
        temp3.append(0)
    two_uni_mat.append(temp)
    three_uni_mat.append(temp1)
    four_uni_mat.append(temp2)
    murmur_uni_mat.append(temp3)

#generate 5000 bits
for i in range(5000):
    #get the number
    rand_num = random.getrandbits(31)
    
    #turn them into binary
    rand_bits = decimalToBinary2(rand_num)

    #store the hashed value
    two_hash_val = decimalToBinary(twoUniHash(a, rand_num, b))
    three_hash_val = decimalToBinary(threeUniHash(a,rand_num,b,c))
    four_hash_val = decimalToBinary(fourUniHash(a,rand_num,b,c,d))
    mur_hash_val = murmurhash3_32(key=np.int32(rand_num), seed=42, positive=True) % 1024
    mur_hash_val = decimalToBinary(mur_hash_val)

    for bit_idx in range(len(rand_bits)):
        #generate the new number
        if rand_bits[bit_idx] == "1":
            new_rand_bits = rand_bits[:bit_idx] + "0" + rand_bits[bit_idx + 1:]
        else:
            new_rand_bits = rand_bits[:bit_idx] + "1" + rand_bits[bit_idx + 1:]
        #get decimal value
        new_rand_num = binaryToDecimal(new_rand_bits)
        new_two_hash = decimalToBinary(twoUniHash(a, new_rand_num, b))
        new_three_hash = decimalToBinary(threeUniHash(a,new_rand_num,b,c))
        new_four_hash = decimalToBinary(fourUniHash(a,new_rand_num,b,c,d))
        new_mur_hash_val = murmurhash3_32(key=np.int32(new_rand_num), seed=42, positive=True) % 1024
        new_mur_hash_val = decimalToBinary(new_mur_hash_val)

        for idx in range(len(two_hash_val)):
            if two_hash_val[idx] != new_two_hash[idx]:
                two_uni_mat[idx][bit_idx] += 1/5000

        for idx in range(len(three_hash_val)):
            if three_hash_val[idx] != new_three_hash[idx]:
                three_uni_mat[idx][bit_idx] += 1/5000

        for idx in range(len(four_hash_val)):
            if four_hash_val[idx] != new_four_hash[idx]:
                four_uni_mat[idx][bit_idx] += 1/5000
            
        for idx in range(len(mur_hash_val)):
            if mur_hash_val[idx] != new_mur_hash_val[idx]:
                murmur_uni_mat[idx][bit_idx] += 1/5000

two_uni_mat = np.array(two_uni_mat)
three_uni_mat = np.array(three_uni_mat)
four_uni_mat = np.array(four_uni_mat)
murmur_uni_mat = np.array(murmur_uni_mat)

plt.imshow(two_uni_mat)
plt.colorbar()
plt.show()

plt.imshow(three_uni_mat)
plt.colorbar()
plt.show()

plt.imshow(four_uni_mat)
plt.colorbar()
plt.show()

plt.imshow(murmur_uni_mat)
plt.colorbar()
plt.show()
