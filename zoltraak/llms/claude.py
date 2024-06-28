import anthropic

from zoltraak.settings import anthropic_api_key


# MODEL = "claude-3-5-sonnet-20240620"
MODEL = "claude-3-haiku-20240307"
# MODEL = "claude-3-sonnet-20240229"
# MODEL = "claude-3-opus-20240229"


def extract_difference(model=MODEL,
                       prompt='',
                       max_tokens=4096,
                       temperature=0.0):

    # print(f'{MODEL} で差分を抽出します。')

    client = anthropic.Anthropic(api_key=anthropic_api_key)

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system="You are a programmer.",
        messages=[
            {"role": "user", "content": prompt}
        ])

    return response.content[0].text.strip()


def generate_response(model=MODEL,
                      prompt='',
                      max_tokens=4096,
                      temperature=0.7):
    """
    Anthropic APIを使用してプロンプトに対する応答を生成する関数。

    Args:
        prompt (str): 応答を生成するためのプロンプト。

    Returns:
        str: 生成された応答テキスト。
    """
    # print(f'{MODEL} で生成します。')

    client = anthropic.Anthropic(api_key=anthropic_api_key)
    # print(prompt)

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )

    # print(response)

    return response.content[0].text.strip()
