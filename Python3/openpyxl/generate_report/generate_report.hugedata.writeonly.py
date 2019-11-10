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
    wb_tpl = openpyxl.load_workbook(template)
    ws_report_tpl = wb_tpl['report'] #workbook.get_sheet_by_name('report')
    workbook = openpyxl.Workbook(write_only=True)
    ws_report = workbook.create_sheet('report')
    
    for row in ws_report_tpl.rows:
        row_tpl = []
        for cell in row:
            cell_tpl = openpyxl.cell.WriteOnlyCell(ws_report)
            cell_tpl.value = cell.value
            cell_tpl.font = cell.font.copy()
            cell_tpl.fill = cell.fill.copy()
            row_tpl.append(cell_tpl)
        ws_report.append(row_tpl)
        
    for idx_row, row in df_output_db.iterrows():
        ws_report.append(row.to_list())
        # if idx_row % 10000 == 0:
            # print(idx_row)
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