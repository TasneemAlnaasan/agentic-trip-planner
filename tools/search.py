from tavily import TavilyClient
from config import settings

client = TavilyClient(settings.tavily_api_key)


def search_prices(query, max_results=3):
    try:
        response = client.search(query, max_results=max_results)
    except Exception:
        return []

    result = []
    for res in response["results"]:
        result.append({
            "title": res.get("title", ""),
            "content": res.get("content", "")[:300],
        })

    return result
