import sys
from loguru import logger

logger.add(
    sink=sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    colorize=False,
    backtrace=True,  # Fully descriptive exceptions
    diagnose=True,  # Fully descriptive exceptions
    enqueue=True,  # Asynchronous, Thread-safe, Multiprocess-safe
)


class StdOutErr(object):
    def __init__(self, logger_object):
        self.logger_object = logger_object

    def write(self, string):
        if len(string) != 0 and string[-1] == "\n":
            string = string[:-1]
        self.logger_object(string)

    def flush(self):
        pass

    def isatty(self):
        pass


sys.stdout = StdOutErr(logger.info)
sys.stderr = StdOutErr(logger.warning)
