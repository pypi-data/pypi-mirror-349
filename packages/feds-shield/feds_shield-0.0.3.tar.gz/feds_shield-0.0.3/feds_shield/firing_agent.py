from .alphabet_load import * 

class FiringAgent: 

    """
    message := str,
    f := str, filename
    """
    def __init__(self,message,f):
        self.message = message
        self.f = f
        self.alphabet = load_alphabet(f)
        return

    def fire(self):
        if len(self.message) == 0: 
            return None 
        c = self.message[0]
        self.message = self.message[1:]
        return self.alphabet[c]