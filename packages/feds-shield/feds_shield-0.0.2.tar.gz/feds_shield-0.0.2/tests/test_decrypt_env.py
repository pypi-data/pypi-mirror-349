from feds_shield.decrypt_env import *

import unittest

'''
python3 -m unittest test_decrypt_env
'''
class Testing(unittest.TestCase):

    def test__DecryptEnv1__decode(self):
        s = "nu_shield1"
        m = "wf1.txt"
        b = ("bk10","bk11")
        a = "std_alpha"
        de = DecryptEnv1(s,m,b,a)
        de.decode()
        assert de.deco == "WHERE is HERE"

if __name__ == '__main__':
    unittest.main()
