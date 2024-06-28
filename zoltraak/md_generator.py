# 2024-06-17 DY revised to enable multiple LLM options
import os
import re
import sys
import threading
import time

import zoltraak
from zoltraak.llms.common import call_llm


def generate_md_from_prompt(model_name,
                            goal_prompt,
                            target_file_path,
                            compiler_path=None,
                            formatter_path=None,
                            language=None,
                            open_file=True):
    """
    promptから要件定義書（マークダウンファイル）を生成する関数

    Args:
        goal_prompt (str): 要件定義書の生成に使用するプロンプト
        target_file_path (str): 生成する要件定義書のパス
        compiler_path (str): コンパイラのパス（デフォルトはNone）
        formatter_path (str): フォーマッタのパス（デフォルトはNone）
        open_file (bool): ファイルを開くかどうかのフラグ（デフォルトはTrue）
    """
    # プロンプトコンパイラとプロンプトフォーマッタを変数として受け取る
    if compiler_path is not None and "grimoires" in compiler_path:
        prompt_compiler = os.path.basename(compiler_path)
    else:
        prompt_compiler = compiler_path

    # 汎用言語フォーマッタへの変更
    if language is not None:
        # formatter_pathに_lang.mdが存在するならそれを、しないならformatter_pathのまま
        lang_formatter_path = os.path.splitext(formatter_path)[0] + "_lang.md"
        if os.path.exists(lang_formatter_path):
            formatter_path = lang_formatter_path

    # フォーマッターについて、デフォフォルダの時見栄えをシンプルにする
    if "grimoires" in formatter_path:
        prompt_formatter = os.path.basename(formatter_path)
    else:
        prompt_formatter = formatter_path

    print(f"""
ステップ1. **:red[起動術式]** を用いて **:green[魔法術式]** を構築する
==============================================================
**:red[起動術式]** (プロンプトコンパイラ) : {prompt_compiler}
**:green[魔法術式]** (要件定義書): {target_file_path}
**:blue[錬成術式]** (プロンプトフォーマッタ): {prompt_formatter}
**:gray[言霊]** (LLMベンダー・モデル 名): {model_name}
==============================================================
    """)

    prompt = create_prompt(goal_prompt,
                           compiler_path,
                           formatter_path,
                           language)

    # スピナー処理にて生成処理と途中経過を表示
    spinner_done = False
    spinner_msg = "ステップ1. **:red[起動術式]** を用いて **:green[魔法術式]** を構築"

    spinner_thread = threading.Thread(target=show_spinner,
                                      args=(lambda: spinner_done, spinner_msg))
    spinner_thread.start()

    response = call_llm(model=model_name, prompt=prompt)

    spinner_done = True
    spinner_thread.join()

    # 生成された要件定義書のファイル保存とフラグに応じてファイルを開く
    md_content = response.strip()
    save_md_content(md_content, target_file_path)

    print_generation_result(target_file_path, compiler_path, open_file)


def show_spinner(done, goal):
    """
    スピナーを表示する関数

    Args:
        done (function): スピナーを終了するかどうかを判定する関数
    """
    progress_bar = "━" * 22

    spinner_base = goal + "中... 🪄 "
    spinner_animation = [
        f"{progress_bar[:i]}☆ﾟ.*･｡ﾟ{' ' * (len(progress_bar) - i)}"
        for i in range(1, len(progress_bar) + 1)
    ] + [f"{progress_bar}☆ﾟ.*･｡"]
    spinner = [spinner_base + anim for anim in spinner_animation]

    while not done():
        for cursor in spinner:
            sys.stdout.write(cursor + "\b" * (len(cursor)+100))
            sys.stdout.flush()
            time.sleep(0.1)


