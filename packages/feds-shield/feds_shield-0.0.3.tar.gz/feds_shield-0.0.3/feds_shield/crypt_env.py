from .structure import *
from .bi_key import * 
from .file_ops import *
from .firing_agent import *
from copy import deepcopy
import csv

"""
a basic encryption environment class
"""
class CryptEnv1: 

    def __init__(self,alphabetFile,shieldFile,bk1File,bk2File,msg,writeFile):
        self.fa = FiringAgent(msg,alphabetFile)
        shield = zero_shield(load_shield_from_file(shieldFile))

        bk1 = load_BiKey(bk1File[0],bk1File[1])
        bk2 = load_BiKey(bk2File[0],bk2File[1])
        self.structure = Structure(shield,bk1,bk2)

        self.initialized = False
        self.wf = "data/" + writeFile
        self.wfo = open(self.wf,"w")
        self.cw = csv.writer(self.wfo,delimiter=",")
        ##self.q = []

    """
    return:
    """
    def encode_one(self):
        x = self.fa.fire()
        print("encoding ",x)

        if type(x) == type(None):
            self.wfo.close()
            return False
        self.structure.absorb_fire(x)
        self.write_to_file()
        self.wfo.write(",")
        return True
        
    def write_to_file(self):
        #shield = unpair_shield(deepcopy(self.structure.shield))
        s2 = []
        for s in self.structure.shield:
            sx = []
            for s_ in s: sx.extend(s_)
            s2.extend([str(s_) for s_ in sx])
        s2 = ",".join(s2)
        self.wfo.write(s2)
        #
        ##self.q.append(s2)
        self.wfo.write(",")
        self.paddy_pat()
        return

    """
    what is a friend or enemy without recognition?
    and however can these terms can figured without
    a center (Centerion)?
    """
    def paddy_pat(self):
        l = len(self.structure.c.feForm)
        sef = [str(s) for s in self.structure.c.feForm]
        sef.append(str(l))
        self.wfo.write(",".join(sef))

def test__CryptEnv1__encode_one():

    a = "std_alpha"
    s = "nu_shield1"
    bk1 = ("bk10","bk11")
    bk2 = ("bk20","bk21")
    msg = "WHERE is HERE"
    writeFile = "data/wf1.txt"
    ce = CryptEnv1(a,s,bk1,bk2,msg,writeFile)

    while ce.encode_one():
        continue

    # test 
    return ce