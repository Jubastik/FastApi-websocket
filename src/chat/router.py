from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from sqlalchemy import insert

from src.chat.models import Message
from src.db_session import get_session

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        await self.add_messages_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_messages_to_database(text: str):
        session = get_session()
        message = Message(message=text)
        session.add(message)
        session.commit()
        session.close()


manager = ConnectionManager()


@router.get("/last_messages")
async def get_last_messages():
    session = get_session()
    messages = session.query(Message).limit(30).all()
    session.close()
    return messages


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Сервер принял: {data}", websocket)
            await manager.broadcast(f"Пользователь #{client_id} сказал: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Пользователь #{client_id} покинул эту тусовку")
