import pandas as pd
import glob


dict_output = {}
dict_output['fileName'] = []
dict_output['sheet'] = []
dict_output['rows'] = []

files = glob.glob('**/*.xlsx', recursive=True)
files = files + glob.glob('**/*.xls', recursive=True)
print(files)
for file in files:
    print(file)
    df_sheet_map = pd.read_excel(file, None)
    sheets = list(df_sheet_map.keys())

    for sheet in sheets:
        df_sheet = df_sheet_map[sheet]
        print('--',sheet, ':', len(df_sheet.index))
        dict_output['fileName'].append(file)
        dict_output['sheet'].append(sheet)
        dict_output['rows'].append(len(df_sheet.index))

df_output = pd.DataFrame(dict_output)

df_output.to_excel("output.xlsx", sheet_name='details', index=False)

# with pd.ExcelWriter('output.xlsx') as writer:  # doctest: +SKIP
#     ...     df1.to_excel(writer, sheet_name='Sheet_name_1')
#     df2.to_excel(writer, sheet_name='Sheet_name_2'