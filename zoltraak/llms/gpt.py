from openai import OpenAI

# from zoltraak.settings import openai_api_key

# MODEL = 'gpt-4o'
MODEL = 'gpt-4o-2024-05-13'


def generate_response(model=MODEL,
                      prompt='',
                      max_tokens=4096,
                      temperature=0.7):

    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # print(f'Response={response.choices[0].message}')

    return response.choices[0].message.content.strip()
