from tools.web_search import search_web
from agent.decomposer import decompose_query
from openai import OpenAI
from config.settings import settings
from utils.prompt_loader import load_prompt
from agent.cleaner import clean_results, filter_relevant

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_report(query: str):

    sub_queries = decompose_query(query)

    all_results = []

    for q in sub_queries:
        results = search_web(q, settings.MAX_SEARCH_RESULTS)
        all_results.extend(results)

    all_results = all_results[:10]

    all_results = clean_results(all_results)
    all_results = filter_relevant(all_results, query)

    all_results = all_results[:8]

    combined_text = "\n\n".join(
        [f"{r['title']}\n{r['content']}" for r in all_results]
    )

    prompt_template = load_prompt("research_prompt")

    prompt = prompt_template.format(
        query=query,
        data=combined_text
    )

    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content, all_results