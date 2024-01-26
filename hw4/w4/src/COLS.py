import re
from SYM import SYM
from NUM import NUM
import pdb
class COLS:
    def __init__(self, row):
        self.x = {}
        self.y = {}
        self.all = {}
        self.names = row.cells
        for at, txt in row.cells.items():
            col = NUM(txt, at) if re.search("^[A-Z]", txt) else SYM(txt, at)
            self.all[len(self.all) + 1] = col
            if not txt.endswith("X"):
                if txt.endswith("!"):
                    self.klass = col
                if any([txt.endswith("!"),txt.endswith("+"),txt.endswith("-")]):
                    self.y[at] = col
                else:
                    self.x[at] = col
    
    def add(self,row):
        d = {}
        d[1] = self.x
        d[2] = self.y
        for _,cols in d.items():
            for _,col in cols.items():
                col.add(row.cells[col.at])
        return row
