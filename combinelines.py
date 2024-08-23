import csv

def extract_handles_from_csv(file_path):
    handles = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 1:
                handles.append([row[0], row[1]])
    return handles
        
handles = extract_handles_from_csv("following.csv")

# print(handles[1], handles[2])

formattedData = []

for i in range(0, len(handles), 2):
    if(handles[i][0] == handles[i + 1][0]):
        formattedData.append([handles[i][0], handles[i][1], handles[i + 1][1]])
        
handle = []

for i in formattedData:
    handle.append(i[2])

print(len(set(handle)))

# with open("formatted_Data.csv", 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
    
#     # Write the 2D array to the CSV file
#     writer.writerows(formattedData)
