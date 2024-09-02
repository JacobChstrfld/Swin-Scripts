import pandas as pd
import os
from datetime import datetime, timedelta
import shutil

yesterday = datetime.today() - timedelta(days=1)
day = yesterday.day
month = yesterday.month
year = yesterday.year
monthString = yesterday.strftime("%b").upper()

rootLocation = "\\\\atlas\\Accounting\\Common\\W2G TAXES\\" + str(year) + " W2G\\TAX DOWNLOADS\\" + monthString
#rootLocation = "\\\\atlas\\Accounting"
#rootLocation = "C:\\Users\\JChesterfield\\Documents\\" + monthString
fileName = str(month) + "-" + str(day) + ".csv"
print(fileName)
os.chdir(rootLocation)
if not os.path.exists('archive'):
    os.mkdir('archive')
data = pd.read_csv(rootLocation + "\\" + fileName, skiprows=[0,1,2])
shutil.move(rootLocation + "\\" + fileName, rootLocation + "\\archive\\original_" + fileName)

#Drop unwanted columns by index
data = data.drop(columns=data.columns[[0,1,2,4,5,7,9,18,19,20,23,24,25,26,27,28,29,30,
                                           31,32,34,35,36,37,38,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58]], axis=1)

#Drop last row if the data type is incorrect
typeOfWagerCol = data['typeofwager_31'].tolist()
numberOfRows = len(typeOfWagerCol) - 1
if ((isinstance(typeOfWagerCol[numberOfRows], str)) == False):
    data = data.drop([data.index[numberOfRows]])

typeOfWagerCol = data['typeofwager_31'].tolist()
numberOfRows = len(typeOfWagerCol) - 1
  
    #Get columns into lists
winnersIDCol = data['winnerstaxpayeridentificationnumbers_9'].tolist()
lastnameCol = data['lastname'].tolist()
firstnameCol = data['firstname'].tolist()
addressCol = data['winnersaddress'].tolist()
cityCol = data['winnerscity'].tolist()
stateCol = data['winnersstate'].tolist()
zipCol = data['winnerszip'].tolist()
reportableCol = data['reportablewinnings_11'].tolist()
timestampCol = data['transactiontimestamp1'].tolist()
taxWithheldCol = data['federalincometaxwithheld_41'].tolist()
transactionCol = data['transaction_5'].tolist()
transactionByCol = data['transactiondoneby1'].tolist()
firstIDCol = data['firstid_11'].tolist()
typeOfWagerCol = data['typeofwager_31'].tolist()
wagerIDCol = []
        
#print(data)
    #Modify columns
for i in range(0, len(typeOfWagerCol)):
    #print(lastnameCol[i])
    #print(typeOfWagerCol[i])
    if (typeOfWagerCol[i][0:4] == "Slot" or typeOfWagerCol[i][0:3] == "ETG"):
        typeOfWagerCol[i] = "SDS"
        wagerIDCol.append("7")
    elif(typeOfWagerCol[i][0:4] == "Keno"):
        typeOfWagerCol[i] = "KENO"
        wagerIDCol.append("5")
    else:
        typeOfWagerCol[i] = "TABLE"
        wagerIDCol.append("9")
        
    lastnameCol[i] += ", " + firstnameCol[i]
    #timestampCol[i] = str(yesterday.month) + "/" + str(yesterday.day) + "/" + str(yesterday.year)
    transactionByCol[i] = str(transactionByCol[i][len(transactionByCol[i])-1] + transactionByCol[i][0]).upper()
    
#Reorder columns and build new dataframe
d = {'winnertaxpayeridentificationnumbers_9': winnersIDCol, 'lastname': lastnameCol, 'winnersaddress': addressCol,
        'winnerscity': cityCol, 'winnersstate': stateCol, 'winnerszip': zipCol, 'reportablewinnings_11': reportableCol,
        'transactiontimestamp1': timestampCol, 'WagerID': wagerIDCol, 'typerofwager_31': typeOfWagerCol,
        'federalincometaxwithheld_41': taxWithheldCol, 'transaction_5': transactionCol,
        'tranactiondoneby1': transactionByCol, 'firstid_11': firstIDCol}
df = pd.DataFrame(data=d)
df = df.rename(columns={"winnertaxpayeridentificationnumbers_9": "Winner's Tax Id No.", 'lastname': "Winner's First Name",
                        'winnersaddress': "Winner's Street Address", 'winnerscity': "Winner City", 'winnersstate': "Winner State",
                        'winnerszip': "Winner Zip", 'reportablewinnings_11': "Gross Winnings", 'transactiontimestamp1': "Date Won",
                        'WagerID': "Type Of Wager", 'typerofwager_31': "Window", "federalincometaxwithheld_41": "Fed Tax W/H",
                        'transaction_5': "Trans", "tranactiondoneby1": "Cashier", 'firstid_11': "First Id"})
df = df.sort_values("Winner's First Name")
df.to_csv(rootLocation + "\\" + fileName, index=False)

