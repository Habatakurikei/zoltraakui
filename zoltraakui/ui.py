import os
import random
from datetime import datetime as dt

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
    msg = '標準コンパイラ（魔導書）のフォルダを見つけることができませんでした。'
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
            st.code(f.read(), language='markdown')


def markdown_zip(to_load):
    '''
    Notify if zip file generated
    '''
    if any(to_load):
        msg = f':package: `{to_load}` 生成物が Zip 形式として '
        msg += '**:red[ポン出し]** されています。'
        st.write(msg)


def fetch_compiler_information(dict_description, selected_compiler):
    '''
    Return compiler key and description respectively from selected compiler
    '''
    key = ''
    description = ''

    if selected_compiler in dict_description:
        key = dict_description[selected_compiler]['compiler']
        description = f'> {dict_description[selected_compiler]["description"]}'

    else:
        description = f'> {config["constants"]["description_not_found"]}'

    return key, description


def write_domain_warning():
    msg = '指定されたコマンドでは領域展開を省略します。ご了承ください。'
    st.warning(msg)


def print_command(command_list):
    command_text = ' '.join(command_list)
    time_stamp = dt.now().isoformat(timespec='seconds')
    print(f'cmd {time_stamp} - {command_text}')


def markdown_command(command_list):
    command_text = ' '.join(command_list)
    msg = f':male_mage: あなたは`{command_text}`を唱えた！'
    st.write(msg)


def show_progress_image():
    if random.randint(0, 1) % 2 == 0:
        st.image(config['files']['progress_image_even'], use_column_width=True)
    else:
        st.image(config['files']['progress_image_odd'], use_column_width=True)


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
