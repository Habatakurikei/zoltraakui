import json
import os
import shutil
import site
from io import StringIO
from subprocess import check_output
from subprocess import Popen
from subprocess import PIPE

import streamlit as st


COMMAND_CAST = 'zoltraak'
COMMAND_VERSION = ['zoltraak', '-v']

UI_TITLE = 'Zoltraak'

APP_GUIDE_PAGE = 'https://github.com/Habatakurikei/zoltraak_ui'
APP_GUIDE_LINK = f'初めてですか？ &#10697;[アプリ紹介と使い方]({APP_GUIDE_PAGE})'

GRIMOIRES_LOCATION = 'zoltraak/grimoires'
DEFAULT_COMPILER_LOCATION = 'compiler'
FORMATTER_LOCATION = 'formatter'
CODE_LOCATION = 'generated'
PREFIX_REQUIREMENT = 'def_'

ZIP_LOCATION = 'zip'
CODE_FOLDER = 'code'
USER_COMPILER_LOCATION = 'user_compiler'
COMPILERS_DESCRIPTION_LOCATION = 'compilers_description.json'

COMPILER_NOT_SELECTED = 'おまかせ'
FORMATTER_NOT_USED = '使わない'
GENERATED_MD_COMMENT = '魔法術式を構築しました'
SKIP_COMMENT = 'を構築中'
DESCRIPTION_NOT_FOUND = '説明文が見つかりませんでした。'


process = None


# Supporting functions

def _get_zoltraak_version():
    response = check_output(COMMAND_VERSION)
    response = response.decode('utf-8').replace('\n', '')
    return response


def _initialize():

    if 'zoltraak_version' not in st.session_state:
        st.session_state.zoltraak_version = _get_zoltraak_version()

    if not os.path.isdir(ZIP_LOCATION):
        os.mkdir(ZIP_LOCATION)

    if not os.path.isdir(USER_COMPILER_LOCATION):
        os.mkdir(USER_COMPILER_LOCATION)

    if 'grimoires_path' not in st.session_state:
        st.session_state.grimoires_path = _find_grimoires_path()

    if 'compilers_description' not in st.session_state:
        st.session_state.compilers_description = _load_compliers_description()

    if 'compiler_list' not in st.session_state:
        st.session_state.compiler_list = _list_default_compilers()

    if 'formatter_list' not in st.session_state:
        st.session_state.formatter_list = _list_formatters()

    if 'prompt' not in st.session_state:
        st.session_state.prompt = _list_formatters()

    if 'default_compiler' not in st.session_state:
        st.session_state.default_compiler = []

    if 'upload_key' not in st.session_state:
        st.session_state.upload_key = 0

    if 'upload_object' not in st.session_state:
        st.session_state.upload_object = None

    if 'user_compiler' not in st.session_state:
        st.session_state.user_compiler = ''

    if 'formatter' not in st.session_state:
        st.session_state.formatter = ''

    if 'language' not in st.session_state:
        st.session_state.language = ''

    if 'command' not in st.session_state:
        st.session_state.command = ''

    if 'generated_requirement' not in st.session_state:
        st.session_state.generated_requirement = ''

    if 'code_path' not in st.session_state:
        st.session_state.code_path = ''

    if 'zip_path' not in st.session_state:
        st.session_state.zip_path = ''


def _find_grimoires_path():
    '''
    Return path of grimoires in site-packages to list up automatically.
    '''
    for entry in site.getsitepackages():
        for root, _, _ in os.walk(entry):
            if root.endswith(GRIMOIRES_LOCATION):
                return root

    return None


def _load_compliers_description():
    '''
    Return dictionary of default compilers description.
    '''
    if os.path.isfile(COMPILERS_DESCRIPTION_LOCATION):
        with open(COMPILERS_DESCRIPTION_LOCATION, 'r', encoding='utf-8') as f:
            json_text = f.read()
        return json.loads(json_text)

    return {}


def _write_compiler_description():

    description = ''

    if (st.session_state.default_compiler in
       st.session_state.compilers_description):
        key = st.session_state.default_compiler
        description = f'> {st.session_state.compilers_description[key]}'

    else:
        description = f'> {DESCRIPTION_NOT_FOUND}'

    return description


def _list_default_compilers():
    '''
    Return list of default compilers.
    '''
    to_seek = os.path.join(st.session_state.grimoires_path,
                           DEFAULT_COMPILER_LOCATION)

    full_list = sorted(os.listdir(to_seek))

    md_files = [i.replace('.md', '') for i in full_list if i.endswith('.md')]

    md_files.insert(0, COMPILER_NOT_SELECTED)

    return md_files


