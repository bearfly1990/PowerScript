import pandas as pd
import numpy as np
df_sheet = pd.read_excel('test_file.xlsx', sheet_name='salary01')
print(df_sheet)

df_sheet = pd.read_excel('test_file.xlsx', sheet_name='salary01', index_col = [0])
print(df_sheet)

df_sheet = pd.read_excel('test_file.xlsx', sheet_name='salary01',  converters = {'Name': str, 'Salary': int}, index_col = [0])

print(df_sheet)
print(df_sheet.index.to_list())
print(df_sheet.shape[0])
print(len(df_sheet))
print(df_sheet.shape[1])
print(df_sheet.columns.to_list())

df_sheet = df_sheet.reset_index()
print(df_sheet)
# df_sheet['Salary'] = df_sheet['Salary'].fillna(0)
# df_sheet.fillna(value=pd.np.nan, inplace=True)
# print(df_sheet)
# df_sheet = pd.read_excel('test_file.xlsx', sheet_name='salary01',  converters = {'Salary': str})
# print(df_sheet)


def replace_nan_to_none(x):
    print(x is np.nan)
    if x is np.nan:
        return None
    return x

df_sheet = df_sheet.where(df_sheet.notnull(), None)

print(df_sheet)
print(df_sheet.index.tolist())
print(df_sheet.values.tolist())
#first
df_sheet.drop_duplicates(['Name', 'gender', 'Company', 'Salary'], keep='last', inplace=True)
print(df_sheet)

# df_sheet_by_gender = df_sheet.loc[df_sheet['gender'].isin(['man', 'female'])]
df_sheet_by_gender = df_sheet[(df_sheet['gender']!='man') & (df_sheet['gender']!='female')]
print(df_sheet_by_gender)
print(df_sheet_by_gender.index.tolist())

def test(x):
    return x not in ['man', 'female']

df_sheet_by_gender = df_sheet[df_sheet['gender'].apply(lambda x: test(x))]
print(df_sheet_by_gender)


df_sheet['new_column'] = df_sheet['Salary'] * 3
print(df_sheet)
df_sheet.to_excel("output.xlsx", sheet_name='newsheet', index=False)
df_sheet.to_excel("output.xlsx", sheet_name='newsheet', index=False, columns=['Name', 'Company', 'Salary'])
print(df_sheet.index.tolist())
print(df_sheet.values.tolist())
