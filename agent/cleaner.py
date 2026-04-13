from typing import List, Dict
from openai import OpenAI
from config.settings import Settings
from utils.prompt_loader import load_prompt

client = OpenAI(api_key=Settings.OPENAI_API_KEY)


def filter_relevant(results, query):
    prompt_template = load_prompt("filter_prompt")

    filtered = []

    for r in results:
        prompt = prompt_template.format(
            query=query,
            content=r.get("content", "")
        )

        response = client.chat.completions.create(
            model=Settings.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
        )

        decision = response.choices[0].message.content.strip()

        if decision == "YES":
            filtered.append(r)

    return filtered


def deduplicate_results(results: List[Dict]) -> List[Dict]:
    seen_urls = set()
    unique = []

    for r in results:
        url = r.get("url")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(r)

    return unique


def trim_content(results: List[Dict], max_chars: int = 500) -> List[Dict]:
    for r in results:
        if r.get("content"):
            r["content"] = r["content"][:max_chars]
    return results


def clean_results(results: List[Dict]) -> List[Dict]:
    results = deduplicate_results(results)
    results = trim_content(results)
    return results