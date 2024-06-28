import os
import shutil
import time

from logger import PythonLogger


DIR_LIST = ['generated', 'generated/requirements', 'requirements',
            'user_compiler', 'zip']

LOG_FILE = 'zoltraak_file_cleaner.log'

TIME_TORELANCE = 3600
INTERVAL_SEC = 3600


class ZoltraakFileCleaner:

    def __init__(self):
        self.logger = PythonLogger(save_as=LOG_FILE)

    def _cleanup_folder(self, target_dir):

        time_now = time.time()

        for candidate in sorted(os.listdir(target_dir)):

            focus = os.path.join(target_dir, candidate)
            time_diff = time_now - os.path.getctime(focus)

            msg = f'File {focus}, Diff = {time_diff:.3f} ? {TIME_TORELANCE} '

            if os.path.isdir(candidate):
                msg += '>> FOLDER SKIP'

            elif TIME_TORELANCE < time_diff:
                if os.path.isdir(focus):
                    shutil.rmtree(focus)
                else:
                    os.remove(focus)
                msg += '>> DELETED'

            else:
                msg += '>> NOT deleted'

            self.logger.write_info(msg)

    def loop(self):

        while True:

            msg = f'loop: start cleaning. Tolerance = {TIME_TORELANCE}'
            self.logger.write_info(msg)

            start_time = time.time()

            for entry in DIR_LIST:
                self.logger.write_info(f'loop: target = {entry}')
                if os.path.isdir(entry):
                    self._cleanup_folder(entry)
                else:
                    msg = f'loop: folder {entry} not existed. Skipped.'
                    self.logger.write_error(msg)

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
