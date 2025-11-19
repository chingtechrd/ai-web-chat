document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatHistory = document.getElementById('chat-history');
    const sendBtn = document.getElementById('send-btn');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage(message, 'user');
        userInput.value = '';
        userInput.disabled = true;
        sendBtn.disabled = true;

        // Add loading message
        const loadingId = 'loading-' + Date.now();
        addMessage('Thinking...', 'ai', loadingId);

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            // Remove loading message
            removeMessage(loadingId);

            if (data.error) {
                addMessage(`Error: ${data.error}`, 'ai');
            } else {
                addMessage(data.response, 'ai');
            }
        } catch (error) {
            removeMessage(loadingId);
            addMessage(`Network error: ${error.message}`, 'ai');
        } finally {
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        }
    });

    function removeMessage(id) {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
        }
    }

    function addMessage(text, sender, id = null) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        if (id) messageDiv.id = id;

        const bubbleDiv = document.createElement('div');
        bubbleDiv.classList.add('bubble');
        bubbleDiv.textContent = text;

        messageDiv.appendChild(bubbleDiv);
        chatHistory.appendChild(messageDiv);

        // Scroll to bottom
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});
