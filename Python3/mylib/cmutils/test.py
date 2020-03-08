from cmutils.log import Logger
logger = Logger(level='INFO', format_file='%(asctime)s [%(levelname)-5.5s] %(message)s', 
logfile_path=f'{__file__}.log', format_confole='%(log_color)s%(asctime)s [%(levelname)-5.5s] %(message)s')
logger = logger.logger

logger.info('test')
logger.warning('warning')
