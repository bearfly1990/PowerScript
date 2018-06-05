import cx_Oracle
import os
# CONN = cx_Oracle.connect('{}/{}@{}'.format(dbInfo['userid'], dbInfo['password'], config['DBInfo']['oracle_tnsname']))
CONN = cx_Oracle.connect('{userid}/{password}@{TNSName}')
existFlag = False
cursor = CONN.cursor()
cursor.execute("select count(*) from pmuser where lower(keycode) = '{}'".format(os.getlogin()))
if cursor.fetchone()[0] >= 1:
    existFlag = True
