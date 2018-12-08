#/usr/bin/python3
import os
import csv
import operator

LIST_MESSAGE_FOLLOW = ['xxx', 'xxx']
LIST_MESSAGE_INIT   = ['xxx', 'xxx','xxx', 'xxx']
def isFloat(valueStr):
    try:
        float(valueStr)
        return True
    except ValueError:
        return False
        
def writeToCSVFile(filePath, rowsList, delimiterX=',',quotecharX=' ', quotingX=csv.QUOTE_MINIMAL):
    with open(filePath, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=delimiterX, quotechar=quotecharX, quoting=quotingX)
        for rows in rowsList:
            spamwriter.writerow(rows)
        
def readCSVRowsList(filePath):
    csvRowsList = []
    with open(filePath, newline='') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvReader:
            csvRowsList.append(row)
    return csvRowsList

def initAndSortByMessageMonth(csvRowsList, columnIndex = 5):
    for i, row in enumerate(csvRowsList):
        isFollow   = False
        isInit      = False
        for follow in LIST_MESSAGE_FOLLOW:
            if(follow.lower() in row[0].lower()):
                row[columnIndex] = csvRowsList[i-1][columnIndex]
                isFollow = True
        for init in LIST_MESSAGE_INIT:
            if(init.lower() in row[0].lower()):
                row[columnIndex] = 'DATAINIT'
                isInit = True
        if(not isInit and not isFollow):
            if(i != 0):
                row[columnIndex] = "#"+row[columnIndex][:6]
    csvRowsList = sorted(csvRowsList, key=lambda row: row[columnIndex], reverse=True)
    return csvRowsList
    
def combineRowsByColumn(csvRowsList, columnIndex = 5):
    resultList = []
    for i, row in enumerate(csvRowsList):
        # keep csv header and do nothing
        if(i == 0):
            resultList.append(row)
            continue
            
        currentValue = row[columnIndex]
        # get the month of last row
        if(i - 1 >= 0):
            lastValue = csvRowsList[i-1][columnIndex]
        else:
            lastValue = None
        # get the month of next row
        if(i + 1 < len(csvRowsList)):
            nextValue = csvRowsList[i+1][columnIndex]
        else:
            nextValue = None
        # if last month is the same with current month, combine them
        if(lastValue != None and lastValue == currentValue):
            for j in range(len(row)):
                #ignore the mmonth column
                if(j == columnIndex):
                    pass
                else:
                    # if is value, calculate them, if not ,just append them with '~'
                    if(isFloat(row[j])):
                        row[j] = "{:.2f}".format(float(row[j]) + float(csvRowsList[i-1][j]))
                    else:
                        row[j] = csvRowsList[i-1][j] + "~" + row[j]
        # if next value is different, just add current row to the new list
        if(currentValue != nextValue):
                resultList.append(row)  
    return resultList            
def __main__():
    resultList = readCSVRowsList("TestResult.csv")
    resultList = initAndSortByMessageMonth(resultList, 5)
    resultList = combineRowsByColumn(resultList, 5)
    writeToCSVFile("TestResultCombined.csv", resultList)
    
__main__()
