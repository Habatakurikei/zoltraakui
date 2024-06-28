# 2024-06-17 DY revised to enable multiple LLM options
import argparse
import os
import subprocess
# import pdb

import zoltraak
from zoltraak.llms.common import call_llm
from zoltraak.converter import MarkdownToPythonConverter


def main():
    parser = argparse.ArgumentParser(
        description="MarkdownファイルをPythonファイルに変換します")
    parser.add_argument("input",
                        help="変換対象のMarkdownファイルのパスまたはテキスト",
                        nargs='?')
    parser.add_argument("--output-dir",
                        help="生成されたPythonファイルの出力ディレクトリ",
                        default="generated")
    parser.add_argument("-p",
                        "--prompt",
                        help="追加のプロンプト情報",
                        default=None)
    parser.add_argument("-c",
                        "--compiler",
                        help="コンパイラー（要件定義書のテンプレート）")
    parser.add_argument("-f",
                        "--formatter",
                        help="コードフォーマッター",
                        default="md_comment")
    parser.add_argument("-cc",
                        "--custom-compiler",
                        help="自作コンパイラー（自作定義書生成文書）")
    parser.add_argument("-v",
                        "--version",
                        action="store_true",
                        help="バージョン情報を表示")
    parser.add_argument("-l",
                        "--language",
                        help="出力言語を指定",
                        default=None)
    parser.add_argument("-d",
                        "--generate-dir",
                        action="store_true",
                        help="要件定義書生成後にディレクトリ生成も実行する")
    parser.add_argument("-m",
                        "--model",
                        help="要件定義書生成に使用する言語モデルを指定",
                        default="anthropic/claude-3-5-sonnet-20240620")

    # pdb.set_trace()
    args = parser.parse_args()

    # print("Arguments:")
    # print(f"input = {args.input}")
    # print(f"-p = {args.prompt}")
    # print(f"-c = {args.compiler}")
    # print(f"-f = {args.formatter}")
    # print(f"-cc = {args.custom_compiler}")
    # print(f"-v = {args.version}")
    # print(f"-l = {args.language}")
    # print(f"-d = {args.generate_dir}")
    # print(f"-m = {args.model}")

    if args.version:
        show_version_and_exit()

    if args.input is None:
        show_usage_and_exit()

    if (args.input.endswith(".md") or
       os.path.isfile(args.input) or
       os.path.isdir(args.input)):
        # 入力がMarkdownファイル、ファイル、またはディレクトリの場合
        if args.compiler is None and args.custom_compiler is None:
            # コンパイラーが指定されていない場合
            args.compiler = "dev_obj"

        elif args.compiler and args.custom_compiler:
            # デフォルトのコンパイラーとカスタムコンパイラーの両方が指定されている場合
            show_compiler_conflict_error_and_exit()

        print("マークダウン処理を開始します。")
        process_markdown_file(args)

    else:
        # 入力がテキストの場合
        if args.compiler and args.custom_compiler:
            # デフォルトのコンパイラーとカスタムコンパイラーの両方が指定されている場合
            show_compiler_conflict_error_and_exit()

        print("テキスト処理を開始します。")
        process_text_input(args)


def show_version_and_exit():
    print(f"zoltraak version {zoltraak.__version__}")
    exit(0)


def show_usage_and_exit():
    print("\033[31mエラー: 入力ファイルまたはテキストが指定されていません。\033[0m")
    print("\033[92m使用方法: zoltraak <mdファイルのパス または テキスト> [オプション]\033[0m")

    msg = "\033[33m例1:\033[0m zoltraak calc.md -p \"ドローンを用いた競技システムを考える\""
    msg += " -c dev_obj"
    print(msg)

    print("  説明: calc.mdファイルを入力とし、ドローンを用いた競技システムの要件定義書を生成します。")
    print("        オブジェクト指向設計のコンパイラー (dev_obj) を使用します。")

    msg = "\033[33m例2:\033[0m zoltraak \"タクシーの経営課題を解決するための戦略ドキュメントを作成する\""
    msg += " -c biz_consult"
    print(msg)

    print("  説明: プロンプトテキストを入力とし、タクシー会社の経営課題解決のための戦略ドキュメントを生成します。")
    print("        ビジネスコンサルティング用のコンパイラー (biz_consult) を使用します。")

    msg = "\033[33m例3:\033[0m zoltraak \"レストランの予約管理システムの要件定義書\""
    msg += " -cc custom_compiler.md"
    print(msg)

    print("  説明: プロンプトテキストを入力とし、レストランの予約管理システムの要件定義書を生成します。")
    print("        カスタムコンパイラー (custom_compiler.md) を使用します。")
    exit(1)


