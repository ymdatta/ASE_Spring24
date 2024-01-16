import Cols
import Row

class Data:
    def  __init__(self, src= [], callback=None):
        rows = {}
        cols =  None
        for x in src:
            self.add(x, callback)

    def add(self, t, callback, row=None):
        row = t.get("cells", t) if isinstance(t, dict) else Row(t)
        if self.cols:
            if callback:
                callback(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = Cols(row)

    def mid(self, cols=None, u=None):
        u = [col.mid() for col in (cols or self.cols.all)]
        return Row(u)

    def div(self, cols=None, u=None):
        u = [col.div() for col in (cols or self.cols.all)]
        return Row(u)

    def small(self, u=None):
        u = [col.small() for col in (self.cols.all)]
        return Row(u)

    def stats(self, cols, callback, ndivs, u):
        ## skipping as per comments in hw2.md
        pass
        # u = {".N": len(self.rows)}
        # for col in getattr(self.cols, cols or "y"):
        #     u[col.txt] =

    def clone(self, rows=None, new=None):
        new = Data([self.cols.names])
        for row in (rows or []):
            new.add(row)
        return new
