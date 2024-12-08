document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("chat-form");
    const messagesDiv = document.getElementById("messages");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const userInput = document.getElementById("user-input").value;
        addMessage(userInput, "user");

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: userInput }),
            });

            const data = await response.json();
            if (data.reply) {
                addMessage(data.reply, "bot");
            } else {
                addMessage("Error: Unable to get a response.", "bot");
            }
        } catch (error) {
            addMessage("Error: Unable to connect to the server.", "bot");
        }

        form.reset();
    });

    function addMessage(text, sender) {
        const message = document.createElement("div");
        message.textContent = text;
        message.classList.add("message", sender);
        messagesDiv.appendChild(message);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
});
