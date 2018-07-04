# ImportMessages
## Summary
项目需要对Json Messages的导入性能进行测试。
在之前已经尝试把数据导入数据库中，但是没有统一的一个流程，都是通过bat文件加载，没有相对自动化的流程。
在开发解决了一些问题和优化了性能之后，决定再次重新导入，并需要测试导入的效率。
所以我就用python脚本，简单的搭建了环境，方便维护和修改，过程中也遇到了一些问题，也优化了一些细节。
当然，还是有非常多的改进空间，比如更好的结果监控。

## 配置文件(Config File)
[Import.ini](Import.ini)是主要的配置文件，一些重要的依赖条件都在这配置。

### DevSetting->Mode
```ini
[DevSetting]
;0-Normal 1-Only Import 2-Test
Mode = 0
```
主要为了切换不同的运行模式，比如在`Test`模式下，不会真正去执行重要的操作，只是验证check和log代码是否能正常运行。在`Import` 模式下，便只会执行导入工作，而不会去启动Import Service。等测试稳定的时候，`Normal`将是默认的选项，正常运行所有功能，逻辑开关已经写在相关代码上。

### TestResult->Level
```ini
[TestResult]
;Level=FILE
Level=DIR
```
这个配置会控制在TestResult文件里的输出结果，如果是`DIR`那么就将只输出文件夹的导入结果。如果是`FILE`，则会把每个文件的导入结果也都输出。
### DBInfo
```ini
[DBInfo]
Path=xxx.ini
oracle_tnsname = xxxxx
```
数据库配置信息。最终数据都是导入到数据库中，而有对应的sql去查询该message是否是真正全部成功导入到数据库中了。
06/07/2018 updated: 数据库信息从xxx.ini里读取，并支持oracle，不过需要在这配置好对应的Service.
### Files
```ini
[Files]
IMPORT_LIST = ImportList.txt
IMPORT_RESULT_LOG = xxx\ImportResult.log
IMPORT_RESULT_LOG_BK =./logs/{:%Y%m%d_%H%M%S}/ImportResultLogBK
TEST_RESULT = ./logs/{:%Y%m%d_%H%M%S}/TestResult.csv
TEST_MONITOR = ./logs/{:%Y%m%d_%H%M%S}/Monitor.csv
```
`IMPORT_LIST`配置了导入配置文件，在该文件中，逐行为需要导入message所在的文件夹，遍历其下的`txt`文件，按文件名排序依次执行导入操作

`TEST_MONITOR` 增加了对内存和CPU的监控，结果写入固定的文件
### Other Configs...
略...
## 主要流程及重要代码
接下来，主要从代码执行逻辑上来介绍，基本上过一遍就能完全理解，还是相对简单的。
### startImport.bat
这个批处理文件是程序的入口，将测试的`workspace`映射到`h`盘，python的执行环境也在其中。
```bat
@echo off
net use h: /delete /y
net use h: "xxx"`
IF EXIST "\\xxx\Python36" SET PATH=%PATH%;"\\xxx\Python36"
pushd %~dp0
python Import.py
pause
```
### checkSettings
导入前的准备工作就是验证下环境是不是期望的，把一些配置文件加载到对应的folder下面。
```python
def checkEnvAndSettings():
    checkUser()
    checkPAMCore()
    checkJAVAHOME()
    checkKettleSetting()
    checkLog4j()
    checkMsgTypeFlowMapping()
```
* checkUser()
    * 工作中的系统需要当前执行导入命令的windows账户存在在DB中，不然import会直接失败
* checkPAMCore()
    * 检测系统环境变量Path中是否配置了需要的路径
* checkJAVAHOME()
    * 设置JavaHome变量，但其实没有实际改变系统的变量，可以通过注册表改变，但需要admin权限运行，而且要用到`winreg`模块
* checkKettleSetting()
    * 最后在执行java时当成参数导入进去，主要配置Algo等与实例性能有关的配置
* checkLog4j()
    * Log4J日志的配置，打开与关闭性能差很多
* checkMsgTypeFlowMapping()
    * 业务和性能相关的配置
### Init JavaServer
导入message之前，需要先把Message Service启动完成，大概需要4分钟时间，是独立的线程。
```python
 _cmd_run_manager = CMD_RUN_MANAGER.format(JAVA_HOME, LOG4J_PATH, KETTLE_HOME, STTAPPMANAGER)
logging.info("CMD_RUN_MANAGER="+_cmd_run_manager)
os.system(_cmd_run_manager)
timeout(600)
```
### runImport
最主要的流程就在`runImport`方法中,下面就简单说下一些主要的方法，其它可以直接参考代码[Import.py](Import.py)
#### readConfigFile
这里其实就是把需要导message的文件夹读取进来。
```python
dirs = readConfigFile(IMPORT_LIST)
```
#### list_of_files
遍历文件夹中的`.txt`文件并排序，这里是写死的。
```python
list_of_files = glob.glob(dir+'/*.txt') 
list_of_files.sort()
```
#### count rows
`getCurrentRowsInDB`函数便是去取该目录下的sql文件中的sql语句，取得导入前后的数据，作差值。\
同时也会查询实际上的message条数，与刚作的差值做比较，期望值是一样的，否则说明有问题。
```python
def getCurrentRowsInDB(dir):
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
```
#### write to csv file
同时，对于结果，会记录在csv文件中
```python
writeResult(importfile, rowsInFile, periodFile, False)
```
### check and backup import result log
Message Service会生成导入的结果log，里面也有导入的情况，但实际上并不是很准确，有时会出现其实数据库里没插入，但log里显示都完成的情况。所以对数据库的查询比较是必要的。
```python
checkImportResultLog(importfile)
```
#### dirTimeBack
对了，为了给点缓冲的时间，我sleep了5秒，所以在计算最后时间的时候需要减掉。
