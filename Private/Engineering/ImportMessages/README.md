# ImportMessages
## Summary
项目需要对Json Messages的导入性能进行测试。
在之前已经尝试把数据导入数据库中，但是没有统一的一个流程，都是通过bat文件加载，而且在过程多发现了许多问题。
在开发解决了一些问题和优化了性能之后，决定再次重新导入，并需要测试导入的效率。
所以我就用python脚本，简单的搭建了环境，方便维护和修改，过程中也遇到了一些问题，也优化了一些细节。
当然，还是有非常多的改进空间，比如更好的结果监控。

## 配置文件(Config File)
[Import.ini](Import.ini)是主要的配置文件，一些重要的依赖条件都在这配置。
```ini
[DevSetting]
;0-Normal 1-Only Import 2-Test
Mode = 0
```
### DevSetting>Mode
主要为了切换不同的运行模式，比如在`Test`模式下，不会真正去执行重要的操作，只是验证监控和log代码是否能正常运行。在'Import' 模式下，便只会执行导入工作，而不会去启动Import Service。等测试稳定的时候，`Normal`将是默认的选项，正常运行。
```ini
[TestResult]
;Level=FILE
Level=DIR
```
### TestResult>Level
这个配置会控制在TestResult文件里的输出结果，如果是`DIR`那么就将只输出文件夹的导入结果。如果是`FILE`，则会把每个文件的导入结果也都输出。

## 主要流程及重要代码
### startImport.bat
### checkSettings
### connect to db
## 特殊库
### configparser
### logging
### pymssql
### csv
### win32wnet

