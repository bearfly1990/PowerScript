import pyodbc as pyodbc
import pandas as pd
import re
import codecs

if __name__=='__main__':
    # text = ''
    # with open('input.txt', 'r', encoding='utf-8') as f:
    #     text = f.readline()

    text = "you are right ☯ thanks"
    print(text)
    # re_multipoint_unicode = re.compile(f'[{chr(0x100)}-{chr(0x10FFFF)}]+')
    # bad_str = chr(0xFF) + chr(0x1F609)
    # text = re_multipoint_unicode.sub(lambda v: codecs.decode(codecs.unicode_escape_encode(v.group())[0]), text)

    # print(text.encode('unicode-escape').decode('utf-8'))
    # text = text.encode('unicode-escape').decode('utf-8')
    # print(text)
    # exit()
    # df_sheet_map = pd.read_excel('input.xlsx', None)
    # df_sheet = df_sheet_map['Sheet1']
    # # print(df_sheet)
    # text = df_sheet.loc[0, 'text']
    conn=pyodbc.connect(r'DRIVER={SQL Server};SERVER=PC-CX\SQLEXPRESS;UID=test;PWD=test')
    cursor = conn.cursor()
    cursor.fast_executemany = False
    cursor.executemany("insert into [BFTest].[dbo].[Test_Invalid_Character](text) values (?)",
                       [[text], [text]])
    conn.commit()
    cursor.close()
    conn.close()
    # cursor.execute('select id, UserName as user_name from [BFTest].[dbo].[Test_Output]')
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row.id, row.user_name)