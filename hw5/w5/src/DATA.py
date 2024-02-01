from COLS import COLS
from ROW import ROW
import pdb
import re, ast, fileinput, random, copy
import Constants

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
        elif type(src) == list:
            for x in src:
                self.add(x, callback)
        else:
            self.add(src, callback)

    def add(self, t, callback=None, row=None):
        if (type(t) == ROW):
            row = t
        else:
            row = ROW(t)

        if self.cols:
            if callback:
                callback(self, row)
            self.rows[1 + len(self.rows)] = self.cols.add(row)
        else:
            self.cols = COLS(row)

    def mid(self, cols=None, u=None):
        u = [col.mid() for _, col in (cols or self.cols.all.items())]
        if (type(u) == list):
            u = self._ltod(u)
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

    def _get_y(self):
        y_list = []
        for at, txt in self.cols.names.items():
            if (txt.endswith("+") or txt.endswith("-")):
                y_list.append(at)

        return y_list

    def _print_4(self, rows, y_ind, budget0=None, i=None):
        if budget0:
            len1 = budget0 + i + 1
        else:
            len1 = len(rows)

        random.shuffle(rows)
        dl = {}
        for i in y_ind:
            dl[i] = 0

        # This is used for calculating the sum of each y column for the len1 rows
        for ind in range(len1):
            for j in y_ind:
                dl[j] += rows[ind].cells[j]

        l = list(dl.values())
        # Calculating the mean of each column with the total count of rows
        nl = [x / len1 for x in l]

        s = ""
        for i in nl:
            s += "{:.2f}".format(i)
            s += "   "

        # print(s)

        return s

    def gate(self):
        firstRow = list(self.rows.values())[0]
        for k, col in self.cols.y.items():
            self.cols.y[k].heaven = col.norm(firstRow.cells[k])
        print(self.cols.y.values())
        rows = list(self.rows.values())
        d=[]
        for i in range(len(rows)):
            d.append(col.norm(rows[i].d2h(self)))
        rows.sort(key=lambda row: row.d2h(self))
        print(rows[30].cells)
        return rows

    def split(self,best,rest,lite,dark):
        selected = DATA([self.cols.names])
        max = 1E30
        out = 0
        for i,row in enumerate(dark):
            b = row.like(best,len(lite),2)
            r = row.like(rest,len(lite),2)
            if b > r :
                selected.add(row)
            temp = abs(b+r) / abs(b-r+1E-300)
            if temp > max:
                out,max = i,temp
        return out,selected, max

    def bestRest(self, rows, want):
        # Sort rows based on distance to heaven
        rows.sort(key=lambda row: row.d2h(self))

        # Initialize best and rest lists with column names
        best, rest = [self.cols.names], [self.cols.names]

        # Split rows into best and rest based on the 'want' parameter
        for i, row in enumerate(rows):
            if i <= want:
                best.append(row)
            else:
                rest.append(row)

        # Create new DATA objects for best and rest rows
        best_data = DATA(best)
        rest_data = DATA(rest)

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
