import csv

d = {}
d['negative'] = 0
d['positive'] = 0
i = 0
with open("diabetes.csv", mode='r') as file:
    csvfile = csv.reader(file)
    for x in csvfile:
        if i > 0 :
            if x[8] == 'negative':
                d['negative'] = d['negative'] + 1
            else:
                d['positive'] = d['positive'] + 1
        i = i + 1
print(d)