## System Monitor by python
之前有用powershell获取CPU，内存的信息[GetCPUMemory.ps1](https://github.com/bearfly1990/PowerScript/blob/master/Powershell/5.1.X/GetCPUMemory.ps1)，利用的是win系统提供的计数器。

今天用python重新写了一个，用的是`psutil`库并且是用OO的思想组织代码，方便之后的重构与维护
### 主要代码
其实代码也不多，专门做了一个模块`sysinfo.py`.

直接调用的`main`函数：
```python
def monitor_cpu_memory():
    """monitor system cpu and memory"""
    cpu_info = CPUInfo()
    mem_info = MemoryInfo()
    while(True):
        print(mem_info)
        print(cpu_info)
        time.sleep(1)
```

在这边我建立了一个基类`SystemInfo`定义了一些基本信息。这里有个细节，因为像cpu和内存的使用是一直变化的，所以在这边我写了一个虚函数（方法），需要子类去实现，并用一个线程每隔一秒就去刷新下需要更新的数据。
```python
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
```
#### MemoryInfo
这个类与基类的契合度最高，所以主要就是实现`refresh`方法。
```python
def refresh(self):
    mem = psutil.virtual_memory()
    self.free   = mem.free
    self.used   = mem.used + mem.buffers + mem.cached
    self.total  = mem.total
    self.units  = Units.MB  
```
### CPUInfo
cpu的数据比较特别，主要的信息都先存储下来，需要用到的时候可以使用。
```python
def refresh(self):
    cpu = psutil.cpu_times_percent(interval=1.00)
    self.user    = round(cpu.user,1)
    self.nice    = round(cpu.nice)
    self.system  = round(cpu.system,1)
    self.idle    = round(cpu.idle,1)
    self.iowait  = round(cpu.iowait,1)
    self.irq     = round(cpu.irq,1)
    self.softirq = round(cpu.softirq,1) 
```
### __str__(self)
每个类都有自己__str__(self)函数，带颜色的输出：
```python
def __str__(self):
    return '\033[1;35;40m CPU: user:%s%% system:%s%% idle:%s%%\033[0 m' % (self.user, self.system, self.idle)
```