def create_prompt(goal_prompt,
                  compiler_path=None,
                  formatter_path=None,
                  language=None):
    """
    LLMへのプロンプトを作成する関数

    Args:
        goal_prompt (str): 要件定義書の生成に使用するプロンプト
        compiler_path (str): コンパイラのパス
        formatter_path (str): フォーマッタのパス

    Returns:
        str: 作成されたプロンプト
    """

    formatter = get_formatter(formatter_path, language)

    if compiler_path is None:
        # 検索関数の起動
        zoltraak_dir = os.path.dirname(zoltraak.__file__)
        compiler_dir = f"{zoltraak_dir}/grimoires/compiler"
        compiler_files = [file for file in os.listdir(compiler_dir)
                          if file.endswith(".md")]

        prompt = "以下のファイルから、goal_promptに最も適したものを選んでください。\n\n"

        for file in compiler_files:
            file_path = os.path.join(compiler_dir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().split("\n")[:3]
            prompt += f"## {file}\n```\n{' '.join(content)}\n```\n\n"

        prompt += f"## goal_prompt\n\n```{goal_prompt}```\n\n"
        prompt += "まず、goal_promptを踏まえて、最初に取るべきステップを明示してください。"
        prompt += "そのステップやgoal_prompt自身と比較して、最も適切なファイルを上位5つ選び、"
        prompt += "それぞれの理由とともに説明してください。また、それぞれの実行プロンプトを、zoltraak "
        prompt += f'\"{goal_prompt}\" -c [ファイル名（拡張子なし）]で、code blockに'
        prompt += '入れて添付してください。' + prompt + formatter

    elif os.path.exists(compiler_path):
        # プロンプトファイルが存在する場合
        with open(compiler_path, "r", encoding="utf-8") as file:
            prompt = file.read().format(prompt=goal_prompt)

        prompt = prompt + formatter

    else:
        # プロンプトファイルが存在しない場合
        print(f"プロンプトファイル {compiler_path} が見つかりません。")
        prompt = ""

    if prompt != "" and language is not None:
        if not formatter_path.endswith("_lang.md"):
            # 言語指定の強調前出しでサンドイッチにしてみる。
            prompt = formatter[formatter.rindex("## Output Language"):]
            prompt += "\n- Follow the format defined in the format section. "
            prompt += "DO NOT output the section itself." + prompt
        elif re.match("(english|英語|en)", language.lower()):
            # 特に英語指示が「デフォルト言語指示」と混同されやすく、効きがやたら悪いので英語の場合は挟み撃ちにする
            prompt = formatter + prompt

    # print(prompt) # デバッグ用
    return prompt


def get_formatter(formatter_path, language=None):
    """
    フォーマッタを取得する関数

    Args:
        formatter_path (str): フォーマッタのパス

    Returns:
        str: フォーマッタの内容
    """
    if formatter_path is None:
        # フォーマッタパスが指定されていない場合
        formatter = ""

    else:
        # フォーマッタパスが指定されている場合
        if os.path.exists(formatter_path):
            with open(formatter_path, "r", encoding="utf-8") as file:
                formatter = file.read()
                if language is not None:
                    # print(formatter_path)
                    if formatter_path.endswith("_lang.md"):
                        formatter = formatter.replace("{language}", language)
                    else:
                        formatter += "\n- You must output everything including"
                        formatter += " code block and diagrams, according to "
                        formatter += "the previous instructions, but make sure"
                        formatter += f"you write your response in {language}."
                        formatter += "\n\n## Output Language\n- You must "
                        formatter += "generate your response using "
                        formatter += f"{language}, which is the language of "
                        formatter += "the formatter just above this sentence."
        else:
            # フォーマッタファイルが存在しない場合
            print(f"フォーマッタファイル {formatter_path} が見つかりません。")
            formatter = ""

    return formatter


def save_md_content(md_content, target_file_path):
    """
    生成された要件定義書の内容をファイルに保存する関数

    Args:
        md_content (str): 生成された要件定義書の内容
        target_file_path (str): 保存先のファイルパス
    """
    requirements_dir = "requirements"
    os.makedirs(requirements_dir, exist_ok=True)

    target_file_name = os.path.basename(target_file_path)
    target_file_path = os.path.join(requirements_dir, target_file_name)

    with open(target_file_path, "w", encoding="utf-8") as target_file:
        target_file.write(md_content)


def print_generation_result(target_file_path, compiler_path, open_file=True):
    """
    要件定義書の生成結果を表示する関数

    Args:
        target_file_path (str): 生成された要件定義書のファイルパス
        compiler_path (str): コンパイラのパス
        open_file (bool): ファイルを開くかどうかのフラグ（デフォルトはTrue）
    """
    req = "requirements"
    target_file_path = f"{req}/{target_file_path}"
    print("")
    print(f"魔法術式を構築しました: {target_file_path}")
