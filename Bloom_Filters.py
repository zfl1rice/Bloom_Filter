import numpy
import random
import bitarray
from sklearn.utils import murmurhash3_32
import math
import csv
import string
import pandas as pd


def hashfunc(m, seed):
    def hash(key):
        return murmurhash3_32(key, seed) % m

    return hash

class BloomFilter:
    def __init__(self, fp_rate, n):
        self.fp_rate = fp_rate
        self.n = n

        #init r and k
        self.r = int(2 ** (math.log(int(self.n * math.log(self.fp_rate) / math.log(0.618)), 2)))
        self.k = int(self.r / self.n * math.log(2))

        #init bitarray
        self.bitarray = bitarray.bitarray(self.r)
        self.bitarray.setall(0)

        self.hashfuncs = [hashfunc(self.r, random.randint(0,1000)) for _ in range(self.k)]


    def insert ( self , key ):
        for i in range(self.k):
            bit_idx = self.hashfuncs[i](key) % self.r
            self.bitarray[bit_idx] = 1

    def test ( self , key ):
        for i in range(self.k):
            hash_idx = self.hashfuncs[i](key) % self.r
            if self.bitarray[hash_idx] == 0:
                return False
        return True


#init membership set
random.seed(42)
membership_set = set(random.sample(range(10000,99999), 10000))

#init testset
test_not = set(random.sample(range(1, 9999), 1000))
test_in = set(random.sample(membership_set, 1000))


def run_experiment(fp_rate, membership_set, test_not, test_in):
    """
    Helper method that determines the actual false positive rate of the bloom filter compared to
    the theoretical false positive rate. We can determine this by inserting a set of integers
    into the bloom filter.
    """
    bf = BloomFilter(fp_rate=fp_rate, n=10000)
    for val in membership_set:
        bf.insert(val)

    fp_count = 0
    
    for t in test_not:
        if bf.test(t):
            fp_count += 1
    

    return fp_count/ (len(test_not))

# print(run_experiment(0.01, membership_set, test_not, test_in))
# print(run_experiment(0.001, membership_set, test_not, test_in))
# print(run_experiment(0.0001, membership_set, test_not, test_in))

data = pd.read_csv("aol.txt", sep="\t")
urllist = data.ClickURL.dropna().unique()

test_list = numpy.random.choice(urllist, 1000)

rand_list = []

for i in range(1000):
    rand_list.append(''.join(random.choices(string.ascii_letters, k=random.randint(5, 25))))


result_df = pd.DataFrame()

theoretical = [0.01, 0.001, 0.0001]
real = [run_experiment(t, membership_set, test_not, test_in) for t in theoretical]

result_df['theoretical fp'] = theoretical
result_df['real fp'] = real
result_df.to_csv("./results.txt", sep = '\t', index=False)


