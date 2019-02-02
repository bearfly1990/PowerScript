#!/usr/bin/python3
"""
author: xiche
create at: 04/22/2018
description:
    System Monitor
Change log:
Date        Author      Version     Description
04/22/2018  xiche       1.0         init
06/06/2018  xiche       1.0.1       fix cpu pecent
06/16/2018  xiche       1.0.2       add class Monitor
08/16/2018  xiche       1.0.3       add MQ monitor
"""
import sys
sys.path.insert(0, r"xxx\pythonlib")
import psutil
import math
import time
import datetime
import csv
import os
from abc import abstractmethod, ABC
from threading import Thread
from cmutils.cmutils_value import Units, convertByteTo
# from lib.cmutils_io import CSVUtils
class SystemInfo(ABC):
    __free      = 0
    __used      = 0
    __total     = 0
    __units     = Units.MB
    __pct_used  = 0
    __file_system = ""

    @abstractmethod
    def refresh(self):
        pass

    def refresh_loop(self):
        while(True):
            self.refresh()
            time.sleep(1)

    def __init__(self, units=Units.MB):
        self.__file_system = psutil.disk_partitions()
        self.refresh()
        # t = Thread(target=self.refresh_loop)
        # t.start()

    @property
    def free(self):
        self.refresh()
        return convertByteTo(self.__free, self.__units)

    @property
    def used(self):
        self.refresh()
        return convertByteTo(self.__used, self.__units)

    @property
    def total(self):
        self.refresh()
        return convertByteTo(self.__total, self.__units)

    @property
    def units(self):
        self.refresh()
        return self.__units.name

    @property
    def pctused(self):
        self.refresh()
        return ("%.2f" % (float(self.__used)/float(self.__total)*100))

    @property
    def file_system(self):
        self.refresh()
        return self.__file_system

    @units.setter
    def units(self, units):
        self.__units = units

    @free.setter
    def free(self, free):
        self.__free = free

    @used.setter
    def used(self, used):
        self.__used = used

    @total.setter
    def total(self, total):
        self.__total = total

    def __str__(self):
        return '\033[1;35;40m Resource use(%s): total:%s used:%s free:%s usedpct:%s\033[0 m' % (self.units, self.total, self.used, self.free, self.pctused)

class MemoryInfo(SystemInfo):
    
    def refresh(self):
        mem = psutil.virtual_memory()
        self.free   = mem.free
        self.used   = mem.used  #+ mem.cached + mem.buff
        self.total  = mem.total
        self.units  = Units.MB  
    def __init__(self, units=Units.MB):
        super().__init__()
    def __str__(self):
        # return '\033[1;35;40m Memory(%s): total:%s used:%s free:%s usedpct:%s\033[0 m' % (self.units, self.total, self.used, self.free, self.pctused)
        return 'Memory(%s): total:%s used:%s free:%s usedpct:%s' % (self.units, self.total, self.used, self.free, self.pctused)

class ProcessInfo(SystemInfo):
    __process_name  = "java.exe"
    __user_name     = os.getlogin()
    __pct_memory    = 0
    __error         = False
    def __init__(self, process_name, user_name, error):
        super().__init__()
        self.__process_name = process_name.lower()
        self.__user_name    = user_name.lower()
        self.__error        = error
    def processinfo(self):
        ps_list = []
        ps_list_error = []
        #print("---->"+self.__process_name.lower())
        for ps in psutil.process_iter():
            try:
                ps_name = ps.name().lower()
                if self.__process_name in ps_name:
                    ps_username = ps.username().lower()
                    if self.__user_name.lower() in ps_username:
                        ps_list.append(ps)
            except (psutil.AccessDenied, psutil.ZombieProcess):
                if self.__process_name in ps_name:
                    ps_list_error.append(ps)
            except psutil.NoSuchProcess:
                continue
        if self.__error:
            ps_list = ps_list + ps_list_error
        return ps_list

    def refresh(self):
        # print("refresh of process")
        self.__pct_memory = 0
        ps_list = self.processinfo()
        for ps in ps_list:
            self.__pct_memory = self.__pct_memory + ps.memory_percent()
        
    @property
    def pct_memory(self):
        self.refresh()
        return "%.2f" % self.__pct_memory

    @property
    def processname(self):
        self.refresh()
        return self.__process_name

            
