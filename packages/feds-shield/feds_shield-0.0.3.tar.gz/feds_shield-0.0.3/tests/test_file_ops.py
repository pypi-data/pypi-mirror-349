from feds_shield.file_ops import *
import unittest

'''
python3 -m unittest test_file_ops
'''
class Testing(unittest.TestCase):
        
    def test__save_shield_to_file(self):
        s = [[1,3,4],[5,10,20],[10,20],[20,30]]
        f = "x"
        save_shield_to_file(s,f)

    def test__load_shield_from_file(self):
        f = "x"
        q = load_shield_from_file(f)
        assert q == [[1,3,4],[5,10,20],[10,20],[20,30]]

if __name__ == '__main__':
    unittest.main()
