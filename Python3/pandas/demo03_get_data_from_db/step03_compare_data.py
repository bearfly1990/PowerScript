import pandas as pd
import pyodbc

def get_key_value(x):
    key_value = [x['id'], x['UserName'], x['Country'], x['Status']]
    return ','.join([str(x).replace(' ', '').lower() for x in key_value])

if __name__=='__main__':

    df_output_user = pd.read_excel('output_user.removed.xlsx', sheet_name='Data')
    df_output_db = pd.read_excel('output_db.xlsx', sheet_name='Data')

    df_output_user['key_value'] = df_output_user.apply(lambda x: get_key_value(x), axis=1)
    df_output_user['source'] = 'User'
    df_user_compare = df_output_user[['key_value', 'source']]

    df_output_db['key_value'] = df_output_db.apply(lambda x: get_key_value(x), axis=1)
    df_output_db['source'] = 'DB'
    df_db_compare = df_output_db[['key_value', 'source']]

    df_compare = pd.concat([df_user_compare, df_db_compare])
    df_compare = df_compare.drop_duplicates(subset=['key_value'], keep=False)

    indexes_user = df_compare.index[df_compare['source'] == 'User'].tolist()
    indexes_db = df_compare.index[df_compare['source'] == 'DB'].tolist()

    df_output_user = df_output_user.iloc[indexes_user]
    df_output_db = df_output_db.iloc[indexes_db]
    writer = pd.ExcelWriter('compare_result.xlsx', engine='openpyxl')
    df_output_user.to_excel(writer, sheet_name='User', index=False)
    df_output_db.to_excel(writer, sheet_name='DB', index=False)
    writer.save()
