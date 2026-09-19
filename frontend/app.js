const messages = document.getElementById("messages");
const input = document.getElementById("questionInput");
const sendButton = document.getElementById("sendButton");


function scrollToBottom() {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: "smooth"
    });
}


function useSuggestion(question) {
    input.value = question;
    input.focus();
}


function addMessage(type, content) {

    const message = document.createElement("div");
    message.className = `message ${type}`;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = type === "user" ? "You" : "AI";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = content;

    message.appendChild(avatar);
    message.appendChild(bubble);

    messages.appendChild(message);

    scrollToBottom();

    return message;
}


function addSources(context, score) {

    if (!context || context.length === 0) {
        return;
    }

    const wrapper = document.createElement("details");
    wrapper.className = "sources";

    const summary = document.createElement("summary");
    summary.textContent =
        `Retrieved context · Top similarity ${score.toFixed(3)}`;

    wrapper.appendChild(summary);

    context.forEach((item, index) => {

        const source = document.createElement("div");
        source.className = "source";

        source.innerHTML = `
            <div class="source-score">
                Chunk ${index + 1} · Similarity ${item.score.toFixed(3)}
            </div>

            <div class="source-text"></div>
        `;

        source.querySelector(".source-text").textContent = item.text;

        wrapper.appendChild(source);
    });

    messages.appendChild(wrapper);

    scrollToBottom();
}


function addLoading() {

    const message = document.createElement("div");
    message.className = "message assistant";
    message.id = "loadingMessage";

    message.innerHTML = `
        <div class="avatar">AI</div>

        <div class="bubble">
            <div class="loading">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;

    messages.appendChild(message);

    scrollToBottom();
}


function removeLoading() {

    const loading = document.getElementById("loadingMessage");

    if (loading) {
        loading.remove();
    }
}


async function sendMessage() {

    const question = input.value.trim();

    if (!question || sendButton.disabled) {
        return;
    }
    
    const welcome = document.getElementById("welcomeMessage");

    if (welcome) {
        welcome.remove();
    }
    
    addMessage("user", question);

    input.value = "";
    sendButton.disabled = true;

    addLoading();

    try {

        const response = await fetch(`${API_URL}/chat`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })
        });


        if (!response.ok) {
            throw new Error("API request failed");
        }


        const data = await response.json();

        removeLoading();

        addMessage("assistant", data.answer);

        addSources(
            data.retrieved_context,
            data.retrieval_score
        );

    } catch (error) {

        removeLoading();

        addMessage(
            "assistant",
            "Something went wrong while connecting to the RAG API."
        );

        console.error(error);

    } finally {

        sendButton.disabled = false;
        input.focus();
    }
}


input.addEventListener("keydown", function(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
    }

});