"""
mylo: to understand "it",  cut "it" up, then seek patterns in the pieces. E.g. here
we use cuts for multi- objective, semi- supervised, rule-based explanation.
(c) Tim Menzies <timm@ieee.org>, BSD-2 license

OPTIONS:
  -b --bins   initial number of bins      = 16
  -B --Bootstraps number of bootstraps    = 512
  -c --cohen  parametric small delta      = .35
  -C --Cliffs  non-parametric small delta = 0.2385
  -f --file   where to read data          = "../data/auto93.csv"
  -F --Far    distance to  distant rows   = .925
  -g --go     start up action             = "help"
  -h --help   show help                   = False
  -H --Halves #examples used in halving   = 512
  -p --p      distance coefficient        = 2
  -s --seed   random number seed          = 1234567891
  -m --min    minimum size               = .5
  -r --rest   |rest| is |best|*rest        = 3
  -T --Top    max. good cuts to explore   = 10
"""

"""
before reading this, do you know about docstrings, dictionary compressions,
regular expressions,and exception handling,
"""
import re, ast
from DATA import DATA
from ROW import ROW

def coerce(x):
   try : return ast.literal_eval(x)
   except Exception: return x.strip()

def oo(x) : print(o(x)); return x

def o(x):
  return x.__class__.__name__ +"{"+ (" ".join([f":{k} {v}" for k,v in sorted(x.items())
                                                           if k[0]!="_"]))+"}"

def bayes():
    wme = {
        'acc' = 0,
        'datas' = {},
        'tries' = 0,
        'n' = 0
    }
    d = DATA('../data/diabetes.csv', lambda data, t: learn(data, t, wme))
    print(wme["acc"] / wme["tries"])
    return wme["acc"] / wme["tries"] > 0.72

def learn(data, row, my, kl):
    my['n'] = my['n'] + 1
    kl = row['cells'][data.cols.klass.at]
    if my['n'] > 10:
        my['tries'] = my['tries'] + 1
        my['acc'] = my['acc'] + (1 if kl == row.likes(my['datas']) else 0)
    my['datas'][kl] = my['datas'].get(kl, DATA(data.cols.names))
    my['datas'][kl].add(row)


# In this code, global settings are kept in `the` (which is parsed from `__doc__`).
# This variable is a `slots`, which is a neat way to represent dictionaries that
# allows easy slot access (e.g. `d.bins` instead of `d["bins"]`)
class SLOTS(dict):
  __getattr__ = dict.get; __setattr__ = dict.__setitem__; __repr__ = o

the = SLOTS(**{m[1]:coerce(m[2]) for m in re.finditer( r"--(\w+)[^=]*=\s*(\S+)",__doc__)})

d = DATA(the.file)
print(d.stats(ndivs=2))
