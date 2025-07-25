document.addEventListener('DOMContentLoaded', () => {
    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search-input');
    const statusUpdates = document.getElementById('status-updates');
    const resultsDiv = document.getElementById('results');

    searchButton.addEventListener('click', async () => {
        const query = searchInput.value;
        if (query.trim() === '') {
            alert('请输入搜索内容');
            return;
        }

        // Disable button and clear previous results
        searchButton.disabled = true;
        searchButton.textContent = '正在搜索...';
        statusUpdates.innerHTML = '<li>开始处理请求...</li>';
        resultsDiv.innerHTML = '';
        document.getElementById('main-agent-output').textContent = '';
        document.getElementById('retrieval-agents-output').textContent = '';
        document.getElementById('fusion-agent-output').textContent = '';

        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Display status updates
            let statusHTML = '';
            data.status.forEach(s => {
                statusHTML += `<li>${s}</li>`;
            });
            statusUpdates.innerHTML = statusHTML;

            // Display agent outputs
            document.getElementById('main-agent-output').textContent = data.outputs.main_agent;
            document.getElementById('retrieval-agents-output').textContent = data.outputs.retrieval_agents;
            document.getElementById('fusion-agent-output').textContent = data.outputs.fusion_agent;

            // Display final result
            resultsDiv.innerHTML = data.result.replace(/\n/g, '<br>');

        } catch (error) {
            console.error('Error during search:', error);
            resultsDiv.innerHTML = '搜索过程中发生错误，请查看控制台获取更多信息。';
        } finally {
            // Re-enable the button
            searchButton.disabled = false;
            searchButton.textContent = '搜索';
        }
    });
});