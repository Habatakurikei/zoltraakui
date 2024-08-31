from pathlib import Path

import streamlit as st

from config import ICON_ANTHROPIC_PATH
from config import ICON_GOOGLE_PATH
from config import ICON_OPENAI_PATH


TAB_IMAGE_NOT_FOUND_MSG = "ファイルがありませんでした。生成失敗した可能性があります。"
TAB_IMAGE_NOT_SUPPORTED_MSG = "このファイル形式は非対応のため表示できません。"
TAB_TEXT_REMARKS = "複数のファイルがある場合はタブで表示を切り替えてください。"
TAB_VOICE_REMARKS = "Voicevoxの利用規約に従い、音声を含むコンテンツを公衆公開" + \
    "される場合はクレジット「Voicevox: ずんだもん」を記載してください。"

TAB_IMAGE_WIDTH = 448
TAB_IMAGE_LIST = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "svg"]
TAB_VIDEO_LIST = ["mp4", "webm", "ogg", "mp3", "wav", "ogg", "opus"]
LANGUAGE_EXTENSIONS = {
    "abap": "abap", "abnf": "abnf", "as": "actionscript", "ada": "ada",
    "agda": "agda", "al": "al", "g4": "antlr4", "apacheconf": "apacheconf",
    "apex": "apex", "apl": "apl", "applescript": "applescript", "aql": "aql",
    "ino": "arduino", "arff": "arff", "adoc": "asciidoc", "asm": "asm6502",
    "s": "asmatmel", "aspx": "aspnet", "ahk": "autohotkey", "au3": "autoit",
    "avs": "avisynth", "avdl": "avroIdl", "sh": "bash", "bas": "basic",
    "bat": "batch", "bbcode": "bbcode", "bicep": "bicep", "birb": "birb",
    "y": "bison", "bnf": "bnf", "b": "brainfuck", "brs": "brightscript",
    "bro": "bro", "bsl": "bsl", "c": "c", "cfc": "cfscript",
    "chai": "chaiscript", "il": "cil", "clj": "clojure", "cmake": "cmake",
    "cob": "cobol", "coffee": "coffeescript", "conc": "concurnas",
    "cpp": "cpp", "cr": "crystal", "cs": "csharp", "cshtml": "cshtml",
    "csp": "csp", "css": "css", "csv": "csv", "cypher": "cypher", "d": "d",
    "dart": "dart", "dwl": "dataweave", "dax": "dax", "dhall": "dhall",
    "diff": "diff", "django": "django", "zone": "dnsZoneFile",
    "dockerfile": "docker", "dot": "dot", "e": "eiffel", "ebnf": "ebnf",
    "editorconfig": "editorconfig", "ejs": "ejs", "ex": "elixir", "elm": "elm",
    "erb": "erb", "erl": "erlang", "etlua": "etlua", "xlsx": "excelFormula",
    "f": "fortran", "factor": "factor", "false": "falselang", "flow": "flow",
    "rules": "firestoreSecurityRules", "fs": "fsharp", "ftl": "ftl",
    "g": "gap", "gcode": "gcode", "gd": "gdscript", "ged": "gedcom",
    "feature": "gherkin", "git": "git", "glsl": "glsl", "gml": "gml",
    "gn": "gn", "go.mod": "goModule", "go": "go", "graphql": "graphql",
    "groovy": "groovy", "haml": "haml", "hbs": "handlebars", "hs": "haskell",
    "hx": "haxe", "hcl": "hcl", "hlsl": "hlsl", "hoon": "hoon", "hpkp": "hpkp",
    "hsts": "hsts", "http": "http", "icgj": "ichigojam", "icon": "icon",
    "icu": "icuMessageFormat", "idr": "idris", "gitignore": "ignore",
    "i7": "inform7", "ini": "ini", "io": "io", "j": "j", "java": "java",
    "javadoc": "javadoc", "js": "javascript", "jexl": "jexl",
    "ol": "jolie", "jq": "jq", "json": "json", "json5": "json5",
    "jsonp": "jsonp", "jsx": "jsx", "jl": "julia", "keepalived": "keepalived",
    "kmn": "keyman", "kt": "kotlin", "kum": "kumir", "kql": "kusto",
    "tex": "latex", "latte": "latte", "less": "less", "ly": "lilypond",
    "liquid": "liquid", "lisp": "lisp", "ls": "livescript", "ll": "llvm",
    "log": "log", "lol": "lolcode", "lua": "lua", "makefile": "makefile",
    "md": "markdown", "mat": "matlab", "ms": "maxscript", "mel": "mel",
    "mmd": "mermaid", "miz": "mizar", "mongodb": "mongodb",
    "monkey": "monkey", "moon": "moonscript", "n1ql": "n1ql", "n4js": "n4js",
    "hdl": "nand2tetrisHdl", "ns": "naniscript", "nasm": "nasm",
    "neon": "neon", "nevod": "nevod", "nginx": "nginx", "nim": "nim",
    "nix": "nix", "nsi": "nsis", "m": "objectivec", "ml": "ocaml",
    "cl": "opencl", "qasm": "openqasm", "oz": "oz", "gp": "parigp",
    "parser": "parser", "pas": "pascal", "ligo": "pascaligo", "px": "pcaxis",
    "pcode": "peoplecode", "pl": "perl", "php": "php", "pq": "powerquery",
    "ps1": "powershell", "pde": "processing", "prolog": "prolog",
    "promql": "promql", "properties": "properties", "proto": "protobuf",
    "psl": "psl", "pug": "pug", "pp": "puppet", "pure": "pure", "py": "python",
    "purs": "purescript", "pb": "purebasic", "q": "q", "qml": "qml",
    "qore": "qore", "qs": "qsharp", "r": "r", "rkt": "racket", "re": "reason",
    "regex": "regex", "rego": "rego", "rpy": "renpy", "rest": "rest",
    "rip": "rip", "roboconf": "roboconf", "robot": "robotframework",
    "rb": "ruby", "rs": "rust", "sas": "sas", "sass": "sass", "scala": "scala",
    "scm": "scheme", "scss": "scss", "sh-session": "shellSession",
    "tpl": "smarty", "sml": "sml", "sol": "solidity", "sln": "solutionFile",
    "smali": "smali", "st": "smalltalk", "soy": "soy", "sparql": "sparql",
    "spl": "splunkSpl", "sqf": "sqf", "sql": "sql", "nut": "squirrel",
    "stan": "stan", "styl": "stylus", "swift": "swift", "systemd": "systemd",
    "t4": "t4Cs", "tt": "t4Templating", "tap": "tap", "tcl": "tcl",
    "textile": "textile", "toml": "toml", "trickle": "tremor", "tsx": "tsx",
    "tt2": "tt2", "txt": None, "ttl": "turtle", "twig": "twig",
    "typoscript": "typoscript", "uc": "unrealscript", "razor": "uorazor",
    "ts": "typescript", "uri": "uri", "vala": "vala", "vm": "velocity",
    "v": "verilog", "vhd": "vhdl", "vim": "vim", "vb": "visualBasic",
    "warpscript": "warpscript", "wat": "wasm", "webidl": "webIdl",
    "wiki": "wiki", "wl": "wolfram", "wren": "wren", "xml": "xmlDoc",
    "xeoracube": "xeora", "xojo": "xojo", "xq": "xquery", "yaml": "yaml",
    "yang": "yang", "zig": "zig"
}


