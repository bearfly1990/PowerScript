import pandas as pd
import pyodbc
import openpyxl
from datetime import datetime

conn=pyodbc.connect(r'DRIVER={SQL Server};SERVER=PC-CX\SQLEXPRESS;UID=test;PWD=test')

def logger_info(message):
    print(f'{datetime.now()}[INFO]', message)
    
    
def query_data_from_db(conn):
    sql_str = 'select UserName, Age, Country, [Status] from [BFTest].[dbo].[Test_Output]'
    sql_query = pd.read_sql_query(sql_str, conn)
    df_output_db = pd.DataFrame(sql_query)
    return df_output_db
    
    
def write_to_excel(template, report):
    workbook = openpyxl.load_workbook(template)
    ws_report = workbook['report'] #workbook.get_sheet_by_name('report')
    row_start = 2
    # print(df_output_db)
    for idx_row, row in df_output_db.iterrows():
        for idx_col in range(len(row)):
            ws_report.cell(column = idx_col+1, row = row_start + idx_row).value = row[idx_col]
    workbook.save(report)        


def large_data(df):
    df_large = df.copy()
    for i in range(17):
        df = df_large.copy()
        df_large=pd.concat([df_large,df])
         
    return df_large
if __name__=='__main__':
    start_time = datetime.now()

    logger_info('query data from db')
    df_output_db = query_data_from_db(conn)

    logger_info('large data')
    df_output_db = large_data(df_output_db)
    df_output_db = df_output_db.reset_index(drop=True)
    logger_info(f'count data:{len(df_output_db)}')
    
    logger_info('write to excel')
    start_time_excel = datetime.now()
    write_to_excel('template.xlsx', 'report.xlsx')
    logger_info(f'write to excel cost time:{datetime.now() - start_time_excel}')
    
    logger_info(f'cost time:{datetime.now()-start_time}')