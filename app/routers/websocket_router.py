from fastapi import APIRouter, Depends

from app.services.message_service import connect_message_websocket_service

router = APIRouter(prefix="/ws", tags=["Chat"])


@router.websocket("/chat/{chat_id}/messages")
async def message_websocket(
    _: None = Depends(connect_message_websocket_service),
):
    pass
