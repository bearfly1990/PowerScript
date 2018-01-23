```Groovy
import groovy.xml.MarkupBuilder;
import groovy.util.*;
import com.eviware.soapui.support.GroovyUtils;

testRunner.testCase.testSuite.project.testSuites["CheckMartValide"].testCases["TC00_Init_Config"].testSteps["InitialConfig"].run(testRunner, context);
// find the module within the library 

def reportsConfig = context.reportsConfig;

//log.info(context.reportsConfig.toString());
def TS_CreateScheduler = testRunner.testCase.testSteps["CreateScheduler"];
def TS_Properties = testRunner.testCase.testSteps["Properties"];

for (String item : reportsConfig.reportNames) {
	try{
	 	if(item != null && !item.allWhitespace){
//		"""
//		{
//			"inputFile": "@inputFile.xanalyzer",///home/user1Tenant2/FX_RATE_AReport.xanalyzer
//
//			"jobName": "@jobName", //
//			"outputFile": "@outputFile",/home/user1Tenant2
//			"runInBackground": true,
//			"jobParameters": [{
//				"name": "REPORT_FORMAT_TYPE",
//				"stringValue": ["PDF"],
//				"type": "string"
//			}]
//		}
//		"""
			def jsonTemplate = reportsConfig.runJsonStr;

			jsonTemplate = jsonTemplate.replaceAll("@inputFile", (reportsConfig.folderRepo + "/" + item).replaceAll(":", "/") );
			
			if(item.contains(":")){
				def tempFolder = reportsConfig.folderRepo + ":" + item.split(":")[0];
				jsonTemplate = jsonTemplate.replaceAll("@jobName", item.split(":")[1]);
				jsonTemplate = jsonTemplate.replaceAll("@outputFile", tempFolder.replaceAll(":", "/"));
			}else{
				jsonTemplate = jsonTemplate.replaceAll("@jobName", item);
				jsonTemplate = jsonTemplate.replaceAll("@outputFile", reportsConfig.folderRepo.replaceAll(":", "/"));
			}
			
			if(item.contains(":")){
				def tempFolder = reportsConfig.folderRepo + ":" + item.split(":")[0];
				jsonTemplate = jsonTemplate.replaceAll("@outputFile", tempFolder.replaceAll(":", "/"));
			}else{
				
			}

	 		TS_Properties.setPropertyValue( "JsonScheduler", jsonTemplate )
	 		//log.info(TS_Properties.getPropertyValue( "JsonScheduler"));
	 		TS_CreateScheduler.run(testRunner, context);
	
			def responseData = TS_CreateScheduler.testRequest.response.getResponseHeaders();
	 		def statusCode = responseData["#status#"];
			log.info(statusCode.toString());
			assert statusCode.toString().contains("200") : statusCode.toString();
	 		endPoint =TS_CreateScheduler.testRequest.messageExchange.getEndpoint();
			log.info(endPoint);
	 		
			Thread.sleep(5000);
	//		def responseHolder = GroovyUtils.getXmlHolder( );
	 		//log.info(URL_FileProperties_final);
	 		
	 	}
	} catch(e){
		log.warn("Scheduler Reports Error:" + e);
	}
}
```
