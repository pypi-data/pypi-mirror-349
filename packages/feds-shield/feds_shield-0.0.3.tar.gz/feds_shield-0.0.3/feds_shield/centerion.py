"""
friends are odd,enemies are even
"""
def shield_idn_enemy(shield):
    s2 = []
    for (i,s) in enumerate(shield):
        for (j,s_) in enumerate(s):
            if not s_ % 2:
                s2.append(s_ + i)
    return s2 

class Centerion: 

    """
    feForm := list<enemy cell idn + its index>
    """
    def __init__(self):
        # friend/enemy formation
        self.feForm = None
        return

    def load_fe(self,shield):
        self.feForm = shield_idn_enemy(shield)

