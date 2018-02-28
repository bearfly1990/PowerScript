/*
 * Created by Ranorex
 * User: QAAuto
 * Date: 3/7/2017
 * Time: 3:39 AM
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Net.Mail;
using System.Threading;
using System.Xml;

using Ranorex;
using Ranorex.Core.Testing;

namespace Publisher.Test.Automation
{
        /// <summary>
        /// Description of Configuration.
        /// </summary>
        public class PubTestAutoUtility
       {
        public static string    ConfigFilePath      = @"../../../WorkSpace/PubTestAutoUtility.ini";
        public static string    VariableFilePath    = "";
        public static string    WorkSpacePath       = "";
        public static string    ExpectFilePath      = "";
        public static string    ExpectPDFPath       = "";
        public static string    ActualFilePath      = "";
        
        public static string    ComparePDFPath      = "";
        public static string    BackUpActFilePath   = "";
        
        public static string    EmailListPath       = @"\\PFS-REGRESS001\Docs\PAMR\PublisherAutomation\EmailList.txt";
        public static string[]  EmailList;
        
        public static string    SendMailAddress     = "PublisherUIAutomation@pfs.com";
        public static string    HostIP              = "172.16.10.34";
        public static string    ReportTitle         = "[QAAuto]Test Result of Test Suite (V{0})";
        public static string    ReportContent       = "<div><font face='Calibri'>Hi ALL,</font></div><div><table><tr><th>Total Cases</th><th>Passed Cases</th><th>Failed Cases</th><th>Pass Rate</th></tr><tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr></table></div><div>{4}</div><div>PAMReport Team</div>";

        public static string    DllPath             = @"C:\Program Files\State Street Global Exchange\Publisher Suite\Publisher Clients\bin\Reporting.Common.dll";
        public static string    BuildVersion        = "";
        public static string    ZipFileName         = "";
		
        public static string    RestartServicePath  = @"RestoreService_Testauto2.bat";
		
        public static string    CloseAppPath        = @"\\pfs-regress001\Docs\PAMR\PublisherAutomation\Tools\Taskkill_App.bat";
        public static string    CloseIEPath         = @"\\pfs-regress001\Docs\PAMR\PublisherAutomation\Tools\Taskkill_IE.bat";
        
        public static Dictionary<string, string> config;
        
        public static XmlDocument VariablesXML;
        
        public static int       PassedNum           = 0;
        public static int       FailedNum           = 0;
        public static int       TotalNum            = 0;
        public static int       IgnoredNum          = 0;
        
        static PubTestAutoUtility()
        {
            ReadConfig();
          
            EmailListPath 		= GetProperty("Email_EmailListPath", EmailListPath);
            EmailList			= System.IO.File.ReadAllLines(EmailListPath);
                                             
            ReportTitle			= GetProperty("ReportTitle", ReportTitle);
            // ReportContent        = getProperty("ReportContent", ReportContent);
                                             
            SendMailAddress		= GetProperty("Email_SendMailAddress", SendMailAddress);
            HostIP				= GetProperty("Email_HostIP", HostIP);
                                             
            DllPath				= GetProperty("Pub_DllPath", DllPath);
            BuildVersion		= System.Diagnostics.FileVersionInfo.GetVersionInfo(DllPath).FileVersion; 
            ZipFileName			= Ranorex.Core.Reporting.TestReport.ReportEnvironment.ReportViewFilePath;
                                 
            WorkSpacePath		= GetProperty("WorkSpacePath", WorkSpacePath);
                                 
            ExpectFilePath		= GetRealPath("ExpectFilePath", ExpectFilePath);
            ExpectPDFPath		= GetRealPath("ExpectPDFPath", ExpectPDFPath);
            ActualFilePath		= GetRealPath("ActualFilePath", ActualFilePath);
            ComparePDFPath		= GetRealPath("ComparePDFPath", ComparePDFPath);
            BackUpActFilePath	= GetRealPath("BackUpActFilePath", BackUpActFilePath);
            RestartServicePath	= GetRealPath("RestartServicePath",RestartServicePath);
            CloseAppPath		= GetRealPath("TaskKill_APP", CloseAppPath);
            CloseIEPath			= GetRealPath("TaskKill_IE", CloseIEPath);
			
			VariableFilePath	= GetRealPath("VariableFilePath", VariableFilePath);
 
			ReadCaseVariables();
        }
		
        public static string GetProperty(string key)
        {
            return config.ContainsKey(key) ? config[key] : null; 
        }    
		
        public static string GetProperty(string key, string defaultValue)
        {
            return config.ContainsKey(key) ? config[key] : defaultValue; 
        }                      
        
		public static string GetRealPath(string key, string defaultValue)
		{
			string result = GetProperty(key, defaultValue);
			return (result == "") ? result : (WorkSpacePath + result);
		}
        public PubTestAutoUtility(){
           
        }
        
        public static void BackupActualFile(){
        	RunScript(BackUpActFilePath);
        }
        
        public static void CloseApplication()
        {    
            RunScript(CloseAppPath);
        }
        
		public static void RestartService()
		{
			RunScript(RestartServicePath);
		}
		
        public static void CloseIE()
        {
            RunScript(CloseIEPath);
        }
        
		public static void RunScript(string scriptPath)
		{
			Process proc = Process.Start(scriptPath);
            proc.WaitForExit();
		}
        public static void GetCaseStatus()
        {
            try
            {
                IList<TestCaseNode> testCasesList = TestSuite.Current.SelectedRunConfig.GetActiveTestCases();
                var testcases = from tCases in testCasesList where (tCases.Name != TestSuite.Current.Name)
                select tCases;
                foreach(TestCaseNode testcase in testcases)
                {
                    if(testcase.Status.Equals(Ranorex.Core.Reporting.ActivityStatus.Failed))
                       FailedNum++;
                    if(testcase.Status.Equals(Ranorex.Core.Reporting.ActivityStatus.Ignored))
                       IgnoredNum++;
                    if(testcase.Status.Equals(Ranorex.Core.Reporting.ActivityStatus.Success))
                       PassedNum++;
                }
                TotalNum    = PassedNum + FailedNum;
            }
            catch(Exception e)
            {
                FailedNum = -1;
                PassedNum = -1;
                TotalNum  = -1;
                //throw new Ranorex.ValidationException(e.Message);
            }
            finally
            {
            	Report.Log(ReportLevel.Info, "Calculate Case passed or failed");
            	if (PassedNum > 0 && PassedNum == TotalNum)
            	{
            		ReportContent	= ReportContent.Replace("<table>", "<table style='border-collapse: collapse;border-spacing: 0px;'>");
            		ReportContent	= ReportContent.Replace("<th>", "<th style='border: 1px solid green;color:green'>");
        			ReportContent	= ReportContent.Replace("<td>", "<td style='border: 1px solid green;color:green'>");
            	}
            	else
            	{
            		ReportContent	= ReportContent.Replace("<table>", "<table style='border-collapse: collapse;border-spacing: 0px;'>");
            		ReportContent	= ReportContent.Replace("<th>", "<th style='border: 1px solid red;color:red'>");
        			ReportContent	= ReportContent.Replace("<td>", "<td style='border: 1px solid red;color:red'>");
            	}
            }
        }
        
        public static void SendReport()
        {
            GetCaseStatus();
            ReportTitle     = string.Format(ReportTitle, BuildVersion);

          
            ReportContent   = string.Format(ReportContent, TotalNum, PassedNum, FailedNum, (PassedNum * 1.0 / TotalNum * 1.0).ToString("P", CultureInfo.InvariantCulture), ZipFileName);
            SendEmail(ReportTitle, ReportContent);
        }

        public static void SendEmail(string reportTitle, string reportContent)
        {
            SendEmail_SMTP(EmailList, reportTitle, reportContent);
        }
        
        public static void SendEmail_SMTP(string[] emailList, string subject, string body)
        {
            using (MailMessage mailMessage = new MailMessage())
            {
                    mailMessage.From        = new MailAddress(SendMailAddress);
                    mailMessage.Subject     = subject;
                    mailMessage.Body        = body;
                    mailMessage.IsBodyHtml  = true;
                    foreach (String item in emailList){
                    	if (!item.Trim().Equals(""))
                    	{
                            mailMessage.To.Add(new MailAddress(item));
                    	}
                    }
                    SmtpClient smtp = new SmtpClient();
                    smtp.Host       = HostIP;
                    smtp.Send(mailMessage);
            }
        }
        
        public static void CompareFile(string fileName)
        {
            string filePath_Expected    = ExpectFilePath + fileName+".xslfo";
            string filePath_Actual      = ActualFilePath + fileName+".xslfo";
            string filePath_Result      = ActualFilePath + fileName+".log";
            
            const string fileNotFound   = "File not found for comparison in Validate_FileContentEqual: {0}";  
            const string noOutputFile    = "There is no output file";
            const string noExpectFile    = "There is no expect file";
            const string resultPass     = "The result is pass";
            const string resultFail     = "The result is fail";
            
            string failMessage          = "";
            string passMessage          = "";
            string logMessage           = "Comparing content of files ({0} vs. {1})";
            bool casePass               = false;
            
            logMessage                  = string.Format(logMessage, filePath_Expected, filePath_Actual);
            
            if (!System.IO.File.Exists(filePath_Actual))
            {
                WriteToFileAppend(filePath_Result, noOutputFile);
            }
            else if (!System.IO.File.Exists(filePath_Expected))
            {
                WriteToFileAppend(filePath_Result, noExpectFile);
                failMessage = string.Format(fileNotFound, filePath_Expected);
            }
            else 
            {
                try
                {
                    string current  = System.IO.File.ReadAllText(filePath_Actual);  
                    string expected = System.IO.File.ReadAllText(filePath_Expected);
                    casePass        = current.Equals(expected);
                }
                catch(Exception e)
                {
                 casePass    = false;
                 failMessage = e.Message;
                }
             
            }
            
           if (casePass)
           {
               passMessage    = resultPass  + System.Environment.NewLine +  logMessage;
               WriteToFileAppend(filePath_Result, passMessage );
               Ranorex.Validate.IsTrue(true, passMessage);  
           }
           else
           {
               failMessage    = resultFail + System.Environment.NewLine + failMessage + System.Environment.NewLine + logMessage;
               WriteToFileAppend(filePath_Result, failMessage);
               Ranorex.Validate.IsTrue(false, failMessage);
           }
        }
        
        public static void ComparePDF(string fileName)
        {
            string filePath_Expected   = ExpectPDFPath + fileName+".pdf";
            string filePath_Current    = ActualFilePath + fileName+".pdf";
            string filePath_Result     = ActualFilePath + fileName+"PDF.log";
            
            const string fileNotFound  = "File not found for comparison in Validate_FileContentEqual: {0}";  
            const string noOutputFile  = "Comparison PDF completes: Failed There is no output file";
            const string noExpectFile  = "Comparison PDF completes: Failed There is no expect file";
            const string resultPass    = "The result is pass";
            const string resultFail    = "The result is fail";
            
            string failMessage         = "";
            string passMessage         = "";
            string logMessage          = "Comparing pdf content of files ({0} vs. {1})";
            bool casePass              = false;
            
            logMessage = string.Format(logMessage, filePath_Expected, filePath_Current); 
            
            // check if file exists  
            if (!System.IO.File.Exists(filePath_Current))  
            {  
                failMessage  = string.Format(fileNotFound, filePath_Current);
                WriteToFileAppend(filePath_Result, noOutputFile);
            }
            else if (!System.IO.File.Exists(filePath_Expected))
            {  
                failMessage  = string.Format(fileNotFound, filePath_Expected);
                WriteToFileAppend(filePath_Result, noExpectFile);
            }     
            else if (filePath_Expected.Equals(filePath_Current))  
            {  
                failMessage  = "The expect and actual files should not be the same path\n";
                WriteToFileAppend(filePath_Result, failMessage);
            }  
            else  
            {   
                string CompareCMD    = ComparePDFPath;
                string ComparePara    = filePath_Expected+" "+filePath_Current+">>"+filePath_Result;
                Process.Start(CompareCMD,ComparePara); 
                Thread.Sleep(5000);
                try{
                    PubTestAutoUtility.WaitFileEnable(filePath_Result);
                    string LogInfo = System.IO.File.ReadAllText(filePath_Result);
                    
                    if(LogInfo.TrimEnd()=="No differences detected.")
                    {
                        casePass = true;
                    }
                
                }catch(Exception e){
                    failMessage = e.Message;
                }
            }
            if (casePass)
            {
                passMessage        = resultPass + System.Environment.NewLine + logMessage;
                WriteToFileAppend(filePath_Result, passMessage );
                Ranorex.Validate.IsTrue(true, passMessage);  
            }
            else
            {
                failMessage        = resultFail + System.Environment.NewLine + failMessage + System.Environment.NewLine + logMessage;
                WriteToFileAppend(filePath_Result, failMessage);
                Ranorex.Validate.IsTrue(false, failMessage);
            }
            
        }
        
        public static void WaitFileEnable(string fileName){
            for(int i = 0; i < 10; i++)
                {
                    if (IsFileInUse(fileName))
                    {
                        Thread.Sleep(5000);
                    }
                    else
                    {
                        break;
                    }
                }
        }
        
        public static bool IsFileInUse(string fileName)
        {
                bool inUse = true;
                if (File.Exists(fileName))
                {
                    FileStream fs = null;
                    try
                    {
                        fs = new FileStream(fileName, FileMode.Open, FileAccess.Read, FileShare.None);
                        inUse = false;
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine(e.Message.ToString());
                    }
                    finally
                    {
                        if (fs != null)
                        {
                            fs.Close();
                        }
                    }
                    return inUse;           //true表示正在使用,false没有使用
                }
                else
                {
                    return false;           //文件不存在则一定没有被使用
                }

        }
        
        public static void ReadConfig()
        {
            config = new Dictionary<string, string>();
            foreach (var row in File.ReadAllLines(ConfigFilePath))
            {
               if(row.Equals("")) continue;
               config.Add(row.Split('=')[0], row.Split(new char[] { '=' }, 2)[1]);
               //Console.WriteLine(row.Split(new char[] { '=' }, 2)[1]);
               //Thread.Sleep(2000);
            }
                  
        }
        
        public static void ReadCaseVariables()
        {
            if (!VariableFilePath.Equals(""))
            {
                VariablesXML = new XmlDocument();
                VariablesXML.Load(VariableFilePath);       
            }
        }
        /// <summary>   
        /// Get variable from xml setting
        /// </summary>   
        /// 
        public static string GetVariable(string TestCaseID, string TestStepID, string VariableID)
        {
            string xpath    = String.Format("/TestSuite/TestCase[@id='{0}']/TestStep[@id='{1}']/Var[@id='{2}']",TestCaseID, TestStepID, VariableID);
                              
            XmlNode node   = VariablesXML.DocumentElement.SelectSingleNode(xpath);
            
            string var     = node.Attributes["value"].InnerText;
            
            return var;
        }
        public static void WriteToFileAppend(string filePath, string content)
        {
            using (StreamWriter sw = File.AppendText(filePath))
            {
                sw.WriteLine(content);
            }
        }
        public static void CheckActualPath()
        {
            CheckActualPath(ActualFilePath);
        }
        public static void CheckActualPath(string ActualPath)
        {
            DirectoryInfo aPath = new DirectoryInfo(ActualPath);
            if(aPath.Exists)
            {}
            else
            {
               aPath.Create();
            }
        }
    }
}
