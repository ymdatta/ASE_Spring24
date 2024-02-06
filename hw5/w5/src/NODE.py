import pdb
import Constants
import Utils

class NODE:
    def __init__(self,data):
        self.here = data

    def walk(self,fun,depth=0):
        self.depth = depth
        fun(self,depth,not (self.lefts or self.rights))
        if self.lefts:
            self.lefts.walk(fun,depth+1)
        if self.rights:
            self.rights.walk(fun,depth+1)

    def show(self,_show,maxDepth):
        def d2h(data):
            return rnd(data.mid().d2h(self.here))

        maxDepth = 0

        def _show(node,depth,leafp,post):
            post = d2h(node.here) + "\t" + self.o(node.here.mid().cells) if leafp else ""
            maxDepth = max(maxDepth,depth)
            print(("|.. " * depth) + post)

        self.walk(_show)
        print("")
        print(("    " * maxDepth) + d2h(self.here) + self.o(self.here.mid().cells))
        print(("    " * maxDepth) + "_" + self.o(self.here.cols.names))

    def o(x):
        return x.__class__.__name__ +"{"+ (" ".join([f":{k} {v}" for k,v in sorted(x.items())
                                                           if k[0]!="_"]))+"}"