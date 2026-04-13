from tavily import TavilyClient
from config.settings import settings

tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)

def search_web(query: str, max_results: int = settings.MAX_SEARCH_RESULTS):
    response = tavily.search(query=query, max_results=max_results)
    results = []

    for r in response.get("results", []):
        results.append({
            "title": r.get("title"),
            "content": r.get("content"),
            "url": r.get("url")
        })

    return results