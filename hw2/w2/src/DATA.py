from COLS import COLS
from ROW import ROW
import pdb
import re, ast, fileinput
import random

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

    def coerce(self, x):
        try : return ast.literal_eval(x)
        except Exception: return x.strip()

    # Split data file into multiple rows.
    def csv(self, file="-"):
        with  fileinput.FileInput(None if file=="-" else file) as src:
            for line in src:
                line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
                if line: yield [self.coerce(x) for x in line.split(",")]
'''
    def gate(self,budget0,budget,some):
        stats = {}
        bests = {}
        rows = random.shuffle(self.rows)
        lite = rows[0:budget0 + 1]
        dark = rows[budget0 + 1:]
        for i in range(0,budget):
            best, rest = bestRest(lite, len(list) ** some)
            todo, selected = split(best, rest, lite, dark)
            stats[i] = selected.mid()
            bests[i] = best.rows[1]
            lite[todo] = dark.pop(todo)
        return stats,bests

    def split(self,best,rest,lite,dark):
        selected = DATA(self.cols.names)
        max = 1E30
        out = 0
        for i,row in dark.items():
            b = row.like(best,len(lite),2)
            r = row.like(rest,len(lite),2)
            if b > r :
                selected.add(row)
            temp = abs(b+r) / abs(b-r+1E-300)
            if temp > max:
                out,max = i,temp
        return out,selected
'''

