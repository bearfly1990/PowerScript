import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import os, time


class PySvc(win32serviceutil.ServiceFramework):  
    # you can NET START/STOP the service by the following name  
    _svc_name_ = "PySvc"  
    # this text shows up as the service name in the Service  
    # Control Manager (SCM)  
    _svc_display_name_ = "Python Test Service"  
    # this text shows up as the description in the SCM  
    _svc_description_ = "This service writes stuff to a file"  
      
    def __init__(self, args):  
        win32serviceutil.ServiceFramework.__init__(self,args)  
        # create an event to listen for stop requests on  
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  
      
    # core logic of the service     
    def SvcDoRun(self):  
        # import servicemanager
        f = open('c:\\test.txt', 'w+')  
        rc = None  
        # if the stop event hasn't been fired keep looping  
        while rc != win32event.WAIT_OBJECT_0:
            f.write('TEST DATA\n')  
            f.flush()  
            # block for 5 seconds and listen for a stop event  
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)  
              
        f.write('SHUTTING DOWN\n')  
        f.close()  
      
    # called when we're being shut down      
    def SvcStop(self):  
        # tell the SCM we're shutting down  
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)  
        # fire the stop event  
        win32event.SetEvent(self.hWaitStop)  
        
if __name__ == '__main__':  
    win32serviceutil.HandleCommandLine(PySvc)         
# class AppServerSvc (win32serviceutil.ServiceFramework):
    # _svc_name_ = "TestService"
    # _svc_display_name_ = "Test Service"

    # def __init__(self,args):
        # win32serviceutil.ServiceFramework.__init__(self,args)
        # self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        # socket.setdefaulttimeout(60)

    # def SvcStop(self):
        # self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # win32event.SetEvent(self.hWaitStop)

    # def SvcDoRun(self):
        # self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              # servicemanager.PYS_SERVICE_STARTED,
                              # (self._svc_name_,''))
        # self.main()

    # def main(self):
        # print("good")
        # while(True):
        # os.system('echo aa>>C:\test.txt.log')
            # time.sleep(3)
        # with open('C:\test.txt', 'w') as f:
            # f.write('lallaa')

# if __name__ == '__main__':
    # win32serviceutil.HandleCommandLine(AppServerSvc)
