from COLS import COLS
from ROW import ROW
from NODE import NODE
import pdb
import re, ast, fileinput, random, copy
import Constants
import Utils

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
        u = {}
        for _, col in (cols or self.cols.x).items():
            u[col.txt] = round(type(col).__getattribute__(col, callback or "mid")(), ndivs)
        for _, col in (cols or self.cols.y).items():
            u[col.txt] = round(type(col).__getattribute__(col, callback or "mid")(), ndivs)
        return list(u.values())

    def stats_divs(self, cols=None, callback=None, ndivs=None, u=None):
        u = {}
        for _, col in (cols or self.cols.x).items():
            u[col.txt] = round(type(col).__getattribute__(col, callback or "div")(), ndivs)
        for _, col in (cols or self.cols.y).items():
            u[col.txt] = round(type(col).__getattribute__(col, callback or "div")(), ndivs)
        return list(u.values())

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

    def _get_x(self):
        x_list = []
        for at, txt in self.cols.names.items():
            if (not txt.endswith("+") or not txt.endswith("-")):
                x_list.append(at)

        return x_list

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

    def gate_smo(self,budget0,budget,some):
        stats = {}
        bests = {}
        rows = list(self.rows.values())
        random_seeds = random.sample(range(100),20)
        for i in range(20):
            Constants.the.seed = random_seeds[i]
            random.shuffle(rows)

            lite = rows[0: budget0]
            dark = rows[budget0:]
            result6 = []
            x_ind = self._get_x()
            for i in range(budget):
                best, rest = self.bestRest(lite, len(lite) ** some)
                todo, selected, max = self.split(best, rest, lite, dark)

                stats[i] = selected.mid()
                bests[i] = best.rows[1]
                lite[todo] = dark.pop(todo)

                s_temp = ""
                for j in x_ind:
                    s_temp += str(list(best.rows.values())[0].cells[j])
                    s_temp += "\t"

                result6.append(s_temp)

            print(f"\n smo{budget+budget0}:\t".join(result6))

        return stats,bests

    def evaluate_all(self):
        rows = list(self.rows.values())
        x_ind = self._get_x()
        rows_temp = copy.deepcopy(rows)
        rows_temp.sort(key=lambda row: row.d2h(self))
        s_temp = ""
        for j in x_ind:
            s_temp += str(rows_temp[0].cells[j])
            s_temp += "\t"
        print("100%:\t",s_temp)

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

    def many(t, n=None):
        if n is None:
            n = len(t)
        return [random.choice(t) for _ in range(n)]

    def coerce(self, x):
        try : return ast.literal_eval(x)
        except Exception: return x.strip()

    # Split data file into multiple rows.
    def csv(self, file="-"):
        with  fileinput.FileInput(None if file=="-" else file) as src:
            for line in src:
                line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
                if line: yield [self.coerce(x) for x in line.split(",")]

    def farapart(self,rows,sortp=None,a=None,b=None,far=None,evals=None):
        far = len(rows) * Constants.the.far
        evals = 1 if a else 2
        a = a if a else random.choice(rows).neighbors(self,rows)[far]
        b = a.neighbors(self,rows)[far]
        if sortp and b.d2h(self) < a.d2h(self):
            a,b = b,a
        return a,b,a.dist(b,self),evals

    def half(self,rows=None,sortp=None,before=None,evals=None):
        some = self.many(rows, min(Constants.the.half,len(rows)))
        a,b,C,evals = self.farapart(some, sortp, before)
        def d(row1,row2):
            return row1.dist(row2,self)
        def project(r):
            return ((d(r,a)**2 + C**2 - d(r,b)**2) / (2*C))
        a_s,b_s = {},{}
        for n,row in enumerate(Utils.keysort(rows,project)):
            if n <= len(rows) // 2:
                a_s[n] = row
            else:
                b_s[n] = row
        return a_s, b_s, a, b, C, d(a, b_s[1]), evals

    def tree(self, sortp=None, _tree=None, evals=None, evals1=None):
        evals = 0
        def _tree(data, above, lefts, rights, node):
            node = NODE(data)
            if len(data.rows) > 2*(len(self.rows)**0.5):
                lefts, rights, node.left, node.right, node.C, node.cut, evals1 = self.half(data.rows, sortp, above)
                evals = evals + evals1
                node.lefts  = _tree(self.clone(lefts),  node.left)
                node.rights = _tree(self.clone(rights), node.right)
            return node
        return _tree(self),evals

    def branch(self,stop=None,rest=None,_branch=None,evals=None):
        evals, rest = 1, {}
        if stop is None:
            stop = 2*(len(self.rows)**0.5)
        def _branch(data, above, left, lefts, rights):
            if len(data.rows) > stop:
                lefts, rights, left = self.half(data.rows, True, above)
                evals = evals+1
                for _,row1 in rights.items():
                    rest[1+len(rest)] = row1
                return _branch(data.clone(lefts), left)
            else:
                return self.clone(data.rows),self.clone(rest),evals
        return _branch(self)
