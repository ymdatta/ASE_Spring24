import NUM
import re
import SYM
class COLS:
    def __init__(self, row):
        self.x = {}
        self.y = {}
        self.all = {}
        self.names = row.cells
        for at, txt in row.cells.items():
            col = NUM(txt, at) if re.search("^[A-Z]", txt) else SYM(txt, at)
            all[len(all) + 1] = col
            if not txt.endswith("X"):
                if txt.endswsith("!"):
                    self.klass = col
                if any([txt.endswith("!"),txt.endswith("+"),txt.endswith("-")]):
                    self.y[at] = col
                else:
                    self.x[at] = col
    
    def add(self,row):
        d = {}
        d[1] = self.x
        d[2] = self.y
        for x,cols in d.items():
            for y,col in cols.items():
                col.add(row.cells[col.at])
        return row