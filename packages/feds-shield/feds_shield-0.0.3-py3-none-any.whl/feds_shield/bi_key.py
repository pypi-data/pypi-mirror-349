import random
from .file_ops import *

"""
fp1 := str,kd file
fp2 := str, opIndex file
"""
def load_BiKey(fp1,fp2):
    s1 = load_shield_from_file(fp1)
    s2 = load_shield_from_file(fp2)[0]
    
    lostus = s2[-2]
    modulo = s2[-1]
    s2 = s2[:-2]

    bk = BiKey([],[],modulo)
    bk.lostus = lostus
    bk.opIndex = s2
    bk.kd = [(sx,sy) for sx,sy in zip(s1[0],s1[1])]
    return bk

class BiKey:

    '''
    operands := list<operator:int>
    opIndex := list<(index:int,operand:binary)>
    '''
    def __init__(self,operands,opIndex,modulo):
        assert BiKey.check_operands(operands)
        # variable used for constructing a new <BiKey> instance 
        self.operands = operands
        assert BiKey.check_index(opIndex,len(self.operands))
        self.opIndex = opIndex
        self.modulo = modulo
        # key data
        self.kd = None
        # binary, ending operator
        self.lostus = None
        return

    @staticmethod
    def check_operands(o):
        for o_ in o:
            if type(o_) != int: 
                return False
            if o_ < 0 or o_ > 99:
                return False
        return True

    @staticmethod
    def check_index(opIndex,l):
        if l == 0: 
            return len(opIndex) == 0

        oi = [o[0] for o in opIndex]
        return min(oi) >= 0 and max(oi) < 8\
            and len(opIndex) == l

    def make_key(self):
        assert self.kd == None, "key already made!"

        i = 0
        j = 0
        l = len(self.opIndex)
        self.kd = []
        while j < 8 and i < l:
            if self.opIndex[i][0] != j:
                self.kd.append(self.py_prng_pad())                    
            else:
                self.kd.append((self.operands[i],self.opIndex[i][1]))
                i += 1
            j += 1
        
        while j < 8:
            self.kd.append(self.py_prng_pad())
            j += 1
        self.opIndex = [o[0] for o in self.opIndex]
        self.operands = None
        self.lostus = 1 if random.random() >= 0.5 else 0

    '''
    a pad unit using standard Python prng
    '''
    def py_prng_pad(self):
        b = 1 if random.random() >= 0.5 else 0
        x = random.randrange(0,100)
        return (x,b)

    """
    return:
    int, f {...[+|*] m_j...} lostus t; j index of key element 
    """
    def apply_int(self,f,t):
        # operate on fire f
        q = f

        for o in self.opIndex:
            if self.kd[o][1]:
                q = q * self.kd[o][0]
            else:
                q = q + self.kd[o][0]
        
        # operate on t
        if self.lostus:
            q = q * t
        else:
            q = q + t
        return q % self.modulo, int(q / self.modulo)

    """
    return:
    int,f from apply
    """
    def invert_apply_int(self,t1,t2,m):
        q = m * self.modulo + t2

        # lostus
        if self.lostus:
            q = int(q / t1)
        else:
            q = q - t1

        # reversia
        for o in self.opIndex[::-1]:
            if self.kd[o][1]:
                q = int(q / self.kd[o][0])
            else:
                q = q - self.kd[o][1]

        # fire
        return q - 1

    '''
    saves shield to file in the following form:

    fp1 <- kd
    fp2 <- index
    '''
    def save(self,fp1,fp2):
        # save kd
        x1 = [x[0] for x in self.kd]
        x2 = [x[1] for x in self.kd]
        y = [x1,x2]
        save_shield_to_file(y,fp1)

        # save index + lostus
        save_shield_to_file([self.opIndex + [self.lostus] + [self.modulo]],fp2)

### test cases

"""
operands := list<operator:int>
opIndex := list<(index:int,operand:binary)>
"""
def bk_case1():
    operands = [20,30,12]
    opIndex = [(0,1),(4,0),(6,1)]
    return (operands,opIndex,40)

def bk_case2():
    operands = [10,1,1,1,3,20,30,12]
    opIndex = [(0,1),(1,0),(2,1),(3,0),(4,0),(5,1),(6,1),(7,0)]
    return (operands,opIndex,200)

def bk_case3():
    operands = [10,30]
    opIndex = [(0,1),(5,1)]
    return (operands,opIndex,59)

def bk_case4():
    operands = []
    opIndex = []
    return (operands,opIndex,84)