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
sqlnet=xxx
userid=xxx
password=xxx
schema=xxx
```
数据库配置信息。最终数据都是导入到数据库中，而有对应的sql去查询该message是否是真正全部成功导入到数据库中了。
### Files
```ini
[Files]
IMPORT_LIST = ImportList.txt
IMPORT_RESULT_LOG = xxx\ImportResult.log
IMPORT_RESULT_LOG_BK =./logs/{:%Y%m%d_%H%M%S}/ImportResultLogBK
TEST_RESULT = ./logs/{:%Y%m%d_%H%M%S}/TestResult.csv
```
`IMPORT_LIST`配置了导入配置文件，在该文件中，逐行为需要导入message所在的文件夹，遍历其下的`txt`文件，按文件名排序依次执行导入操作
### Other Configs...
略...
## 主要流程及重要代码
接下来，主要从代码执行逻辑上来介绍，基本上过一遍就能完全理解，还是相对简单的。
### startImport.bat
### checkSettings
### connect to db
## 特殊库
### configparser
### logging
### pymssql
### csv
### win32wnet

