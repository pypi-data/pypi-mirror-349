from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from src.mindbank_poc.core.services.chat_service import (
    ChatService,
    ChatInfo,
    MessageInfo,
    SendMessageRequest,
)
from pydantic import BaseModel


router = APIRouter(
    prefix="/agent_chat",
    tags=["agent_chat"],
)

def get_chat_service() -> ChatService:
    # In production, inject real service (with DB/retrieval integration)
    return ChatService()

@router.get("/providers")
async def list_llm_chat_providers():
    """
    List all available LLMChatProviders and their supported models/configs.
    """
    providers = get_llm_chat_providers()
    result = []
    for p in providers:
        info = p["info"]
        # Example: extract models and default_model from config or info
        models = info.get("models") or [info.get("current_config", {}).get("model")] if info.get("current_config", {}).get("model") else []
        default_model = info.get("default_model") or (models[0] if models else None)
        result.append({
            "id": info.get("id"),
            "name": info.get("name"),
            "models": models,
            "default_model": default_model,
            "config_schema": info.get("config_schema", {}),
        })
    return result

@router.get("/list", response_model=List[ChatInfo])
async def list_chats(
    connector_id: Optional[str] = Query(None),
    participant: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    chat_service: ChatService = Depends(get_chat_service),
):
    """
    List chats with optional filtering by connector or participant.
    """
    return await chat_service.list_chats(
        connector_id=connector_id,
        participant=participant,
        limit=limit,
        offset=offset,
    )

@router.get("/{chat_id}/history", response_model=List[MessageInfo])
async def get_chat_history(
    chat_id: str = Path(...),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    chat_service: ChatService = Depends(get_chat_service),
):
    """
    Fetch chat history (messages) for a given chat_id, with pagination and sorting.
    """
    return await chat_service.get_chat_history(
        chat_id=chat_id,
        limit=limit,
        offset=offset,
        sort_order=sort_order,
    )

@router.post("/{chat_id}/send", response_model=MessageInfo)
async def send_message(
    chat_id: str = Path(...),
    request: SendMessageRequest = None,
    author: str = Query(..., description="Author of the message (agent or user)"),
    chat_service: ChatService = Depends(get_chat_service),
):
    """
    Send a message to a chat as the agent or user.
    """
    if request is None:
        raise HTTPException(status_code=400, detail="Request body required")
    return await chat_service.send_message(
        chat_id=chat_id,
        request=request,
        author=author,
    )
