import shutil
import time

import streamlit as st
from zoltraakklein import ZoltraakKlein

from config import COMPILER_ADVICE_MSG
from config import COMPILER_CONFIRM_MSG
from config import COMPILER_DESCRIPTION
from config import COMPILER_OPTION_MSG
from config import COMPILER_OPTIONS
from config import COMPILER_SELECT_MSG
from config import CONFIRM_FULL_EXPANSION_MSG
from config import CONFIRM_SINGLE_EXPANSION_MSG
from config import DOMAIN_EXPANSION_MSG
from config import DOMAIN_LIMIT_MSG
from config import LLM_GEN_RD
from config import LLM_NAMING
from config import RD_GENERATION_MSG
from config import REQUEST_INPUT_MSG
from config import USER_DIR
from config import WAIT_FOR_COMPLETION
from config import WAIT_FOR_ERROR
from config import WAIT_FOR_EXPANSION
from config import ZIP_PATH
from ui_body import compiler_selection_button
from ui_body import set_page_title
from ui_body import show_outputs
from ui_body import write_compiler
from ui_body import write_project_name
from ui_body import write_request
from ui_body import write_takt_time
from ui_sidebar import markdown_sidebar_footer
from ui_sidebar import markdown_sidebar_header
from ui_sidebar import show_instruction
from ui_sidebar import write_instruction_information
from utils import fetch_instruction
from utils import generate_zip
from utils import Progress
from utils import sanitize_prompt


def _initialize():

    set_page_title()

    if not ZIP_PATH.is_dir():
        ZIP_PATH.mkdir(exist_ok=True)
    if 'category' not in st.session_state:
        st.session_state.category = None
    if 'compiler' not in st.session_state:
        st.session_state.compiler = None
    if 'instruction' not in st.session_state:
        st.session_state.instruction = None
    if 'progress' not in st.session_state:
        st.session_state.progress = None
    if 'zip_path' not in st.session_state:
        st.session_state.zip_path = None
    if 'zk' not in st.session_state:
        st.session_state.zk = None


def _cleanup():
    if st.session_state.zk.project_path.is_dir():
        shutil.rmtree(str(st.session_state.zk.project_path))
    if st.session_state.zip_path:
        st.session_state.zip_path.unlink()
        st.session_state.zip_path = None
    if 'request' in st.session_state:
        del st.session_state.request
    st.session_state.instruction = None
    st.session_state.progress = None
    st.session_state.zk = None


@st.dialog("コンパイラの確認")
def _confirm_compiler(compiler: str):
    global COMPILER_ADVICE_MSG, COMPILER_OPTION_MSG
    st.write(COMPILER_CONFIRM_MSG)
    st.write(COMPILER_OPTION_MSG.format(compiler=compiler))
    st.write(COMPILER_ADVICE_MSG.format(
        advice=COMPILER_DESCRIPTION[compiler]['advice']))
    request = sanitize_prompt(st.text_input(REQUEST_INPUT_MSG))
    if st.button("要件定義書を生成する"):
        if request:
            st.session_state.request = request
            st.rerun()
        else:
            st.error("リクエスト内容を入力してください")


@st.dialog("プロジェクト削除の確認")
def _confirm_cleanup():
    st.write("**:red[本当に削除しますか？]**")
    if st.button("はい"):
        st.session_state.clear = True
        st.rerun()


@st.dialog("領域展開（一段）の確認")
def _confirm_single_expansion():
    st.write(CONFIRM_SINGLE_EXPANSION_MSG)
    if st.button("はい"):
        st.session_state.single_expansion = True
        st.rerun()


@st.dialog("領域展開（全開）の確認")
def _confirm_full_expansion():
    st.write(CONFIRM_FULL_EXPANSION_MSG)
    if st.button("はい"):
        st.session_state.full_expansion = True
        st.rerun()


def _generate_rd(bar):
    '''
    Generate project name and RD documents.
    '''
    st.session_state.progress.next()
    bar.progress(st.session_state.progress.percent(),
                 text=st.session_state.progress.text())
    st.session_state.zk.name_for_requirement(**LLM_NAMING)
    st.session_state.progress.next()
    bar.progress(st.session_state.progress.percent(),
                 text=st.session_state.progress.text())
    st.session_state.zk.generate_requirement(**LLM_GEN_RD)


