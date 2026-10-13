from config import settings
from tavily import TavilyClient

client = TavilyClient(settings.tavily_api_key)


def search_prices(query, max_results=3):
    """
    Searches the web for approximate info (prices, costs)
    """
    response = client.search(query, max_results=max_results)

    result = []
    for res in response["results"]:
        result.append({
            "title": res.get("title", ""),
            "content": res.get("content", ""),
        })

    return result
