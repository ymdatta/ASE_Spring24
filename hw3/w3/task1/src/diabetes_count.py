import csv

d = {}
d['negative'] = 0
d['positive'] = 0
i = 0
with open("hw3/w3/data/diabetes.csv", mode='r') as file:
    csvfile = csv.reader(file)
    for x in csvfile:
        if i > 0 :
            if x[8] == 'negative':
                d['negative'] = d['negative'] + 1
            else:
                d['positive'] = d['positive'] + 1
        i = i + 1
print(d)
print("Negative Class  =",d['negative']/(d['negative'] + d['positive'])*100, "%")
print("Positive Class  =",d['positive']/(d['negative'] + d['positive'])*100, "%")
