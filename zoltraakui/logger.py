import logging
import os
from logging.handlers import RotatingFileHandler


BACKUP_COUNT = 5
LEVEL_DEBUG = 'debug'
LEVEL_INFO = 'info'
LOG_PATH = os.path.join(os.path.dirname(__file__), 'log')
MAX_BYTES = 1000000


class PythonLogger:

    def __init__(self,
                 save_as='logging.log',
                 level='debug'):
        '''
        Initialize a logger instance.
        Indicate info for INFO level, otherwise DEBUG.
        '''
        if not os.path.isdir(LOG_PATH):
            os.mkdir(LOG_PATH)

        self.logger = logging.getLogger()

        if level == 'info':
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.DEBUG)

        self.handler = RotatingFileHandler(
            filename=os.path.join(LOG_PATH, save_as),
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT)

        log_format = '[%(levelname)s][%(asctime)s] %(message)s'

        self.handler.setFormatter(logging.Formatter(log_format))
        self.logger.addHandler(self.handler)
        self.logger.info('PythonLogger: logger opened')

    def write_debug(self, message):
        self.logger.debug(message)

    def write_info(self, message):
        self.logger.info(message)

    def write_error(self, message):
        self.logger.error(message)

    def __del__(self):
        self.logger.info('PythonLogger: close logger')
        self.handler.close()
        self.logger.removeHandler(self.handler)