def show_compiler_error_and_exit():
    print("\033[31mエラー: コンパイラーが指定されていません。\033[0m")
    print("-c オプションでデフォルトのコンパイラーを指定するか、")
    print("-cc オプションで自作のコンパイラー（要件定義書のテンプレート）のファイルパスを指定してください。")
    print("\033[92mデフォルトのコンパイラー:\033[0m")
    print("\033[33m- dev_obj: オブジェクト指向設計を用いた開発タスクに関する要件定義書を")
    print("生成するコンパイラ\033[0m")
    print("  説明: オブジェクト指向の原則に基づいて、開発タスクの要件定義書を生成します。クラス図、シーケンス図、")
    print("ユースケースなどを含みます。")
    print("\033[33m- dev_func: 関数型プログラミングを用いた開発タスクに関する要件定義書を")
    print("生成するコンパイラ\033[0m")
    print("  説明: 関数型プログラミングの原則に基づいて、開発タスクの要件定義書を生成します。純粋関数、不変性、")
    print("高階関数などの概念を取り入れます。")
    print("\033[33m- biz_consult: ビジネスコンサルティングに関するドキュメントを生成するコンパイラ\033[0m")
    print("  説明: 企業の課題解決や戦略立案のためのコンサルティングドキュメントを生成します。市場分析、SWOT分析、")
    print("アクションプランなどを含みます。")
    print("\033[33m- general_def: 一般的な開発タスクに関する要件定義書を生成するコンパイラ\033[0m")
    print("  説明: 様々な開発タスクに対応した汎用的な要件定義書を生成します。システムの目的、機能要件、")
    print("非機能要件などを網羅します。")
    print("\033[33m- general_reqdef: 一般的な要求事項に関する要件定義書を生成するコンパイラ\033[0m")
    print("  説明: システム開発以外の一般的な要求事項について、要件定義書を生成します。プロジェクトの目標、")
    print("スコープ、制約条件などを明確にします。")
    exit(1)


def show_compiler_conflict_error_and_exit():
    print("\033[31mエラー: -c オプションと -cc オプションは同時に指定できません。\033[0m")
    exit(1)


def process_markdown_file(args):
    """
    Markdownファイルを処理する
    """
    md_file_path = args.input
    output_dir = os.path.abspath(args.output_dir)
    model = args.model
    prompt = args.prompt

    zoltraak_dir = os.path.dirname(zoltraak.__file__)

    if args.custom_compiler:
        # カスタムコンパイラーが指定されている場合
        compiler_path = get_custom_compiler_path(args.custom_compiler)

    else:
        # カスタムコンパイラーが指定されていない場合
        if args.compiler == "None":
            compiler_path = None
        else:
            compiler_path = os.path.join(zoltraak_dir,
                                         "grimoires/compiler",
                                         args.compiler)
            compiler_path += ("" if args.compiler.endswith(".md") else ".md")
            # print(f"デフォルトコンパイラーのパス: {compiler_path}")

    if compiler_path is not None and not os.path.exists(compiler_path):
        msg = f"コンパイラ {compiler_path} が存在しないため"
        msg += "検索モードに切り替わります。"
        print(msg)
        compiler_path = None

    formatter_path = os.path.join(zoltraak_dir,
                                  "grimoires/formatter",
                                  args.formatter)
    formatter_path += ("" if args.formatter.endswith(".md") else ".md")

    language = None if args.language is None else args.language

    # print("compiler_path:", compiler_path)
    # print("formatter_path:", formatter_path)
    # print("language:", args.language)

    md_file_rel_path = os.path.relpath(md_file_path, os.getcwd())
    py_file_rel_path = os.path.splitext(md_file_rel_path)[0] + ".py"
    py_file_path = os.path.join(output_dir, py_file_rel_path)

    mtp = MarkdownToPythonConverter(md_file_path,
                                    py_file_path,
                                    model=model,
                                    prompt=prompt,
                                    compiler_path=compiler_path,
                                    formatter_path=formatter_path,
                                    language=language,
                                    generate_directry=args.generate_dir)

    # Pythonファイルの出力ディレクトリを作成（既に存在する場合は何もしない）
    os.makedirs(os.path.dirname(py_file_path), exist_ok=True)

    mtp.convert()


