from zoltraakklein import ZoltraakKlein


DUMMY_COMPILER_NAME = 'ビジネス書／新書（縦書き）'
DUMMY_COMPILER_ID = 'book_business'
DUMMY_PROJECT_NAME = 'request_conditions_generator'


'''
You can skip RD generation and start domain expansion as debug mode.
Note that menu and RD files are already generated in same project folder.

Steps:

(1) set DUMMY_COMPILER_NAME, DUMMY_COMPILER_ID, DUMMY_PROJECT_NAME

(2) include following to the main.py
from zoltraakui.debug import sideloading_zk
from zoltraakui.debug import DUMMY_COMPILER_NAME
from zoltraakui.debug import DUMMY_COMPILER_ID

(3) replace zk initialization with the following codes
in the bottom of _initialize() function in the main.py
    if 'zk' not in st.session_state:
        st.session_state.zk = sideloading_zk()
        st.session_state.request = 'dummy'
        st.session_state.compiler = DUMMY_COMPILER_NAME
        st.session_state.instruction = fetch_instruction(DUMMY_COMPILER_ID)
        st.session_state.progress = Progress(2, st.session_state.zk.limit)
'''


def sideloading_zk():
    '''
    Sideload the zk instance.
    This function is only for debug purpose.
    '''
    zk = ZoltraakKlein(compiler=DUMMY_COMPILER_ID, request='dummy')
    zk.load_project(project_name=DUMMY_PROJECT_NAME, current_power=5)
    return zk
