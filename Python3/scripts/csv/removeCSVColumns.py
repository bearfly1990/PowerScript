import csv

file_in = "removeColumns_in.csv"
file_out = "removeColumns_out.csv";
file_map = "removeColumns.txt"

def del_cvs_col(fname, newfname, idxs, delimiter=','):
    with open(fname, 'r') as csvin, open(newfname, 'w', newline='') as csvout:
        reader = csv.reader(csvin, delimiter=delimiter)
        writer = csv.writer(csvout, delimiter=delimiter)
        rows = (tuple(item for idx, item in enumerate(row) if idx not in idxs) for row in reader)
        writer.writerows(rows)  
        
def removeColumns(sourceCSVPath, targetCSVPath, columnsNeedRemovedPath):
    csvFile = open(sourceCSVPath, "r")
    columnsNeedRemoved = []
    sourceColumns = []
    result = []
    
    with open(columnsNeedRemovedPath) as f:
        columnsNeedRemoved = f.read().splitlines()
        
    reader = csv.reader(csvFile)
    for row in reader:
        sourceColumns = row
        break;
        
    for idx, item_csv in enumerate(sourceColumns):
        keyExist = False
        for item_key in columnsNeedRemoved:
            if(item_key.strip().upper() == item_csv.strip().upper()):
                keyExist = True
                break
        if keyExist:
           result.append(idx)
    del_cvs_col(sourceCSVPath, targetCSVPath, result, ',')
    
removeColumns(file_in, file_out, file_map)
