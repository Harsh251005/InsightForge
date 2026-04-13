from openai import OpenAI
from config.settings import Settings
from utils.prompt_loader import load_prompt

client = OpenAI(api_key=Settings.OPENAI_API_KEY)


def decompose_query(query: str):

    prompt_template = load_prompt("decompose_prompt")
    prompt = prompt_template.format(query=query)

    response = client.chat.completions.create(
        model=Settings.MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.choices[0].message.content

    # simple parsing
    sub_queries = []
    for line in text.split("\n"):
        line = line.strip()
        if line and any(char.isdigit() for char in line[:2]):
            sub_queries.append(line.split(".", 1)[-1].strip())

    return sub_queries