def set_llm_icon(file_path: Path):
    '''
    Show relevant icon for the LLM given the file path.
    '''
    icon_path = None
    source = file_path.name

    if "openai" in source.lower():
        icon_path = ICON_OPENAI_PATH
    elif "anthropic" in source.lower():
        icon_path = ICON_ANTHROPIC_PATH
    elif "google" in source.lower():
        icon_path = ICON_GOOGLE_PATH

    if icon_path:
        st.image(str(icon_path))


def show_audio(file_list: list[str]):
    st.write(TAB_VOICE_REMARKS)
    for entry in file_list:
        path = Path(entry)
        st.write(f':musical_note: {path.name}')
        if path.is_file():
            ext = path.suffix.lower()[1:]
            st.audio(str(path), format=f"audio/{ext}", start_time=0,
                     loop=False, autoplay=False)
        else:
            st.error(TAB_IMAGE_NOT_FOUND_MSG)


def show_menu(menu: Path):
    st.write(f':memo: {menu.name}')
    st.code(menu.read_text(encoding="utf-8"),
            language="yaml",
            line_numbers=True)


def show_presentation(file_list: list[str]):
    '''
    This function covers for presentation files in pdf and png format.
    Use `streamlit-pdf-viewer` to show pdf files.
    Note that pptx and epub are not supported by streamlit.
    '''
    for entry in file_list:
        path = Path(entry)
        st.write(f':page_facing_up: {path.name}')
        if path.is_file():
            ext = path.suffix.lower()[1:]
            if ext == "md":
                st.code(path.read_text(encoding="utf-8"),
                        language="markdown",
                        line_numbers=True)
            elif ext in TAB_IMAGE_LIST:
                st.image(str(path), width=TAB_IMAGE_WIDTH)
            else:
                st.warning(TAB_IMAGE_NOT_SUPPORTED_MSG)
        else:
            st.error(TAB_IMAGE_NOT_FOUND_MSG)


