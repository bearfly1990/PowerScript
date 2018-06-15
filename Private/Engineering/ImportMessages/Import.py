#/usr/bin/python3
"""
author: xiche
create at: 04/09/2018
description:
    The progress to test the benchmark of import json messages
Change log:
Date        Author      Version    Description
04/09/2018  xiche       1.0        Set up this script
04/17/2018  xiche       1.0.1      Add the test result 'True/False' in 'TestResult.csv'
04/19/2018  xiche       1.0.2      Add function to get the date in the message and write to 'TestResult.csv'
05/22/2018  xiche       1.0.3      Separate config to different folder e.g. configs/PR1XPFIMORT01 configs/PR1XPFIAPP01
05/05/2018  xiche       1.0.4      Add CPU Memory Monitor
"""
import os
import glob
import configparser
import pymssql
import cx_Oracle
import time
import datetime
import csv
import shutil
import win32wnet
import subprocess
import re
import traceback
import queue as Queue
from threading import Thread
from lib.cmutils_log import Logger
from lib.cmutils_io import ConfigUtils
from lib.cmutils_monitor import CPUInfo, MemoryInfo
# import winreg
# import ctypes
# from ConfigParser import SafeConfigParser

# from subprocess import call
# config = configparser.ConfigParser()
# config = configParser.SafeConfigParser()
CONFIG_SPACE    = r"xxx\configs"
COMPUTER_NAME   = os.environ['COMPUTERNAME']

config      = configparser.RawConfigParser(strict=False)
config_db   = configparser.RawConfigParser(strict=False)
# RawConfigParser

config.read('%s\\%s\\Import.ini' % (CONFIG_SPACE,COMPUTER_NAME))
def getTestResultLevel(x):
    return{
        'DIR':1,
        'FILE':2   
    }.get(x, 3)
    
def getCheckSql(x):
    return{
        '1':True,
        '0':False   
    }.get(x, False)
    
CPU_INFO = CPUInfo()
MEM_INFO = MemoryInfo()
TEST_ENDED = Queue.Queue()
#TEST_ENDED.put(False)
'''
class Registry(object):
    def __init__(self, key_location, key_path):
        self.reg_key = winreg.OpenKey(key_location, key_path, 0, winreg.KEY_ALL_ACCESS)

    def set_key(self, name, value):
        try:
            _, reg_type = winreg.QueryValueEx(self.reg_key, name)
        except WindowsError:
            # If the value does not exists yet, we (guess) use a string as the
            # reg_type
            reg_type = winreg.REG_SZ
        winreg.SetValueEx(self.reg_key, name, 0, reg_type, value)

    def delete_key(self, name):
        try:
            winreg.DeleteValue(self.reg_key, name)
        except WindowsError:
            # Ignores if the key value doesn't exists
            pass
'''
TIME_IMPORT_START = datetime.datetime.now()
DEVMODE  = config['DevSetting']['Mode']

DRIVER_L  = config['DriverMapping']['L']
DRIVER_M  = config['DriverMapping']['M']

# log
LOG_LEVEL = config['LogConfig']['Level']
LOG_FORMAT= config['LogConfig']['Format_Console']
LOG_FORMAT_FILE = config['LogConfig']['Format_File']
LOGFILE  = config['LogConfig']['LogFile'].format(TIME_IMPORT_START)
LOGDIR   = config['LogConfig']['LogDir'].format(TIME_IMPORT_START)

# Environment
KETTLE_HOME     = "KETTLE_HOME"
JAVA_HOME       = "JAVA_HOME"

PATH            = os.environ["PATH"]
if(config.has_option('EnvVar', 'JAVA_HOME') and config['EnvVar']['JAVA_HOME'].strip()):
    os.environ["JAVA_HOME"]     = config['EnvVar']['JAVA_HOME']
JAVA_HOME                   = os.environ["JAVA_HOME"]

if(config.has_option('EnvVar', 'KETTLE_HOME') and config['EnvVar']['KETTLE_HOME'].strip()):
    os.environ["KETTLE_HOME"]   = config['EnvVar']['KETTLE_HOME'].format(COMPUTER_NAME)
KETTLE_HOME                 = os.environ["KETTLE_HOME"]
KETTLE_HOME                 = KETTLE_HOME.format(COMPUTER_NAME)

