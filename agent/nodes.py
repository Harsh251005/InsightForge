from agent.decomposer import decompose_query
from tools.web_search import search_web
from config.settings import settings
from agent.cleaner import clean_results, filter_relevant
from openai import OpenAI
from utils.prompt_loader import load_prompt

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def decomposer_node(state):
    sub_queries = decompose_query(state["query"])
    return {"sub_queries": sub_queries}


def search_node(state):
    all_results = []

    for q in state["sub_queries"]:
        results = search_web(q, settings.MAX_SEARCH_RESULTS)
        all_results.extend(results)

    return {"results": all_results}


def filter_node(state):
    cleaned = clean_results(state["results"])
    filtered = filter_relevant(cleaned, state["query"])

    return {"filtered_results": filtered}


def report_node(state):

    combined_text = "\n\n".join(
        [f"{r['title']}\n{r['content']}" for r in state["filtered_results"]]
    )

    prompt_template = load_prompt("research_prompt")

    prompt = prompt_template.format(
        query=state["query"],
        data=combined_text
    )

    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )

    return {"report": response.choices[0].message.content}