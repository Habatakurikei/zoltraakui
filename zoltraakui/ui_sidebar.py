import streamlit as st

from config import AUTHOR_NAME
from config import AUTHOR_SNS
from config import BANNER_PATH
from config import MONJU_TITLE
from config import MONJU_URL
from config import load_architect_description


def markdown_sidebar_footer():
    '''
    Footer information in sidebar.
    '''
    st.sidebar.markdown("---")
    msg = f':iphone: こちらもお試しください：[{MONJU_TITLE}]({MONJU_URL})'
    st.sidebar.write(msg)
    msg = f'**{chr(0x1D54F)}** 制作者： [{AUTHOR_NAME}]({AUTHOR_SNS})'
    st.sidebar.write(msg)


def markdown_sidebar_header():
    '''
    Header information in sidebar.
    '''
    st.sidebar.image(str(BANNER_PATH), use_column_width="auto")


def show_instruction(instruction: dict, steps_done: int):
    '''
    Show instruction document in sidebar.
    Highlight with green for steps completed.
    '''
    architect_dict = load_architect_description()

    msg = ""

    for key, value in instruction.items():
        if key < steps_done:
            msg += f"**:red[火力 {key}:]**\n\n"
            item_format = "  - **:red[{item}]**\n"
        else:
            msg += f"**火力 {key}**:\n\n"
            item_format = "  - **{item}**\n"
        for _, architect in value.items():
            translation = architect_dict[architect.split("(")[0]]
            msg += item_format.format(item=translation)
        msg += "\n"

    st.sidebar.markdown(msg)


def write_instruction_information(compiler: str):
    '''
    Write instruction title in sidebar to show progress of domain expansion.
    '''
    msg = f":orange_book: **{compiler}** の領域展開指示書"
    st.sidebar.write(msg)
