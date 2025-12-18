const username = localStorage.getItem("username");
if(!username){
    window.location.href = "/";
}

const chatBox = document.getElementById("chatBox");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("sendBtn");
const imageInput = document.getElementById("imageInput");

const ws = new WebSocket(`ws://${window.location.host}/ws`);

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const div = document.createElement("div");
    div.className = "message";
    div.innerHTML = `<b>${data.name}:</b> ${data.message || ""}`;
    if(data.image){
        const img = document.createElement("img");
        img.src = data.image;
        div.appendChild(img);
    }
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
};

sendBtn.onclick = async () => {
    let imageUrl = "";
    if(imageInput.files.length > 0){
        const formData = new FormData();
        formData.append("file", imageInput.files[0]);
        const res = await fetch("/upload", {method: "POST", body: formData});
        const data = await res.json();
        imageUrl = data.url;
    }

    ws.send(JSON.stringify({
        name: username,
        message: messageInput.value,
        image: imageUrl
    }));

    messageInput.value = "";
    imageInput.value = "";
};
