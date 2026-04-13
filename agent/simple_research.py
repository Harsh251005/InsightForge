from tools.web_search import search_web
from openai import OpenAI
from config.settings import Settings
from utils.prompt_loader import load_prompt

client = OpenAI(api_key=Settings.OPENAI_API_KEY)


def generate_report(query: str):

    results = search_web(query, Settings.MAX_SEARCH_RESULTS)

    combined_text = "\n\n".join(
        [f"{r['title']}\n{r['content']}" for r in results]
    )

    prompt_template = load_prompt("research_prompt")

    prompt = prompt_template.format(
        query=query,
        data=combined_text
    )

    response = client.chat.completions.create(
        model=Settings.MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content, results