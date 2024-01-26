from COLS import COLS
from ROW import ROW
import pdb
import re, ast, fileinput

class DATA:
    def _ltod(self, a):
        d = {}
        for i in a:
            d[1 + len(d)] = i

        return d

    def  __init__(self, src= [], callback=None):
        self.rows = {}
        self.cols =  None
        if type(src) == str:
            for x in self.csv(src):
                self.add(self._ltod(x), callback)
        else:
            self.add(src, callback)

    def add(self, t, callback=None, row=None):
        row = ROW(t)
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

    def stats(self, cols=None, callback=None, ndivs=None, u=None):
        u = {".N": len(self.rows)}
        for _, col in (cols or self.cols.y).items():
            u[col.txt] = round(type(col).__getattribute__(col, callback or "mid")(), ndivs)
        return u

    def clone(self, rows=None, new=None):
        new = DATA([self.cols.names])
        for row in (rows or []):
            new.add(row)
        return new

    # Usage:
    # best, rest = data.bestRest(rows, want)
    def bestRest(self, rows, want):
        # Sort rows based on distance to heaven
        rows.sort(key=lambda row: row.d2h(self))

        # Initialize best and rest lists with column names
        best, rest = [self.cols.names], [self.cols.names]

        # Split rows into best and rest based on the 'want' parameter
        for i, row in enumerate(rows):
            if i < want:
                best.append(row)
            else:
                rest.append(row)

        # Create new DATA objects for best and rest rows
        best_data = DATA.new(best)
        rest_data = DATA.new(rest)

        return best_data, rest_data

    def coerce(self, x):
        try : return ast.literal_eval(x)
        except Exception: return x.strip()

    # Split data file into multiple rows.
    def csv(self, file="-"):
        with  fileinput.FileInput(None if file=="-" else file) as src:
            for line in src:
                line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
                if line: yield [self.coerce(x) for x in line.split(",")]
