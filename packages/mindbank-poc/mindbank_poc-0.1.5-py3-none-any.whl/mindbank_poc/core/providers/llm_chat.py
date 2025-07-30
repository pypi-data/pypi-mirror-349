from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime

# Import the provider service
from mindbank_poc.core.services.provider_service import get_provider_service
from mindbank_poc.core.models.provider import ProviderModel
from mindbank_poc.core.common.types import ProviderType

def select_llm_chat_provider(
    archetype: Optional[str] = None,
    source: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Select the best LLMChatProvider instance for the given context using ProviderSelector.
    Falls back to offline provider if needed.
    """
    from mindbank_poc.core.providers.selector import ProviderSelector
    
    # Get provider service
    provider_service = get_provider_service()
    
    # Get providers of LLM_CHAT type using the enum 
    all_providers = provider_service.get_all_providers()
    providers = [p for p in all_providers if p.provider_type == ProviderType.LLM_CHAT]
    
    # Convert to format expected by ProviderSelector
    provider_infos = [p.dict(exclude={"instance"}) for p in providers]
    provider_map = {p.id: p for p in providers}

    selected_info = ProviderSelector.select_provider(
        provider_infos,
        ProviderType.LLM_CHAT.value,
        archetype=archetype,
        source=source,
        metadata=metadata
    )
    if not selected_info:
        # Fallback to offline
        for p in providers:
            if p.provider_type == ProviderType.LLM_CHAT and "offline" in p.id:
                return p
        return None
    return provider_map.get(selected_info["id"])

class Message:
    """
    Minimal message model for LLM chat context.
    """
    def __init__(self, message_id: str, chat_id: str, author: str, content: str, timestamp: datetime, metadata: Dict[str, Any] = None):
        self.message_id = message_id
        self.chat_id = chat_id
        self.author = author
        self.content = content
        self.timestamp = timestamp
        self.metadata = metadata or {}

class LLMChatProvider(ABC):
    """
    Abstract base class for LLM chat providers.
    """

    @abstractmethod
    async def generate_chat_response(
        self,
        messages: List[Message],
        config: Dict[str, Any]
    ) -> Message:
        """
        Generate a chat response given the message history and config.
        """
        pass

class OpenAILLMChatProvider(LLMChatProvider):
    """
    OpenAI-based LLM chat provider (gpt-3.5-turbo, gpt-4, etc).
    """

    async def generate_chat_response(
        self,
        messages: List[Message],
        config: Dict[str, Any]
    ) -> Message:
        """
        Call OpenAI API to generate a chat response.
        (Stub: implement OpenAI integration here)
        """
        # Example stub: return a dummy message
        return Message(
            message_id="openai-dummy",
            chat_id=messages[-1].chat_id if messages else "unknown",
            author="openai",
            content="(OpenAI LLM response placeholder)",
            timestamp=datetime.utcnow(),
            metadata={"provider": "openai"}
        )

class OfflineFallbackLLMChatProvider(LLMChatProvider):
    """
    Offline fallback LLM chat provider.
    Returns a simple echo or retrieval-based response.
    """

    async def generate_chat_response(
        self,
        messages: List[Message],
        config: Dict[str, Any]
    ) -> Message:
        """
        Return a fallback response (e.g., echo last user message or retrieval result).
        """
        last_user = next((m for m in reversed(messages) if m.author != "openai"), None)
        content = last_user.content if last_user else "(no user message found)"
        return Message(
            message_id="offline-fallback",
            chat_id=messages[-1].chat_id if messages else "unknown",
            author="offline-fallback",
            content=f"(Offline fallback) {content}",
            timestamp=datetime.utcnow(),
            metadata={"provider": "offline-fallback"}
        )

# Create provider instances
openai_provider = OpenAILLMChatProvider()
offline_fallback_provider = OfflineFallbackLLMChatProvider()

# Register LLM providers in the provider service
def register_llm_chat_providers():
    provider_service = get_provider_service()
    
    openai_llm_model = ProviderModel(
        id="openai-llm-chat",
        name="OpenAI LLM Chat",
        description="OpenAI LLM Chat (LLM Chat Provider)",
        provider_type=ProviderType.LLM_CHAT,  # Use the enum value instead of string
        supported_archetypes=["chat", "dialogue"],
        config_schema={},
        current_config={
            "api_key": "",
            "model": "gpt-3.5-turbo",
            "model_path": "",
            "status": "active",
            "temperature": 0.7
        },
        status="active",
        capabilities=["llm_chat"],
        filters=[],
        instance=openai_provider
    )
    
    offline_llm_model = ProviderModel(
        id="offline-fallback-llm-chat",
        name="Offline Fallback LLM Chat",
        description="Offline Fallback LLM Chat (LLM Chat Provider)",
        provider_type=ProviderType.LLM_CHAT,  # Use the enum value instead of string
        supported_archetypes=["chat", "dialogue"],
        config_schema={},
        current_config={
            "api_key": "",
            "model": "echo",
            "model_path": "",
            "status": "active",
            "temperature": 0.7
        },
        status="active",
        capabilities=["llm_chat"],
        filters=[],
        instance=offline_fallback_provider
    )
    
    # Save to repository
    provider_service.repository.save_provider(openai_llm_model)
    provider_service.repository.save_provider(offline_llm_model)

# Register providers when module is imported
register_llm_chat_providers()
