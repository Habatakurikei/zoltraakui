import os
from subprocess import Popen
from subprocess import PIPE

import streamlit as st


COMMAND = 'zoltraak'
UI_TITLE = ':sparkles: Zoltraak'

DEFAULT_COMPILERS = ['dev_func', 'dev_obj', 'biz_consult', 'general_def', 'general_reqdef', 'dev_react_fastapi']
OUTPUT_PATH = 'requirements/'

generated_file = ''
compiler_selected = ''
user_compiler = ''
process = None


# Supporting functions

def _find_generated_file(process):

    global generated_file

    stdout, stderr = process.communicate()

    if stdout:
        generated_file = stdout.decode('utf-8')
        # print(f'STDOUT = {stdout}')
        generated_file = generated_file.split('\r\n')[-2]

    else:
        generated_file = ''

    return generated_file


def _show_generated_file():

    global generated_file

    if not any(generated_file):
        return

    col_clear, col_save = st.columns(2)

    with col_clear:
        if st.button('結果を消去', key='clear'):
            generated_file = ''
            st.experimental_rerun()

    with col_save:
        if st.button('結果を保存', key='save'):
            pass

    with open(generated_file, 'r', encoding='utf-8') as f:
        st.markdown(f.read())


# Main screen

st.set_page_config(page_title=UI_TITLE, page_icon='sparkler')
st.title(UI_TITLE)


# Sidebar

prompt = st.sidebar.text_area('プロンプト')

compiler_selected = st.sidebar.selectbox('標準コンパイラ', DEFAULT_COMPILERS)
user_compiler = st.sidebar.file_uploader('自作コンパイラ', type='md')

if st.sidebar.button('生成', key='call'):

    if not any(prompt):
        st.error('プロンプトを入力してください')

    else:
        to_call = [COMMAND, f'\"{prompt}\"']

        if user_compiler is None:
            to_call.append('-c')
            to_call.append(compiler_selected)

        else:
            to_call.append('-cc')
            to_call.append(user_compiler)

        process = Popen(to_call, shell=False, stdout=PIPE, stderr=PIPE)
        process.wait()

        generated_file = os.path.join(OUTPUT_PATH, _find_generated_file(process))
        print(f'Saved as {generated_file}')

        _show_generated_file()