def show_rd(file_list: list[str]):
    '''
    This funciton covers for main RDs, fixed 3 columns to show in screen.
    '''
    columns = st.columns(len(file_list))
    for (column, entry) in zip(columns, file_list):
        path = Path(entry)
        with column:
            set_llm_icon(path)
            st.write(f':memo: {path.name}')
            if path.is_file():
                st.code(path.read_text(encoding="utf-8"),
                        language="markdown",
                        wrap_lines=True)
            else:
                st.error(TAB_IMAGE_NOT_FOUND_MSG)


def show_text(file_list: list[str]):
    '''
    This function shows text files in each sub-tab.
    '''
    st.write(TAB_TEXT_REMARKS)
    file_names = [Path(file).name for file in file_list]
    sub_tabs = st.tabs(file_names)
    for (sub_tab, entry) in zip(sub_tabs, file_list):
        with sub_tab:
            path = Path(entry)
            st.write(f':memo: {path.name}')
            if path.is_file():
                ext = path.suffix.lower()[1:]
                if ext in LANGUAGE_EXTENSIONS:
                    language = LANGUAGE_EXTENSIONS[ext]
                else:
                    language = None
                st.code(path.read_text(encoding="utf-8"),
                        language=language,
                        line_numbers=True)
            else:
                st.error(TAB_IMAGE_NOT_FOUND_MSG)


def show_vision(file_list: list[str]):
    '''
    This function covers images and vides.
    '''
    for entry in file_list:
        path = Path(entry)
        st.write(f':frame_with_picture: {path.name}')
        if path.is_file():
            ext = path.suffix.lower()[1:]
            if ext in TAB_IMAGE_LIST:
                st.image(str(path), width=TAB_IMAGE_WIDTH)
            elif ext in TAB_VIDEO_LIST:
                st.write(TAB_VOICE_REMARKS)
                st.video(str(path), format=f"video/{ext}", start_time=0,
                         loop=False, autoplay=False, muted=False)
            else:
                st.warning(TAB_IMAGE_NOT_SUPPORTED_MSG)
        else:
            st.error(TAB_IMAGE_NOT_FOUND_MSG)


# Tab Showcase Settings

TAB_OUTPUT_LIST = {
    "3d_model": {
        "name": "3Dモデル",
        "function": show_vision,
    },
    "character_image": {
        "name": "キャラクターアイコン",
        "function": show_vision,
    },
    "character_rd": {
        "name": "キャラクター要件定義",
        "function": show_text,
    },
    "character_voice": {
        "name": "キャラクター音声",
        "function": show_audio,
    },
    "chart": {
        "name": "チャート",
        "function": show_vision,
    },
    "cover_image": {
        "name": "表紙画像",
        "function": show_vision,
    },
    "epub": {
        "name": "EPUB電子書籍",
        "function": show_presentation,
    },
    "epub_pictuire": {
        "name": "EPUB絵本",
        "function": show_presentation,
    },
    "image": {
        "name": "イメージ画像",
        "function": show_vision,
    },
    "image_prompt": {
        "name": "画像生成プロンプト",
        "function": show_text,
    },
    "page_image": {
        "name": "ページ画像",
        "function": show_vision,
    },
    "page_script": {
        "name": "原稿",
        "function": show_text,
    },
    "page_speech": {
        "name": "読み上げ音声",
        "function": show_audio,
    },
    "presentation": {
        "name": "プレゼン資料",
        "function": show_presentation,
    },
    "rd": {
        "name": "要件定義書",
        "function": show_rd,
    },
    "src": {
        "name": "コード／文章",
        "function": show_text,
    },
    "video_pikapikapika": {
        "name": "トレイラー映像",
        "function": show_vision,
    },
    "video_presentation": {
        "name": "プレゼン動画",
        "function": show_vision,
    },
    "voice": {
        "name": "音声",
        "function": show_audio,
    }
}
