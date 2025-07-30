'''
performs a statistical test to determine
the degree of bijectivity of the bi_key
given the alphabet. 

provided are basic tests and are non-conclusive
for determining whether a key satisfies cryptographic
standards.
'''
from .bi_key import *

######################################################

'''
constructs a mapping a -> bk.apply_int(i,a); a in intAlphabet
'''
def bijective_dictionary__BiKey_on_int(bk,i,intAlphabet):
    
    d = {}

    for j in intAlphabet:
        j2 = bk.apply_int(i,j)[0]
        d[j] = j2
    return d

'''
NOTE: does not take into account the confines of SPACE(bk.apply_int(*))
      w.r.t. intAlphabet.
'''
def bijective_measure_on_dictionary(d):
    return len(set(d.values())) / len(d)
    
'''
calculates the mean bijective measure of BiKey
on the range of alphabetic characters

bk := key
intAlphabet := list(int)
'''
def bijective_measure_test__BiKey(bk,intAlphabet):
    m = 0.0
    for a in intAlphabet:
        m += bijective_measure_on_dictionary(bijective_dictionary__BiKey_on_int(bk,a,intAlphabet))
    return m / len(intAlphabet)


#############################################################

def identity_measure_on_dictionary(d):
    if len(d) == 0: return 0.
    c = 0
    for (k,v) in d.items():
        if k == v:
            c += 1
    return c / len(d)

'''
calculates the mean identity measure of BiKey
on the range of alphabetic characters

bk := key
intAlphabet := list(int)
'''
def identity_measure_test__BiKey(bk,intAlphabet):
    m = 0.0
    for a in intAlphabet:
        m += identity_measure_on_dictionary(bijective_dictionary__BiKey_on_int(bk,a,intAlphabet))
    return m / len(intAlphabet)

#############################################################

# TODO: def random_shield_values(layerSizes)

# test bk_case1
DEFAULT_TEST_ALPHABET = list(range(0,100))

def bijective_measure_test__case1(f1,f2,intAlphabet = DEFAULT_TEST_ALPHABET):
    intAlphabet = list(range(0,100))
    bk = load_BiKey(f1,f2)
    bk.modulo = 100
    return bijective_measure_test__BiKey(bk,intAlphabet)

def identity_measure_test__case1(f1,f2,intAlphabet = DEFAULT_TEST_ALPHABET):
    intAlphabet = list(range(0,100))
    bk = load_BiKey(f1,f2)
    bk.modulo = 100
    return identity_measure_test__BiKey(bk,intAlphabet)

"""
bijective_measure_test__case1("bk10","bk11")
identity_measure_test__case1("bk10","bk11")
"""
