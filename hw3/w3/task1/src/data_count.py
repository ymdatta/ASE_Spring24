import csv
import pprint
import argparse

parser = argparse.ArgumentParser(description='Print Classes and their percentage in the data')
parser.add_argument('-f', '--file', help='Path to the data file')
args = parser.parse_args()

d = {}
with open(args.file, mode='r') as file:
    csvfile = csv.reader(file)
    length = len(next(csvfile))
    rows = 0
    for x in csvfile:
        if rows > 0:
            d[x[length - 1]] = d.get(x[length - 1], 0) + 1
        rows += 1
    
for key in d.keys():
    d[key] = str(round((d[key] / rows) * 100, 2)) + "%"

print("Total Rows : ", rows)
pprint.pprint(d)