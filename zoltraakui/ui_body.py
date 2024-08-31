from pathlib import Path

import streamlit as st
from zoltraakklein.yaml_manager import YAMLManager

from config import COMPILER_DESCRIPTION
from config import COMPILER_OPTIONS
from config import IMAGE_PATH
from config import MENU_ITEM_SUM_MSG
from config import MENU_NONEXIST_ERROR_MSG
from config import MENU_NO_CONTENT_MSG
from config import PROGRESS_BAR_STYLE
from config import TITLE
from ui_tabs import show_menu
from ui_tabs import TAB_OUTPUT_LIST


def compiler_selection_button(compiler: str):
    '''
    Show the relevant image and description of the compiler.
    And set a selection button to proceed request input.
    '''
    ans = False
    img = next((v for k, d in COMPILER_OPTIONS.items()
                for i, v in d.items() if i == compiler), None)
    st.image(str(IMAGE_PATH / img),
             caption=compiler,
             use_column_width=False)
    st.markdown(COMPILER_DESCRIPTION[compiler]['description'])
    if st.button('このコンパイラを選択', key='execute'):
        ans = True
    return ans


def set_page_title():
    '''
    Set the page title and icon.
    Also set the progress bar style.
    '''
    title = TITLE
    icon = 'sparkles'
    st.set_page_config(page_title=title, page_icon=icon, layout='wide')
    st.title(f':{icon}: {title}')
    st.markdown(PROGRESS_BAR_STYLE, unsafe_allow_html=True)


def show_outputs(menu_path: Path):
    '''
    Main function to show all the production contents.
      1. show sum of generated files
      2. show full list of menu
      3. show each production content
    '''
    global MENU_ITEM_SUM_MSG
    if not menu_path.exists():
        st.error(MENU_NONEXIST_ERROR_MSG)
    else:
        menu_source = YAMLManager(str(menu_path))
        st.write(MENU_ITEM_SUM_MSG.format(sum=menu_source.sum_of_items()))
        menu_dict = menu_source.config
        menu_items = [key for key in TAB_OUTPUT_LIST
                      if key in menu_dict.keys()]
        tab_names = [TAB_OUTPUT_LIST[key]['name'] for key in TAB_OUTPUT_LIST
                     if key in menu_dict.keys()]
        if not any(tab_names):
            st.error(MENU_NO_CONTENT_MSG)
        else:
            tabs = st.tabs(["生成物一覧（メニュー）"]+tab_names)
            with tabs[0]:
                show_menu(menu_path)
            for (entry, key) in zip(tabs[1:], menu_items):
                with entry:
                    to_do = TAB_OUTPUT_LIST[key]['function']
                    to_do(menu_dict[key].values())


def write_compiler(compiler: str):
    msg = f':notebook: コンパイラ： **{compiler}**'
    st.write(msg)


def write_project_name(project_name: str):
    msg = f':file_folder: プロジェクト名： **{project_name}**'
    st.write(msg)


def write_request(request: str):
    msg = f':lower_left_fountain_pen: リクエスト内容： **{request}**'
    st.write(msg)


def write_takt_time(takt_time: dict[str, float]):
    '''
    Show the takt time.
    '''
    minutes, seconds = divmod(sum(takt_time.values()), 60)
    msg = f":stopwatch: タクトタイム： **合計 {int(minutes)} 分 {seconds:.1f} 秒**"
    msg += " 【内訳】"
    for work, elapsed_time in takt_time.items():
        if work == "naming":
            msg += f"命名：{elapsed_time:.1f} 秒"
        elif work == "rd_generation":
            msg += f"/要件定義生成：{elapsed_time:.1f} 秒"
        else:
            step = work.split('_')[-1]
            msg += f"/領域展開火力 {int(step)}：{elapsed_time:.1f} 秒"
    st.write(msg)
