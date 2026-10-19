const form = document.getElementById("chat-form");
const input = document.getElementById("question");
const chatBox = document.getElementById("chat-box");
const sendButton = document.getElementById("send-button");

function addMessage(text, sender) {
    const message = document.createElement("div");
    message.className = `message ${sender}`;
    message.textContent = text;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = input.value.trim();
    if (!question) return;

    addMessage(question, "user");
    input.value = "";
    sendButton.disabled = true;
    sendButton.textContent = "Thinking...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Request failed.");
        }

        const answer = Array.isArray(data.answer)
            ? JSON.stringify(data.answer, null, 2)
            : String(data.answer ?? "No results found.");

        addMessage(answer, "bot");
    } catch (error) {
        addMessage(error.message || "Unable to connect to the server.", "bot");
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Send";
        input.focus();
    }
});