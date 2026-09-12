import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key)


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
