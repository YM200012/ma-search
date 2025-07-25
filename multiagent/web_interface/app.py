from flask import Flask, render_template, request, jsonify
import sys
import os
# Add project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main_agent.agent import analyze_query
from retrieval_agents.agent import search_tavily # Updated import
from fusion_agent.agent import fuse_and_summarize

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    # 1. Main Agent: Analyze query to get keywords
    status_updates = ["主控智能体：正在分析您的请求..."]
    keywords = analyze_query(query)
    print(keywords)
    if not keywords:
        status_updates.append("主控智能体：无法从您的请求中提取关键词。")
        return jsonify({'status': status_updates, 'result': '无法处理您的请求，请尝试换一种问法。'})

    status_updates.append(f"主控智能体：已将您的请求分解为以下方向：{', '.join(keywords)}")
    main_agent_output = "\n".join(keywords)

    status_updates.append("检索智能体：正在为每个方向启动串行检索...")

    # 2. Retrieval Agents: Search and scrape for each keyword serially
    retrieved_contents = []
    retrieval_agent_outputs = []

    for i, keyword in enumerate(keywords):
        status_updates.append(f"检索智能体 {i + 1}：正在检索 '{keyword}'...")
        content = search_tavily(keyword)
        retrieved_contents.append(content)
        retrieval_agent_outputs.append(f"Agent {i + 1} (关键词: {keyword}):\n---\n{content}")

    status_updates.append("检索智能体：所有检索任务已完成。")
    status_updates.append("融合智能体：正在整合信息并生成最终摘要...")

    # 3. Fusion Agent: Fuse and summarize the content
    final_summary = fuse_and_summarize(query, retrieved_contents)

    status_updates.append("处理完成！")

    return jsonify({
        'status': status_updates,
        'outputs': {
            'main_agent': main_agent_output,
            'retrieval_agents': "\n\n".join(retrieval_agent_outputs),
            'fusion_agent': final_summary
        },
        'result': final_summary
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)