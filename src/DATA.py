from COLS import COLS
from ROW import ROW
import pdb
import re, ast, fileinput

class DATA:
    def coerce(self, x):
        try : return ast.literal_eval(x)
        except Exception: return x.strip()

    # Split data file into multiple rows.
    def csv(self, file="-"):
        with  fileinput.FileInput(None if file=="-" else file) as src:
            for line in src:
                line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
                if line: yield [self.coerce(x) for x in line.split(",")]

    def  __init__(self, src= [], callback=None):
        self.rows = {}
        self.cols =  None
        for x in self.csv(src):
            self.add(x, callback)

    def add(self, t, callback, row=None):
        row = t.get("cells", t) if isinstance(t, dict) else ROW(t)
        if self.cols:
            if callback:
                callback(self, row)
            self.rows[1 + len(self.rows)] = self.cols.add(row)
        else:
            self.cols = COLS(row)

    def mid(self, cols=None, u=None):
        u = [col.mid() for col in (cols or self.cols.all)]
        return ROW(u)

    def div(self, cols=None, u=None):
        u = [col.div() for col in (cols or self.cols.all)]
        return ROW(u)

    def small(self, u=None):
        u = [col.small() for col in (self.cols.all)]
        return ROW(u)

    def stats(self, cols, callback, ndivs, u):
        ## skipping as per comments in hw2.md
        pass
        # u = {".N": len(self.rows)}
        # for col in getattr(self.cols, cols or "y"):
        #     u[col.txt] =

    def clone(self, rows=None, new=None):
        new = DATA([self.cols.names])
        for row in (rows or []):
            new.add(row)
        return new