# reg = Registry(winreg.HKEY_LOCAL_MACHINE,r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')
# reg.set_key('KETTLE_HOME',KETTLE_HOME)

# os.putenv("JAVA_HOME", os.environ["JAVA_HOME"])
# os.putenv("KETTLE_HOME", os.environ["KETTLE_HOME"])
LOG4J_PATH                  = config['EnvVar']['LOG4J_PATH']
LOG4J_PATH                  = LOG4J_PATH.format(COMPUTER_NAME)
STTAPPMANAGER               = config['EnvVar']['STTAPPMANAGER']
MSG_TYPE_FLOW_MAPPING       = config['EnvVar']['MSG_TYPE_FLOW_MAPPING']
MSG_TYPE_FLOW_MAPPING       = MSG_TYPE_FLOW_MAPPING.format(COMPUTER_NAME)

PAM_CORE                    = config['EnvVar']['PAM_CORE']
PFS_ROOT                    = config['EnvVar']['PFS_ROOT']
PFS_ROOT                    = PFS_ROOT.format(COMPUTER_NAME)

MSG_TYPE_FLOW_MAPPING_TO    = "{}\MsgTypeFlowMapping.txt".format(r'L:\PAM\Wsys\PDI_Transforms' if 'none' in PFS_ROOT.lower() else PFS_ROOT)#config['EnvVar']['MSG_TYPE_FLOW_MAPPING_TO']
IMPORT_LIST                 = config['Files']['IMPORT_LIST'].format(COMPUTER_NAME)
TEST_RESULT                 = config['Files']['TEST_RESULT'].format(TIME_IMPORT_START)
TEST_MONITOR                = config['Files']['TEST_MONITOR'].format(TIME_IMPORT_START)
IMPORT_RESULT_LOG           = config['Files']['IMPORT_RESULT_LOG']
IMPORT_RESULT_LOG_BK        = config['Files']['IMPORT_RESULT_LOG_BK'].format(TIME_IMPORT_START)
TEST_RESULT_LEVEL           = getTestResultLevel(config['TestResult']['Level'])
CHECK_SQL                   = getCheckSql(config['TestResult']['CheckSql'])
# KETTLE_SETTINS              = config['KettleSetting']
# EXPECTED_STT_MAX_ACTIVE_CONNECTIONS = config['KettleSetting']['STT_MAX_ACTIVE_CONNECTIONS']
KETTLE_SETTINGS             = []
for (each_key, each_val) in config.items('KettleSetting'):
    KETTLE_SETTINGS.append(each_val)
    
MESSAGE_TYPE_FLOW_MAPPINGS  = []
for (each_key, each_val) in config.items('MessageTypeFlowMapping'):
    MESSAGE_TYPE_FLOW_MAPPINGS.append(each_val)

CMD_RUN_MANAGER = config['CMD']['StartServer']

CMD_RUN_IMPORT = config['CMD']['RunImport']

if not os.path.exists(LOGDIR):
    os.makedirs(LOGDIR)
'''Config logging'''
# logging.basicConfig(
    # level=LOG_LEVEL,
    # #format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    # format=LOG_FORMAT,
    # handlers=[
        # logging.FileHandler("{0}/{1}".format(LOGDIR,LOGFILE)),
        # logging.StreamHandler()
# ])
format_file_str = "%(asctime)s [%(levelname)-5.5s] %(message)s"
format_console_str = "%(log_color)s%(asctime)s [%(levelname)-5.5s] %(message)s"
logfile_path_str = "{0}/{1}".format(LOGDIR,LOGFILE)
logging = Logger(level=LOG_LEVEL,format_file=format_file_str, format_console=format_console_str, logfile_path = logfile_path_str).logger

def checkDriverMapping():
    if(DEVMODE == '0'):
        subprocess.call("net use l: /delete /y", shell=True)
        subprocess.call("net use m: /delete /y", shell=True)
        os.system("net use l: {}".format(DRIVER_L))
        os.system("net use m: {}".format(DRIVER_M))
        logging.info("Driver L: Deleted and Mapped:" +  DRIVER_L)
        logging.info("Driver M: Deleted and Mapped:" +  DRIVER_M)
    else:
        try:
            logging.info("Driver L: Mapped:" +  win32wnet.WNetGetUniversalName("L:", 1))
            logging.info("Driver M: Mapped:" +  win32wnet.WNetGetUniversalName("M:", 1))
        except:
            logging.warn("Driver L: and M: Is Not Mapped")
            os.system("net use l: {}".format(DRIVER_L))
            os.system("net use m: {}".format(DRIVER_M))
