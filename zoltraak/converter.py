# 2024-05-28 DY fully revised to follow PEP8
import difflib
import hashlib
import os
import subprocess
import sys
import threading

from zoltraak.llms.common import call_llm
from zoltraak.gencode import TargetCodeGenerator
from zoltraak.md_generator import generate_md_from_prompt
from zoltraak.md_generator import show_spinner


class MarkdownToPythonConverter:

    def __init__(self,
                 md_file_path,
                 py_file_path,
                 model=None,
                 prompt=None,
                 compiler_path=None,
                 formatter_path=None,
                 language=None,
                 generate_directry=False):
        self.md_file_path = md_file_path
        self.py_file_path = py_file_path
        self.model = model
        self.prompt = prompt
        self.compiler_path = compiler_path
        self.formatter_path = formatter_path
        self.language = language
        self.generate_directry = generate_directry

    def convert(self):

        if self.prompt is None:
            # プロンプトが指定されていない場合
            self.source_file_path = self.md_file_path
            self.target_file_path = self.py_file_path
            self.past_source_folder = "past_md_files"

        else:
            # プロンプトが指定されている場合
            self.source_file_path = self.md_file_path
            self.target_file_path = self.md_file_path
            self.past_source_folder = "past_prompt_files"

            if os.path.exists(self.md_file_path):
                # マークダウンファイルが存在する場合
                msg = f"{self.md_file_path} は既存のファイルです。プロンプトに従って変更を提案します。"
                print(msg)
                self.propose_target_diff(self.target_file_path, self.prompt)
                return

        # for debug
        # print(f'source_file_path = {self.source_file_path}')
        # print(f'target_file_path = {self.target_file_path}')
        # print(f'past_source_folder = {self.past_source_folder}')

        if os.path.exists(self.source_file_path):
            # ソースファイルが存在する場合
            self.source_hash = self.calculate_file_hash(self.source_file_path)
            os.makedirs(self.past_source_folder, exist_ok=True)
            self.past_source_file_path = os.path.join(
                self.past_source_folder,
                os.path.basename(self.source_file_path))
        else:
            self.past_source_file_path = None
            self.source_hash = None

        if os.path.exists(self.target_file_path):
            # ターゲットファイルが存在する場合
            self.handle_existing_target_file()
        else:
            self.handle_new_target_file()

    def calculate_file_hash(self, file_path):
        with open(file_path, "rb") as file:
            content = file.read()
            return hashlib.md5(content).hexdigest()

    def handle_existing_target_file(self):
        with open(self.target_file_path, "r", encoding="utf-8") as target_file:
            lines = target_file.readlines()
            if len(lines) > 0 and lines[-1].startswith("# HASH: "):
                embedded_hash = lines[-1].split("# HASH: ")[1].strip()
                if self.source_hash == embedded_hash:
                    if self.prompt is None:
                        cmd = [sys.executable, self.target_file_path]
                        print(f'再帰呼び出しをします: {" ".join(cmd)}')
                        subprocess.run(cmd)
                    else:
                        to_read = self.target_file_path
                        with open(to_read, "r", encoding="utf-8") as md_file:
                            md_content = md_file.read()
                        return md_content
                else:
                    print(f"{self.source_file_path}の変更を検知しました。")
                    print("ソースファイルの差分:")
                    if os.path.exists(self.past_source_file_path):
                        self.display_source_diff()

    def display_source_diff(self):

        to_read = self.past_source_file_path
        with open(to_read, "r", encoding="utf-8") as old_source_file:
            old_source_lines = old_source_file.readlines()

        to_read = self.source_file_path
        with open(to_read, "r", encoding="utf-8") as new_source_file:
            new_source_lines = new_source_file.readlines()

        source_diff = difflib.unified_diff(old_source_lines,
                                           new_source_lines,
                                           lineterm='',
                                           n=0)
        source_diff_text = ''.join(source_diff)

        print(source_diff_text)

        if self.prompt is not None:
            self.propose_target_diff(self.target_file_path, self.prompt)
            print(f"ターゲットファイル: {self.target_file_path}")

        else:
            self.handle_target_file_modification()

    def handle_new_target_file(self):

        if self.prompt is None:
            # 下記の変数をGeneratorに渡す前にパスを指定しないと読み込みエラーになる
            if 'requirements' not in self.source_file_path:
                self.source_file_path = 'requirements/' + self.source_file_path

            if 'requirements' not in self.target_file_path:
                buff = self.target_file_path.split('/')
                buff.insert(-1, 'requirements')
                self.target_file_path = '/'.join(buff)

            target_file_path_base = os.path.split(self.target_file_path)[1]

            print(f"""
高級言語コンパイル中: {target_file_path_base} は新しいファイルです。処理にお時間をいただきます。
{self.source_file_path} -> {target_file_path_base}
                  """)

            target = TargetCodeGenerator(self.source_file_path,
                                         self.target_file_path,
                                         self.past_source_file_path,
                                         self.source_hash)
            target.generate_target_code()

        else:

            if self.compiler_path is None:
                task_str = "検索結果生成中"
            else:
                task_str = "要件定義書執筆中"

            msg = f"{task_str}: {self.target_file_path} は新しいファイルです。"
            msg += "処理にお時間をいただきます。"
            print(msg)

            generate_md_from_prompt(
                self.model,
                self.prompt,
                self.target_file_path,
                compiler_path=self.compiler_path,
                formatter_path=self.formatter_path,
                language=self.language,
                open_file=True
            )

            # moved from md_generator.py
            if self.generate_directry:
                # ユーザーがyと答えた場合、zoltraakコマンドを実行してディレクトリを構築
                spinner_done = False
                spinner_msg = "ステップ2. **:green[魔法術式]** から領域を構築"
                spinner_thread = threading.Thread(
                    target=show_spinner,
                    args=(lambda: spinner_done, spinner_msg))
                spinner_thread.start()

                cmd = ["zoltraak", self.target_file_path]
                print(f'再帰呼び出しをします: {" ".join(cmd)}')

                subprocess.run(cmd)

                spinner_done = True
                spinner_thread.join()

    def propose_target_diff(self, target_file_path, prompt):
        """
        ターゲットファイルの変更差分を提案する関数

        Args:
            target_file_path (str): 現在のターゲットファイルのパス
            prompt (str): promptの内容
        """
        # プロンプトにターゲットファイルの内容を変数として追加
        with open(target_file_path, "r", encoding="utf-8") as target_file:
            current_target_code = target_file.read()

        prompt = f'''
下記の三連バッククォート内に書かれているコンテンツを修正したいです。
```
{current_target_code}
```

要求内容：{prompt}

要求内容を満たせるように元のコンテンツをどう修正すべきか差分を返してください。
結果は下記に示す Unified Diff 形式で返してください。解説は不要です。

Unified Diff 形式の例：
@@ -1,4 +1,4 @@
 line1
-line2
+line2 modified
 line3
-line4
+line4 modified
        '''
        target_diff = call_llm(prompt=prompt, temperature=0.0)

        # ターゲットファイルの差分を表示
        print("ターゲットファイルの差分:")
        print(target_diff)

        # 差分をターゲットファイルに自動で適用
        print("差分はAIが処理します。")

        self.apply_diff_to_target_file(target_file_path, target_diff)
        print(f"{target_file_path} に差分を自動で適用しました。")

    def apply_diff_to_target_file(self, target_file_path, target_diff):
        """
        提案された差分をターゲットファイルに適用する関数

        Args:
            target_file_path (str): ターゲットファイルのパス
            target_diff (str): 適用する差分
        """
        # ターゲットファイルの現在の内容を読み込む
        with open(target_file_path, "r", encoding="utf-8") as file:
            current_content = file.read()

        # プロンプトを作成してAPIに送信し、修正された内容を取得
        prompt = f'''
下記の三連バッククォート内に書かれているコンテンツを修正したいです。
```
{current_content}
```

修正したい内容は Unified Diff 形式ですでに下記のように用意されています。
{target_diff}

元のコンテンツにこの修正を反映させてコンテンツ全体を更新してください。
修正後のコンテンツ全体を三連バッククォート無しで返してください。解説は不要です。
        '''

        modified_content = call_llm(prompt=prompt, temperature=0.3)

        # 修正後の内容をターゲットファイルに書き込む
        with open(target_file_path, "w", encoding="utf-8") as file:
            file.write(modified_content)

        # print(f"{target_file_path}に修正を適用しました。")
