from typing import List, Optional, Any
from datetime import datetime
from pydantic import BaseModel

class ChatInfo(BaseModel):
    chat_id: str
    title: Optional[str]
    connector_id: Optional[str]
    participants: Optional[List[str]]
    metadata: Optional[dict] = None

class MessageInfo(BaseModel):
    message_id: str
    chat_id: str
    author: str
    content: str
    timestamp: datetime
    metadata: Optional[dict] = None

class SendMessageRequest(BaseModel):
    content: str
    connector_id: Optional[str] = None
    metadata: Optional[dict] = None
    provider_id: Optional[str] = None  # LLM provider to use (optional, explicit)
    model: Optional[str] = None        # Model name to use (optional, explicit)
    sources: Optional[List[str]] = None  # List of connector/source IDs to use (optional)

from src.mindbank_poc.core.providers.llm_chat import (
    select_llm_chat_provider,
    Message as LLMMessage,
)
from datetime import datetime

class ChatService:
    """
    Service for chat operations: listing chats, fetching history, sending messages.
    """

    async def list_chats(
        self,
        connector_id: Optional[str] = None,
        participant: Optional[str] = None,
        filters: Optional[dict] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[ChatInfo]:
        """
        List chats with optional filtering by connector, participant, or custom filters.
        """
        raise NotImplementedError

    async def get_chat_history(
        self,
        chat_id: str,
        limit: int = 50,
        offset: int = 0,
        filters: Optional[dict] = None,
        sort_order: str = "desc",
    ) -> List[MessageInfo]:
        """
        Fetch chat history (messages) for a given chat_id, with pagination and filters.
        """
        raise NotImplementedError

    async def send_message(
        self,
        chat_id: str,
        request: SendMessageRequest,
        author: str,
    ) -> MessageInfo:
        """
        Send a message to a chat as the agent or user.
        If author is 'agent' or 'ai', use LLMChatProvider to generate a response.
        Supports explicit provider/model selection from request.
        """
        if author in ("agent", "ai"):
            # Fetch chat history (stub: should call get_chat_history)
            chat_history = []  # Should be List[MessageInfo]
            # Convert to LLMMessage format
            llm_history = [
                LLMMessage(
                    message_id=m.message_id,
                    chat_id=m.chat_id,
                    author=m.author,
                    content=m.content,
                    timestamp=m.timestamp,
                    metadata=m.metadata or {},
                )
                for m in chat_history
            ]
            # Add the new user message to history
            user_message = LLMMessage(
                message_id="user-msg",
                chat_id=chat_id,
                author="user",
                content=request.content,
                timestamp=datetime.utcnow(),
                metadata=request.metadata or {},
            )
            llm_history.append(user_message)

            # Provider selection logic
            provider = None
            if request.provider_id:
                # Explicit provider selection
                from src.mindbank_poc.core.providers.llm_chat import get_llm_chat_providers
                providers = get_llm_chat_providers()
                for p in providers:
                    if p["info"]["id"] == request.provider_id:
                        provider = p["instance"]
                        break
            if provider is None:
                # Fallback to selector
                provider = select_llm_chat_provider(archetype="chat")
            if provider is None:
                raise RuntimeError("No LLMChatProvider available")

            # Build config, include model and sources if provided
            config = {}
            if request.model:
                config["model"] = request.model
            if request.sources:
                config["sources"] = request.sources

            # Generate response
            llm_response = await provider.generate_chat_response(
                llm_history,
                config=config
            )
            # Convert to MessageInfo
            return MessageInfo(
                message_id=llm_response.message_id,
                chat_id=llm_response.chat_id,
                author=llm_response.author,
                content=llm_response.content,
                timestamp=llm_response.timestamp,
                metadata=llm_response.metadata,
            )
        else:
            # For user messages, just echo/save (stub)
            return MessageInfo(
                message_id="user-msg",
                chat_id=chat_id,
                author=author,
                content=request.content,
                timestamp=datetime.utcnow(),
                metadata=request.metadata or {},
            )
