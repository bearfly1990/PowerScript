#!/usr/bin/python3
"""
author: xiche
create at: 04/22/2018
description:
    System Monitor->cpu, memory
Change log:
Date        Author      Version    Description
04/22/2018  xiche       1.0        init
"""
from lib.sysinfo import CPUInfo, MemoryInfo
import time

def monitor_cpu_memory():
    """monitor system cpu and memory"""
    cpu_info = CPUInfo()
    mem_info = MemoryInfo()
    while(True):
        print(mem_info)
        print(cpu_info)
        time.sleep(1)
     
def __main__():
    monitor_cpu_memory()
__main__()
