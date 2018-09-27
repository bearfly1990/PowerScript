#/usr/bin/python3
"""
author: xiche
create at: 09/18/2018
description:
    Common utils for python script
Change log:
Date        Author      Version    Description
09/18/2018  xiche       1.0        Init

"""
import os
import time
def timeout(seconds):
    os.system('timeout {}'.format(seconds))
	
def sleep(seconds):
    time.sleep(seconds)
    
def kill_task(task_name):
    # os.system("tskill {} /a".format(task_name))
    os.system("taskkill /IM {}".format(task_name))
    
    
        
