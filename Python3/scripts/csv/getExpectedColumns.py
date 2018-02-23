import csv

file_expectedColumns = "getExpectedColumns.txt"
file_input = "getExpectedColumns_in.csv";
file_output= "getExpectedColumns_out.csv";

def del_cvs_col(fname, newfname, idxs, delimiter=','):
    with open(fname, 'r') as csvin, open(newfname, 'w', newline='') as csvout:
        reader = csv.reader(csvin, delimiter=delimiter)
        writer = csv.writer(csvout, delimiter=delimiter)
        rows = (tuple(item for idx, item in enumerate(row) if idx not in idxs) for row in reader)
        writer.writerows(rows)  
        
def removeNotMappedColumn(sourceCSVPath, targetCSVPath, expectedColumnsPath):
    csvFile = open(sourceCSVPath, "r")
    expectedColumns = []
    sourceColumns = []
    result = []
    
    with open(expectedColumnsPath) as f:
        expectedColumns = f.read().splitlines()
        
    reader = csv.reader(csvFile)
    for row in reader:
        sourceColumns = row
        break;
        
    for idx, item_csv in enumerate(sourceColumns):
        keyExist = False
        for item_key in expectedColumns:
            if(item_key.strip().upper() == item_csv.strip().upper()):
                keyExist = True
                break
        if not keyExist:
           result.append(idx)
    del_cvs_col(sourceCSVPath, targetCSVPath, result, ',')
    
removeNotMappedColumn(file_input, file_output, file_expectedColumns)
