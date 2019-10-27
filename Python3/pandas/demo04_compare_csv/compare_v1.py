import pandas as pd
import numpy as np


def read_mapping(file):
    mapping = {}
    with open(file, 'r') as f:
        rows = f.readlines()
    for row in rows:
        key, value = row.split(',')
        mapping[key.strip()] = value.strip()
    return mapping

def compare_csv(csv1_path, csv2_path, mapping, column):
    df_csv1=pd.read_csv(csv1_path)
    df_csv2=pd.read_csv(csv2_path)

    for index,row in df_csv1.iterrows():
        old_value = row[column]
        if old_value in mapping:
            expect_value = mapping.get(old_value)
            new_value = df_csv2.loc[index,column]
            if expect_value != new_value:
                print(f'File-<{csv2_path}> Col-<{column}> Row-<{index+1}> should be <{expect_value}>, but <{new_value}> found')
        else:
            print(f'File-<{csv1_path}> Col-<{column}> Row-<{index+1}> value-<{old_value}> is not in the mapping file')                
        # print(row[column], df_csv2.loc[index,column])


if __name__=='__main__':
    mapping_info = read_mapping('mapping_info.txt')

    for column in mapping_info.keys():
        mapping_file = mapping_info[column]
        column_mapping = read_mapping(mapping_file)
        compare_csv('source_old.csv', 'source_new.csv', column_mapping, column)

