"""
mylo: to understand "it",  cut "it" up, then seek patterns in the pieces. E.g. here
we use cuts for multi- objective, semi- supervised, rule-based explanation.
(c) Tim Menzies <timm@ieee.org>, BSD-2 license

OPTIONS:
  -b --bins   initial number of bins      = 16
  -B --Bootstraps number of bootstraps    = 512
  -c --cohen  parametric small delta      = .35
  -C --Cliffs  non-parametric small delta = 0.2385
  -F --Far    distance to  distant rows   = .925
  -g --go     start up action             = "help"
  -h --help   show help                   = False
  -H --Halves #examples used in halving   = 512
  -p --p      distance coefficient        = 2
  -s --seed   random number seed          = 1234567891
  -m --min    minimum size               = .5
  -r --rest   |rest| is |best|*rest        = 3
  -T --Top    max. good cuts to explore   = 10
  -k --k      max. good cuts to explore   = 10
  -c --cohen    small effect size               = .35
  -f --file    where to read data          = ./../data/auto93.csv
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

def print_stats(d):
    mid = d.stats(ndivs=2)
    div = d.stats_divs(ndivs=2)
    m = ""
    for x in mid:
        m += str(x)
        m += "\t"
    print("mid:\t",m)

    di = ""
    for x in div:
        di += str(x)
        di += "\t"
    print("div:\t",di)

def print_50(d):
    rows = list(d.rows.values())
    random.seed(Constants.the.seed)
    random.shuffle(rows)
    x_ind = d._get_x()
    y_ind = d._get_y()

    for i in range(0, 50):
        s = ""
        for j in x_ind:
            s += str(rows[i].cells[j])
            s += "\t"

        print("any50:\t",s)

def print_smo(d):
    budget0 = 4
    budget = 5
    some = 0.5
    d.gate_smo(budget0,budget,some)

d = DATA(Constants.the.file)
print_stats(d)
print_50(d)
print_smo(d)