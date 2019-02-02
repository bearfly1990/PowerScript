# import sys, time
 
# for i in range(5):
#     sys.stdout.write('{0}/5\r'.format(i + 1))
#     sys.stdout.flush()
#     time.sleep(1)

# for i in range(5):
#     sys.stdout.write(str(i) * (5 - i) + '\r')
#     sys.stdout.flush()
#     time.sleep(1)

# for i in range(5):
#     sys.stdout.write(' ' * 10 + '\r')
#     sys.stdout.flush()
#     sys.stdout.write(str(i) * (5 - i) + '\r')
#     sys.stdout.flush()
#     time.sleep(1)

# for i in range(5):
#     sys.stdout.write(' ' * 10 + '\r')
#     sys.stdout.flush()
#     print(i)
#     sys.stdout.write(str(i) * (5 - i) + '\r')
#     sys.stdout.flush()
#     time.sleep(1)

# class ProgressBar:
#     def __init__(self, count = 0, total = 0, width = 50):
#         self.count = count
#         self.total = total
#         self.width = width
#     def move(self):
#         self.count += 1
#     def log(self, s):
#         sys.stdout.write(' ' * (self.width + 9) + '\r')
#         sys.stdout.flush()
#         print(s)
#         progress = int(self.width * self.count / self.total)
#         sys.stdout.write('{0:3}/{1:3}: '.format(self.count, self.total))
#         sys.stdout.write('#' * progress + '-' * (self.width - progress) + '\r')
#         if progress == self.width:
#             sys.stdout.write('\n')
#         sys.stdout.flush()
 
# bar = ProgressBar(total = 10)
# for i in range(10):
#     bar.move()
#     bar.log('We have arrived at: ' + str(i + 1))
#     time.sleep(1)


# from time import sleep
# from tqdm import tqdm
# for i in tqdm(range(1, 500)):
#     sleep(0.01)

# from time import sleep
# from timeit import timeit
# import re
 
# # Simple demo
# from tqdm import trange
# for i in trange(16, leave=True):
#     sleep(0.1)
 
# # Profiling/overhead tests
# stmts = filter(None, re.split(r'\n\s*#.*?\n', __doc__))
# for s in stmts:
#     print(s.replace('import tqdm\n', ''))
#     print(timeit(stmt='try:\n\t_range = xrange'
#                       '\nexcept:\n\t_range = range\n' + s, number=1),
#           'seconds')




# from __future__ import division
# import sys,time
# j = '#'
# if __name__ == '__main__':
#   for i in range(1,61):
#     j += '#'
#     sys.stdout.write(str(int((i/60)*100))+'% '+j+'->'+ "\r")
#     sys.stdout.flush()
#     time.sleep(0.5)

 
# import sys
# from time import sleep
# def viewBar(i):
#     """
#     进度条效果
#     :param i:
#     :return:
#     """
#     output = sys.stdout
#     for count in range(0, i + 1):
#         second = 0.1
#         sleep(second)
#         output.write('\rcomplete percent ----->:%.0f%%' % count)
#     output.flush()

# viewBar(100)




# from time import sleep
# from tqdm import tqdm
# for i in tqdm(range(1, 500)):
#     sleep(0.01)


# class ProgressBar():
#   def __init__(self, width=50):
#     self.pointer = 0
#     self.width = width
#   def __call__(self,x):
#      # x in percent
#      self.pointer = int(self.width*(x/100.0))
#      return "|" + "#"*self.pointer + "-"*(self.width-self.pointer)+ "|\n %d percent done" % int(x)
 
# if __name__ == '__main__':
#     import time,os
# pb = ProgressBar()
# for i in range(101):
#     os.system('cls')
#     print( pb(i))
#     time.sleep(0.1)



# import sys
# import time
# def view_bar(num,total):
#     rate = num / total
#     rate_num = int(rate * 100)
#     #r = '\r %d%%' %(rate_num)
#     r = '\r%s>%d%%' % ('=' * rate_num, rate_num,)
#     sys.stdout.write(r)
#     sys.stdout.flush
# if __name__ == '__main__':
#     for i in range(0, 101):
#         time.sleep(0.1)
#         view_bar(i, 100)


import sys, time
import random
import _thread
class ShowProcess():
    """
    显示处理进度的类
    调用该类相关函数即可实现处理进度的显示
    """
    i = 0 # 当前的处理进度
    max_steps = 0 # 总共需要处理的次数
    max_arrow = 50 #进度条的长度
    infoDone = 'done'

    # 初始化函数，需要知道总共的处理次数
    def __init__(self, max_steps, infoDone = 'Done'):
        self.max_steps = max_steps
        self.i = 0
        self.infoDone = infoDone

    # 显示函数，根据当前的处理进度i显示进度
    # 效果为[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
    def show_process(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        num_arrow = int(self.i * self.max_arrow / self.max_steps) #计算显示多少个'>'
        num_line = self.max_arrow - num_arrow #计算显示多少个'-'
        percent = self.i * 100.0 / self.max_steps #计算完成进度，格式为xx.xx%
        process_bar = '[' + '#' * num_arrow + '-' * num_line + ']'\
                      + '%.2f' % percent + '%' + '\r' #带输出的字符串，'\r'表示不换行回到最左边
        sys.stdout.write(process_bar) #这两句打印字符到终端
        sys.stdout.flush()
        if self.i >= self.max_steps:
            self.close()

    def close(self):
        print('')
        print(self.infoDone)
        self.i = 0

# if __name__=='__main__':
#     max_steps = 100

#     process_bar = ShowProcess(max_steps, 'OK')

#     for i in range(max_steps):
#         process_bar.show_process()
#         time.sleep(0.01)
VALUE = 0

def start_import():
    global VALUE
    while(True):
        VALUE += 1
        time.sleep(0.1 * random.random())
        if VALUE == 100:
            time.sleep(2)
            break

def monitor_process( threadName, delay):
    max_steps = 100
    process_bar = ShowProcess(max_steps, 'OK') # 1.在循环前定义类的实体， max_steps是总的步数， infoDone是在完成时需要显示的字符串
    # for i in range(max_steps): 
    while(True):   
        process_bar.show_process(VALUE)      # 2.显示当前进度
        time.sleep(1) 
        if(VALUE == 100):
            process_bar.show_process(100)
            break

_thread.start_new_thread( monitor_process, ("Thread-1", 2, ) )
start_import()
print("???")
print("FFIGH")
# from time import sleep
# from tqdm import tqdm
# # pbar = tqdm(["a", "b", "c", "d"])
# # for char in pbar:
# #     pbar.set_description("Processing %s" % char)

# pbar = tqdm(total=100, ascii=True)
# for i in range(10):
#     pbar.update(10)
#     a = 0
#     sleep(0.5)
        
# pbar.close()