def get_custom_compiler_path(custom_compiler):
    compiler_path = os.path.abspath(custom_compiler)
    if not os.path.exists(compiler_path):
        print(f"エラー: 指定されたカスタムコンパイラーのファイル '{compiler_path}' ")
        print("が存在しません。以下の点を確認してください:")
        print("1. ファイルが指定されたパスに存在することを確認してください。")
        print("2. カスタムコンパイラーのファイルパスが正しいことを確認してください。")
        print("3. ファイル名の拡張子が '.md' であることを確認してください。")
        print("4. ファイルの読み取り権限があることを確認してください。")
    # print(f"カスタムコンパイラー: {compiler_path}")
    return compiler_path


def process_text_input(args):

    text = args.input

    md_file_path = generate_md_file_name(text)
    print(f"新しい要件定義書 {md_file_path} が生成されました。")

    cmd = f'zoltraak {md_file_path} '

    if '\"' not in text:
        text = f'\"{text}\"'

    cmd += f'-p {text} '

    if args.custom_compiler:
        cmd += f'-cc {args.custom_compiler} '

    else:
        cmd += f'-c {args.compiler} '

    cmd += f'-f {args.formatter} '
    cmd += f'-l {args.language} '
    cmd += f'-m {args.model}'

    if args.generate_dir:
        cmd += ' -d'

    print(f'再帰呼び出しをします: {cmd}')

    subprocess.run(cmd.split(" "))


def generate_md_file_name(prompt):

    print("空の要件定義書を作成します。")

    # requirementsディレクトリが存在しない場合は作成する
    requirements_dir = "requirements"
    if not os.path.exists(requirements_dir):
        os.makedirs(requirements_dir)

    # zoltraak/requirements/内のファイル名を全て取得
    existing_files = [file for file in os.listdir(requirements_dir)
                      if file.startswith("def_")]
    # print("existing_files:", existing_files)

    # 既存のファイル名と被らないようにファイル名を生成するプロンプトを作成
    # file_name_prompt = f"「{prompt}」"
    # file_name_prompt += "を想定した要件定義書のファイル名をdef_hogehoge.mdの形式で提案してください。"
    # file_name_prompt = f"{prompt}"
    # file_name_prompt += "に基づいて要件定義書のファイル名をdef_hogehoge.mdの形式で提案してください。"
    # file_name_prompt += "ただし、以下の既存のファイル名と重複しないようにしてください。\n"
    # file_name_prompt += f"{', '.join(existing_files)}\n"
    # file_name_prompt += "ファイル名を1つだけ英語で返してください。日本語は使わないでください。"

    to_ask = f'Please suggest a file name that represents "{prompt}". '
    to_ask += 'The format shall be def_hogehoge.md. '
    to_ask += 'And do not suggest existing file names such that: \n'
    to_ask += f"{', '.join(existing_files)}.\n"
    to_ask += 'Return the file name only. No descriptions are needed.'

    # print("file_name_prompt:", to_ask)

    file_name = call_llm(prompt=to_ask, temperature=0.3)

    return file_name
