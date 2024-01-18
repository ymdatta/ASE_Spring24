import csv

d = {}

i = 0
length = 0
with open("hw3/w3/data/soybean.csv", mode='r') as file:
    csvfile = csv.reader(file)
    length = len(next(csvfile))
    rows = 0
    res = {}
    for x in csvfile:
        rows += 1
        if i > 0:
            d[x[length - 1]] = d.get(x[length - 1], 0) + 1
        i = i + 1
    print("Total Rows : ", rows)
    for key in d.keys():
        res[key] = str((d[key]/rows)*100) + "%"
print(res)
