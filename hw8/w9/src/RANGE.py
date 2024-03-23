import math
import Constants

class RANGE:
    def __init__(self, at, txt, lo, hi=None):
        self.at = at
        self.txt = txt
        self.scored = 0
        self.x = {'lo': lo, 'hi': hi or lo}
        self.y = {}
    def __str__(self):
        return "{{at: {}, scored: {}, txt: '{}', x: {{hi: {}, lo: {}}}, y: {{{}}}}}".format(
            self.at, self.scored, self.txt, self.x['hi'], self.x['lo'],
            ', '.join('{}: {}'.format(k, v) for k, v in self.y.items()))

    def add(self, x, y):
        self.x['lo'] = min(self.x['lo'], x)
        self.x['hi'] = max(self.x['hi'], x)
        self.y[y] = self.y.get(y, 0) + 1

    def show(self):
        lo, hi, s = self.x['lo'], self.x['hi'], self.txt
        if lo == -math.inf:
            return "{} < {}".format(s, hi)
        elif hi == math.inf:
            return "{} >= {}".format(s, lo)
        elif lo == hi:
            return "{} == {}".format(s, lo)
        else:
            return "{} <= {} < {}".format(lo, s, hi)

    def score(self, goal, LIKE, HATE):
        return self._score(self.y, goal, LIKE, HATE)

    def merge(self, other):
        both = RANGE(self.at, self.txt, self.x['lo'])
        both.x['lo'] = min(self.x['lo'], other.x['lo'])
        both.x['hi'] = max(self.x['hi'], other.x['hi'])
        for t in [self.y, other.y]:
            for k, v in t.items():
                both.y[k] = both.y.get(k, 0) + v
        return both

    def merged(self, other, tooFew):
        both = self.merge(other)
        e1, n1 = self.entropy(self.y)
        e2, n2 = self.entropy(other.y)
        if n1 <= tooFew or n2 <= tooFew:
            return both
        if self.entropy(both.y)[0] <= (n1 * e1 + n2 * e2) / (n1 + n2):
            return both

    @staticmethod
    def entropy(t):
        n = sum(t.values())
        e = sum([-v / n * math.log(v / n, 2) for v in t.values()])
        return e, n

    @staticmethod
    def _score(t, goal, LIKE, HATE):
        like = sum([n for klass, n in t.items() if klass == goal])
        hate = sum([n for klass, n in t.items() if klass != goal])
        tiny = 1E-30
        like /= (LIKE + tiny)
        hate /= (HATE + tiny)
        return like ** Constants.the.Support / (like + hate) if hate <= like else 0
