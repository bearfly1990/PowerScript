# AMS
**AMS**(Asset Management Software)是道富位于瑞士的前子公司[**Allocare**](http://www.allocare.com/)的主要产品，为用户提供资产管理的功能。
做为重要的报表模块，系统中已经存在历史比较悠久和丰富的商业报表。
最初介入该项目时，一项主要工作即是将其中的一部分报表汉化，为新加坡客户提供支持。
AMS中的报表主要有两种设计方案，一种为基本active report使用VBScript开发，另一种则使用Crystal Report开发，存在相同报表同时存在两种版本的情况。
两种方案各有千秋，比如使用VBScript结合ChartFX可以绘制出丰富的Charts，制作报表非常灵活。
而Crystal Report作为专业的可视化报表制作工具，制作报表相对便利与快速。
AMS使用SqlServer数据库，内置开发了大量与业务相关的存储过程，而每一张报表都有对应一个上层存储过程作为数据源。
当创建和更改报表时，主要的数据处理逻辑都是写在该存储过程中。
