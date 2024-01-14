import re

class Num:
    def __init__(self, s="", n=0):
        self.txt        = s
        self.at         = n
        self.n          = 0
        self.mu         = 0
        self.m2         = 0
        self.hi         = -1E+30
        self.lo         =  1E+30
        self.heaven     = 0 if re.search(r"-$", s) else 1

        ## TODO: Need for integration to get cohen from CLI
        self.cohen      = 0.35

    def add(self, x, d):
        if x != "?":
            self.n      += 1
            d           = x - self.mu
            self.mu     += (d / self.n)
            self.m2     += (d * (x - self.mu))
            self.lo     =   min(x, self.lo)
            self.hi     =   max(x, self.hi)

    def mid(self):
        return self.mu
    
    def div(self):
        return 0 if (self.n < 2) else (pow((self.m2) / (self.n - 1), 0.5))

    def small(self):
        return self.cohen * self.div()

    def same(self, other):
        """ 
            from Cohen, J. 1998. Statistical Power Analysis for the Behavioral Sciences. 2nd ed. 
            Hillsdale, NJ: Lawrence Erlbaum Associates.
        """ 
        pooledSd        = pow((pow(self.div(), 2) + pow(other.div(), 2)) / 2, 0.5)
        n12             = self.n + other.n
        """
            correction from Hedges, Larry, and Ingram Olkin. 1985. 
            “Statistical Methods in Meta-Analysis.” Stat Med. Vol. 20.
        """
        correction      = 1 if n12 >= 50 else ((n12 - 3) / (n12 - 2.25))
        print (pooledSd, n12, correction)
        return ((abs(self.mu - other.mu) / pooledSd) * correction) <= self.cohen

    def norm(self, x):
        return x if x == "?" else ((x - self.lo) / (self.hi - self.lo + 1E-30))

    def like(self, x, _, nom, denom):
        mu              = self.mid()
        sd              = self.div() + 1E-30
        nom             = pow(2.718, ((-0.5) * pow(x - mu, 2) / (pow(sd, 2))))
        denom           = ((sd * 2.5) + 1E-30)
        return    (nom / denom)


