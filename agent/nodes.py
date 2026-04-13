from agent.decomposer import decompose_query
from tools.web_search import search_web
from config.settings import Settings
from agent.cleaner import clean_results, filter_relevant, rank_results
from openai import OpenAI
from utils.prompt_loader import load_prompt
from concurrent.futures import ThreadPoolExecutor, as_completed

client = OpenAI(api_key=Settings.OPENAI_API_KEY)


def decomposer_node(state):
    sub_queries = decompose_query(state["query"])
    return {"sub_queries": sub_queries}


def search_node(state):
    queries = state["sub_queries"]
    all_results = []

    with ThreadPoolExecutor(max_workers=Settings.MAX_WORKERS    ) as executor:
        futures = [
            executor.submit(search_web, q, Settings.MAX_SEARCH_RESULTS)
            for q in queries
        ]

        for future in as_completed(futures):
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as e:
                print(f"Search failed: {e}")

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
        model=Settings.MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )

    return {"report": response.choices[0].message.content}


def ranking_node(state):
    cleaned = clean_results(state["results"])
    ranked = rank_results(cleaned, state["query"])

    # take top-k
    top_results = ranked[:Settings.TOP_K_RESULTS]

    return {"filtered_results": top_results}