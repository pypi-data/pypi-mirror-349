'''
loads user-file alphabet into memory  
'''
import json
from .file_ops import *
    
def save_alphabet(d,f):
    with open(modifini(f),'w') as fi:
        return json.dump(d,fi)

def load_alphabet(f):
    with open(modifini(f),'r') as fi:
        return json.load(fi)


std_symbols = ['\n','@','.','!','?','(',')','[',']','{','}','$','%','\t', ' ']

'''
saves standard alphabet:
a-zA-Z0-9 
.!?()[]{}$%

into file `std_alpha.csv`
'''
def save_std_alphabet():
    d = {}

    # 97-123
    for i in range(97,123):
        d[chr(i)] = i
    # 65-91
    for i in range(65,91):
        d[chr(i)] = i
    # 0-9
    for i in range(48,58):
        d[chr(i)] = i

    # 33,63,96
    for s in std_symbols:
        d[s] = ord(s) 

    save_alphabet(d,'std_alpha')