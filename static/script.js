const protocol = location.protocol === 'https:' ? 'wss' : 'ws';
const ws = new WebSocket(`${protocol}://${location.host}/ws`);
const messages = document.getElementById("messages");
const input = document.getElementById("input");
const send = document.getElementById("send");

ws.onmessage = (event) => {
  const message = document.createElement("div");
  message.textContent = event.data;
  messages.appendChild(message);
  messages.scrollTop = messages.scrollHeight;
};

send.onclick = () => {
  if(input.value.trim() !== "") {
    ws.send(input.value);
    input.value = "";
  }
};

input.addEventListener("keydown", (e) => {
  if(e.key === "Enter") {
    send.click();
  }
});
