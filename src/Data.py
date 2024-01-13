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
