# Publisher Automation Test Summary
## 1. Automation UI TestSuites
### 1.1 Test Suites
All of these UI test are designed by [Ranorex](https://www.ranorex.com/).
They are stored in the public shared folder, so each VM could visit this.
It's easy to start the test by running the build .exe file.
The codes used in the test is C#, of course you could use Java or other language which Ranorex supported.
- Publisher Designer
- Publisher Manager
- Publisher Portal
- Publisher Delivery
- Publisher TAM(Saas Mode)
- ...

### 1.2 VM(Virtual Machine) Management
There are 3 virtual Machines used for QA UI Automation Test.
Each VM have triggers(Schedulers) to install the Publisher Client and run the test.
The best solution is each Test using its own DB, but for history reason( I'm lazy:laughing:)
Due to the DB related, so the time to trigger the Test Suite is very important.

BTW, The **1st** step to run the test is to restore the DB

* VM-1
DB: TestAuto
  * Publisher Portal (≈25mins)
Actually, Portal only need Web Broswer(IE/FireFox), no mather which VM is both ok.
Due to the web operation, it's very quick to finish, easier to find elemments than desktop App.
  * Publisher Delivery (≈30mins)
This functionality is in Publihser Manager.
We should start [Papercut](http://papercut.codeplex.com/) service before the test. It's the main tools to catch the emails.
Then Test will compare the emails with baseline.

* VM-2
DB: TestE2E
  * Publisher Designer (≈2h)
  That's the main Test for the Publisher Client, it include almost the base operations for users.
Specially, it's trigger by the [TeamCity](http://www.jetbrains.com/teamcity/).
So we have to start the TeamCity Agent Server first.

* VM-3
DB: TestAuto
  * Publisher Manager (≈1h)
Publisher Manager it's smaller thant Designer, the main functionality is to trigger the task and run reports.
To check reports are generated successfully or not.
from 5.4, we also add an **SFTP** Delivery Type, so before run this test case, we should start the tiny SFTP Server.
  * Publisher TAM(Saas Mode)(≈10mins)
TAM = Tenant Management
It's a new features from 5.3, we only concern about the TAM Administrator, so only tiny test cases.

## 2. QA Deployment
Demploy the latest Publisher in the enviroment and restore the DB.
### 2.1 DataBase
In Publisher, there are two type: Sql Server / Oracle Database, and before any new integration, the DB sould be restored to the Base Line(Base DB). Restore scripts(Powershell) in the DB Server, and be called by TeamCity Agent.
* Sql Server
  * There is a Base DB called \*\*\*BaseTrunk, this DB is important and could not be changed unbending. Only the test case will be added or changed, otherwise, we could not change anything in the baseline.
* Oracle
  * Actually, Oracle data is based on the SqlServer, there is also a Oracle base DB, but the data is queried from the SqlServer Base DB by script. Only when the DB strucutre is changed, we could apply the updates. and other Oracle DB are based on the base DB.
### 2.2 Install latest version
After the build on TeamCity, the artifacts(msi installer) are stored in the shared folder. Each enviroment have the scheduler task to copy and install the latest version. they are triggered by the TeamCity step.
