# Publisher Summary
## Publisher Designer
### Report Elements
#### Data Source
Publisher support several Data Sources
for example:
- Sql Server
- Oracle
- ODBC
- OLEDB
- ESP (StateSteet Inner DS)

User could define functions to retrieve data from different Data Sources

#### Report Module
Report Module is the base element for creating report in Publisher
- DataTable
- LayoutTable
- Paragraph
- TOC(Table of Content)
- Chart
- NoteHeader/NoteFooter
- ...

#### Designer Report
User could create report by using the already created Modules or define own new elements.
When report is finished, could release it to different areas, you could create any folder as you like.There is a 'default' folder to use.
- Public
- System
- Private

#### Run Report
User could run released reports here, user could test the report could run successfully or not. so that could comfirm the service could run it too.

#### User Defined Function
User could define own functions to handle the data

#### Stylesheet
Report could be run with different defined stylesheet. **e.g. font/color/height/width...**

### Functional Buttons
#### Permission
There are diffrent roles and permissions in publisher
- Administrator
- Release Manager
- Data Source Manager
- Publisher User
- User Defined Rolles

#### Parameters
User could define different parameters give them default values, report could import them and override.

#### Data Source Permission
User should give the data source permission to the report, then the report could run.

#### ...

## Publisher Manager
### Task
User could define Task to run the report, there are 3 types:
- TimeTrigger
- DBTrigger
- FileTrigger

### External Document
User could run external document as report, e.g. txt file

### Repository
The reports are stored into repository after running from task.
There are also **3** areas(system/public/private) and distinguash report and package

### Delivery
User could define Subscriber and Subscriber Group to receive report by 3 ways:
- Email
- File System(Folder)
- SFTP

### Overview
#### Monitor
User could see the running report status

#### Task Overview
User could see the task status - running/finished/error

#### Logs
- Application Service
- Publishing Service
- Delivery Service
- Web API

## Publisher Portal
Portal is web interactive platform, should be set up in IIS.

### Templates
Templates are the reports released to Public/Private

### Reports
Template could be create to report, then schedule/run this report

### Scheduler
User could see  the schedulers here. there are several scheduler types:
- Once
- Hourly
- Daily
- Monthy

### Repository
Similar as in Publisher Manager, reports runned will be stored here.

### Monitor
We could see succeed/failed reports.

## Web API
Publisher support api to control the service.
