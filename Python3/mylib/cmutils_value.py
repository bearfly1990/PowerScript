#/usr/bin/python3
"""
author: xiche
create at: 04/22/2018
description:
    Common utils for python script
Change log:
Date        Author      Version    Description
04/2/2018   xiche       1.0        Init

"""
from enum import Enum
class Units(Enum):
    KB = 1
    MB = 2
    GB = 3
def convertByteTo(value, units, decimal=2):
    '''Conver byte to KB/MB/GB'''
    if(units is Units.KB):
        value = round(value/1024,decimal)
    elif(units is Units.MB):
        value = round(value/1024/1024,decimal)
    elif(units is Units.GB):
        value = round(value/1024/1024/1024,decimal)  
    return value
    
def isFloat(valueStr):
    try:
        float(valueStr)
        return True
    except ValueError:
        return False
	

        
