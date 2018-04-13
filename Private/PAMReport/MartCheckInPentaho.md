## Mart Check In Pentaho
为了检验数据库里的字段是否都能正常使用，在Web UI上将所有的字段都加入到报表中。然后设计自动化case，使用SoupUI发起Request, 让这些报表定时循环生成。Request使用的是Pentaho BAServer提供的[API](https://help.pentaho.com/Documentation/8.0/Developer_Center/REST_API)。但资料有限，当时我直接用浏览器的debug工具去截取http请求来的到request的样例。
***
There are 19 Marts in impala database, we should check them each time when they are updated.
And we plan to create automated test cases for regression test.
* All columns should be include in the report
  * There are too many columns in some marts, so we seperate them into several reports in one folder
* Trigger such reports and if the marts are ok, the reports should be generated successfully.
* Using SoapUI to request API Service by Pentaho BA Server.
### Sample Steps
1. Create Reports which include all of the columns for each mart
2. Prepare properties files include the report information
3. Create configuration file for init the SoapUI project, include property file information, related test steps...
4. Get Authorization.
5. Delete the generated reports last time.
6. Scheduler all the report.
7. Check the expected reports are generated successfully or not
