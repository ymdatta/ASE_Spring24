from COLS import COLS
from ROW import ROW
import pdb
import re, ast, fileinput, random, copy

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
        count = 0
        for i in y_ind:
            dl[i] = 0

        for ind in range(0, len1):
            count += 1
            for j in y_ind:
                dl[j] += rows[ind].cells[j]

        l = list(dl.values())
        nl = [x / count for x in l]

        s = ""
        for i in nl:
            s += str(i)
            s += "   "

        print(s)

        return nl

    def gate(self,budget0,budget,some):
        stats = {}
        bests = {}
        rows = list(self.rows.values())
        random.shuffle(rows)

        print("1. y values of first 6 examples in ROWS")
        y_ind = self._get_y()

        for i in range(0, 7):
            s = ""
            for j in y_ind:
                s += str(rows[i].cells[j])
                s += "   "

            print(s)

        print("2. y values of first 50 examples in ROWS")
        for i in range(0, 51):
            s = ""
            for j in y_ind:
                s += str(rows[i].cells[j])
                s += "   "

            print(s)

        print("3. sort rows based on distance to heaven")
        rows_temp = copy.deepcopy(rows)
        rows_temp.sort(key=lambda row: row.d2h(self))
        rows_temp.reverse()

        s_temp = ""
        for j in y_ind:
            s_temp += str(rows[0].cells[j])
            s_temp += "   "

        print(s_temp)
        print()

        lite = rows[0: budget0 + 1]
        dark = rows[budget0 + 1:]
        for i in range(0,budget):
            best, rest = self.bestRest(lite, len(lite) ** some)
            todo, selected = self.split(best, rest, lite, dark)

            print("4. rand: y values of centroid of (from DARK, select BUDGET0+i rows at random)")
            self._print_4(dark, y_ind, budget0, i)

            print("5. mid, y values of centroid of SELECTED")
            self._print_4(list(selected.rows.values()), y_ind)

            print("6. y values of first row in BEST")
            s_temp = ""
            for j in y_ind:
                s_temp += str(list(best.rows.values())[0].cells[j])
                s_temp += "   "

            print(s_temp)

            stats[i] = selected.mid()
            bests[i] = best.rows[1]
            lite[todo] = dark.pop(todo)
        return stats,bests

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
        return out,selected

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
