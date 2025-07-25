import requests
import json
import sys
import os

# Add project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import API_URL, API_KEY, MODEL_NAME

def fuse_and_summarize(query, contexts):
    """
    Fuses and summarizes the scraped content from multiple sources using the LLM.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    context_str = "\n\n---\n\n".join(contexts)

    prompt = f"你是一个信息整合专家。请根据以下用户原始查询和从多个来源检索到的背景信息，生成一个全面、连贯的回答。请直接回答问题，不要提及你是从多个来源整合的信息。\n\n用户查询：{query}\n\n背景信息：\n{context_str}"

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000, # Allow for a more detailed summary
        "temperature": 0.7
    }

    try:
        response = requests.post(f"{API_URL}/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        
        completion = response.json()
        summary = completion['choices'][0]['message']['content'].strip()
        return summary

    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM API for summarization: {e}")
        return "抱歉，在整合信息时发生错误。"
    except (KeyError, IndexError) as e:
        print(f"Error parsing LLM response for summarization: {e}")
        print(f"Raw response: {response.text}")
        return "抱歉，在解析摘要时发生错误。"

if __name__ == '__main__':
    # Example usage
    test_query = "AI in healthcare advancements"
    test_contexts = [
        "Context 1: AI is helping doctors diagnose diseases earlier. Machine learning models can detect patterns in medical images that are invisible to the human eye.",
        "Context 2: Another advancement is in drug discovery. AI algorithms can analyze vast datasets of chemical compounds to predict which ones are likely to be effective against a particular disease, speeding up the research process significantly.",
        "Context 3: Personalized medicine is also a key area. AI can analyze a patient's genetic information and lifestyle to create customized treatment plans."
    ]
    
    print(f"Fusing content for query: '{test_query}'")
    final_summary = fuse_and_summarize(test_query, test_contexts)
    print("\nFinal Summary:")
    print(final_summary)