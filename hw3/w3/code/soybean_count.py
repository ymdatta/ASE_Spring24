import csv

d = {}

i = 0
length = 0
with open("soybean.csv", mode='r') as file:
    csvfile = csv.reader(file)
    for x in csvfile:
        length = len(x)
        break

with open("soybean.csv", mode='r') as file:
    csvfile = csv.reader(file)
    for x in csvfile:
        if i > 0:
            if x[length - 1] in d:
                d[x[length - 1]] = d[x[length - 1]] + 1
            else:
                d[x[length - 1]] = 1
        i = i + 1

print(d)
