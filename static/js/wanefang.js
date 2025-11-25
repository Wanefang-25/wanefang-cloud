const chatEl = document.getElementById("chat");
const promptEl = document.getElementById("prompt");
const sendBtn = document.getElementById("send");
const statusEl = document.getElementById("status");

async function sendMessage() {
  const text = (promptEl.value || "").trim();
  if (!text) return;

  statusEl.textContent = "";
  appendMessage("user", text);
  sendBtn.disabled = true;

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    if (!res.ok) {
      throw new Error(`Server error: ${res.status}`);
    }

    const data = await res.json();

    if (data.reply) {
      appendMessage("wanefang", data.reply);
    } else if (data.error) {
      appendMessage(
        "wanefang",
        "The cosmic winds bring only an error: " + data.error
      );
    } else {
      appendMessage(
        "wanefang",
        "The ether is strangely quiet. No reply was found."
      );
    }
  } catch (err) {
    console.error(err);
    statusEl.textContent =
      "Wanefang’s connection flickered. Try again in a moment.";
  } finally {
    sendBtn.disabled = false;
    promptEl.value = "";
    promptEl.focus();
  }
}

function appendMessage(role, text) {
  const div = document.createElement("div");
  div.classList.add("wf-message");

  if (role === "user") {
    div.classList.add("wf-message-user");
  } else {
    div.classList.add("wf-message-wanefang");
  }

  div.textContent = text;
  chatEl.appendChild(div);
  chatEl.scrollTop = chatEl.scrollHeight;
}

sendBtn.addEventListener("click", sendMessage);

promptEl.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
    e.preventDefault();
    sendMessage();
  }
});
