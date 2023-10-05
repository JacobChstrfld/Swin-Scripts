import pandas as pd

fileName = "Current Policy Stat enrolled TMs.xlsx"       
df = pd.read_excel(fileName, header=0)
policyNames = df['Username'].tolist()

for i in range(0, len(policyNames)):
    policyNames[i] = policyNames[i].split("@", 1)[0]
       
data = pd.read_csv("SwinUsers.csv")
swinNames = data['SamAccountName'].tolist()
departments = data['department'].tolist()
names2 = []
departments2 = []

for i in range(0, len(swinNames)):
    name = swinNames[i]
    department = departments[i]
    for j in range(0, len(policyNames)):
        if (name.lower() == policyNames[j].lower()):
            break
        elif(j == len(policyNames) - 1):
            names2.append(name)
            departments2.append(department)
            
   
frame = pd.DataFrame(list(zip(names2, departments2)), columns = ['Names', 'Department'])
frame.to_csv("UsersNotFound.csv", index=False)
