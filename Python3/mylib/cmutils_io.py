#/usr/bin/python3
"""
author: xiche
create at: 06/16/2018
description:
    Utils for io operation
Change log:
Date         Author      Version    Description
06/16/2018    xiche      1.0.1      add replace variables features for TxtUtils
06/17/2018    xiche      1.0.2      add TxtUtils.read_first_line
07/30/2018    xiche      1.0.3      add cls for class method
08/10/2018    xiche      1.0.4      add class PathUtils
08/18/2018    xiche      1.0.5      add TxtUtils.read_string_from_txt
08/30/2018    xiche      1.1.0      change the method names style
"""
import csv
import os

class PathUtils:

    @staticmethod
    def check_make_dir_exist(filePath):
        fileDir = getDirFromFullPath(filePath)
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)
    @staticmethod
    def get_dir_name_from_full_path(filePath):
        fileDir = filePath
        index1 = filePath.rfind("\\")
        index2 = filePath.rfind("/")
        index = index1 if index1 > index2 else index2
        if(index > -1):
            fileDir = filePath[0:index]
        return fileDir
        
    @staticmethod
    def get_filename_from_full_path(fullPath):
        file_name = os.path.basename(fullPath)
        # lastIndex = fullPath.rfind('\\')
        # if(lastIndex == -1):
            # lastIndex = fullPath.rfind('/')
            
        # if(lastIndex == -1):
            # lastIndex = 0
            
        # return fullPath[lastIndex:]
        return file_name
        
class CSVUtils:

    @staticmethod
    def write_to_csv_file(filePath, rowsList, delimiterX=',',quotecharX=' ', quotingX=csv.QUOTE_MINIMAL):
        with open(filePath, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=delimiterX, quotechar=quotecharX, quoting=quotingX)
            for rows in rowsList:
                spamwriter.writerow(rows)
                
    @staticmethod
    def read_csv_row_list(filePath):
        csvRowsList = []
        with open(filePath, newline='') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in csvReader:
                csvRowsList.append(row)
        return csvRowsList

class TxtUtils:
    @classmethod
    def write_list_to_file_with_newline(cls, filePath, rowsList, mode='w'):
        PathUtils.check_make_dir_exist(filePath)
        with open(filePath, mode) as f:
            for row in rowsList:
                f.write("%s\n" % row)
                
    @classmethod            
    def write_list_to_txt_file(cls, filePath, rowsList, mode='w'):
        PathUtils.check_make_dir_exist(filePath)
        with open(filePath, mode, newline='') as f:
            for row in rowsList:
                f.write("%s" % row)
                
    @classmethod
    def remove_first_line(cls, filePath):
        rowList = cls.read_txt_rows_list_with_newline(filePath)
        rowList = list(rowList)
        cls.write_list_to_txt_file(filePath, rowList[1:])
    
    @classmethod
    def read_first_line(cls, filePath):
        rowList = []
        with open(filePath, newline='') as f:
            rowList = f.read().splitlines()
            rowList = (x for x in rowList if x.strip())
            rowList = list(rowList)
        return rowList[0] if len(rowList) > 0 else ""
    
    @classmethod
    def read_string_from_txt(cls, filePath):
        with open(filePath, newline='') as f:
            return f.read()
              
    @classmethod
    def read_txt_rows_list(cls, filePath):
        rowList = []
        with open(filePath, newline='') as f:
            rowList = f.read().splitlines()
            rowList = (x for x in rowList if x.strip())
        return list(rowList)
        
    @classmethod
    def read_txt_rows_list_with_newline(cls, filePath):
        rowList = []
        with open(filePath, newline='') as f:
            rowList = f.readlines()
            rowList = (x for x in rowList if x.strip())
        return list(rowList)
        
    @classmethod
    def replace_variables(cls, file_template, file_destination, dict):
        new_lines = []
        for line in cls.read_txt_rows_list_with_newline(file_template):
            for key,val in dict.items():
                line = line.replace(key, val)
            new_lines.append(line)
        cls.write_list_to_txt_file(file_destination, new_lines)
        
class ConfigUtils:
    @staticmethod
    def set(filePath, section, key, value):
        lines = []
        new_lines = []
        sec_expected = False
        key_expected = False
        set_ready    = False
        with open(filePath, 'r', newline='') as f:
            lines = f.readlines()
            
        for index, line in enumerate(lines):
            is_section = "[" in line.strip().lower()
            if(is_section and section.lower() in line.strip().lower()):
                sec_expected = True
                new_lines.append(line)
                continue
            if(sec_expected and key.lower() in line.lower()):
                key_expected = True
                line = "{0}={1}\r\n".format(key, value)
                new_lines.append(line)
                continue
            if(is_section and sec_expected and not key_expected):
                new_lines.append("{0}={1}\r\n".format(key, value))
                sec_expected = False
                key_expected = True
            new_lines.append(line)
               
        with open(filePath, 'w', newline='') as f:
            f.writelines(new_lines)
