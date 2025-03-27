import logging

from starlette.websockets import WebSocket

from coffee_shop.sqlalchemy_db.models.user import User

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.user_connections: dict[int, WebSocket] = {}
        self.admin_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user: User):
        if user.is_superuser:
            self.admin_connections[user.id] = websocket
            logger.info(f"Admin with user_id {user.id} connected")
        else:
            self.user_connections[user.id] = websocket
            logger.info(f"User with id {user.id} connected")

    async def disconnect(self, user: User):
        if user.is_superuser:
            if user.id in self.admin_connections:
                del self.admin_connections[user.id]
                logger.info(f"Admin with user_id {user.id} disconnected")
        else:
            if user.id in self.user_connections:
                del self.user_connections[user.id]
                logger.info(f"User with id {user.id} disconnected")

    async def send_personal_message(self, message: str, user_id: int):
        websocket = self.user_connections.get(user_id) or self.admin_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)
