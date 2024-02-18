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

import math
import Constants

class SYM:
    def __init__(self, s="", n=0):
        self.txt        = s
        self.at         = n
        self.n          = 0
        self.has        = {}
        self.mode       = None
        self.most       = 0

        ## TODO: Need for integration to get
        ## low attribute frequency kludge from CLI
        self.m          = Constants.the.m


    def add(self, x):
        if x != "?":
            self.n += 1
            self.has[x] = 1 + self.has.get(x, 0)
            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x

    def mid(self):
        return self.mode

    def div(self, e):
        e = 0
        for _, v in self.has.items():
            # *, / -> right to left
            e = e - v / self.n * math.log((v / self.n), 2)
        return e

    def small(self, _):
        return 0

    def like(self, x, prior):
        return ((self.has.get(x, 0) + (self.m * prior)) / (self.n +  self.m))


    def dist(self, x, y):
        if x == '?' and y =='?':
            return 1
        elif x == y:
            return 0
        else:
            return 1
