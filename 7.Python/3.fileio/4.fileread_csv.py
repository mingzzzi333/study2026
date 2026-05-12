import csv

filename = "data.csv"
data=[]

with open(filename, "r") as file:
    # data = file.read()
    # print(data)
    csv_reader = csv.reader(file)
    for row in csv_reader:
        data.append(row)
        
print(row)
#2. 모던 방식 (dict)형태로 복원
data2=[]
with open(filename,"r") as file:
    csv_reader=csv.DictReader(file)
    for row in csv_reader:
        data2.append(row)

print(data2)