def _list_formatters():
    '''
    Return list of formatters.
    '''
    to_seek = os.path.join(st.session_state.grimoires_path, FORMATTER_LOCATION)

    full_list = sorted(os.listdir(to_seek))

    md_files = [i for i in full_list if i.endswith('.md')]

    md_files.insert(0, FORMATTER_NOT_USED)

    return md_files


def _find_user_compiler():
    '''
    Save user compiler and return name from Streamlit UploadedFile style.
    '''
    user_compiler = ''

    if st.session_state.upload_object is not None:
        user_compiler = os.path.join(USER_COMPILER_LOCATION,
                                     st.session_state.upload_object.name)

    return user_compiler


def _make_first_command():
    '''
    Make command line based on different options applied.
    '''
    command_list = [COMMAND_CAST, f'\"{st.session_state.prompt}\"']

    if (any(st.session_state.default_compiler) or
       any(st.session_state.user_compiler)):
        command_list.extend(_add_option_commands())

    return command_list


def _make_refine_command():
    '''
    Make command line for refining generated documents
    '''
    source = st.session_state.generated_requirement

    command_list = [COMMAND_CAST, source, '-p', f'\"{st.session_state.prompt}\"']

    if (any(st.session_state.default_compiler) or
       any(st.session_state.user_compiler)):
        command_list.extend(_add_option_commands())

    return command_list


def _add_option_commands():

    command_list = []

    if st.session_state.default_compiler == COMPILER_NOT_SELECTED:
        pass

    elif not any(st.session_state.user_compiler):
        command_list.append('-c')
        command_list.append(st.session_state.default_compiler)

    else:
        _upload_user_compiler()
        command_list.append('-cc')
        command_list.append(st.session_state.user_compiler)

    if st.session_state.formatter != FORMATTER_NOT_USED:
        command_list.append('-f')
        command_list.append(st.session_state.formatter)

    if any(st.session_state.language):
        command_list.append('-l')
        command_list.append(st.session_state.language)

    return command_list


def _upload_user_compiler():

    if st.session_state.upload_object is not None:
        to_read = st.session_state.upload_object.getvalue()
        stringio = StringIO(to_read.decode('utf-8'))

        with open(st.session_state.user_compiler, 'w', encoding='utf-8') as f:
            f.write(stringio.read())


def _markdown_command(command_list):
    command_text = ' '.join(command_list)
    command_md = f':male_mage: あなたは`{command_text}`を唱えた！'
    return command_md


def _find_requirement_file(source):
    candidate_requirement = source.split(':')[1]
    candidate_requirement = candidate_requirement.split('.md')[0]
    candidate_requirement = candidate_requirement.replace(' ', '')
    candidate_requirement += '.md'
    return candidate_requirement


def _seek_code_path():

    project_name = os.path.split(st.session_state.generated_requirement)[-1]
    project_name = project_name.replace(PREFIX_REQUIREMENT, '')
    project_name = project_name.replace('.md', '')

    to_seek = os.path.join(CODE_LOCATION, project_name)

    answer = to_seek if os.path.isdir(to_seek) else ''

    return answer


def _generate_zip():

    project_name = os.path.split(st.session_state.code_path)[-1]

    work_path = os.path.join(ZIP_LOCATION, project_name)

    # Make a work folder
    if os.path.isdir(work_path):
        shutil.rmtree(work_path)

    os.mkdir(work_path)

    # Copy files, then execute zip
    shutil.copy(st.session_state.generated_requirement, work_path)
    shutil.copytree(st.session_state.code_path,
                    os.path.join(work_path, CODE_FOLDER))

    save_as = os.path.join(ZIP_LOCATION, project_name)
    shutil.make_archive(save_as, 'zip', root_dir=work_path)

    # Clean up work folder
    shutil.rmtree(work_path)

    return save_as + '.zip'


def _generate_download_button():
    '''
    Make download button for generated docs.
    '''
    if any(st.session_state.code_path):
        st.session_state.zip_path = _generate_zip()
        save_as = os.path.split(st.session_state.zip_path)[-1]

        with open(st.session_state.zip_path, 'rb') as f:
            st.download_button(label='zip保存',
                               data=f,
                               file_name=save_as,
                               mime='application/octet-stream')

    else:
        to_handle = st.session_state.generated_requirement
        save_as = os.path.split(to_handle)[-1]

        with open(to_handle, 'r', encoding='utf-8') as f:
            st.download_button(label='md保存',
                               data=f,
                               file_name=save_as,
                               mime='text/plain;charset=UTF-8')