checkDriverMapping()
config_db.read(config['DBInfo']['Path'])

dbInfo = config_db['DB']
CONN = None
DB_TYPE = "Sqlserver"

try:             
    CONN = cx_Oracle.connect('{}/{}@{}'.format(dbInfo['userid'], dbInfo['password'], config['DBInfo']['oracle_tnsname']))
    DB_TYPE = "Oracle"
    logging.warn("Oracle connected{}/{}@{}".format(dbInfo['userid'], dbInfo['password'], config['DBInfo']['oracle_tnsname']))
except Exception as e1:
    try:
        # CONN = cx_Oracle.connect('pruus22/pruus22@pfidb12c.world')
        CONN = pymssql.connect(dbInfo['sqlnet'], dbInfo['userid'], dbInfo['password'], dbInfo['source'])
    except Exception as e2:
        logging.error(traceback.format_exc())
        logging.error("Connect to Database Error")
        exit()
    

def timeout(second):
    os.system('timeout '+str(second))
def getDateInMessage(filePath): 
    dateStr = ""
    with open(filePath, "rt") as f:
        for line in f:
            dateStr = re.search("([0-9]{4}[0-9]{2}[0-9]{2})", line).group(0)
            break
    return dateStr
def getLastNameFromFullPath(fullPath):
    lastIndex = fullPath.rfind('\\')
    if(lastIndex == -1):
        lastIndex = fullPath.rfind('/')
    return fullPath[lastIndex:]
'''c:\\aa\\bb\\cc\\file.txt => c:\\aa\\bb'''
def getLastDirPath(fullPath):
    lastIndex = fullPath.rfind('\\')
    lastIndex = fullPath.rfind('\\', 0, lastIndex - 1)
    if(lastIndex == -1):
        lastIndex = fullPath.rfind('/')
        lastIndex = fullPath.rfind('/', 0, lastIndex - 1)
    return fullPath[0:lastIndex]

def load_properties(filepath, sep='=', comment_char='#'):
    '''
    Read the file passed as parameter as a properties file.
    '''
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"') 
                props[key] = value 
    return props

def checkUser():
    existFlag = False
    cursor = CONN.cursor()

    cursor.execute("select xxx from pmuser where xxx = '{}'".format(os.getlogin()))
    # print("-----")
    # for row in cursor:
        # existFlag = True
        # print('row = %r' % (row,))
    # domain = os.environ['userdnsdomain']
    if cursor.fetchone()[0] >= 1:
        existFlag = True;
        
    if(existFlag):
        try:
            logging.info("DB:Server=%s,userid=%s,password=%s,database=%s",str(dbInfo['sqlnet']), str(dbInfo['userid']), str(dbInfo['password']), str(dbInfo['source']))
        except:
            logging.info("DB:Server=%s,userid=%s,password=%s,database=%s",str(dbInfo['sqlnet']), str(dbInfo['userid']), str(dbInfo['password']), str(dbInfo['schema']))
        logging.info("OK! - User {} is in the DB".format(os.getlogin()))
    else:
        logging.error("Please confirm your login name is in the DB!")
        exit()

