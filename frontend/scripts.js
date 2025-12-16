// Adiciona um ouvinte de evento que é acionado quando o conteúdo do DOM é totalmente carregado
document.addEventListener('DOMContentLoaded', () => {
    // Dados mocados para o histórico de feedback
    const feedbackHistory = [
        { prompt: "Initial prompt", feedback: "The agent is too formal." },
        { prompt: "Updated prompt v2", feedback: "The agent is better now." }
    ];

    const currentPrompt = "You are a helpful assistant.";

    // Exibe o prompt atual na interface
    document.getElementById('current-prompt').textContent = currentPrompt;

    // Preenche o histórico de feedback na interface
    const feedbackHistoryList = document.getElementById('feedback-history');
    feedbackHistory.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `Prompt: "${item.prompt}" - Feedback: "${item.feedback}"`;
        feedbackHistoryList.appendChild(li);
    });
});

// Função para alternar entre as abas de chat e feedback
function openTab(tabName) {
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.classList.remove('active');
    });

    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.classList.remove('active');
    });

    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');
}

// Função assíncrona para enviar uma mensagem para o agente
async function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (!message) return;

    const chatHistory = document.getElementById('chat-history');
    const sendButton = document.getElementById('send-button');
    const loading = document.getElementById('loading');

    // Exibe a mensagem do usuário na interface
    const userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('message', 'user-message');
    userMessageDiv.textContent = message;
    chatHistory.appendChild(userMessageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    // Limpa o campo de entrada e desabilita os controles enquanto a mensagem está sendo enviada
    messageInput.value = '';
    messageInput.disabled = true;
    sendButton.disabled = true;
    loading.style.display = 'block';

    try {
        // Envia a mensagem para a API do agente
        const response = await fetch('http://localhost:8000/api/v1/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        const agentMessage = data.response;

        // Exibe a resposta do agente na interface
        const agentMessageDiv = document.createElement('div');
        agentMessageDiv.classList.add('message', 'agent-message');
        agentMessageDiv.textContent = agentMessage;
        chatHistory.appendChild(agentMessageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;

    } catch (error) {
        console.error('Error sending message:', error);
        // Exibe uma mensagem de erro na interface em caso de falha
        const errorMessageDiv = document.createElement('div');
        errorMessageDiv.classList.add('message', 'agent-message');
        errorMessageDiv.textContent = 'Error: Could not get a response from the agent.';
        chatHistory.appendChild(errorMessageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    } finally {
        // Reabilita os controles de entrada após a conclusão da requisição
        messageInput.disabled = false;
        sendButton.disabled = false;
        loading.style.display = 'none';
    }
}

// Função para enviar feedback sobre a resposta do agente
function sendFeedback() {
    const feedbackInput = document.getElementById('feedback-input');
    const feedback = feedbackInput.value.trim();

    if (!feedback) return;
    
    console.log('Feedback sent:', feedback);

    // Adiciona o feedback ao histórico na interface
    const feedbackHistoryList = document.getElementById('feedback-history');
    const li = document.createElement('li');
    li.textContent = `Feedback: "${feedback}"`;
    feedbackHistoryList.appendChild(li);

    // Limpa o campo de entrada de feedback
    feedbackInput.value = '';
}
