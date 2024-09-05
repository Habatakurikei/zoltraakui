import json
from importlib import resources
from pathlib import Path


TITLE = "Zoltraak"
AUTHOR_NAME = "ダイブツ"
AUTHOR_SNS = "https://x.com/habatakurikei"
MONJU_TITLE = "マルチAIブレインストーミングmonju"
MONJU_URL = "https://monju.ai/"


# Paths

SYSTEM_DIR = resources.files('zoltraakklein').parent.resolve()
USER_DIR = Path(__file__).parent.resolve()

IMAGE_PATH = USER_DIR / 'images'
TEMPORARY_PATH = USER_DIR / 'zip_work'
ZIP_PATH = USER_DIR / 'zip'

BANNER_PATH = USER_DIR / 'images/zk_banner.png'
ICON_OPENAI_PATH = USER_DIR / 'images/icon_gpt.png'
ICON_ANTHROPIC_PATH = USER_DIR / 'images/icon_claude.png'
ICON_GOOGLE_PATH = USER_DIR / 'images/icon_gemini.png'

# Messages

CONFIRM_SINGLE_EXPANSION_MSG = "**:red[完了までお時間いただきます。本当に実行しますか？]**"
CONFIRM_FULL_EXPANSION_MSG = "**:red[全工程完了まで5分以上かかる場合があります。]**\n\n" + \
    "**:red[同意の上、領域展開を実行しますか？]**"

COMPILER_OPTION_MSG = ":notebook: 選択したコンパイラ：**{compiler}**"
COMPILER_ADVICE_MSG = "💡 リクエスト入力のアドバイス：**{advice}**"

COMPILER_CONFIRM_MSG = \
    "アドバイスにしたがってリクエスト内容を入力し、問題なければ" + \
    "「要件定義書を作成する」ボタンを押してください"

COMPILER_SELECT_MSG = \
    "**何を作ろうとしていますか？** カテゴリと **:green[コンパイラ]** から" + \
    "あなたが作りたいものを1つ選んでください。"

DOMAIN_EXPANSION_MSG = "領域展開中。終わるまでアプリを操作しないでください。"
DOMAIN_LIMIT_MSG = "火力オーバーで領域展開できません"

MENU_NONEXIST_ERROR_MSG = "メニューが見つかりませんでした。生成物を表示できません。"
MENU_NO_CONTENT_MSG = "表示できるコンテンツが見つかりませんでした。"
MENU_ITEM_SUM_MSG = ":books: メニューを除く **{sum}** 個のファイルが記録されています。"

RD_GENERATION_MSG = "要件定義書を生成中。終わるまでアプリを操作しないでください。"

REQUEST_INPUT_MSG = ":lower_left_fountain_pen: リクエスト内容"

# Compiler settings

COMPILER_OPTIONS = {
    "ビジネス": {
        "企画書": "eyecatch_general_proposal.png",
        "事業計画書": "eyecatch_business_plan.png",
        "戦略的コンサル資料": "eyecatch_strategic_consultant.png",
        "市場調査": "eyecatch_marketing_research.png",
        "商談資料（段取り）": "eyecatch_business_negotiation.png",
    },
    "マルチメディア": {
        "ネット記事": "eyecatch_web_article.png",
        "キャラクター設定生成": "eyecatch_virtual_human.png",
        "プレゼン資料": "eyecatch_presentation_marp.png",
        "ビジネス書／新書（縦書き）": "eyecatch_book_business.png",
        "科学／技術解説書（横書き）": "eyecatch_book_technical.png",
        "絵本": "eyecatch_book_picture.png",
    },
    "ライフスタイル": {
        "レシピ考案": "eyecatch_cooking_recipe.png",
        "旅のしおり": "eyecatch_travel_plan.png",
        "コーディネート相談": "eyecatch_outfit_idea.png",
    },
    "システム開発": {
        "プロジェクト要件定義": "eyecatch_project_rd.png",
        "ソフトウェア": "eyecatch_software_development.png",
        "MVPシステム開発提案": "eyecatch_akira_papa.png",
    },
}


def load_compiler_description():
    compiler_description_path = resources.files('zoltraakklein.rosetta')
    compiler_description_path /= 'compiler_description.json'
    return json.loads(compiler_description_path.read_text(encoding='utf-8'))


COMPILER_DESCRIPTION = load_compiler_description()

# Architect settings


def load_architect_description():
    architect_description_path = resources.files('zoltraakklein.rosetta')
    architect_description_path /= 'architect_description.json'
    return json.loads(architect_description_path.read_text(encoding='utf-8'))


ARCHITECT_DESCRIPTION = load_architect_description()

# LLM settings

LLM_NAMING = {
    'naming': {
        'provider': 'anthropic',
        'model': 'claude-3-haiku-20240307'
    }
}

LLM_GEN_RD = {
    'openai': {
        'provider': 'openai',
        'model': 'gpt-4o'
    },
    'anthropic': {
        'provider': 'anthropic',
        'model': 'claude-3-haiku-20240307'
    },
    'google': {
        'provider': 'google',
        'model': 'gemini-1.5-flash-exp-0827'
    }
}

# Progress bar settings

PROGRESS_BAR_OFFSET = 2
PROGRESS_READY = "準備中"
PROGRESS_NAMING = "新規プロジェクトを命名"
PROGRESS_GEN_RD = "要件定義書を生成"
PROGRESS_EXPANSION = "領域展開 **:red[{power}]**"
PROGRESS_BAR_STYLE = """
<style>
.stProgress .st-bo {
    background-color: red;
}
</style>
"""

# Timers for execution

WAIT_FOR_COMPLETION = 3
WAIT_FOR_ERROR = 3
WAIT_FOR_EXPANSION = 1
