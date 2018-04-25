import logging
from colorlog import ColoredFormatter

LOG_LEVEL = logging.DEBUG

LOG_FORMAT_CONSOLE = "%(log_color)s%(asctime)s [%(levelname)-5.5s] %(message)s"
LOG_FORMAT_FILE = "%(asctime)s [%(levelname)-5.5s] %(message)s"

logging.root.setLevel(LOG_LEVEL)

# formatter = ColoredFormatter(LOG_FORMAT_CONSOLE)

formatter_console = ColoredFormatter(
	LOG_FORMAT_CONSOLE,
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
# use default Formatter for file
formatter_file = logging.Formatter(LOG_FORMAT_FILE)

handler_stream = logging.StreamHandler()
handler_stream.setLevel(LOG_LEVEL)
handler_stream.setFormatter(formatter_console)

handler_file = logging.FileHandler("colorlog.log")
handler_file.setLevel(LOG_LEVEL)
handler_file.setFormatter(formatter_file)


log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)
# set file and console hander to log
log.addHandler(handler_stream)
log.addHandler(handler_file)


log.debug("A quirky message only developers care about")
log.info("Curious users might want to know this")
log.warn("Something is wrong and any user should be informed")
log.error("Serious stuff, this is red for a reason")
log.critical("OH NO everything is on fire")

