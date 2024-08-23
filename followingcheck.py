import csv

def extract_handles_from_csv(file_path):
    handles = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 1:
                handles.append(row[1].strip())
    return handles

handles = extract_handles_from_csv("following.csv")

# print(len(handles))

# names = []

for i in range(len(handles) - 2, 0, -2):
    if(handles[i].startswith("@")):
        print(i, handles[i])
        break

# name = 1
# for i in handles:
#     if(name % 2 == 0 and i[0] != "@"):
#         print(name, i)
#     name += 2
