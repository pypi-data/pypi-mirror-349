from .bi_key import *
from .alphabet_load import * 
from .structure import * 
from copy import deepcopy

#WARNING: alphabet assumed to be 1-to-1
"""
"""
def invert_alphabet(a):
    a2 = {}
    for k,v in a.items():
        a2[v] = k
    return a2 

"""
a basic decryption environment class
decrypts character by character
"""
class DecryptEnv1:

    def __init__(self,shieldFile,msgFile,biKeyFile,alphabetFile): 
        self.shieldFile = shieldFile
        self.shieldObj = load_shield_from_file(self.shieldFile)
        self.shieldLen = sum([len(x) for x in self.shieldObj]) * 2
        self.shieldHole = int(len(self.shieldObj[0]) / 2) 
        self.msgFile = msgFile        

        # open message file in reverse
        with open("data/" + self.msgFile,"r") as mf: 
            msg = mf.readlines()
            msg = msg[0][:-1]
            msg = msg.split(",")
            self.msg = [int(x) for x in msg][::-1]

        self.bk = load_BiKey(biKeyFile[0],biKeyFile[1])
        self.alphabet = invert_alphabet(load_alphabet(alphabetFile))
        self.deco = ""
        self.decoh = [] 

        # each is char encoding
        # s2 s1
        self.s1,self.s2 = None,None
        self.is_active = True

    def decode(self):
        while self.decode_one():continue

    """
    """
    def decode_one(self):

        if not self.is_active:
            print("[!!] BROKEN ENCRYPTION")
            return False 
        
        if len(self.msg) == 0:
            # case: use initial shield
            self.s1 = deepcopy(self.s2)
            self.s2 = zero_shield(self.shieldObj)
            s2 = []
            for q in self.s2: s2.extend(q)
            self.s2 = s2

            qi = self.decode_pair()
            self.register_decode_pair(qi)
            if not self.is_active:
                print("[!!] BROKEN ENCRYPTION")
                return False
            self.deco += self.alphabet[qi]

            ##3 ?? 
            self.deco = self.deco[::-1]
            return False

        l = self.msg.pop(0)
        self.pop_pad(l)
        x = self.shieldLen
        
        # fetch the msg
        q = []
        for i in range(0,self.shieldLen,2):
            q.append((self.msg[1],self.msg[0]))
            self.msg.pop(0)
            self.msg.pop(0)
        q = q[::-1]

        # case: initial, re-loop to collect parent
        if type(self.s2) == type(None):
            self.s2 = q
            return self.decode_one()

        # decode
        self.s1 = deepcopy(self.s2)
        self.s2 = q
        qi = self.decode_pair()
        self.register_decode_pair(qi)
        if not self.is_active:
            print("[!!] BROKEN ENCRYPTION")
            return False
        self.deco += self.alphabet[qi]
        self.decoh.append(self.s1)
        return True 

    def decode_pair(self):
        # decode pair
        i = self.shieldHole
        try:
            return self.bk.invert_apply_int(self.s2[i][0],self.s1[i][0],self.s1[i][1])
        except:
            return False

    def register_decode_pair(self,dp): 
        if type(dp) == bool:
            self.is_active = False
        if dp not in self.alphabet:
            self.is_active = False 
        return

    def pop_pad(self,x):
        while x > 0:
            self.msg = self.msg[1:]
            x -= 1
