"""
mylo: to understand "it",  cut "it" up, then seek patterns in the pieces. E.g. here
we use cuts for multi- objective, semi- supervised, rule-based explanation.
(c) Tim Menzies <timm@ieee.org>, BSD-2 license

OPTIONS:
  -b --bins   initial number of bins      = 16
  -B --Bootstraps number of bootstraps    = 512
  -c --cohen  parametric small delta      = .35
  -C --Cliffs  non-parametric small delta = 0.2385
  -F --far    distance to  distant rows   = .95
  -g --go     start up action             = "help"
  -h --help   show help                   = False
  -H --half   #examples used in halving   = 256
  -p --p      distance coefficient        = 2
  -s --seed   random number seed          = 1234567891
  -m --min    minimum size               = .5
  -r --rest   |rest| is |best|*rest        = 3
  -T --Top    max. good cuts to explore   = 10
  -k --k      max. good cuts to explore   = 10
  -c --cohen    small effect size               = .35
  -f --file    where to read data          = ../data/auto93.csv
  -h --help     show help                       = false
  -k --k        low class frequency kludge      = 1
  -m --m        low attribute frequency kludge  = 2
  -s --seed     random number seed              = 31210
"""

"""
before reading this, do you know about docstrings, dictionary compressions,
regular expressions,and exception handling,
"""
import re, ast
from DATA import DATA
from ROW import ROW
import pdb
import sys
import Constants
import random
import Utils


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

setDocValue()
UpdateCLAValues()
#bayes()

wme = {
    'acc' : 0.0,
    'datas' : {},
    'tries' : 0,
    'n' : 0
}

def _get_string(d):
    s = "{"
    for i in d.values():
        s += " " + str(i)
    s += "}"

    return s

# d = DATA(Constants.the.file)
# r1 = d.rows[1]
# rows = r1.neighbors(d)
# count = 0
# for row in rows:
#     if (count % 30 == 0):
#         print(count + 1, _get_string(row.cells), round(row.dist(r1, d), 2))
#     count += 1

#print("Week 5 Sort based on First of Rows as Heaven")
def eg_branch(the=Constants.the):
    d = DATA(the.file)
    best, rest, evals = d.branch()
    print("centroid of output cluster:")
    print(Utils.o(best.mid().cells, 2))
    print("evals: ", evals)

def eg_doubletap(the=Constants.the):
    d = DATA(the.file)
    best1, rest, evals1 = d.branch(32)
    best2, _, evals2 = best1.branch(4)
    print(Utils.o(best2.mid().cells, 2), Utils.o(rest.mid().cells, 2))
    print(evals1 + evals2)

def eg_tree(the=Constants.the):
    data_instance = DATA(the.file)
    t, evals = data_instance.tree(True)
    t.show()
    print("evals: ", evals)

eg_tree()
# eg_branch()
# eg_doubletap()