def checkImportResultLog(importFilePath):
    lins=[]
    recordsRead = -1
    loaded = -1
    processed = -1
    failedToLoad = -1
    failedToProcess = -1
    try:
        with open(IMPORT_RESULT_LOG) as f:
            lines = f.read().splitlines();
        for line in lines:
            line = line.strip()
            if("Records Read:" in line):
                recordsRead = line.split(":")[1].strip()
            if("Loaded:" in line):
                loaded = line.split(":")[1].strip()
            if("Processed:" in line):
                processed = line.split(":")[1].strip()
            if("Failed to Load:" in line):
                failedToLoad = line.split(":")[1].strip()
            if("Failed to Process:" in line):
                failedToProcess = line.split(":")[1].strip()
        logging.debug("Records Read:%s",recordsRead)  
        logging.debug("Loaded:%s",loaded)
        logging.debug("Processed:%s",processed)
        logging.debug("Failed to Load:%s",failedToLoad)
        logging.debug("Failed to Process:%s",failedToProcess)
        logging.info("Read:%s = Loaded:%s = Processed:%s | Failed Load=%s, Failed Process=%s",recordsRead,loaded,processed,failedToLoad,failedToProcess)
        if(int(failedToLoad) != 0):
            logging.error("Failed to Load:%s",failedToLoad)
        if(int(failedToProcess) != 0):
            logging.error("Failed to Process:%s",failedToProcess)
        if(int(loaded) <= 0 ):
            logging.error("No successed Loaded")
        if not os.path.exists(IMPORT_RESULT_LOG_BK):
            os.makedirs(IMPORT_RESULT_LOG_BK)
        moveToPath = IMPORT_RESULT_LOG_BK + getLastNameFromFullPath(importFilePath)+".ImportResult.log"
        if(os.path.exists(moveToPath)):
            shutil.move(IMPORT_RESULT_LOG, moveToPath+"_2.log")
        else:
            shutil.move(IMPORT_RESULT_LOG, moveToPath)
    except FileNotFoundError:
        logging.error("%s IS NOT EXISTED, PLEASE HAVE A CHECK", IMPORT_RESULT_LOG)
    return failedToProcess
    
def checkEnvVar(VarKey):
    try:
        logging.info(VarKey +"="+os.environ[VarKey])
    except KeyError:
        logging.error("THERE IS NO "+VarKey+" DEFINED")
    # finally:
        # print("finally")
        
def checkJAVAHOME():
    if(not JAVA_HOME.strip()):
        logging.error("Please set JAVA_HOME")
        exit()
    logging.info("JAVA_HOME={}".format(JAVA_HOME))
    # finally:
        # print("finally")
          
def checkKettleSetting():
    logging.info('#Kettle Settings:#')
    logging.info('KETTLE_HOME='+KETTLE_HOME)
    kettleProps = KETTLE_HOME+"/.kettle/kettle.properties"
    try:
        props   = load_properties(kettleProps)
    except FileNotFoundError:
        logging.error("FILE <"+kettleProps+"> NOT FOUND")
        exit()
    for key in KETTLE_SETTINGS:
        logging.info ('%s=' % key + props[key])

def checkPAMCore():
    _pam_core = PAM_CORE
    if(_pam_core.lower() in PATH.lower()):
        pass
    else:
        logging.error(PAM_CORE+" is not defined in PATH")
        exit()
    
def checkLog4j():
    logging.info(LOG4J_PATH)
    
def checkMsgTypeFlowMapping():
    logging.info("#MsgTypeFlowMapping Settings:#")
    if(not "none" in PFS_ROOT.lower()):
        M_PAM_INI             = config['EnvVar']['M_PAM_INI']
        ConfigUtils.set(M_PAM_INI, "Securities", "PFS_ROOT", PFS_ROOT)
    with open(MSG_TYPE_FLOW_MAPPING_TO, "rt") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                for msg in MESSAGE_TYPE_FLOW_MAPPINGS:
                    if( msg in line):
                        logging.info(line)


def readConfigFile(filePath='ImportConfig.txt'):
    with open(filePath) as f:
        content = f.read().splitlines();
    return [x.strip() for x in content if (not "#" in x and x.strip())]
    
def countInvalidRowsInFile(filePath):
    count = 0
    try:
        with open(filePath) as f:
            content = f.read().splitlines();
        for line in content:
            if(line.strip()):
                count = count + 1
    except FileNotFoundError:
        logging.error("FILE %s NOT FOUND!", filePath)
    return count
    
def initJavaServer():
    _cmd_run_manager = ""
    if(DEVMODE == '0'):
        _cmd_run_manager = CMD_RUN_MANAGER.format(JAVA_HOME, LOG4J_PATH, KETTLE_HOME, STTAPPMANAGER)
        logging.info("CMD_RUN_MANAGER="+_cmd_run_manager)
        os.system(_cmd_run_manager)
        timeout(360)
    
