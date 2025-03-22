async function sendMessage() {
    let input = document.getElementById("user-input").value;
    let chatBox = document.getElementById("chat-messages");

    if (input.trim() === "") return;

    let userMessage = <p><strong>You:</strong> ${input}</p>;
    chatBox.innerHTML += userMessage;

    // Show loading message
    let botMessage = <p><strong>Bot:</strong> Thinking...</p>;
    chatBox.innerHTML += botMessage;

    try {
        const response = await fetch("http://localhost:5000/chatbot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input })
        });

        const data = await response.json();
        chatBox.innerHTML = chatBox.innerHTML.replace("Thinking...", data.reply);
    } catch (error) {
        chatBox.innerHTML = chatBox.innerHTML.replace("Thinking...", "Error fetching response.");
    }

    chatBox.scrollTop = chatBox.scrollHeight;
    document.getElementById("user-input").value = "";
}