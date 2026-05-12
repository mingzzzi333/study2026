import csv

data = [
    ["Name", "Age", "City"],
    ["김민준", 28, "서울"],
    ["이서연", 34, "부산"],
    ["박지호", 22, "인천"]
]

filename = "data.csv"
with open(filename, "w", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)  # writerows(data)

data2 = [
    {"Name": "김민준", "Age": 28, "City": "서울"},
    {"Name": "이서연", "Age": 34, "City": "부산"},
    {"Name": "박지호", "Age": 22, "City": "인천"},
]

with open(filename, "w", newline="") as file:
    headers = data2[0].keys()
    csv_writer = csv.DictWriter(file, fieldnames=headers)  # fieldnames
    csv_writer.writeheader()
    csv_writer.writerows(data2)  # writerows(data2)