import sys
sys.path.insert(0, r"\\nj.pfs.net\departments\Development\Team Engineering\xiche\pythonlib")
import os
import time
import datetime
from cmutils.cmutils_io import TxtUtils
filename = r'C:\Users\Public\Documents\ImportResult.log'
# file = open(filename)
# if os.path.exists(filename):
    # props   = os.stat(filename)
    # current = last =  props.st_mtime
    # print("current:", time.ctime(current), "/last:", time.ctime(last))
current = last = -1
rows_current = rows_last = 0
while 1:
    # props   = os.stat(filename)
    # current = props.st_mtime
    if os.path.exists(filename):
        props = os.stat(filename)
        current = props.st_mtime
        
        print(datetime.datetime.now(),":", time.ctime(current))
        if current > last:
            last = current
            rows_current = TxtUtils.read_txt_rows(filename)
            rows_added = rows_current - rows_last
            rows_last = rows_current
            print("{} : File is updated, {} rows are added.".format(datetime.datetime.now(), rows_added))
            os.system("echo {}:File({}) is updated, {} rows are added. >> file_monitor.log".format(datetime.datetime.now(), filename, rows_added))
    else:
        print("file ({}) is not exist".format(filename))
        rows_current = rows_last = 0
    time.sleep(1)
