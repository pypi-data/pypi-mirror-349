from .centerion import *
from .alphabet_load import *
from .file_ops import *
from copy import deepcopy
from .bi_key import *

def zero_shield(shield):
    for (i,s) in enumerate(shield):
        for (j,s_) in enumerate(s):
            shield[i][j] = [shield[i][j],0]
    return shield

def unpair_shield(shield):
    shield_ = shield
    for (i,s) in enumerate(shield_):
        for (j,s_) in enumerate(s):
            shield_[i][j] = shield_[i][j][0]
    return shield_

class Structure:

    '''
    fk := BiKey, fire key 
    fek := BiKey,friend/enemy key
    '''
    def __init__(self,shield,fk,fek):
        self.shield = shield
        self.fk = fk
        self.fek = fek
        self.c = Centerion()

    def absorb_fire(self,f,verbose=False):

        # register fire
        self.register_fire(deepcopy(f),self.fk,verbose)

        # update f/e formation
        q = deepcopy(self.shield)
        self.register_fire(f,self.fek,False)
        self.c.load_fe(unpair_shield(self.shield))
        self.shield = q
        return

    '''
    registers fire by the pattern:

    ----------------------------------------------
                        ... ... ...
                        L05|L15|L25|...
                        L03|L13|L23|...
                        L01|L11|L21|...
    |F=I=R=E>           L00|L10|L20|... CENTERION
                        L02|L12|L22|...
                        L04|L14|L24|...
                        L06|L16|L26|...
                        ... ... ...

    ----------------------------------------------
    
    elaboration: 
    - LXY := cell unit of shield, X is layer index w.r.t. to fire and 
             Y is the order (least->greatest) of impact of fire on layer X.
             
             Ex. L01 gets hit before L02 before L03.

             Every layer can have an arbitrary number of cells comprising it.
             For even-sized layers, both points of the median are hit by fire first.
             For odd-sized layers, the median is hit by fire first.

             For layers q and q + 1, every cell of layer q
             is hit by the fire before the cells of layer q + 1.

             For fire value F, The impact is felt by the cells by
             <F,F-1,F-2,F - |SHIELD|>; |SHIELD| := number of cells comprising the shield 
    '''
    def register_fire(self,f,bk,verbose = True):
        l = len(self.shield)
        for i in range(l):
            f = self.register_fire_on_layer(bk,f,i,verbose)
        return

    def register_fire_on_layer(self,bk,f,i,verbose=True):
        ls = len(self.shield[i])
        if ls == 0: return

        # calculate center
        q = None
        q2 = int(ls / 2)
        e = 0
        oddSwitch = 0
        if ls % 2:
            q = [q2,q2 + 1]
        else:
            q = [q2 - 1,q2]
            e = 1

        if verbose:
            print("taking fire {} at layer {}".format(f,i))
        
        while q[0] >= 0 or q[1] < ls:

            # case: even, register both
            if e:
                # one
                x1 = bk.apply_int(f,self.shield[i][q[0]][0])

                # two
                x2 = bk.apply_int(f,self.shield[i][q[1]][0])

                if verbose:
                    print("fire {} on cell {}: {}->{},{} ->{}".format(\
                        f,q,self.shield[i][q[0]],x1,self.shield[i][q[1]],x2))

                self.shield[i][q[0]] = x1
                self.shield[i][q[1]] = x2
                q[0] -= 1
                q[1] += 1

            # case: odd, register one
            else:
                x = bk.apply_int(f,self.shield[i][q[oddSwitch]][0])
                s_ = self.shield[i][q[oddSwitch]]
                self.shield[i][q[oddSwitch]] = x

                if verbose:
                    print("fire {} on cell {}: {}->{}".format(f,q[oddSwitch],s_,x))

                if oddSwitch:
                    q[oddSwitch] += 1
                else:
                    q[oddSwitch] -= 1
                oddSwitch = (oddSwitch + 1) % 2
            f -= 1
        return f

def collect_structure_shield_history(s,msg):
    shields = []
    for m in msg:
        shields.append(deepcopy(s.shield))
        s.absorb_fire(ord(m))
    shields.append(deepcopy(s.shield))
    return shields
