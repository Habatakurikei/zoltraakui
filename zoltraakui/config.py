import json
import os
import site
import yaml
from subprocess import check_output


def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        loaded = yaml.safe_load(f)
    return loaded


def fetch_zoltraak_version():
    response = check_output(config['zoltraak']['version_command'])
    response = response.decode('utf-8').split(' ')[-1]
    return response


def find_grimoires_path():
    '''
    Return path of grimoires in site-packages to list up automatically.
    '''
    for entry in site.getsitepackages():
        for root, _, _ in os.walk(entry):
            if root.endswith(config['paths']['grimoires']):
                return root
    return None


def list_default_compilers():
    '''
    Return list of default compilers.
    '''
    to_seek = os.path.join(grimoires_path,
                           config['paths']['default_compilers'])

    full_list = sorted(os.listdir(to_seek))

    md_files = [i.replace('.md', '') for i in full_list if i.endswith('.md')]

    md_files.insert(0, config['constants']['compiler_not_selected'])

    return md_files


def load_compilers_description():
    '''
    Return dictionary of default compilers description.
    '''
    to_load = config['files']['default_compilers_description']
    if os.path.isfile(to_load):
        with open(to_load, 'r', encoding='utf-8') as f:
            json_text = f.read()
        return json.loads(json_text)
    return {}


def list_formatters():
    '''
    Return list of formatters.
    '''
    to_seek = os.path.join(grimoires_path,
                           config['paths']['formatters'])

    full_list = sorted(os.listdir(to_seek))

    md_files = [i for i in full_list if i.endswith('.md')]

    md_files.insert(0, config['constants']['formatter_not_used'])

    return md_files


config = load_config()
zoltraak_version = fetch_zoltraak_version()
grimoires_path = find_grimoires_path()
compiler_list = list_default_compilers()
compilers_description = load_compilers_description()
formatter_list = list_formatters()
