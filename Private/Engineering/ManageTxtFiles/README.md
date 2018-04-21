## 处理txt文件
在最近的项目中，需要创建数据用来测试。有时生成的文件太大，需要分散到小的文件中，或者反之。

之前已经有用java写的生成数据的代码，但是改起来不太方便，也没有针对性，用python就方便很多。

代码其实很简单，以后工作中有用到的话，可以直接拿来用，不用再花时间造轮子了：
```python
#/usr/bin/python3
"""
author: xiche
create at: 04/21/2018
description:
There are two operations in this script
    1. Aggregate several txt files to one file by the file name order which contains the same part name 
    2. Seperate one large txt file to several small files, you could control how many files you want to generate
Change log:
Date        Author      Version    Description
04/21/2018  xiche       1.0        Set up this script
"""
import os
import glob

# Aggregate all the files which name contains the name as below
AGGREGATED_INPUT_FILE_PART_NAME = "WKLMF"
AGGREGATED_OUTPUT_FILE_NAME     = "AggregatedFiles.txt"

# The original file which want to seperate to several files
SEPERATED_INPUT_FILE_NAME   = "AggregatedFiles.txt"
# Output files which are like Seperated_1.txt/Seperated_2.txt/Seperated_3.txt
SEPERATED_OUTPUT_FILE_NAME  = "Seperated.txt"
SEPERATED_OUTPUT_FILE_NUMS  = 6

def getFileNameWithoutSuffix(fullPath):
    """Get filename without suffix: Filename.txt => FileName"""
    lastIndex = fullPath.rfind('.')
    return fullPath[:lastIndex]

def getFileNameSuffix(fullPath):
    """Get file name suffix like .txt"""
    lastIndex = fullPath.rfind('.')
    return fullPath[lastIndex:]

def writeRowsListToFile(filePath, fileRows):
    with open(filePath, 'w') as f:
        for rows in fileRows:
            for row in rows:
                f.write("%s\n" % row)
            
# def writeRowsToFile(filePath, rows):
    # with open(filePath, 'w') as f:
        # for row in rows:
            # f.write("%s\n" % row)
            
def aggregateTxtFilesToOneFile(inputFilesPartName, outputFileName):
    """Main function to aggregate txt files"""
    totalRows = []
    list_of_files = glob.glob('./*{}*'.format(inputFilesPartName))
    for filePath in list_of_files:
        with open(filePath) as f:
            lines = f.read().splitlines()
            totalRows.append(lines)
    writeRowsListToFile(outputFileName, totalRows)

def seperateTxtFilesToSeveralFiles(inputFileName, outputFileName, outputFileNums):
    """Main function to seperate txt files"""
    totalRows   = []
    totalRowNums = 0
    rowsEachFile = 0
    with open(inputFileName) as f:
        totalRows = f.read().splitlines()
        totalRowNums = len(totalRows)
    if(totalRowNums % outputFileNums == 0):
        rowsEachFile = int(totalRowNums/outputFileNums)
    else:
        rowsEachFile = int(totalRowNums/outputFileNums) + 1

    for i in range(outputFileNums):
        with open("{}_{}{}".format(getFileNameWithoutSuffix(outputFileName), i+1, getFileNameSuffix(outputFileName)), 'w') as f:
            for j in range(rowsEachFile):
                f.write("%s\n" % totalRows[i *rowsEachFile  + j])
            
def __main__():
    aggregateTxtFilesToOneFile(AGGREGATED_INPUT_FILE_PART_NAME, AGGREGATED_OUTPUT_FILE_NAME)
    seperateTxtFilesToSeveralFiles(SEPERATED_INPUT_FILE_NAME, SEPERATED_OUTPUT_FILE_NAME, SEPERATED_OUTPUT_FILE_NUMS)
__main__()
```
