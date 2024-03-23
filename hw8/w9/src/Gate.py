"""
mylo: to understand "it",  cut "it" up, then seek patterns in the pieces. E.g. here
we use cuts for multi- objective, semi- supervised, rule-based explanation.
(c) Tim Menzies <timm@ieee.org>, BSD-2 license

OPTIONS:
  -b --bins   initial number of bins      = 16
  -B --Beam   max number of ranges        = 10
  -c --cohen  parametric small delta      = .35
  -C --Cliffs  non-parametric small delta = 0.2385
  -F --far    distance to  distant rows   = .92
  -g --go     start up action             = "help"
  -h --help   show help                   = False
  -H --half   #items to use in clustering     = 256
  -p --p      distance coefficient        = 2
  -s --seed   random number seed          = 1234567891
  -m --min    minimum size               = .5
  -r --rest   |rest| is |best|*rest        = 3
  -T --Top    max. good cuts to explore   = 10
  -k --k      max. good cuts to explore   = 10
  -c --cohen    small effect size               = .35
  -f --file    where to read data          =  ../data/auto93.csv
  -h --help     show help                       = false
  -k --k        low class frequency kludge      = 1
  -m --m        low attribute frequency kludge  = 2
  -s --seed     random number seed              = 31210
  -S --Support coeffecient on best            = 2
"""

"""
before reading this, do you know about docstrings, dictionary compressions,
regular expressions,and exception handling,
"""
import re, ast
from DATA import DATA
from ROW import ROW
from SAMPLE import SAMPLE
import pdb
import sys
import Constants
from RANGE import RANGE
import random
import math


def coerce(x):
   try : return ast.literal_eval(x)
   except Exception: return x.strip()

def oo(x) : print(o(x)); return x

def o(x):
  return x.__class__.__name__ +"{"+ (" ".join([f":{k} {v}" for k,v in sorted(x.items())
                                                           if k[0]!="_"]))+"}"
def setDocValue():
    options = re.findall(r'-(\w+)\s+--(\w+)\s+.*=\s*(\S+)', __doc__)
    for option in options:
        short_form, full_form, default_value = option
        Constants.the[full_form] = coerce(default_value)
        Constants.opt_dir[short_form] = full_form


def UpdateCLAValues():
    options = {}
    CLArguments = sys.argv[1:]
    if("--help" in CLArguments or "-h" in CLArguments):
        Constants.the["help"] = 'True'
        return

    for i in range(0, len(CLArguments), 2):
        options[CLArguments[i]] = CLArguments[i+1]

    for opt,val in options.items():
        if opt.startswith('--'):
            Constants.the[opt[2:]] = coerce(val)
        elif opt.startswith('-'):
            Constants.the[Constants.opt_dir[opt[1:]]] = coerce(val)
    return Constants.the


def bayes():
    wme = {
        'acc' : 0.0,
        'datas' : {},
        'tries' : 0,
        'n' : 0
    }
    d = DATA(Constants.the.file, lambda data, t: learn(data, t, wme))
    print(wme["acc"] / wme["tries"] * 100)
    print(wme["acc"] / wme["tries"] > 0.72)
    return wme["acc"] / wme["tries"] > 0.72

def learn(data, row, my):
    my['n'] = my['n'] + 1
    kl = row.cells[data.cols.klass.at]
    if my['n'] > 10:
        my['tries'] = my['tries'] + 1
        my['acc'] = my['acc'] + (1 if kl  == row.likes(my['datas'])[0] else 0)

    if kl not in my['datas']:
      my['datas'][kl] = DATA(data.cols.names)

    my['datas'][kl].add(row.cells)

# In this code, global settings are kept in `the` (which is parsed from `__doc__`).
# This variable is a `slots`, which is a neat way to represent dictionaries that
# allows easy slot access (e.g. `d.bins` instead of `d["bins"]`)
class SLOTS(dict):
  __getattr__ = dict.get; __setattr__ = dict.__setitem__; __repr__ = o

Constants.the = SLOTS(**{m[1]:coerce(m[2]) for m in re.finditer( r"--(\w+)[^=]*=\s*(\S+)",__doc__)})

#setDocValue()
#UpdateCLAValues()

def _mergeds(ranges, too_few):
    t = []
    i=1
    while i <= len(ranges):
        a = ranges[i - 1]
        if i < len(ranges):
            both = a.merged(ranges[i], too_few)
            if both:
                a = both
                i += 1
        t.append(a)
        i += 1
    if len(t) < len(ranges):
        return _mergeds(t, too_few)
    for i in range(1, len(t)):
        t[i].x['lo'] = t[i - 1].x['hi']
    t[0].x['lo'] = -math.inf
    t[-1].x['hi'] = math.inf
    return t

def _ranges1(col, rowss):
    out = {}
    nrows = 0
    for y, rows in rowss.items():
        nrows += len(rows)
        for row in list(rows):
            x = row.cells[col.at]
            if x != "?":
                bin = col.bin(x)
                if bin not in out:
                    out[bin] = RANGE(col.at, col.txt, x)
                out[bin].add(x, y)
    out = list(out.values())
    out.sort(key=lambda a: a.x['lo'])
    return out if hasattr(col, 'has') else _mergeds(out, nrows / Constants.the.bins)

def bins():
    d = DATA(Constants.the.file)
    best, rest, _ = d.branch()
    LIKE = list(best.rows.values())
    # HATE = random.sample(rest.rows, min(3 * len(LIKE), len(rest.rows)))
    HATE = random.sample(list(rest.rows.values()), min(3 * len(LIKE), len(rest.rows)))

    def score(range_):
        return range_.score("LIKE", len(LIKE), len(HATE))

    t = []
    for col in list(d.cols.x.values()):
        print("")
        for range_ in _ranges1(col, {"LIKE": LIKE, "HATE": HATE}):
            print(range_)
            t.append(range_)

    # t.sort(key=lambda a: score(a), reverse=True)
    # max_score = score(t[0])
    # print("\n#scores:\n")
    # for v in t[:Constants.the.Beam]:
    #     if score(v) > max_score * 0.1:
    #         print("{:.2f}".format(round(score(v), 2)), v)
    # print({"LIKE": len(LIKE), "HATE": len(HATE)})

bins()
