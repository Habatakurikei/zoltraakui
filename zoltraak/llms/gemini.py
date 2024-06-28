import google.generativeai as genai

from zoltraak.settings import gemini_api_key


MODEL = 'gemini-1.5-flash'


genai.configure(api_key=gemini_api_key)


def generate_response(model=MODEL,
                      prompt='',
                      max_tokens=65536,
                      temperature=0.7):
    """
    Gemini APIを使用してプロンプトに対する応答を生成する関数。

    Args:
        prompt (str): 応答を生成するためのプロンプト。

    Returns:
        str: 生成された応答テキスト。
    """
    # print(f'{MODEL} で生成します。')

    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)

    return response.text.strip()
