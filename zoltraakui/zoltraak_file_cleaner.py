import logging
import os
import shutil
import time
from logging.handlers import RotatingFileHandler


BACKUP_COUNT = 5
MAX_BYTES = 1000000

DIR_LIST = ['generated', 'generated/requirements', 'requirements',
            'user_compiler', 'zip']
LOG_LOCATION = 'log/zoltraak_file_cleaner.log'

TIME_TORELANCE = 3600
INTERVAL_SEC = 3600


class DYLogger:

    def __init__(self, save_as=None):

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        self.handler = RotatingFileHandler(filename=save_as,
                                           maxBytes=MAX_BYTES,
                                           backupCount=BACKUP_COUNT)

        log_format = '[%(levelname)s][%(asctime)s] %(message)s'

        self.handler.setLevel(logging.DEBUG)
        self.handler.setFormatter(logging.Formatter(log_format))

        self.logger.addHandler(self.handler)

        self.logger.info('DYLogger: logger opened')

    def write_debug(self, message):
        self.logger.debug(message)

    def write_info(self, message):
        self.logger.info(message)

    def write_error(self, message):
        self.logger.error(message)

    def __del__(self):
        self.logger.info('DYLogger: close logger')
        self.handler.close()
        self.logger.removeHandler(self.handler)


class ZoltraakFileCleaner:

    def __init__(self):
        self.logger = DYLogger(LOG_LOCATION)

    def _cleanup_folder(self, target_dir):

        time_now = time.time()

        for candidate in sorted(os.listdir(target_dir)):

            focus = os.path.join(target_dir, candidate)
            time_diff = time_now - os.path.getctime(focus)

            if 'requirements' in candidate:
                pass

            elif TIME_TORELANCE < time_diff:
                if os.path.isdir(focus):
                    shutil.rmtree(focus)
                else:
                    os.remove(focus)
                msg = f'Deleted {focus}, Time Diff = {time_diff:.3f}'
                self.logger.write_info(msg)

    def loop(self):

        while True:

            msg = f'loop: start cleaning. Tolerance = {TIME_TORELANCE}'
            self.logger.write_info(msg)

            start_time = time.time()

            for entry in DIR_LIST:
                self.logger.write_info(f'loop: target = {entry}')
                self._cleanup_folder(entry)

            elapsed_time = time.time() - start_time

            msg = f'loop: elapsed time (sec) = {elapsed_time:.3f}'
            self.logger.write_debug(msg)

            time_to_sleep = INTERVAL_SEC - elapsed_time

            msg = f'loop: sleep for {time_to_sleep:.3f} sec'
            self.logger.write_debug(msg)

            time.sleep(time_to_sleep)


def main():

    service = ZoltraakFileCleaner()

    try:
        service.loop()

    except Exception as e:
        msg = f'ZoltraakFileCleaner: stopped with error {e}'
        service.logger.write_error(msg)

    except KeyboardInterrupt:
        msg = 'ZoltraakFileCleaner: stopped with KeyboardInterrupt'
        service.logger.write_debug(msg)

    else:
        msg = 'ZoltraakFileCleaner: stop without errors'
        service.logger.write_info(msg)


if __name__ == '__main__':
    main()