def getSqlStr(dir):
    checkSqlFile1 = dir+"\\checkResult.sql"
    checkSqlFile2 = getLastDirPath(checkSqlFile1)+"\\checkResult.sql"
    checkSqlFile3 = getLastDirPath(checkSqlFile2)+"\\checkResult.sql"
    sqlStr = "select -1"
    try:
        with open(checkSqlFile1) as f:
            # content = f.read().splitlines();
            sqlStr  = f.read().replace('\n', '')
    except FileNotFoundError:
        try:
            with open(checkSqlFile2) as f:
                # content = f.read().splitlines();
                # sqlStr = content[0]
                sqlStr  = f.read().replace('\n', '')
        except FileNotFoundError:
            try:
                with open(checkSqlFile3) as f:
                    # content = f.read().splitlines();
                    # sqlStr = content[0]
                    sqlStr  = f.read().replace('\n', '')
            except FileNotFoundError:
                logging.error("File %s is not found!", checkSqlFile1)
                logging.error("File %s is not found!", checkSqlFile2)
                logging.error("File %s is not found!", checkSqlFile3)
    return sqlStr
    
def getCurrentRowsInDB(dir):
    if CHECK_SQL:
        pass
    else:
        return 0
    resultRows = 0
    cursor = CONN.cursor()
    sqlStr = getSqlStr(dir)
    try:
        cursor.execute(sqlStr)
        for row in cursor:
            resultRows = row[0]
            break
    except Exception:
        logging.error("SQL ERROR:%s", sqlStr)
    return resultRows
    
def checkImportResultInDB(dir, rowsBefore, rowsAfter, expectedRows):
    if CHECK_SQL:
        pass
    else:
        return 0
    resultRows = rowsAfter - rowsBefore
    rowsAreMatched = (resultRows == expectedRows)
    logging.info("Rows DB Added:%s = %s - %s", resultRows, rowsAfter, rowsBefore)
    logging.info("Rows Expected:%s", expectedRows)
    
    if(not rowsAreMatched or expectedRows == 0):
        logging.error("Rows not matched!")
        logging.error("Failed Import %s", dir)
    else:
        logging.info("Successed Import %s", dir)
    return rowsAreMatched
        
def writeResult(pathStr, rows, time, messageStr, isDIR, rowsAreMatched_DB, rowsAreMatched_LOG, failedToProcess):
    writeFlag = False
    TEST_RESULT_LEVEL == 1 # DIR = 1 FILE = 2
    # if (isDIR and ".txt" in pathStr):
        # writeFlag = False
    if(TEST_RESULT_LEVEL == 1 and isDIR):
        writeFlag = True
    if(TEST_RESULT_LEVEL == 2):
        writeFlag = True
        
    if(writeFlag):
        timeStr = "{:.2f}".format(time)
        timeStrMinutes = "{:.2f}".format(time/60)
        timAvgStr = "-1"
        if(rows > 0):
            timAvgStr = "{:.4f}".format(time/rows)
        '''    
            with open(TEST_RESULT, 'a') as writer:
                writer.write("%s :\n\ttotal:%s avg:%s rows:%s\n" % (pathStr,timeStr, timAvgStr, rows))
        '''
        myData = [pathStr,rows, timeStr, timeStrMinutes,timAvgStr, messageStr, rowsAreMatched_DB,rowsAreMatched_LOG, failedToProcess]
        myFile = open(TEST_RESULT, 'a', newline='')  
        with myFile:  
            writer = csv.writer(myFile)
            writer.writerow(myData)    
        
def initTestResult():
    myData = ['path', 'rows', 'timeused(s)','timeused(m)','avgtime', 'messageDate', 'rowsAreMatchedInDB', 'rowsAreMatchedByLog', 'failedToProcess']
    # csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE)
    # myFile = open(TEST_RESULT, 'w')  
    # with myFile:  
        # writer = csv.writer(myFile, dialect='myDialect')
   
    myFile = open(TEST_RESULT, 'w', newline='')  
    with myFile:  
        writer = csv.writer(myFile)
        writer.writerow(myData) 
        
