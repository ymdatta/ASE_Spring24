"""
MIT License

Copyright (c) 2024 Mohan Yelugoti 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import re
import pdb

class NUM:
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

    def add(self, x, d=0):
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
        n12             = self.n + other.n
        pooledSd        = pow((((self.n - 1) * (pow(self.div(), 2))) + ((other.n - 1) * (pow(other.div(), 2)))) / (n12 - 2), 0.5)
        """
            correction from Hedges, Larry, and Ingram Olkin. 1985. 
            “Statistical Methods in Meta-Analysis.” Stat Med. Vol. 20.
        """
        correction      = 1 if n12 >= 50 else ((n12 - 3) / (n12 - 2.25))
        print (pooledSd, n12, correction)
        return ((abs(self.mu - other.mu) / pooledSd) * correction) <= self.cohen

    def norm(self, x):
        return x if x == "?" else ((x - self.lo) / (self.hi - self.lo + 1E-30))

    def like(self, x, _, nom=None, denom=None):
        mu              = self.mid()
        sd              = self.div() + 1E-30
        nom             = pow(2.718, ((-0.5) * pow(x - mu, 2) / (pow(sd, 2))))
        denom           = ((sd * 2.5) + 1E-30)
        return    (nom / denom)