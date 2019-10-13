import pandas as pd
import pyodbc

if __name__=='__main__':
    conn=pyodbc.connect(r'DRIVER={SQL Server};SERVER=PC-CX\SQLEXPRESS;UID=test;PWD=test')
    sql_str = 'select * from [BFTest].[dbo].[Test_Output]'

    sql_query = pd.read_sql_query(sql_str, conn)
    df_output_db = pd.DataFrame(sql_query)

    writer = pd.ExcelWriter('output_db.xlsx', engine='openpyxl')
    df_output_db.to_excel(writer, sheet_name='Data', index=False)
    writer.save()