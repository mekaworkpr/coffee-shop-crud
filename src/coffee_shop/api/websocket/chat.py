import logging

from fastapi import APIRouter
from starlette import status
from starlette.exceptions import HTTPException
from starlette.websockets import WebSocket, WebSocketDisconnect

from coffee_shop.api.websocket.connection_manager import ConnectionManager
from coffee_shop.repositories.user import UserRepository
from coffee_shop.sqlalchemy_db.session import async_session

chat_router = APIRouter()

logger = logging.getLogger(__name__)

manager = ConnectionManager()

@chat_router.websocket("/support/{user_id}")
async def support_websocket_endpoint(
        websocket: WebSocket,
        user_id: int
):
    await websocket.accept()

    user_repository = UserRepository()

    async with async_session() as session:
        user = await user_repository.get_by_pk(user_id, "id", session=session)

    if not user:
        await websocket.send_text(f"User {user_id} not found")
        raise HTTPException(status_code=status.WS_1008_POLICY_VIOLATION, detail="User not found")

    await manager.connect(websocket, user)

    try:
        while True:
            data = await websocket.receive_json()
            try:
                target_user_id = data.get("target_user_id")
                message = data.get("message")

                if not target_user_id or not message:
                    raise ValueError("target_user_id or message fields are not specified")

                if user.is_superuser:
                        if target_user_id in manager.user_connections:
                            await manager.send_personal_message(f"From support: {message}", target_user_id)
                            logger.info(f"Admin {user.id} sending to User with id {target_user_id} message: {message}")
                        else:
                            await manager.send_personal_message(
                                f"User with id {target_user_id} is not connected", user.id
                            )
                else:
                    if target_user_id in manager.admin_connections:
                        await manager.send_personal_message(f"To support: {message}", target_user_id)
                    else:
                        await manager.send_personal_message(
                            f"Admin with id {target_user_id} is not connected", user.id
                        )
            except ValueError as e:
                logger.info(e)
                raise e

    except WebSocketDisconnect:
        await manager.disconnect(user)

    except Exception as e:
        logger.error(f"Error in WebSocket for user with id {user.id}: {e}")
        await manager.disconnect(user)

        await websocket.close()
