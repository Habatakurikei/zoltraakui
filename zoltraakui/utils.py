import re
import shutil
from importlib import resources
from pathlib import Path

from zoltraakklein import ZoltraakKlein
from zoltraakklein.yaml_manager import YAMLManager

from config import PROGRESS_BAR_OFFSET
from config import PROGRESS_EXPANSION
from config import PROGRESS_GEN_RD
from config import PROGRESS_NAMING
from config import PROGRESS_READY
from config import TEMPORARY_PATH
from config import ZIP_PATH


class Progress:
    '''
    Manage percent and text for progress bar.
    '''
    def __init__(self, progress: int, limit: int):
        self._progress = progress
        self._limit = limit + PROGRESS_BAR_OFFSET

    def next(self):
        self._progress += 1

    def percent(self):
        return round(self._progress / self._limit * 100)

    def text(self):
        global PROGRESS_EXPANSION
        text = ":male_mage: "
        if self._progress == 0:
            text += PROGRESS_READY
        elif self._progress == 1:
            text += PROGRESS_NAMING
        elif self._progress == 2:
            text += PROGRESS_GEN_RD
        elif 3 <= self._progress:
            text += PROGRESS_EXPANSION.format(power=self._fire())
        else:
            text += "?"
        return text + f" ({self.percent()} %)"

    def _fire(self):
        fire_list = [":fire:"] * (self._progress-PROGRESS_BAR_OFFSET)
        return "".join(fire_list)


def fetch_instruction(compiler: str):
    '''
    Fetch the instruction yaml document for the given compiler.
    The library is under zoltraakklein site-package.
    '''
    instruction_path = resources.files('zoltraakklein.instructions')
    instruction_path /= f'{compiler}.yaml'
    return YAMLManager(str(instruction_path))


def generate_zip(zk: ZoltraakKlein):
    '''
    Generate a zip file from the project.
    '''
    output_path = ZIP_PATH / zk.project_name
    output_file = Path(str(output_path) + '.zip')
    work_path = TEMPORARY_PATH / zk.project_name

    if output_file.exists():
        output_file.unlink()

    if work_path.is_dir():
        shutil.rmtree(work_path)

    shutil.copytree(zk.project_path, work_path)
    shutil.make_archive(output_path, 'zip', root_dir=work_path)
    shutil.rmtree(work_path)

    return output_file


def sanitize_prompt(prompt_org: str):
    '''
    Remove all the special characters from the prompt to avoid errors.
    '''
    sanitized_prompt = re.sub(r'\s+', ' ', prompt_org)
    sanitized_prompt = sanitized_prompt.replace(r'\n', '')
    sanitized_prompt = sanitized_prompt.replace(r'\r', '')
    sanitized_prompt = sanitized_prompt.replace(' ', r'\u0020')
    return sanitized_prompt.strip()
