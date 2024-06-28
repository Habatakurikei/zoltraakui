# Zoltraak ウェブアプリのコード解説

このページでは Python ファイルに基づいて Zoltraak ウェブアプリケーションの構造と機能の概要を示します。

## 概要

Zoltraak は、ユーザーのプロンプトに基づいて要件とコードを生成する Python ベースのアプリケーションのです。
Streamlit で構築された Web インターフェースを使用し、さまざまな AI モデルと対話してテキストを生成します。

## 主な機能
1. カスタム コンパイラの選択とアップロード
2. 複数の AI モデル (GPT, Claude, Gemini) から選択
3. ユーザー プロンプトに基づく要件定義書生成
4. コード生成（オプション）
5. 生成されたコンテンツのダウンロード オプション (Markdown および Zip)
6. 生成された要件定義の改良

## 主要コンポーネント

### 1. ユーザー インターフェース (ui.py)
- Streamlit ベースのユーザー インターフェースを処理します
- ページ レイアウト、ボタン、およびユーザー入力を管理します
- 生成された要件を表示し、ダウンロード オプションを提供します

### 2. 構成 (config.py)
- YAML ファイルから構成を読み込みます
- パス、コンパイラ情報、およびアプリケーション設定を管理します
- 使用可能なフォーマッタと LLM を一覧表示する関数を提供します

### 3. ユーティリティ関数 (utils.py)
- ファイル操作を処理します (パスの検索、zip ファイルの生成)
- ユーザー入力をサニタイズします
- ユーザーがアップロードしたコンパイラを管理します

### 4. ログ記録 (logger.py)
- ローテーション付きのカスタム ログ記録システムを実装します

### 5. メイン アプリケーション ロジック (main.py)
- アプリケーションの状態を初期化します
- メイン画面とサイドバー コンポーネントを管理します
- ユーザーの操作を処理し、Zoltraak をトリガーしますコマンド

### 6. Zoltraak コマンド実行 (cast.py)
- Zoltraak のコマンドライン引数を構築します
- Zoltraak コマンドを実行し、その出力を処理します

### 7. ファイル クリーニング サービス (zoltraak_file_cleaner.py)
- 生成されたファイルとフォルダーを定期的にクリーンアップします
- ファイル削除ボタンが別でありますが、ユーザー様がファイルを消し忘れた場合でもプライバシーを保護するために働きます

### 注
- アプリケーションは複数の言語とフォーマッタをサポートしているようですが、一部のオプションは現在 UI に表示されていません
- アプリケーションは Zoltraak のバージョン管理システムを使用します
- 安全対策が講じられています無効な入力を処理します、例えば半角スペースなど
- この解説は Claude 3.5 Sonnet の Archifact で生成されました

## 図解

### クラス図

```mermaid
classDiagram
    class PythonLogger {
        -logger: Logger
        -handler: RotatingFileHandler
        +__init__(save_as: str, level: str)
        +write_debug(message: str)
        +write_info(message: str)
        +write_error(message: str)
        +__del__()
    }

    class ZoltraakFileCleaner {
        -logger: PythonLogger
        +__init__()
        -_cleanup_folder(target_dir: str)
        +loop()
    }

    class Config {
        +load_config()
        +fetch_zoltraak_version()
        +find_grimoires_path()
        +load_default_compilers()
        +list_formatters()
        +list_llms()
        +make_domain_options()
    }

    class Utils {
        +find_user_compiler(uploaded_object)
        +upload_user_compiler(uploaded_object)
        +sanitize_prompt(prompt_org: str)
        +eligible_to_expand_domain(selected_compiler: str)
        +delete_user_compiler(uploaded_object)
        +find_requirement_file(source: str)
        +find_code_path(generated_requirement: str)
        +generate_zip(generated_requirement: str, code_path: str)
    }

    class UI {
        +set_page_title()
        +stop_ui()
        +write_zoltraak_version()
        +markdown_introduction()
        +markdown_requirement(to_load)
        +markdown_zip(to_load)
        +fetch_compiler_information(dict_description, selected_compiler)
        +write_domain_warning()
        +print_command(command_list)
        +markdown_command(command_list)
        +show_progress_image()
        +generate_download_button(generated_requirement)
        +write_progress(line)
    }

    class Cast {
        +make_first_command(prompt: str)
        +make_refine_command(source: str, prompt: str)
        +make_option_commands(default_compiler, uploaded_object, formatter, language, llm, to_expand_domain)
        +cast_zoltraak(command_list)
    }

    class MainApplication {
        -_initialize()
        -_cleanup()
        -_process_main_screen()
        -_process_sidebar()
        +main()
    }

    MainApplication --> PythonLogger
    MainApplication --> Config
    MainApplication --> Utils
    MainApplication --> UI
    MainApplication --> Cast
    ZoltraakFileCleaner --> PythonLogger
    Cast --> Utils
    Cast --> UI
```

### シーケンス図

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant MainApplication
    participant Config
    participant Cast
    participant Zoltraak
    participant Utils
    participant Logger

    User->>UI: Enter prompt and settings
    UI->>MainApplication: Trigger generation
    MainApplication->>Config: Load configuration
    MainApplication->>Cast: Prepare command
    Cast->>Utils: Sanitize inputs
    Cast->>Zoltraak: Execute command
    Zoltraak->>Logger: Log progress
    Logger->>UI: Display progress
    Zoltraak-->>Cast: Return generated files
    Cast-->>MainApplication: Process results
    MainApplication->>Utils: Generate zip (if needed)
    MainApplication->>UI: Update display
    UI-->>User: Show results and download options
    
    opt User requests refinement
        User->>UI: Request refinement
        UI->>MainApplication: Trigger refinement
        MainApplication->>Cast: Prepare refinement command
        Cast->>Zoltraak: Execute refinement
        Zoltraak->>Logger: Log progress
        Logger->>UI: Display progress
        Zoltraak-->>Cast: Return refined files
        Cast-->>MainApplication: Process refined results
        MainApplication->>UI: Update display
        UI-->>User: Show refined results
    end
```
