import os
import shutil
import time

import streamlit as st

from cast import cast_zoltraak
from cast import make_first_command
from cast import make_option_commands
from cast import make_refine_command
from config import config
from config import dict_default_compilers
from config import domain_option_list
# from config import formatter_list
from config import grimoires_path
from config import llm_list
from logger import LEVEL_INFO
from logger import PythonLogger
from ui import fetch_compiler_information
from ui import generate_download_button
from ui import markdown_command
from ui import markdown_introduction
from ui import markdown_requirement
from ui import markdown_zip
# from ui import print_command
from ui import set_page_title
from ui import show_progress_image
from ui import stop_ui
from ui import write_zoltraak_version
from utils import delete_user_compiler
from utils import find_code_path


LOG_FILE = 'zoltraakui.log'


def _initialize():

    zip_location = config['paths']['zip']
    if not os.path.isdir(zip_location):
        os.mkdir(zip_location)

    user_compiler_location = config['paths']['user_compiler']
    if not os.path.isdir(user_compiler_location):
        os.mkdir(user_compiler_location)

    if 'prompt' not in st.session_state:
        st.session_state.prompt = ''

    if 'default_compiler' not in st.session_state:
        st.session_state.default_compiler = ''

    if 'upload_key' not in st.session_state:
        st.session_state.upload_key = 0

    if 'uploaded_object' not in st.session_state:
        st.session_state.uploaded_object = None

    if 'formatter' not in st.session_state:
        st.session_state.formatter = ''

    if 'language' not in st.session_state:
        st.session_state.language = ''

    if 'req_gen_mode' not in st.session_state:
        st.session_state.req_gen_mode = config['llms']['gpt']

    if 'to_expand_domain' not in st.session_state:
        st.session_state.to_expand_domain = config['constants']['make_dir_no']

    if 'command' not in st.session_state:
        st.session_state.command = ''

    if 'generated_requirement' not in st.session_state:
        st.session_state.generated_requirement = ''

    if 'code_path' not in st.session_state:
        st.session_state.code_path = ''

    if 'zip_path' not in st.session_state:
        st.session_state.zip_path = ''

    if 'logger' not in st.session_state:
        st.session_state.logger = PythonLogger(save_as=LOG_FILE,
                                               level=LEVEL_INFO)


def _cleanup():

    if st.session_state.uploaded_object is not None:
        delete_user_compiler(st.session_state.uploaded_object)
        st.session_state.uploaded_object = None
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

    if any(st.session_state.command):
        st.session_state.command = ''


def _process_main_screen():

    set_page_title()

    has_requirement_generated = os.path.exists(
        st.session_state.generated_requirement)

    # print(f'generated requirement found = {has_requirement_generated}')

    if not has_requirement_generated:
        st.image(config['files']['eyecatch'], use_column_width=True)

    else:
        markdown_command(st.session_state.command)
        markdown_requirement(st.session_state.generated_requirement)

        col_clear, col_save = st.columns(2)

        with col_clear:
            if st.button('結果を消去', key='clear'):
                _cleanup()
                st.rerun()

        with col_save:
            st.session_state.code_path = find_code_path(
                st.session_state.generated_requirement)
            st.session_state.zip_path = generate_download_button(
                st.session_state.generated_requirement)

        markdown_zip(st.session_state.zip_path)

        if st.button('プロンプトを基に修正', key='refine'):
            to_cast = make_refine_command(
                st.session_state.generated_requirement,
                st.session_state.prompt)

            # 2024-05-21 Disabled options for refinement.
            # This usage might be confused for both developers and users.
            # to_cast.extend(make_option_commands(
            #     st.session_state.default_compiler,
            #     st.session_state.uploaded_object,
            #     st.session_state.formatter,
            #     st.session_state.language))

            # print_command(to_cast)
            st.session_state.logger.write_info(to_cast)
            markdown_command(to_cast)
            st.session_state.command = to_cast

            _ = cast_zoltraak(to_cast)
            time.sleep(3)

            st.rerun()


def _process_sidebar():

    markdown_introduction()

    compiler_selected = st.sidebar.selectbox(
        ':books: 何を作りたいですか？（コンパイラ）',
        list(dict_default_compilers.keys()))

    st.session_state.default_compiler, compiler_description = \
        fetch_compiler_information(dict_default_compilers, compiler_selected)

    st.sidebar.markdown(compiler_description)

    st.session_state.prompt = st.sidebar.text_input(
        ':lower_left_fountain_pen: リクエスト内容（簡潔なプロンプト）')

    # 2024-05-21 Hide formatter option to simplify interface
    # st.session_state.formatter = st.sidebar.selectbox(
    #     'フォーマッター', formatter_list)

    st.session_state.uploaded_object = st.sidebar.file_uploader(
        ':ledger: 自作コンパイラ（オプション）',
        type='md',
        accept_multiple_files=False,
        key=st.session_state.upload_key)

    # 2024-06-23 Hide language option to simplify interface
    # st.session_state.language = st.sidebar.text_input(':a: 使用言語')

    st.session_state.req_gen_mode = st.sidebar.radio(
        ':dizzy: 要件定義書生成モデル',
        llm_list,
        index=0,
        horizontal=False)

    st.session_state.to_expand_domain = st.sidebar.radio(
        ':star2: 領域術式も実行しますか？',
        domain_option_list,
        index=0,
        horizontal=False)

    # print for debug purpose
    # print('*** Parameters for Debug')
    # print(f'prompt = {st.session_state.prompt}')
    # print(f'default_compiler = {st.session_state.default_compiler}')
    # print(f'formatter = {st.session_state.formatter}')
    # print(f'uploaded_object = {st.session_state.uploaded_object}')
    # print(f'req_gen_mode = {st.session_state.req_gen_mode}')
    # print(f'to_expand_domain = {st.session_state.to_expand_domain}')
    # print(f'code_path = {st.session_state.code_path}')
    # print(f'zip_path = {st.session_state.zip_path}')

    if st.sidebar.button('生成', key='cast'):

        if not any(st.session_state.prompt):
            st.error('プロンプトを入力してください')

        else:
            to_cast = make_first_command(st.session_state.prompt)
            to_cast.extend(make_option_commands(
                st.session_state.default_compiler,
                st.session_state.uploaded_object,
                st.session_state.formatter,
                st.session_state.language,
                st.session_state.req_gen_mode,
                st.session_state.to_expand_domain))

            show_progress_image()

            # print_command(to_cast)
            st.session_state.logger.write_info(to_cast)
            markdown_command(to_cast)
            st.session_state.command = to_cast

            st.session_state.generated_requirement = cast_zoltraak(to_cast)
            time.sleep(3)

            st.rerun()

    write_zoltraak_version()


def main():

    if grimoires_path is None:
        stop_ui()

    _initialize()
    _process_main_screen()
    _process_sidebar()


if __name__ == '__main__':
    main()
