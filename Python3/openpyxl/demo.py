import openpyxl
import datetime
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
# from openpyxl.drawing.image import Image

def testReadExcel():
    wb = openpyxl.load_workbook('test.xlsx')
    print(type(wb))
    print(wb.sheetnames)
    print(wb['salary'])

    sheet_salary = wb['salary']
    sheet_salary = wb.active

    print("title:%s" % sheet_salary.title)

    print("A1:%s B1:%s C1:%s" % (sheet_salary['A1'].value, sheet_salary['B1'].value, sheet_salary['C1'].value))
    print("A2:%s B2:%s C2:%s" % (sheet_salary['A2'].value, sheet_salary['B2'].value, sheet_salary['C2'].value))
    print("A3:%s B3:%s C3:%s" % (sheet_salary['A3'].value, sheet_salary['B3'].value, sheet_salary['C3'].value))

    cell = sheet_salary['A1']
    print(cell.value)
    print("column:%s row:%s coordinate:%s" % (cell.row, cell.column, cell.coordinate))

    cell_A1 = sheet_salary.cell(column = 1, row = 1)
    cell_A2 = sheet_salary.cell(column = 1, row = 2)
    cell_B1 = sheet_salary.cell(column = 2, row = 1)
    cell_B2 = sheet_salary.cell(column = 2, row = 2)

    print("A1:%s B1:%s" % (cell_A1.value, cell_B1.value))
    print("A2:%s B3:%s" % (cell_A2.value, cell_B2.value))

    for i in range(1, 2):
            print("column:%s row:%s coordinate:%s" % (
                sheet_salary.cell(column = 1, row = i).value, 
                    sheet_salary.cell(column = 2, row = i).value, 
                        sheet_salary.cell(column = 3, row = i).value)
                )

    for i in range(1, 2):
        for j in range(1, 2, 3):
            columnChar = chr(ord('A')+j)
            rowNum = i
            print("%s%s:%s" % (columnChar, rowNum, sheet_salary[columnChar+str(rowNum)].value))

    print("max_row:%s" % sheet_salary.max_row)
    print("max_column:%s" % sheet_salary.max_column)

def testWriteNewExcel():
    wb = Workbook()
    dest_filename = 'test.xlsx'

    ws1 = wb.active
    ws1.title = "salary"

    # for row in range(1, 40):
    #     ws1.append(range(600))

    ws1['A1'] = 'id'
    ws1['B1'] = 'name'
    ws1['C1'] = 'salary'
    ws1['A2'] = 1
    ws1['B2'] = 'xiche'
    ws1['C2'] = 9999
    ws1['A3'] = datetime.datetime(2010, 7, 21)
    print(ws1['A1'].number_format)
    wb.guess_types = True
    ws1['B3'] = '3.14%'
    wb.guess_types = False
    print(ws1['B3'])
    print(ws1['B3'].number_format)


    ws1["A4"] = "=SUM(1, 1)"
    ws1.merge_cells('A5:E5')
    ws1.merge_cells('A6:E7')
    ws1.unmerge_cells('A6:E7')
    # image = Image('logo.png')
    # ws1.add_image(img, 'C1')

    ws2 = wb.create_sheet(title="Pi")

    ws2['F5'] = 3.14

    ws3 = wb.create_sheet(title="Data")
    for row in range(10, 20):
        for col in range(27, 54):
            ws3.cell(column=col, row=row, value="{0}".format(get_column_letter(col)))
    print(ws3['AA10'].value)
    
    wb.save(filename = dest_filename)

testWriteNewExcel()
testReadExcel()
