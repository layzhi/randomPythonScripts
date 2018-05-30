import csv

f = open('chipotle.tsv', mode='rU')
# with open('chipotle.tsv', mode='rU') as f:
#     file_nested_list = [row for row in csv.reader(f,delimiter='\t')]

file_nested_list = []
count = []
numCount = 0
sum = 0
#num_orders = len(set([row[0] for row in data]))
for row in csv.reader(f, delimiter='\t'):
    #read csv into a list
    file_nested_list.append(row)

    #add unique id into list count
    if row[0] not in count:
        count.append(row[0])

header = file_nested_list[0]
#print(header)
data = file_nested_list[1:]

# strip the dollar sign and trailing space
# prices = [float(row[4][1:-1]) for row in data]
# round(sum(prices) / 1834, 2)
for x in data:
    sum = sum + float(x[4][1:-1])
avg = round(sum/1834,2)
#print(avg)

soda = []
for drink in data:
    if('Canned' in drink[2]):
        soda.append(drink[3])
unique_soda = set(soda)

#calculate the avg num of toppings per burrito
burritoCount = 0
toppingCount = 0
for description in data:
    if('Burrito' in description[2]):
        burritoCount += 1
        toppingCount += (description[3].count(',') + 1) 
#print(repr(burritoCount)+ ' '+repr(toppingCount))
print(round(toppingCount/ float(burritoCount),2))

#dictionary in which the keys represent chip orders and values that represent the total orders
chips = {}
for row in data:
    if('Chips' in row[2]):
        if row[2] not in chips:
            chips[row[2]] = int(row[1])
        else:
            chips[row[2]] += int(row[1])
#print (chips)

#defaultdict saves me the troble of checking whether a key exists
from collections import defaultdict
dchips = defaultdict(int)
for row in data:
    if('Chips' in row[2]):
        dchips[row[2]] += int(row[1])
print(dchips)