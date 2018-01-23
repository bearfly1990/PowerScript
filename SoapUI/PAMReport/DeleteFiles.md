```Groovy
import groovy.xml.MarkupBuilder;
import groovy.util.*;
import com.eviware.soapui.support.GroovyUtils;

testRunner.testCase.testSuite.project.testSuites["CheckMartValide"].testCases["TC00_Init_Config"].testSteps["InitialConfig"].run(testRunner, context);
def reportsConfig = context.reportsConfig;


log.info(context.reportsConfig.toString());
def TS_GetFileID = testRunner.testCase.testSteps["GetFileID"];
def TS_DeleteFile = testRunner.testCase.testSteps["DeleteFile"];
def TS_Properties = testRunner.testCase.testSteps["Properties"];

for (String item : reportsConfig.reportNames) {
	try{
	 	if(item != null && !item.allWhitespace){
	 		log.info("delete "+item+"...")
	 		def URL_FileProperties = testRunner.testCase.testSuite.project.getPropertyValue( "URL_FileProperties" );
	 		def URL_FileProperties_final = URL_FileProperties.replaceAll("@FullFilePath",reportsConfig.folderRepo + ":" + item + reportsConfig.outputType);
			
	 		//TS_GetFileID.setPropertyValue( "URL_FileProperties", URL_FileProperties_final);
	 		TS_Properties.setPropertyValue( "API_FileProperties", URL_FileProperties_final )
	 		//testRunner.runTestStep(TS_GetFileID);
	 		TS_GetFileID.run(testRunner, context);
			//log.info(TS_GetFileID.getPropertyValue("rawRequest"));
			//def responseData = TS_GetFileID.testRequest.request.endPoint();
			//log.info(responseData["#status#"]);
	
			def endPoint = TS_GetFileID.testRequest.messageExchange.getEndpoint();
			//endPoint = TS_DeleteFile.testRequest.messageExchange.getEndpoint();
	 		//log.info(endPoint);
	
	 		
	 		def responseData = TS_GetFileID.testRequest.response.getResponseHeaders();
	 		def statusCode = responseData["#status#"];
			//log.info(statusCode.toString());
			if(statusCode.toString().contains("200")){
				def responseContent = TS_GetFileID.testRequest.response.responseContent;
				def repositoryFileDto = new XmlSlurper().parseText(responseContent);
				//log.info(repositoryFileDto.id);
				
				
				TS_Properties.setPropertyValue( "FileID", repositoryFileDto.id.toString());
				log.info(TS_Properties.getPropertyValue( "FileID"));
				
				TS_DeleteFile.run(testRunner, context);


				responseData = TS_DeleteFile.testRequest.response.getResponseHeaders();
	 			statusCode = responseData["#status#"];
	 			
				endPoint = TS_DeleteFile.testRequest.messageExchange.getEndpoint();
		 		log.info(endPoint);
				log.info(statusCode);
				
			}else{
				//testRunner.fail();
				endPoint = TS_DeleteFile.testRequest.messageExchange.getEndpoint();
		 		log.info(endPoint);
				throw new Exception("File not Found:" + URL_FileProperties_final);
			}
			Thread.sleep(3000);
			//def responseHolder = GroovyUtils.getXmlHolder( );
	 		//log.info(URL_FileProperties_final);
	 		
	 	}
	} catch(e){
		log.warn("Delete File Error:" + e);
	}
}
//def reportInfo = testRunner.testCase.getTestStepByName("GetFileID_XML").getPropertyValue("response")
//log.info(reportInfo);
//def parser = new XmlParser()
//def doc = parser.parse(reportInfo.toString());
//def repositoryFileDto = new XmlSlurper().parseText(reportInfo)
//log.info("id: ${repositoryFileDto.id}")

//def request = context.testCase.getTestStepByName("GetFileID_XML").getTestRequest()
//log.info(request.getRequestHeaders)
```