class CPUInfo(SystemInfo):
    user    = ""
    # nice    = ""
    system  = ""
    idle    = ""
    cpuPercent = ""
    # iowait  = ""
    # irq     = ""
    # softirq = ""
    def refresh(self):
        # cpu = psutil.cpu_times_percent(interval=1.00, percpu=False)
        # self.__pct_used   = cpu.dpc
        # self.user    = round(cpu.user,2)
        # self.nice    = round(cpu.nice)
        # self.system  = round(cpu.system,2)
        # self.idle    = round(cpu.idle,2)
        self.cpuPercent = psutil.cpu_percent(interval=1, percpu=False)
        # self.iowait  = round(cpu.iowait,1)
        # self.irq     = round(cpu.irq,1)
        # self.softirq = round(cpu.softirq,1)
        # steal = round(cpu.steal,1)
        # guest = round(cpu.guest,1)
    def __init__(self):
        super(CPUInfo, self).__init__()
    @property
    def pctused(self):
        self.refresh()
        return self.cpuPercent
        # return self.user + self.system

    def __str__(self):
        return 'CPU: user:%s%% system:%s%% idle:%s%% usedPCT:%s%%' % (self.user, self.system, self.idle, self.pctused)
        # return '\033[1;35;40m CPU: user:%s%% system:%s%% idle:%s%%\033[0 m' % (self.user, self.system, self.idle)

class DiskInfo(SystemInfo):
    def refresh(self):
        cpu = psutil.cpu_times_percent(interval=1.00)
        disk_all    = psutil.disk_usage('/')
        self.total  = disk_all.total
        self.used   = disk_all.used
        self.free   = disk_all.free
        self.units  = Units.GB   
    def __init__(self):
        SystemInfo.__init__(self)

    def __str__(self):
        return 'Disk(%s): total:%s used:%s free:%s usedpct:%s' % (self.units, self.total, self.used, self.free, self.pctused)
        # return '\033[1;35;40m Disk(%s): total:%s used:%s free:%s usedpct:%s\033[0 m' % (self.units, self.total, self.used, self.free, self.pctused)

class Monitor():
    __file_monitor  = None
    __queue_status  = None
    __info_cpu      = None
    __info_memory   = None
    __info_post_server  = None
    __info_mq_service   = None
    __console_out   = False
    __process_name  = None
    def __init__(self, file_monitor, queue_status, cansole_out=False):
        self.__file_monitor = file_monitor
        self.__queue_status = queue_status
        self.__info_cpu     = CPUInfo()
        self.__info_memory  = MemoryInfo()
        self.__info_post_server = ProcessInfo("java.exe", os.getlogin(), False)
        self.__info_mq_service  = ProcessInfo("java.exe", "system", True)
        self.__console_out  = cansole_out
        
    def writeMonitor(self):
        monitor_header = ['Time', 'CPU(%)', 'Memory(%)', 'Java.exe {}(%)'.format(os.getlogin()), 'Java.exe MQ(%)']
        # if(self.__info_process.pct_memory > -1):
        #     monitor_header.append(self.__info_process.processname)

        monitor_result = open(self.__file_monitor, 'w', newline='')  
        with monitor_result:  
            writer = csv.writer(monitor_result)
            writer.writerow(monitor_header)

        monitor_result = open(self.__file_monitor, 'a', newline='')  
        with monitor_result as f:  
            writer = csv.writer(monitor_result)
            isEnded = False
            while(not isEnded):
                try:
                    self.__queue_status.get(False)
                    isEnded = True
                except:
                    isEnded = False
                monitor_data = ['{:%Y/%m/%d %H:%M:%S}'.format(datetime.datetime.now()), self.__info_cpu.pctused, self.__info_memory.pctused, self.__info_post_server.pct_memory, self.__info_mq_service.pct_memory]
               
                # if(self.__info_process.pct_memory > -1):
                #     monitor_data.append()
               
                writer.writerow(monitor_data)
                f.flush()
                if(self.__console_out):
                    print(monitor_data)
                time.sleep(1)
               
                
    def startMonitor(self):

        # CSVUtils.writeToCSVFile(self.__file_monitor, monitor_header)
        t = Thread(target=self.writeMonitor, args=())
        t.start()
        
