from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="../static"), name="static")

# Connected clients
clients = []

# Index page
@app.get("/")
async def get_index():
    with open("../frontend/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# Chat page
@app.get("/chat")
async def get_chat():
    with open("../frontend/chat.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Broadcast to all clients
            for client in clients:
                if client != websocket:
                    await client.send_json(data)
    except WebSocketDisconnect:
        clients.remove(websocket)

# File upload
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs("../static/images", exist_ok=True)
    file_location = f"../static/images/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"url": f"/static/images/{file.filename}"}
