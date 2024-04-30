import base64
import os
import site
from subprocess import Popen
from subprocess import PIPE

import streamlit as st


COMMAND = 'zoltraak'
UI_TITLE = ':sparkles: Zoltraak'

GRIMOIRES_LOCATION = 'zoltraak/grimoires'
COMPILER_PATH = 'compiler'
FORMATTER_PATH = 'formatter'
HOLD_PATH = 'hold_path.txt'

COMPILER_NOT_USED = 'おまかせ'
FORMATTER_NOT_USED = '使わない'
GENERATED_MD_COMMENT = '魔法術式を構築しました'

default_compiler = ''
formatter = ''
user_compiler = ''

process = None


# Supporting functions

def _find_grimoires_path():
    '''
    Return path of grimoires in site-packages to list up automatically.
    '''
    for entry in site.getsitepackages():
        for root, _, _ in os.walk(entry):
            if root.endswith(GRIMOIRES_LOCATION):
                return root

    return None


def _list_default_compilers():
    '''
    Return list of default compilers.
    '''
    global grimoires_path

    to_seek = os.path.join(grimoires_path, COMPILER_PATH)

    full_list = sorted(os.listdir(to_seek))

    md_files = [i for i in full_list if i.endswith('.md')]

    md_files.insert(0, COMPILER_NOT_USED)

    return md_files


def _list_formatters():
    '''
    Return list of formatters.
    '''
    global grimoires_path

    to_seek = os.path.join(grimoires_path, FORMATTER_PATH)

    full_list = sorted(os.listdir(to_seek))

    md_files = [i for i in full_list if i.endswith('.md')]

    md_files.insert(0, FORMATTER_NOT_USED)

    return md_files


def _make_command():
    '''
    Make command line based on different options applied.
    '''
    global prompt, default_compiler, user_compiler, formatter

    command_list = [COMMAND, f'\"{prompt}\"']

    if default_compiler == COMPILER_NOT_USED:
        pass

    elif user_compiler is None:
        command_list.append('-c')
        command_list.append(default_compiler)

    else:
        command_list.append('-cc')
        command_list.append(user_compiler)

    if formatter != FORMATTER_NOT_USED:
        command_list.append('-f')
        command_list.append(formatter)

    return command_list


def _find_generated_file(process):
    '''
    Return generated md file name from stdout.
    '''
    stdout, stderr = process.communicate()

    print(f'STDOUT = {stdout.decode("utf-8")}')
    print(f'STDERR = {stderr.decode("utf-8")}')

    generated_file = ''

    if any(stdout):

        source = stdout.decode('utf-8')

        for line in source.split('\n'):
            if GENERATED_MD_COMMENT in line:
                generated_file = line.split(':')[1]
                generated_file = generated_file.split('.md')[0]
                generated_file = generated_file.replace(' ', '')
                generated_file += '.md'
                break

    return generated_file


def _write_path_file(to_write):
    '''
    Save text file containing path to generated markdown.
    '''
    if any(to_write):
        with open(HOLD_PATH, 'w', encoding='utf-8') as f:
            f.write(to_write)

    else:
        st.error('生成したファイルを見つけることができませんでした')
        _delete_path_file()


def _delete_path_file():
    if os.path.exists(HOLD_PATH):
        os.remove(HOLD_PATH)


def _generate_download_link(md_file_path):
    '''
    Return hyperlink tag of downloadable generated md file from path.
    '''
    save_as = os.path.split(md_file_path)[1]

    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_contents = f.read()
        b64 = base64.b64encode(md_contents.encode()).decode()
        a_tag = f'<a href="data:text/plain;base64,{b64}" '
        a_tag += f"download=\'{save_as}\'>右クリックで保存する</a>"

    return a_tag


# Main screen

st.set_page_config(page_title=UI_TITLE, page_icon='sparkler')
st.title(UI_TITLE)

print(f'generated markdown to load = {os.path.exists(HOLD_PATH)}')
if os.path.exists(HOLD_PATH):
    # get path of generated md file
    with open(HOLD_PATH, 'r', encoding='utf-8') as f:
        to_load = f.read()

    # read md file and show on main screen
    with open(to_load, 'r', encoding='utf-8') as f:
        st.markdown(f.read())

    col_clear, col_save = st.columns(2)

    with col_clear:
        if st.button('結果を消去', key='clear'):
            _delete_path_file()
            st.rerun()

    with col_save:
        download_link = _generate_download_link(to_load)
        st.markdown(download_link, unsafe_allow_html=True)

# Sidebar

prompt = st.sidebar.text_area('プロンプト')

grimoires_path = _find_grimoires_path()

print(f'grimoires_path = {grimoires_path}')

if grimoires_path is None:
    st.error('コンパイラのフォルダを見つけることができませんでした')

else:
    default_compiler = st.sidebar.selectbox('標準コンパイラ',
                                            _list_default_compilers())

    formatter = st.sidebar.selectbox('フォーマッター', _list_formatters())

    user_compiler = st.sidebar.file_uploader('自作コンパイラ', type='md')

print(f'default_compiler = {default_compiler}')
print(f'formatter = {formatter}')
print(f'user_compiler = {user_compiler}')

if st.sidebar.button('生成', key='call'):

    if not any(prompt):
        st.error('プロンプトを入力してください')

    else:
        to_call = _make_command()

        print(f'Call = {to_call}')
        process = Popen(to_call, shell=False, stdout=PIPE, stderr=PIPE)

        process.wait()

        path_found = _find_generated_file(process)

        _write_path_file(path_found)

        print(f'Saved as {path_found}')

        st.rerun()
