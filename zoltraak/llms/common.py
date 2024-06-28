import zoltraak.llms.claude as claude
import zoltraak.llms.gemini as gemini
import zoltraak.llms.gpt as gpt


def call_llm(model='anthropic/claude-3-haiku-20240307',
             prompt='',
             max_tokens=4096,
             temperature=0.7):

    icon = ':dizzy: '
    given_llm = model.split('/')

    if len(given_llm) != 2:
        msg = "言語モデルは google/gemini-1.5-flash のように指定してください"
        raise Exception(msg)

    if "google" in given_llm[0]:
        print(icon + f"Google {given_llm[1]} を召喚します。")
        response = gemini.generate_response(model=given_llm[1],
                                            prompt=prompt,
                                            max_tokens=max_tokens,
                                            temperature=temperature)

    elif "anthropic" in given_llm[0]:
        print(icon + f"Anthropic {given_llm[1]} を召喚します。")
        response = claude.generate_response(model=given_llm[1],
                                            prompt=prompt,
                                            max_tokens=max_tokens,
                                            temperature=temperature)

    elif "openai" in given_llm[0]:
        print(icon + f"OpenAI {given_llm[1]} を召喚します。")
        response = gpt.generate_response(model=given_llm[1],
                                         prompt=prompt,
                                         max_tokens=max_tokens,
                                         temperature=temperature)

    else:
        msg = f"ベンダー名に{given_llm[0]}が指定されました。未対応です。"
        msg += "使用可能なベンダーは anthropic/google/openai のみです。"
        raise Exception(msg)

    print("召喚終了しました。")

    return response
