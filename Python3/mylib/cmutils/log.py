#/usr/bin/python3
'''
author: xiche
create at: 06/16/2018
description:
    Utils for log
Change log:
Date          Author      Version    Description
08/31/2018    xiche       1.0.1      Add change_logging_file
09/12/2018    xiche       1.1.0      ShowProcess
09/27/2018    xiche       1.1.1      Add VMTalk
10/10/2018    xiche       1.1.2      Add VMTalk.hear, VMTalk.wait
08/25/2019    xiche       2.0.0      change folder  
'''
import os,sys, time, logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from colorlog import ColoredFormatter
from threading import Thread
from datetime import datetime
from cmutils.io import TxtUtils
class Logger:
    # __LOG_FORMATTER_FILE =  ''
    # __LOG_FILE_PATH = ''
    # __LOG_FORMATTER_CONSOLE = ''
    
    # __LOG_LEVEL         = logging.INFO
    
    # __HANDLER_STREAM    = None
    # __HANDLER_FILE      = None
    
    

    def __init__(self, **options):
        self.__LOGGER                   = logging.getLogger(__name__)
        
        self.__LOG_LEVEL                = self.get_log_level(options.get("level"))
        self.__LOG_FORMATTER_FILE       = logging.Formatter(options.get("format_file"))
        self.__LOG_FILE_PATH            = options.get("logfile_path")
        self.__LOG_FORMATTER_CONSOLE    = self.init_colored_formatter(options.get("format_console"))
        
        logging.root.setLevel(self.__LOG_LEVEL)
        
        self.__HANDLER_STREAM = logging.StreamHandler()
        self.__HANDLER_STREAM.setLevel(self.__LOG_LEVEL)
        self.__HANDLER_STREAM.setFormatter(self.__LOG_FORMATTER_CONSOLE)

        self.__HANDLER_FILE = logging.FileHandler(self.__LOG_FILE_PATH)
        self.__HANDLER_FILE.setLevel(self.__LOG_LEVEL)
        self.__HANDLER_FILE.setFormatter(self.__LOG_FORMATTER_FILE)
        
        self.__LOGGER.setLevel(self.__LOG_LEVEL)
        self.__LOGGER.addHandler(self.__HANDLER_STREAM)
        self.__LOGGER.addHandler(self.__HANDLER_FILE)

    def change_logging_file(self, file_name):
        self.__LOGGER.removeHandler(self.__HANDLER_FILE)
        self.__HANDLER_FILE = logging.FileHandler(file_name)
        self.__HANDLER_FILE.setLevel(self.__LOG_LEVEL)
        self.__HANDLER_FILE.setFormatter(self.__LOG_FORMATTER_FILE)
        self.__LOGGER.addHandler(self.__HANDLER_FILE)
        
    @property
    def logger(self):
        return self.__LOGGER

    def get_log_level(self,x):
        return {
            'DEBUG':logging.DEBUG,
            'INFO': logging.INFO,
            'ERROR': logging.ERROR,
            'WARN': logging.WARN
        }.get(x, logging.INFO)

    def init_colored_formatter(self, format_str):
        formatter = ColoredFormatter(
            format_str,
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'bold_yellow',
                'ERROR':    'bold_red',
                'CRITICAL': 'bold_red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        )
        return formatter

class ShowProcess():
    pct_now = 0 # current progress
    max_steps = 0 # total steps
    max_arrow = 50 # length of the process bar
    infoDone = 'done'

    def __init__(self, max_steps, infoDone = 'Done'):
        self.max_steps = max_steps
        self.pct_now = 0
        self.infoDone = infoDone
        self.count_now = 0
        self.total = 0

    # [>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
    def show_process(self, pct_now=None):
        if pct_now is not None:
            self.pct_now = pct_now
        else:
            self.pct_now
        # calc how many '>'
        num_arrow = int(self.pct_now * self.max_arrow / self.max_steps) 
        # calc how many '-'
        num_line = self.max_arrow - num_arrow 
        # calc percent of finished (xx.xx%)
        percent = self.pct_now * 100.0 / self.max_steps
        #'\r' means to the left
        process_bar = "[{0}{1}] {2:.2f}% ({3}/{4})\r".format('>'*num_arrow, '-'*num_line, percent, self.count_now, self.total)
        # print to console
        sys.stdout.write(process_bar) 
        sys.stdout.flush()
        if self.pct_now >= self.max_steps:
            self.close()

    def close(self):
        print('')
        # print(self.infoDone)
        self.pct_now = 0


    def monitor_process(self):
        while(True):   
            self.show_process(self.pct_now)
            time.sleep(1) 
            if(self.pct_now >= 100):
                self.show_process(100)
                break

    def startMonitor(self):
        t = Thread(target=self.monitor_process, args=())
        t.start()
        
class VMTalk():
    def __init__(self, talk_path, who='INFO'):
        self.talk_path = talk_path
        self.who = who

    def say(self, content):
        current_time = datetime.now()
        content = '{:%Y-%m-%d %H:%M:%S} [{}] > {}'.format(current_time, self.who, content)
        TxtUtils.write_str_append_to_file_first_line(self.talk_path, content)
        
    def hear(self):
        return TxtUtils.read_first_line(self.talk_path)
        
    def wait(self, message_wait):
        while(True):
            message_now = TxtUtils.read_first_line(self.talk_path)
            if(message_wait.lower() in message_now.lower()):
                break;
            time.sleep(2)
        
