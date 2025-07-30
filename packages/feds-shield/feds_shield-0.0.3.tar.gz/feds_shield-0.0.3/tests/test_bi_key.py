from feds_shield.bi_key import *
import unittest

'''
python3 -m unittest test_bi_key
'''
class Testing(unittest.TestCase):
        
    def test__BiKey__make_key1(self):
        bc = bk_case1()
        bk = BiKey(bc[0],bc[1],bc[2])
        bk.make_key()
        q = [c[0] for c in bc[1]]
        for i,q_ in enumerate(q): 
            assert bk.kd[q_][0] == bc[0][i]
            assert bk.kd[q_][1] == bc[1][i][1]
        return

    def test__BiKey__make_key2(self):
        bc = bk_case2()
        bk = BiKey(bc[0],bc[1],bc[2])
        bk.make_key()
        q = [(x1,x2[1]) for (x1,x2) in zip(bc[0],bc[1])]
        assert bk.kd == q
        return

    def test__BiKey__make_key3(self):
        bc = bk_case3()
        bk = BiKey(bc[0],bc[1],bc[2])
        bk.make_key()
        q = [c[0] for c in bc[1]]
        for i,q_ in enumerate(q): 
            assert bk.kd[q_][0] == bc[0][i]
            assert bk.kd[q_][1] == bc[1][i][1]
        return

    def test__BiKey__make_key4(self):
        bc = bk_case4()
        bk = BiKey(bc[0],bc[1],bc[2])
        bk.make_key()
        assert len(bk.kd) == 8

    """
    demonstrates using bi-key
    """
    def test__BiKey__apply_int__case1(self):
        bc = bk_case1()
        bk = BiKey(bc[0],bc[1],bc[2])
        bk.make_key()
        q = bk.apply_int(20,98)[0]
        assert q in [0,18]

    def test__BiKey__reapply_int__case1(self):
        bk = load_BiKey("bk10","bk11")
        q = bk.apply_int(20,98)[0] 
        assert q == 18

    def test__BiKey__invert_apply_int(self):
        bk = load_BiKey("bk10","bk11")

        f = 39
        t = 61
        t2 = bk.apply_int(f,t)
        tx = bk.invert_apply_int(t,t2[0],t2[1])
        assert(tx == f)

        f= 65
        t = 23
        t2 = bk.apply_int(f,t)
        tx = bk.invert_apply_int(t,t2[0],t2[1])
        assert(tx == f)
            



if __name__ == '__main__':
    unittest.main()
