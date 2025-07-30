#    def __init__(self,shield,fk,fek):

from feds_shield.structure import *
from feds_shield.bi_key import *
import unittest


'''
python3 -m unittest test_structure
'''
class Testing(unittest.TestCase):

    def test__Structure__register_fire_on_layer(self):
        
        # case 1
        shield = load_shield_from_file('x')
        fk = load_BiKey("bk10","bk11")
        fek = load_BiKey("bk20","bk21")
        s = Structure(zero_shield(shield),fk,fek)
        s.register_fire_on_layer(s.fk,97,0,False)
        assert unpair_shield(s.shield) == [[1, 3, 4], [5, 10, 20], [10, 20], [20, 30]]

        # case 2
        fk2 = load_BiKey("bk30","bk31")
        s = Structure(zero_shield(shield),fk2,fek)
        s.register_fire_on_layer(s.fk,97,0,False)
        assert unpair_shield(s.shield) == [[0, 22, 13], [5, 10, 20], [10, 20], [20, 30]]
        return

if __name__ == '__main__':
    unittest.main()
