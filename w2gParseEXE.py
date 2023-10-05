import csv
import os
from datetime import datetime, timedelta


yesterday = datetime.today() - timedelta(days=1)
day = yesterday.day
month = yesterday.month
year = yesterday.year
monthString = yesterday.strftime("%b").upper()


# # For testing purposes
# root_loc = "/mounts/W2G/2022 W2G/EVERI/TEST/"
# file_name = "2-17.csv"
#root_loc = "C:\\Users\\JChesterfield\\Desktop\\CodingStuffNew\\" + monthString

root_loc = "\\\\atlas\\Accounting\\Common\\W2G Taxes\\" + str(year) + " W2G\\EVERI\\" + monthString
print(root_loc)
file_name = str(month) + "-" + str(day) + ".csv"
new_file_name = "new_" + file_name

try:
    os.chdir(root_loc)
    if file_name.endswith('.xlsx'):
        pass
    elif file_name.endswith('.csv'):
        headerLine = None
        with open(file_name) as f:
            csvReader = csv.reader(f)
            csv_out = open(new_file_name, 'w')
            csvWriter = csv.writer(csv_out)
            headers = {}
            for row in csvReader:
                if row[0] == "Winner's Tax Id No.":
                    headerLine = csvReader.line_num
                    for col in range(0, len(row)):
                        headers[row[col]] = col
                    # print(headers)
                    headers["Window"] = headers["Type Of Wager"]+1
                    row.insert(headers["Window"], "Window")
                    # print(headers)
                    row.pop(headers["Winner's Last Name"])
                elif headerLine != None:
                    if row[1] == "":
                        csvEOF_line = csvReader.line_num
                        row.pop(headers["Winner's Last Name"])
                    else:
                        # Combine first name and last name into first name column
                        fName = row[headers["Winner's First Name"]]
                        lName = row[headers["Winner's Last Name"]]
                        row[headers["Winner's First Name"]
                            ] = lName + ", " + fName

                        # Change Type of Column to numerica value
                        # Create new value for Window Value
                        typeOfCell = row[headers["Type Of Wager"]]
                        newTypeOfWindow = row[headers["Window"]]
                        if typeOfCell.lower() == "slot":
                            newTypeOf = 7
                            newTypeOfWindow = 'SDS'
                        elif typeOfCell.lower() == "keno":
                            newTypeOf = 5
                            newTypeOfWindow = 'KENO'
                        elif typeOfCell.lower() == 'table games' or typeOfCell.lower() == 'table game':
                            newTypeOf = 9
                            newTypeOfWindow = 'TG'
                        else:
                            newTypeOf = typeOfCell
                        row[headers["Type Of Wager"]] = newTypeOf

                        # Cashier column to 2 initials
                        cashierCell = row[headers["Cashier"]]
                        row[headers["Cashier"]] = cashierCell[:2].upper()

                        # Make indexing changes to row before writing
                        row.insert(headers["Window"], newTypeOfWindow)
                        row.pop(headers["Winner's Last Name"])
                csvWriter.writerow(row)

        # Archive original and rename new file to original name
        f.close()
        csv_out.close()
        if not os.path.exists('archive'):
            os.mkdir('archive')
        os.rename(file_name, "archive/original_" + file_name)
        os.rename(new_file_name, file_name)
        
        #Change TaxId Numbers to social security number format
        rf = open(file_name)
        r = csv.reader(rf) # Here your csv file
        lines = list(r)
        l = ''
        cur = 0
        curL = 0
        curS = 0
        temp = ['0', '0', '0', '-', '0', '0', '-', '0','0','0', '0']
        
        for line in lines:
            if (len(line) == 0 or len(line[0])  < 3 or not line[0][1].isdigit() or not line[0][2].isdigit()):
                cur += 1
                continue
            temp = ['0', '0', '0', '-', '0', '0', '-', '0','0','0', '0']
            curL = 0
            curS = 0
            l = len(line[0])
            if (l > 2):
                curL = 9 - l
                if(l == 6 or l == 5): curL += 1
                elif(l < 5): curL += 2
                for x in range(curL, 11):
                    if temp[curL].isdigit():
                        temp[curL] = line[0][curS]
                        curS += 1
                    curL += 1             
            lines[cur][0] = ''.join(temp)
            cur += 1
        
        wf = open(new_file_name, 'w')
        writer = csv.writer(wf)
        writer.writerows(lines)
        rf.close()
        wf.close()
        #print("No SSN Version Removed")
        os.remove(file_name)
        #print("Renaming Almost Final Version")
        os.rename(new_file_name, file_name)
        
        # loop through and remove blank rows from input file
        with open(file_name, newline='') as in_file:
            with open(new_file_name, 'w', newline='') as out_file:
                writer = csv.writer(out_file)
                for row in csv.reader(in_file):
                    if any(field.strip() for field in row):
                        writer.writerow(row)
        out_file.close()
        in_file.close()
        
        rf = open(new_file_name, encoding="utf-8")
        r = csv.reader(rf) # Here your csv file
        lines = list(r)
        rf.close()
        start = 0
        end = 0
        lines2 = []
    
        
        #finds start and end index of the data that needs to be sorted and moves it into a second list called lines2
        for x in range(len(lines)):
            if (len(lines[x]) > 0 and len(lines[x][0]) > 2 and lines[x][0][0] == 'W' and lines[x][0][1] == 'i'):
                start = x+1
                headerLine = lines[x]
            elif (start > 0 and len(lines[x]) > 0 and len(lines[x][0]) > 0 and lines[x][0][0].isdigit() and (len(lines[x+1]) == 0 or
                        len(lines[x+1][0]) == 0 or not lines[x+1][0][0].isdigit())):
                lines2.append(lines[x])
                end = x
            elif(len(lines[x]) > 0 and len(lines[x][0]) > 0 and lines[x][0][1].isdigit() and lines[x][0][2].isdigit()):
                lines2.append(lines[x])
                

        #sort data
        lines2.sort(key=lambda x: x[1])
        
        lines.clear()
        lines.append(headerLine) 

        #write sorted data to original list read from input file
        for line in lines2:
            lines.append(line)

        #write sorted data to file
        wf = open(new_file_name, 'w', encoding="utf-8")
        writer = csv.writer(wf)
        writer.writerows(lines)
        rf.close()
        wf.close()
        
        #remove empty rows
        with open(new_file_name, newline='', encoding="utf-8") as in_file:
            with open("new.csv", 'w', newline='', encoding="utf-8") as out_file:
                writer = csv.writer(out_file)
                for row in csv.reader(in_file):
                    if any(field.strip() for field in row):
                        writer.writerow(row)
        out_file.close()
        in_file.close()

        #print("Removing Blank Rows Version")
        os.remove(file_name)
        #print("Renaming Final Version")
        os.rename("new.csv", file_name)
        os.remove(new_file_name)
        print("Complete")
        #f = open("/scripts/outputLog.txt", "a")
        #f.write("[Success] -- w2g.py ran at " + str(datetime.now()) + "\n")
        #f.close
    elif file_name.endswith('.xls'):
        pass
except Exception as e:
    #f = open("/scripts/outputLog.txt", "a")
    #f.write("[Failure] -- w2g.py ran at " + str(datetime.now()) +
    #        "with the following error: " + str(e) + "\n")
    #f.close
    print("ERROR" + str(e))
