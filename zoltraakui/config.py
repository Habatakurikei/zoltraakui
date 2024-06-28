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


def load_default_compilers():
    '''
    Return dictionary information of default compilers.
    '''
    to_load = config['files']['default_compilers_description']
    dict_compilers = {}

    if os.path.isfile(to_load):
        with open(to_load, 'r', encoding='utf-8') as f:
            json_text = f.read()

        dict_compilers = json.loads(json_text)

    return dict_compilers


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


def list_llms():
    llm_list = []
    llm_list.append(config['llms']['gpt'])
    llm_list.append(config['llms']['claude'])
    llm_list.append(config['llms']['gemini'])
    return llm_list


def make_domain_options():
    option_list = []
    option_list.append(config['constants']['make_dir_no'])
    option_list.append(config['constants']['make_dir_yes'])
    return option_list


config = load_config()
zoltraak_version = fetch_zoltraak_version()
grimoires_path = find_grimoires_path()
dict_default_compilers = load_default_compilers()
formatter_list = list_formatters()
llm_list = list_llms()
domain_option_list = make_domain_options()
