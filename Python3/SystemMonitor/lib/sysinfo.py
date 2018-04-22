#!/usr/bin/python3
"""
author: xiche
create at: 04/22/2018
description:
    System Monitor
Change log:
Date        Author      Version    Description
04/22/2018  xiche       1.0        init
"""
import psutil
import math
import time
from abc import abstractmethod, ABC
from threading import Thread
from lib.cmutil import Units, convertByteTo
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
        t = Thread(target=self.refresh_loop)
        t.start()

    @property
    def free(self):
        return convertByteTo(self.__free, self.__units)

    @property
    def used(self):
        return convertByteTo(self.__used, self.__units)

    @property
    def total(self):
        return convertByteTo(self.__total, self.__units)

    @property
    def units(self):
        return self.__units.name

    @property
    def pctused(self):
        return ("%.2f%%" % (float(self.__used)/float(self.__total)*100))

    @property
    def file_system(self):
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
        self.used   = mem.used + mem.buffers + mem.cached
        self.total  = mem.total
        self.units  = Units.MB  
    def __init__(self, units=Units.MB):
        super().__init__()
    def __str__(self):
        return '\033[1;35;40m Memory(%s): total:%s used:%s free:%s usedpct:%s\033[0 m' % (self.units, self.total, self.used, self.free, self.pctused)

class CPUInfo(SystemInfo):
    user    = ""
    nice    = ""
    system  = ""
    idle    = ""
    iowait  = ""
    irq     = ""
    softirq = ""
    def refresh(self):
        cpu = psutil.cpu_times_percent(interval=1.00)
        # self.__pct_used   = cpu.dpc
        self.user    = round(cpu.user,1)
        self.nice    = round(cpu.nice)
        self.system  = round(cpu.system,1)
        self.idle    = round(cpu.idle,1)
        self.iowait  = round(cpu.iowait,1)
        self.irq     = round(cpu.irq,1)
        self.softirq = round(cpu.softirq,1)
        # steal = round(cpu.steal,1)
        # guest = round(cpu.guest,1)
    def __init__(self):
        super(CPUInfo, self).__init__()
    def __str__(self):
        return '\033[1;35;40m CPU: user:%s%% system:%s%% idle:%s%%\033[0 m' % (self.user, self.system, self.idle)

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
        return '\033[1;35;40m Disk(%s): total:%s used:%s free:%s usedpct:%s\033[0 m' % (self.units, self.total, self.used, self.free, self.pctused)
