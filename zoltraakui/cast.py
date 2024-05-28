from subprocess import PIPE
from subprocess import Popen

from config import config
from ui import write_progress
from utils import find_requirement_file
from utils import find_user_compiler
from utils import upload_user_compiler


def make_first_command(prompt):
    '''
    Make command line based on different options applied.
    '''
    command_list = [config['zoltraak']['cast_command']]
    command_list.append(f'\"{prompt}\"')
    return command_list


def make_refine_command(source, prompt):
    '''
    Make command line for refining generated documents.
    source: markdown/directry path as source
    '''
    command_list = [config['zoltraak']['cast_command'], source, '-p']
    command_list.append(f'\"{prompt}\"')
    return command_list


def make_option_commands(default_compiler,
                         uploaded_object,
                         formatter,
                         language,
                         to_make_directry):
    '''
    Arrange options for base command based on given parameters.
    '''
    command_list = []

    if uploaded_object is not None:
        upload_user_compiler(uploaded_object)
        user_compiler = find_user_compiler(uploaded_object)
        command_list.append('-cc')
        command_list.append(user_compiler)

    elif default_compiler == config['constants']['compiler_not_selected']:
        pass

    else:
        command_list.append('-c')
        command_list.append(default_compiler)

    if not any(formatter):
        pass

    elif formatter != config['constants']['formatter_not_used']:
        command_list.append('-f')
        command_list.append(formatter)

    if any(language):
        command_list.append('-l')
        command_list.append(language)

    if to_make_directry == config['constants']['make_dir_yes']:
        command_list.append('-d')

    return command_list


def cast_zoltraak(command_list):
    '''
    Execute zoltraak with an given command list.
    Return path to requirement file generated.
    Note: unable to find requirement file from stdout in -p option.
    '''
    generated_file = ''

    keyword = config['constants']['generated_md_comment']

    process = Popen(command_list, shell=False, stdout=PIPE, stderr=PIPE)

    while True:

        line = process.stdout.readline()

        if not line and process.poll() is not None:
            break

        elif config['constants']['skip_comment'] in line.decode('utf-8'):
            pass

        elif keyword in line.decode('utf-8'):
            generated_file = find_requirement_file(line.decode('utf-8'))

        else:
            write_progress(line.decode('utf-8'))

    stdout, stderr = process.communicate()

    print(f'STDOUT = {stdout.decode("utf-8")}')
    print(f'STDERR = {stderr.decode("utf-8")}')

    return generated_file