def _expand_domain(bar):
    '''
    Conduct single domain expansion.
    '''
    st.session_state.progress.next()
    bar.progress(st.session_state.progress.percent(),
                 text=st.session_state.progress.text())
    try:
        st.session_state.zk.expand_domain()
        while st.session_state.zk.expansion_in_progress:
            time.sleep(WAIT_FOR_EXPANSION)
    except Exception as e:
        st.error(f"領域展開中に例外が発生しました: {e}")
        time.sleep(WAIT_FOR_ERROR)


def _show_progress_bar():
    return st.progress(st.session_state.progress.percent(),
                       text=st.session_state.progress.text())


def _show_zk_parameters():
    write_request(st.session_state.request)
    write_compiler(st.session_state.compiler)
    write_takt_time(st.session_state.zk.takt_time)


def _show_buttons():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("削除して最初の画面に戻る"):
            _confirm_cleanup()
    with col2:
        if st.button("領域展開（一段）"):
            _confirm_single_expansion()
    with col3:
        if st.button("領域展開（全開）"):
            _confirm_full_expansion()
    with col4:
        st.session_state.zip_path = generate_zip(st.session_state.zk)
        if st.session_state.zip_path.exists():
            with open(st.session_state.zip_path, "rb") as f:
                st.download_button(label="生成物ダウンロード",
                                   data=f,
                                   file_name=st.session_state.zip_path.name,
                                   mime="application/octet-stream")
        else:
            st.session_state.zip_path = None
            st.warning("ダウンロードできるファイルが生成されていません")


def _show_outputs():
    st.subheader(":crown: 生成物ショーケース", divider="gray")
    write_project_name(st.session_state.zk.project_name)
    show_outputs(st.session_state.zk.project_menu)


def _render_main_screen():

    if 'clear' in st.session_state:
        del st.session_state.clear
        _cleanup()
        st.rerun()

    if 'single_expansion' in st.session_state:
        del st.session_state.single_expansion
        bar = _show_progress_bar()
        if st.session_state.zk.is_expansion_capable():
            st.info(DOMAIN_EXPANSION_MSG)
            _show_zk_parameters()
            _show_outputs()
            _expand_domain(bar)
        else:
            st.error(DOMAIN_LIMIT_MSG)
            time.sleep(WAIT_FOR_ERROR)
        st.rerun()

    if 'full_expansion' in st.session_state:
        bar = _show_progress_bar()
        if st.session_state.zk.is_expansion_capable():
            st.info(DOMAIN_EXPANSION_MSG)
            _show_zk_parameters()
            _show_outputs()
            _expand_domain(bar)
        else:
            st.warning("領域展開完了")
            time.sleep(WAIT_FOR_COMPLETION)
            del st.session_state.full_expansion
        st.rerun()

    elif isinstance(st.session_state.zk, ZoltraakKlein):
        bar = _show_progress_bar()
        if not st.session_state.zk.project_name:
            st.info(RD_GENERATION_MSG)
            _generate_rd(bar)
            st.rerun()
        else:
            _show_zk_parameters()
            _show_buttons()
            _show_outputs()

    elif 'request' in st.session_state:
        id = COMPILER_DESCRIPTION[st.session_state.compiler]['identifier']
        st.session_state.zk = ZoltraakKlein(
            compiler=id,
            request=st.session_state.request,
            work_dir=USER_DIR)
        st.session_state.instruction = fetch_instruction(id)
        st.session_state.progress = Progress(0, st.session_state.zk.limit)
        st.rerun()

    elif st.session_state.compiler:
        answer = compiler_selection_button(st.session_state.compiler)
        if answer:
            _confirm_compiler(st.session_state.compiler)

    else:
        st.warning('コンパイラを選択してください')


def _render_sidebar():

    markdown_sidebar_header()

    if isinstance(st.session_state.zk, ZoltraakKlein):
        write_instruction_information(st.session_state.compiler)
        show_instruction(st.session_state.instruction.config,
                         st.session_state.zk.current_power)

    else:
        st.sidebar.markdown(COMPILER_SELECT_MSG)
        st.session_state.category = st.sidebar.selectbox(
            ':bookmark: **カテゴリ**', COMPILER_OPTIONS.keys())
        st.session_state.compiler = st.sidebar.radio(
            ':notebook: **:green[コンパイラ]**',
            COMPILER_OPTIONS[st.session_state.category].keys(),
            index=0,
            horizontal=False)

    markdown_sidebar_footer()


def main():
    _initialize()
    _render_sidebar()
    _render_main_screen()


if __name__ == '__main__':
    main()
