# Publisher Summary
## 1. Publisher Designer
### 1.1 Report Elements
#### 1.1.1 Data Source
Publisher support several Data Sources
for example:
- Sql Server
- Oracle
- ODBC
- OLEDB
- ESP (StateSteet Inner DS)

User could define functions to retrieve data from different Data Sources
#### 1.1.2 Report Module
Report Module is the base element for creating report in Publisher
- DataTable
- LayoutTable
- Paragraph
- TOC(Table of Content)
- Chart
- NoteHeader/NoteFooter
- ...
#### 1.1.3 Designer Report
User could create report by using the already created Modules or define own new elements.
When report is finished, could release it to different areas, you could create any folder as you like.There is a 'default' folder to use.
- Public
- System
- Private
#### 1.1.4 Run Report
User could run released reports here, user could test the report could run successfully or not. so that could comfirm the service could run it too.
#### 1.1.5 User Defined Function
User could define own functions to handle the data
#### 1.1.6 Stylesheet
Report could be run with different defined stylesheet. **e.g. font/color/height/width...**

### 1.2 Functional Buttons
#### 1.2.1 Permission
There are diffrent roles and permissions in publisher
- Administrator
- Release Manager
- Data Source Manager
- Publisher User
- User Defined Rolles
#### 1.2.2 Parameters
User could define different parameters give them default values, report could import them and override.
#### 1.2.3 Data Source Permission
User should give the data source permission to the report, then the report could run.
#### 1.2.4 ...
## 2. Publisher Manager
### 2.1 Task
User could define Task to run the report, there are 3 types:
- TimeTrigger
- DBTrigger
- FileTrigger
### 2.2 External Document
User could run external document as report, e.g. txt file
### 2.3 Repository
The reports are stored into repository after running from task.
There are also **3** areas(system/public/private) and distinguash report and package
### 2.4 Delivery
User could define Subscriber and Subscriber Group to receive report by 3 ways:
- Email
- File System(Folder)
- SFTP
### 2.5 Overview
#### 2.5.1 Monitor
User could see the running report status
##### 2.5.2 Task Overview
User could see the task status - running/finished/error
##### 2.5.3 Logs
- Application Service
- Publishing Service
- Delivery Service
- Web API
## 3. Publisher Portal
Portal is web interactive platform, should be set up in IIS.
### 3.1 Templates
Templates are the reports released to Public/Private
### 3.2 Reports
Template could be create to report, then schedule/run this report
### 3.3 Scheduler
User could see  the schedulers here. there are several scheduler types:
- Once
- Hourly
- Daily
- Monthy
### 3.4 Repository
Similar as in Publisher Manager, reports runned will be stored here.
### 3.5 Monitor
We could see succeed/failed reports.

## 4. Web API
Publisher support api to control the service.