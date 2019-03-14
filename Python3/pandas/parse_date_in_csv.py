import csv
from datetime import datetime
import pandas as pd
import numpy as np

def read_csv_rows_list(file_path):
    csv_row_list = []
    with open(file_path, newline='') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvReader:
            csv_row_list.append(row)
    return csv_row_list

def use_csv_directly():
    csv_row_list = read_csv_rows_list('sample.csv')
    csv_row_list = csv_row_list[1:]
    for row in csv_row_list:
        row[0] = datetime.strptime(row[0], '%Y-%m-%d')
    [print(row) for row in csv_row_list]



data = pd.read_csv('sample.csv',encoding='utf-8',)

data[u'HolidayDate'] = pd.to_datetime(data[u'HolidayDate'])

# data[u'HolidayDate'].astype(str)
# data[u'HolidayDate'] = data[u'HolidayDate'].apply(lambda x :datetime.strptime(x, '%Y-%m-%d'))
data = np.array(data)#np.ndarray()
data_list = data.tolist()
[print(row) for row in data_list]
#data.to_csv('sample.output.csv',index=False, encoding='utf-8')
