from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import time
import os

app = FastAPI()

# Монтируем папку static для отдачи CSS и JS
app.mount("/static", StaticFiles(directory="static"), name="static")

clients = {}

@app.get("/")
async def get():
    # Читаем шаблон из папки templates
    path = os.path.join("templates", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    user_id = str(int(time.time() * 1000))
    clients[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            message = f"User {user_id}: {data}"
            for uid, conn in clients.items():
                await conn.send_text(message)
    except WebSocketDisconnect:
        del clients[user_id]
