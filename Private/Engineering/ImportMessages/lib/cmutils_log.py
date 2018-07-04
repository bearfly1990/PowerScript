import logging
from colorlog import ColoredFormatter

class Logger:
    __LOG_FORMATTER_FILE =  ''
    __LOG_FILE_PATH = ''
    __LOG_FORMATTER_CONSOLE = ''
    
    __LOG_LEVEL         = logging.INFO
    
    __HANDLER_STREAM    = None
    __HANDLER_FILE      = None
    
    __LOGGER            = logging.getLogger(__name__)

    def __init__(self, **options):
       
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
        self.__LOGGER.addHandler(self.__HANDLER_FILE )

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
