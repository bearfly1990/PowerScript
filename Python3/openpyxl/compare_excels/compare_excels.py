# author: xiche
# create at: 01/20/2019
# description:
#     simple script to compare excel
# Change log:
# Date          Author      Version     Description
# 01/20/2019    xiche       1.0         init
# 01/21/2019    xiche       1.1         add compare csvs

import openpyxl
import copy
import csv


def compare_cell(cell01, cell02):
    if(cell01.value != cell02.value):
        print('{}{}: {} / {}'.format(cell01.column,
                                     cell01.row, cell01.value, cell02.value))
    elif(cell01.data_type != cell02.data_type):
        print('{}{}: {} / {}'.format(cell01.column,
                                     cell01.row, cell01.data_type, cell02.data_type))
    elif(cell01.number_format != cell02.number_format):
        print('{}{}: {} / {}'.format(cell01.column, cell01.row,
                                     cell01.number_format, cell02.number_format))

def compare_sheet(sheet01, sheet02):

    if(sheet01.max_row != sheet02.max_row):
        print('row is not matched! {} / {}'.format(sheet01.max_row, sheet02.max_row))

    if(sheet01.max_column != sheet02.max_column):
        print('column is not matched! {} / {}'.format(sheet01.max_column,
                                                      sheet02.max_column))

    max_row = max(sheet01.max_row, sheet02.max_row)
    max_column = max(sheet01.max_column, sheet02.max_column)

    for index_row in range(max_row):
        for index_col in range(max_column):
            compare_cell(sheet01.cell(column=index_col+1, row=index_row+1),
                         sheet02.cell(column=index_col+1, row=index_row+1))


def compare_excels(excel_file01, excel_file02):
    print('------compare {} & {}------'.format(excel_file01, excel_file02))
    wb01 = openpyxl.load_workbook(excel_file01)
    wb02 = openpyxl.load_workbook(excel_file02)

    sheet_names_01 = wb01.get_sheet_names()
    sheet_names_02 = wb02.get_sheet_names()

    if(len(sheet_names_01) != len(sheet_names_02)):
        print('sheets number are not matched!')
        return

    for i in range(len(sheet_names_01)):
        if(len(sheet_names_01[i]) != len(sheet_names_02[i])):
            print('sheets name not matched!\n{}:{} / {}:{}'.format(excel_file01,
                                                                   sheet_names_01[i], excel_file02, sheet_names_02[i]))
            return
        sheet01 = wb01.get_sheet_by_name(sheet_names_01[i])
        sheet02 = wb02.get_sheet_by_name(sheet_names_02[i])

        print('compare {}:{} & {}:{}'.format(excel_file01,
                                             sheet01.title, excel_file02, sheet02.title))
        compare_sheet(sheet01, sheet02)


def compare_csv(csv_file01, csv_file02):
    print('------compare {} & {}------'.format(csv_file01, csv_file02))
    is_diff = False
    with open(csv_file01, newline='') as csv_01, open(csv_file02, newline='') as csv_02:
        csv_reader_01 = csv.reader(csv_01, delimiter=',', quotechar='|')
        csv_reader_02 = csv.reader(csv_02, delimiter=',', quotechar='|')
        csv_list_01 = list(csv_reader_01)
        csv_list_02 = list(csv_reader_02)
        ccsv_list_02_copy = copy.deepcopy(csv_list_02)

        for line in csv_list_01:
            if line not in csv_list_02:
                is_diff = True
                print('{}:{}'.format(csv_file01, line))
            else:
                ccsv_list_02_copy.remove(line)

        for line in ccsv_list_02_copy:
            print('{}:{}'.format(csv_file02, line))

        if not is_diff:
            print('No difference between these two csv')


if __name__ == '__main__':
    compare_excels('test01.xlsx', 'test01.copy.xlsx')
    compare_excels('test01.xlsx', 'test02.xlsx')
    compare_excels('test01.xlsx', 'test03.xlsx')
    compare_excels('test01.xlsx', 'test04.xlsx')
    compare_csv('demo01.csv', 'demo01.copy.csv')
    compare_csv('demo01.csv', 'demo02.csv')
