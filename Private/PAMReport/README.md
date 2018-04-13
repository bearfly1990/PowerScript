### PAMReport
原来的报表是直接在PamPilot直接生成，以txt格式为主，最初并没有很好的设计，不够强大和友好。\
PAMReport是对这一块的补充，Adapter组负责数据的迁移和不同数据库之间的兼容。\
DataModel组负责重新设计数据结构，基于Hadoop,使用impla进行分析查询。\
对于报表，使用Pentaho报表工具重新进行设计，并发布在BAServer(Web Portal)上,客户可以直接查看丰富的分析报表。\
我在Publisher进入尾声时期，有空闲时间便做一些辅助性的测试工作，也做了一些小工具来帮忙测试。

### To-Do List
* [x] [Check Report Generated](https://github.com/bearfly1990/PowerScript/blob/master/Private/PAMReport/MartCheckInPentaho.md)
* [x] [对比不同数据库](https://github.com/bearfly1990/PowerScript/blob/master/Java/Scripts/PAMDataCompare/PAMDataCompare.md)
* [x] [对比相同结构数据库](https://github.com/bearfly1990/PowerScript/blob/master/Java/Scripts/DBCompare/DBCompare.md)
* [x] Compare report between PAM and Pentaho Server
