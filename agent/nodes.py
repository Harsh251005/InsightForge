from agent.decomposer import decompose_query
from tools.web_search import search_web
from config.settings import settings
from agent.cleaner import clean_results, filter_relevant, rank_results
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.prompt_loader import load_prompt

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def decomposer_node(state):
    logs = state.get("logs", [])
    logs.append("🔍 Decomposing query...")

    sub_queries = decompose_query(state["query"])

    # depth control
    if state.get("depth") == "basic":
        sub_queries = sub_queries[:3]   # fewer queries
    else:
        sub_queries = sub_queries[:6]   # more coverage

    logs.append(f"Generated {len(sub_queries)} sub-queries")

    return {
        "sub_queries": sub_queries,
        "logs": logs
    }


def search_node(state):
    logs = state.get("logs", [])
    logs.append("🌐 Searching web...")

    from concurrent.futures import ThreadPoolExecutor, as_completed
    from tools.web_search import search_web

    queries = state["sub_queries"]
    all_results = []

    # depth-based result count
    max_results = 3 if state.get("depth") == "basic" else 5

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(search_web, q, max_results)
            for q in queries
        ]

        for future in as_completed(futures):
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as e:
                print(f"Search failed: {e}")

    logs.append(f"Collected {len(all_results)} results")

    return {
        "results": all_results,
        "logs": logs
    }

def filter_node(state):
    cleaned = clean_results(state["results"])
    filtered = filter_relevant(cleaned, state["query"])

    return {"filtered_results": filtered}


def report_node(state):
    logs = state.get("logs", [])
    logs.append("📝 Generating final report with citations...")

    # Number sources
    numbered_sources = []
    for idx, r in enumerate(state["filtered_results"], start=1):
        numbered_sources.append({
            "id": idx,
            "title": r["title"],
            "content": r["content"],
            "url": r["url"]
        })

    # Prepare data with IDs
    combined_text = "\n\n".join(
        [
            f"[{s['id']}] {s['title']}\n{s['content']}"
            for s in numbered_sources
        ]
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

    report = response.choices[0].message.content

    logs.append("✅ Report ready with citations")

    return {
        "report": report,
        "sources": numbered_sources,
        "logs": logs
    }

def ranking_node(state):
    logs = state.get("logs", [])
    logs.append("⚖️ Ranking results...")

    cleaned = clean_results(state["results"])
    ranked = rank_results(cleaned, state["query"])

    top_results = ranked[:8]

    logs.append(f"Selected top {len(top_results)} results")

    return {
        "filtered_results": top_results,
        "logs": logs
    }


def reflection_node(state):
    logs = state.get("logs", [])
    logs.append("🧠 Reflecting on gathered data...")

    combined_text = "\n\n".join(
        [f"{r['title']}\n{r['content']}" for r in state["filtered_results"]]
    )

    prompt_template = load_prompt("reflection_prompt")

    prompt = prompt_template.format(
        query=state["query"],
        data=combined_text
    )

    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )

    decision = response.choices[0].message.content.strip()

    need_more = decision != "YES"

    if need_more:
        logs.append("🔁 More research needed")
    else:
        logs.append("✅ Sufficient information gathered")

    return {
        "need_more_research": need_more,
        "iteration": state.get("iteration", 0) + 1,
        "logs": logs
    }


def expand_query_node(state):
    logs = state.get("logs", [])
    logs.append("🔁 Expanding query for deeper research...")

    new_query = f"{state['query']} latest insights detailed analysis"

    return {
        "sub_queries": [new_query],
        "logs": logs
    }