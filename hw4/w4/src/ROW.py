import pdb
import Constants
import math

class ROW:
    def __init__(self,t):
        self.cells = {}
        ind = 1
        for i in t.values():
            self.cells[ind] = i
            ind += 1

        #TODO: low class frequency kludge
        self.k = Constants.the.k

    # Distance to best values (and _lower_ is _better_).
    def d2h(self, data, d=None, n=None):
        d, n = 0, 0
        for k, col in data.cols.y.items():
            n += 1
            d += pow(abs(col.heaven - col.norm(self.cells[k])), 2)

        return pow(d, 0.5) / pow(n, 0.5)

    # Return the 'data' (from 'datas') that I like the best
    def likes(self, datas, n=None, nHypotheses=None, most=None, tmp=None, out=None):
        n, nHypotheses = 0, 0
        for _, data in datas.items():
            n = n + len(data.rows)
            nHypotheses += 1

        for k, data in datas.items():
            tmp = self.like(data, n, nHypotheses)
            if (most == None) or (tmp > most):
                most, out = tmp, k

        return out, most

    # Return the 'data' from ('datas') that I like the best
    def like(self, data, n, nHypotheses, prior=None, out=None, v=None, inc=None):
        prior   =   (len(data.rows) + self.k) / (n + (self.k) * nHypotheses)
        out     =   math.log(prior)

        for _, col in data.cols.x.items():
            v   =   self.cells[col.at]
            if v != "?":
                inc     =   col.like(v, prior)
                if (inc == 0):
                    # TODO: based on how lua handles this code.
                    return 0
                out     =   out + math.log(inc)
        return pow(math.exp(1), out)
