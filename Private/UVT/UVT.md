## UVT
**UVT** stands for **Unit Value Trade**, 主要用来根据一定的设定和业务逻辑计算不同的Unit的值。
目前我初步接触到的是数据导入的功能。数据源文件为csv文件，用户根据xls文件里的标准准备好数据。
导入程序会验证csv文件中的格式与数据是否正确，是否满足业务上数据的关联需求，验证能否通过，这些都是要测试的。
### 数据导入
以最近测的US为例，该US做的是Unit Value File Settings的导入。针对UVFile,原先系统中只有单个的设置，
不能满足灵活的设置需求，所以新添加了在Grid中存放多条设定，原先的单条设置保持不变。
#### Unit Value File Settings Import
在UVT根目录下，会有一个固定名字的exe导入程序,e.g. UVFSI.exe。
在Data目录下，会有一个UVFSI.xls文档，记录了导入所需要的格式，和一些限定条件。
用户（测试）首先要把xls文档中sheet1的csv格式取出来，构建一个同名的csv文件（UVFSI.csv）
当数据准备好之后，就可以直接单击根目录下的UVFSI.exe，这样就能直接执行导入的操作。
而导入完成后（不论失败或者成功），在xls同目录下，会生成一个UVFSI.op文档。记录导入的状态。