def _cleanup():

    if any(st.session_state.user_compiler):
        os.remove(st.session_state.user_compiler)
        st.session_state.user_compiler = ''
        st.session_state.upload_key += 1

    if any(st.session_state.code_path):
        shutil.rmtree(st.session_state.code_path)
        st.session_state.code_path = ''

    if any(st.session_state.zip_path):
        os.remove(st.session_state.zip_path)
        st.session_state.zip_path = ''

    if any(st.session_state.generated_requirement):
        os.remove(st.session_state.generated_requirement)
        st.session_state.generated_requirement = ''


# Main screen

st.set_page_config(page_title=UI_TITLE, page_icon='sparkles')
st.title(':sparkles: ' + UI_TITLE)

_initialize()

to_seek = st.session_state.generated_requirement
has_requirement_generated = os.path.exists(to_seek)

print(f'generated requirement found = {has_requirement_generated}')

if has_requirement_generated:

    st.write(st.session_state.command)

    # read md file and show on main screen
    st.write(f':orange_book: `{to_seek}`')

    with open(to_seek, 'r', encoding='utf-8') as f:
        st.markdown(f.read())

    col_refine, col_save = st.columns(2)

    with col_refine:
        if st.button('プロンプトを基に修正', key='refine'):
            to_call = _make_refine_command()
            st.session_state.command = _markdown_command(to_call)
            st.markdown(st.session_state.command)

            process = Popen(to_call, shell=False, stdout=PIPE, stderr=PIPE)
            process.wait()

            stdout, stderr = process.communicate()
            print(f'STDOUT = {stdout.decode("utf-8")}')
            print(f'STDERR = {stderr.decode("utf-8")}')

            st.rerun()

    with col_save:
        _generate_download_button()

    if st.button('結果を消去', key='clear'):
        st.session_state.command = ''
        st.session_state.generated_requirement = ''
        _cleanup()
        st.rerun()


# Sidebar

print(f'grimoires_path = {st.session_state.grimoires_path}')

if st.session_state.grimoires_path is None:
    message = 'グリモワのフォルダを見つけることができませんでした。'
    message += 'Zoltraakが正しくインストールされているか確認してください。'
    st.error(message)
    st.stop()

st.sidebar.write(APP_GUIDE_LINK)

st.session_state.prompt = st.sidebar.text_area('プロンプト')

st.session_state.default_compiler = st.sidebar.selectbox(
    '標準コンパイラ', st.session_state.compiler_list)

st.sidebar.markdown(_write_compiler_description())

st.session_state.formatter = st.sidebar.selectbox(
    'フォーマッター',
    st.session_state.formatter_list)

# Remining task: upload user compiler and run
st.session_state.upload_object = st.sidebar.file_uploader(
    '自作コンパイラ',
    type='md',
    accept_multiple_files=False,
    key=st.session_state.upload_key)
st.session_state.user_compiler = _find_user_compiler()

st.session_state.language = st.sidebar.text_input('使用言語')

# print for debug purpose
print(f'descriptions = {st.session_state.compilers_description}')
print(f'prompt = {st.session_state.prompt}')
print(f'default_compiler = {st.session_state.default_compiler}')
print(f'formatter = {st.session_state.formatter}')
print(f'upload_object = {st.session_state.upload_object}')
print(f'user_compiler = {st.session_state.user_compiler}')
print(f'language = {st.session_state.language}')

if st.sidebar.button('生成', key='call'):

    if not any(st.session_state.prompt):
        st.error('プロンプトを入力してください')

    else:
        to_call = _make_first_command()
        st.session_state.command = _markdown_command(to_call)
        st.write(st.session_state.command)

        process = Popen(to_call, shell=False, stdout=PIPE, stderr=PIPE)

        while True:
            line = process.stdout.readline()

            if not line and process.poll() is not None:
                break

            elif GENERATED_MD_COMMENT in line.decode('utf-8'):
                generated_file = _find_requirement_file(line.decode('utf-8'))
                st.session_state.generated_requirement = generated_file

            elif SKIP_COMMENT in line.decode('utf-8'):
                pass

            else:
                st.write(line.decode('utf-8'))

        st.session_state.code_path = _seek_code_path()

        print(f'Found file as {st.session_state.generated_requirement}')

        st.rerun()

st.sidebar.write(f'Powered with {st.session_state.zoltraak_version}')
