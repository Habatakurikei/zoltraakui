import os

import streamlit as st

from config import config
from config import zoltraak_version
from utils import find_code_path
from utils import generate_zip


def set_page_title():
    page_title = config['ui']['title']
    st.set_page_config(page_title=page_title, page_icon='sparkles')
    st.title(':sparkles: ' + page_title)


def stop_ui():
    msg = 'グリモワール（標準コンパイラ）のフォルダを見つけることができませんでした。'
    msg += 'Zoltraakが正しくインストールされているか確認してください。'
    st.error(msg)
    st.stop()


def write_zoltraak_version():
    msg = f'Powered with Zoltraak ver. {zoltraak_version}'
    st.sidebar.write(msg)


def markdown_introduction():
    msg = '初めてですか? &#10697; '
    msg += f'[アプリ紹介と使い方]({config["ui"]["guide_link"]})'
    st.sidebar.write(msg)


def markdown_requirement(to_load):
    '''
    Read md file and show on main screen
    '''
    if any(to_load):
        st.write(f':orange_book: `{to_load}`')

        with open(to_load, 'r', encoding='utf-8') as f:
            st.markdown(f.read())


def fetch_compiler_description(description_dictionary, selected_compiler):

    description = ''

    if selected_compiler in description_dictionary:
        description = f'> {description_dictionary[selected_compiler]}'

    else:
        description = f'> {config["constants"]["description_not_found"]}'

    return description


def markdown_command(command_list):
    command_text = ' '.join(command_list)
    msg = f':male_mage: あなたは`{command_text}`を唱えた！'
    st.write(msg)


def generate_download_button(generated_requirement):
    '''
    Make download button for generated docs.
    '''
    zip_path = ''
    code_path = find_code_path(generated_requirement)

    if any(code_path):
        zip_path = generate_zip(generated_requirement, code_path)
        save_as = os.path.split(zip_path)[-1]

        with open(zip_path, 'rb') as f:
            st.download_button(label='zip保存',
                               data=f,
                               file_name=save_as,
                               mime='application/octet-stream')

    else:
        save_as = os.path.split(generated_requirement)[-1]

        with open(generated_requirement, 'r', encoding='utf-8') as f:
            st.download_button(label='md保存',
                               data=f,
                               file_name=save_as,
                               mime='text/plain;charset=UTF-8')

    return zip_path


def write_progress(line):
    st.write(line)