def runImport():
    initTestResult()
    _cmd_run_import = ""
    dirs = readConfigFile(IMPORT_LIST)
    list_of_files = []
    for dir in dirs:
        logging.info("-----START IMPORT-----")
        countRowsDir = 0
        list_of_files = glob.glob(dir+'/*.txt') 
        list_of_files.sort()
        rowsInDBBefore_Dir = getCurrentRowsInDB(dir)
        timeStartDir  =  time.time()
        dirTimeBack = 0
        messageDateStr = ''
        failedToProcessDir = 0
        if(len(list_of_files) > 0):
            messageDateStr = getDateInMessage(list_of_files[0])
        rowsAreMatched = False
        for importfile in list_of_files:
            rowsInFile = countInvalidRowsInFile(importfile)
            rowsInDBBefore_File = getCurrentRowsInDB(dir)
            countRowsDir += rowsInFile
            countRowsFile = rowsInFile
            timeStartFile  =  time.time()
            
            _cmd_run_import = CMD_RUN_IMPORT.format(importfile)
            logging.info(_cmd_run_import)
            #Real to call the import
            if(DEVMODE == '0' or DEVMODE == '1'):
                os.system(_cmd_run_import)
            timeEndFile  =  time.time()
            
            periodFile  = timeEndFile - timeStartFile
            periodFileStr = "{:.2f}".format(periodFile)
            logging.info("Finished:"+importfile)
            logging.info("Import Time(s):%s", periodFileStr)
            rowsInDBAfter_File = getCurrentRowsInDB(dir)
            rowsAreMatched = checkImportResultInDB(importfile, rowsInDBBefore_File, rowsInDBAfter_File, rowsInFile)
            # time.sleep(5)
            '''Change the time back because sleep'''
            failedToProcessFile = int(checkImportResultLog(importfile))
            failedToProcessDir  = failedToProcessDir + failedToProcessFile
            writeResult(importfile, rowsInFile, periodFile, messageDateStr, False, rowsAreMatched,failedToProcessFile == 0, failedToProcessFile)
            
        timeEndDir  =  time.time()
        #{:10.4f}
        
        periodDir = timeEndDir - timeStartDir + dirTimeBack
        periodDirStr = "{:.2f}".format(periodDir)
        logging.info("Finished:"+dir)
        logging.info("Import Time(s):%s", periodDirStr)
        
        rowsInDBAfter_Dir = getCurrentRowsInDB(dir)
        
        rowsAreMatched = checkImportResultInDB(dir, rowsInDBBefore_Dir, rowsInDBAfter_Dir, countRowsDir)
        
        logging.info("-----END IMPORT-----")
        writeResult(dir, countRowsDir, periodDir, messageDateStr, True, rowsAreMatched, failedToProcessDir == 0, failedToProcessDir)
        
        if(DEVMODE == '0' or DEVMODE == '1'):
            timeout(5)
            dirTimeBack = dirTimeBack - 5
        
            
def startMonitor():
    monitor_header = ['Time', 'CPU(%)', 'Memory(%)']
    monitor_result = open(TEST_MONITOR, 'w', newline='')  
    with monitor_result:  
        writer = csv.writer(monitor_result)
        writer.writerow(monitor_header)
    t = Thread(target=writeMonitor, args=(TEST_ENDED,))
    t.start()
    
def writeMonitor(test_ended):
    monitor_result = open(TEST_MONITOR, 'a', newline='')  
    with monitor_result as f:  
        writer = csv.writer(monitor_result)
        isEnded = False
        while(not isEnded):
            try:
                temp = test_ended.get(False)
                isEnded = True
            except:
                isEnded = False
            monitor_data = ['{:%Y/%m/%d %H:%M:%S}'.format(datetime.datetime.now()), CPU_INFO.user, MEM_INFO.pctused]
            writer.writerow(monitor_data)
            f.flush()
            time.sleep(2)
        
def checkEnvAndSettings():
    pass
    checkUser()
    checkPAMCore()
    checkJAVAHOME()
    checkKettleSetting()
    checkLog4j()
    checkMsgTypeFlowMapping()
    goon = input("ARE THE SETTINGS OK?(Y/N): ")
    if(goon.upper() == "Y"):
        pass
    else:
        logging.warn("PLEASE CHANGE THE SETTINGS FIRST!")
        TEST_ENDED.put(True)
        exit()
def __main__():
    pass
    # checkDriverMapping() have move ahead at line 184
    startMonitor()
    logging.info("-----START TO RUN IMPORT PROCESS!-----")
    logging.info("-----CHECK SETTINGS-----")
    checkEnvAndSettings()
    initJavaServer()
    runImport()
    print("Import Finished!")
    timeout(120)
    TEST_ENDED.put(True)
__main__()
