import pdb

class ROW:
    def __init__(self,t):
        self.cells = {}
        ind = 1
        for i in t:
            self.cells[ind] = i
            ind += 1
    
    # def d2h() ignored as per hw2 instruction

    # def likes() ignored as per hw2 instruction

    # def like() ignored as per hw2 instruction
