import pdb
import Constants
import Utils

class NODE:
    def __init__(self,data):
        self.here = data
        self.lefts = None
        self.left = None
        self.rights = None
        self.right = None
        self.C = None
        self.cut = None

    def walk(self,fun,depth=0):
        self.depth = depth
        fun(self,depth,not (self.lefts or self.rights))
        if self.lefts:
            self.lefts.walk(fun,depth+1)
        if self.rights:
            self.rights.walk(fun,depth+1)

    def show(self,_show=None,maxDepth=0):
        def d2h(data):
            return round(data.mid().d2h(self.here))

        maxDepth = 0

        def _show(node,depth,leafp):
            nonlocal maxDepth
            post = "\t" + self.o(node.here.mid().cells, 2) if leafp else ""
            maxDepth = max(maxDepth,depth)
            print(("|.. " * depth) + post)

        self.walk(_show)
        print("")
        print(("    " * maxDepth) + self.o(self.here.mid().cells, 2))
        print(("    " * maxDepth) + "_" + self.o(self.here.cols.names))

    def o(self, t, n=None, u=None):
        if isinstance(t, (int, float)):
            return str(round(t, n))
        if not isinstance(t, dict) and not isinstance(t, list):
            return str(t)

        u = []
        for k, v in t.items() if isinstance(t, dict) else enumerate(t):
            if str(k)[0] != "_":
                if len(t) > 0:
                    u.append(self.o(v, n))
                else:
                    u.append(f"${self.o(k, n)}: ${self.o(v, n)}")

        return "{" + ", ".join(u) + "}"
    # def o(self, x):
    #     return x.__class__.__name__ +"{"+ (" ".join([f":{k} {v}" for k,v in sorted(x.items())
    #                                                        if k[0]!="_"]))+"}"
