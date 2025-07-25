import requests
import json
import sys
import os

# Add project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import API_URL, API_KEY, MODEL_NAME

def analyze_query(query):
    """
    Analyzes the user query using the LLM to break it down into search keywords.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"你是一个智能搜索助手。请将以下用户查询分解为最多7个、简洁的、用于搜索引擎的关键词短语。如果你觉得不能分解这么多，请不要刻意分解，扭曲原始查询内容含义。请只返回关键词短语，每个短语占一行，不要有任何其他多余的文字或编号。\n\n用户查询：{query}"

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100,
        "temperature": 0.5
    }

    try:
        response = requests.post(f"{API_URL}/chat/completions", headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        completion = response.json()
        content = completion['choices'][0]['message']['content'].strip()
        
        # Split the content into a list of keywords
        keywords = [kw.strip() for kw in content.split('\n') if kw.strip()]
        print(keywords)
        return keywords

    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM API: {e}")
        return []
    except (KeyError, IndexError) as e:
        print(f"Error parsing LLM response: {e}")
        print(f"Raw response: {response.text}")
        return []

if __name__ == '__main__':
    # Example usage
    test_query = "告诉我关于人工智能在医疗保健领域的最新进展"
    print(f"Analyzing query: '{test_query}'")
    search_keywords = analyze_query(test_query)
    print("\nGenerated keywords:")
    for keyword in search_keywords:
        print(f"- {keyword}")