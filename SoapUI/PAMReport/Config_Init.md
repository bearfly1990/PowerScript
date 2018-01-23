```Groovy
import groovy.xml.MarkupBuilder;
import groovy.util.*;

def testDataFolder = testRunner.testCase.testSuite.getPropertyValue("OutputFolder");
def testDataOutputType = testRunner.testCase.testSuite.getPropertyValue("OutputType");
def testDataStr = "";
//def martMap  = testRunner.testCase.getTestStepByName("MartMap");
def martMapTC = testRunner.testCase.testSuite.project.testSuites["CheckMartValide"].testCases["TC00_Init_Config"]
def martMap = martMapTC.testSteps["MartMap_Single"];
//def martMap = martMapTC.testSteps["MartMap_Mart"];
//def martMap = martMapTC.testSteps["MartMap_Full"];
for( prop in martMap.propertyNames  )
{
    testDataStr= testDataStr + martMap.properties[prop].value +";"
}

//def testDataStr = """
//FX_RATE_AReport;
//"""

def scheduleReportJsonTemplate = """
{
	"inputFile": "@inputFile.xanalyzer",
	"jobName": "@jobName",
	"outputFile": "@outputFile",
	"runInBackground": true,
	"jobParameters": [{
		"name": "REPORT_FORMAT_TYPE",
		"stringValue": ["CSV"],
		"type": "string"
	}]
}
"""
///home/user1Tenant2/FX_RATE_AReport.xanalyzer
///home/user1Tenant2
class PAMReportsConfig {
   String folderRepo;
   String[] reportNames;
   String runJsonStr;
   String outputType;
}

def reportsConfig = new PAMReportsConfig();
def testDataArray = testDataStr.replaceAll("\r","").replaceAll("\n", "").split(";")
reportsConfig.folderRepo = testDataFolder;
reportsConfig.reportNames = testDataArray;
reportsConfig.runJsonStr = scheduleReportJsonTemplate;
reportsConfig.outputType = testDataOutputType;
//log.info(reportsConfig.folderRepo);
//log.info(reportsConfig.reportNames.toString());

context.setProperty( "reportsConfig", reportsConfig )
//log.info context.toString();

```
