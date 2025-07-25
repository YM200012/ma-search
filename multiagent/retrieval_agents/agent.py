import os
from tavily import TavilyClient
import sys

# Add the parent directory to the Python path to allow importing 'config'
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TAVILY_API_KEY

def search_tavily(keyword):
    """
    Performs a web search for the given keyword using the Tavily Search API.
    """
    if not TAVILY_API_KEY:
        return "Tavily API key not found. Please set it in the config.py file."

    try:
        tavily = TavilyClient(api_key=TAVILY_API_KEY)
        # Search for the keyword and get the content of the top result
        response = tavily.search(query=keyword, search_depth="basic", max_results=1)
        
        if not response or 'results' not in response or not response['results']:
            return f"No search results found for '{keyword}'."

        # Extract the content from the first result
        first_result = response['results'][0]
        return first_result['content']

    except Exception as e:
        return f"Error during Tavily search for '{keyword}': {e}"

if __name__ == '__main__':
    # Example usage
    test_keyword = "Latest advancements in AI-powered drug discovery"
    print(f"Searching for: '{test_keyword}'")
    scraped_content = search_tavily(test_keyword)
    print("\nScraped Content:")
    print(scraped_content)