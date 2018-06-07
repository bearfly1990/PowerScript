import csv
import os

def getDirFromFullPath(filePath):
    fileDir = filePath
    index1 = filePath.rfind("\\")
    index2 = filePath.rfind("/")
    index = index1 if index1 > index2 else index2
    if(index > -1):
        fileDir = filePath[0:index]
    return fileDir

def checkDir(filePath):
    fileDir = getDirFromFullPath(filePath)
    if not os.path.exists(fileDir):
        os.makedirs(fileDir)

class CSVUtils:
    @staticmethod
    def writeToCSVFile(filePath, rowsList, delimiterX=',',quotecharX=' ', quotingX=csv.QUOTE_MINIMAL):
        with open(filePath, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=delimiterX, quotechar=quotecharX, quoting=quotingX)
            for rows in rowsList:
                spamwriter.writerow(rows)
    @staticmethod
    def readCSVRowsList(filePath):
        csvRowsList = []
        with open(filePath, newline='') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in csvReader:
                csvRowsList.append(row)
        return csvRowsList

class TxtUtils:
    @staticmethod
    def writeToTxtFile(filePath, rowsList, mode='w'):
        checkDir(filePath)
        with open(filePath, mode, newline='') as f:
            for row in rowsList:
                f.write("%s\r\n" % row)

    @staticmethod
    def readTxtRowsList(filePath):
        rowList = []
        with open(filePath, newline='') as f:
            rowList = f.read().splitlines()
            rowList = (x for x in rowList if x.strip())
        return rowList

class ConfigUtils:
    @staticmethod
    def set(filePath, section, key, value):
        lines = []
        new_lines = []
        sec_expected = False
        key_expected = False
        set_ready    = False
        with open(filePath, 'r', newline='') as f:
            lines = f.readlines()
            
        for index, line in enumerate(lines):
            is_section = "[" in line.strip().lower()
            if(is_section and section.lower() in line.strip().lower()):
                sec_expected = True
                new_lines.append(line)
                continue
            if(sec_expected and key.lower() in line.lower()):
                key_expected = True
                line = "{0}={1}\r\n".format(key, value)
                new_lines.append(line)
                continue
            if(is_section and sec_expected and not key_expected):
                new_lines.append("{0}={1}\r\n".format(key, value))
                sec_expected = False
                key_expected = True
            new_lines.append(line)
               
        with open(filePath, 'w', newline='') as f:
            f.writelines(new_lines)
                
            
            
            
            

        
