import Constants
from RULE import RULE
class RULES:
    def __init__(self, ranges, goal, rowss):
        #for k, v in rowss.items():
            #print(k, len(v))

        self.goal = goal
        self.rowss = rowss
        self.LIKE = 0
        self.HATE = 0
        self.likeHate()

        self.sorted = self.top(self.tryy(self.top(ranges)))

    def powerset(self, s):
        t = [[]]
        for i in range(len(s)):
            for j in range(len(t)):
                t.append([s[i]] + t[j])
        return t

    def likeHate(self):
        for y, rows in self.rowss.items():
            if y == self.goal:
                self.LIKE += len(rows)
            else:
                self.HATE += len(rows)

    def score(self, t):
        like, hate, tiny = 0, 0, 1E-30
        for klass, n in t.items():
            if klass == self.goal:
                like += n
            else:
                hate += n
        like, hate = like/(self.LIKE + tiny), hate/(self.HATE + tiny)
        if hate > like:
            return 0
        else:
            return (like**Constants.the.Support)/(like + hate)

    def tryy(self, ranges):
        u = []
        for subset in self.powerset(ranges):
            if len(subset) > 0:
                rule = RULE(subset)
                preds = rule.selectss(self.rowss)
                if preds['LIKE']==0 and preds['HATE']==0:
                    rule.scored = 0
                else:
                    rule.scored = self.score(preds)

                if rule.scored > 0.01:
                    u.append(rule)
        return u

    def top(self, t):
        t.sort(key=lambda x: x.scored, reverse=True)
        u = []
        for x in t:
            if x.scored >= t[0].scored * 0.1:
                u.append(x)
        return u[:Constants.the.Beam]