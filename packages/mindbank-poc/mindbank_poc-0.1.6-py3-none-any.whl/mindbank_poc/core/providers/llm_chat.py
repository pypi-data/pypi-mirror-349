from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime
import logging

# Import the provider service
from mindbank_poc.core.services.provider_service import get_provider_service
from mindbank_poc.core.models.provider import ProviderModel
from mindbank_poc.core.common.types import ProviderType
from mindbank_poc.core.providers.selector import ProviderSelector

logger = logging.getLogger(__name__)

# --- Provider Instances Definition ---
# Define instances at the module level to ensure they are singletons
openai_provider_instance = None
offline_fallback_provider_instance = None

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
        logger.info(f"OpenAILLMChatProvider generating response with config: {config}")
        return Message(
            message_id="openai-dummy-response",
            chat_id=messages[-1].chat_id if messages else "unknown",
            author="openai",
            content=f"(OpenAI LLM PoC Response to: '{messages[-1].content if messages else ''}')",
            timestamp=datetime.utcnow(),
            metadata={"provider": "openai", "model_used": config.get("model", "gpt-3.5-turbo")}
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
        logger.info(f"OfflineFallbackLLMChatProvider generating response with config: {config}")
        last_user_msg = next((m for m in reversed(messages) if m.author == "user"), None)
        content = f"Echo: {last_user_msg.content}" if last_user_msg else "(Offline fallback: No user message found)"
        return Message(
            message_id="offline-fallback-response",
            chat_id=messages[-1].chat_id if messages else "unknown",
            author="offline-fallback",
            content=content,
            timestamp=datetime.utcnow(),
            metadata={"provider": "offline-fallback"}
        )

# Initialize instances after class definitions
openai_provider_instance = OpenAILLMChatProvider()
offline_fallback_provider_instance = OfflineFallbackLLMChatProvider()

# Map of provider IDs to their singleton instances
_LLM_PROVIDER_INSTANCES: Dict[str, LLMChatProvider] = {
    "openai-llm-chat": openai_provider_instance,
    "offline-fallback-llm-chat": offline_fallback_provider_instance,
}

def register_llm_chat_providers():
    """Registers LLM ProviderModels with the ProviderService."""
    provider_service = get_provider_service()
    
    openai_model_config = {
        "api_key": "", "model": "gpt-3.5-turbo", "status": "active", "temperature": 0.7
    }
    openai_llm_model = ProviderModel(
        id="openai-llm-chat",
        name="OpenAI LLM Chat",
        description="Provides chat functionality using OpenAI models like GPT-3.5-turbo and GPT-4.",
        provider_type=ProviderType.LLM_CHAT,
        current_config=openai_model_config,
        config_schema={"type": "object", "properties": {"api_key": {"type": "string"}, "model": {"type": "string"}}},
    )
    
    offline_model_config = {
        "model": "echo", "status": "active"
    }
    offline_llm_model = ProviderModel(
        id="offline-fallback-llm-chat",
        name="Offline Fallback LLM Chat",
        description="A fallback provider that echoes user input or provides simple canned responses when offline.",
        provider_type=ProviderType.LLM_CHAT,
        current_config=offline_model_config,
    )
    
    # Save ProviderModels to repository
    if not provider_service.get_provider("openai-llm-chat"):
        provider_service.repository.save_provider(openai_llm_model)
        logger.info("Registered openai-llm-chat provider model.")
    if not provider_service.get_provider("offline-fallback-llm-chat"):
        provider_service.repository.save_provider(offline_llm_model)
        logger.info("Registered offline-fallback-llm-chat provider model.")

# Ensure providers are registered when module is imported
register_llm_chat_providers()

def get_llm_chat_provider_instance_by_id(provider_id: str) -> Optional[LLMChatProvider]:
    """Gets a specific LLM provider instance by its ID."""
    return _LLM_PROVIDER_INSTANCES.get(provider_id)

def get_llm_chat_providers_info_and_instance() -> List[Dict[str, Any]]:
    """
    Get all available LLM chat provider models (info) and their instances.
    Ensures instances are correctly fetched from the _LLM_PROVIDER_INSTANCES map.
    """
    provider_service = get_provider_service()
    provider_models = provider_service.get_providers_by_type(ProviderType.LLM_CHAT)
    
    result = []
    for p_model in provider_models:
        instance = _LLM_PROVIDER_INSTANCES.get(p_model.id)
        if instance:
            provider_info_dict = p_model.dict() # Get all fields from ProviderModel
            result.append({
                "info": provider_info_dict,
                "instance": instance 
            })
        else:
            logger.warning(f"Instance not found for LLM chat provider model ID: {p_model.id} in _LLM_PROVIDER_INSTANCES map.")
    return result

def select_llm_chat_provider_instance(
    archetype: Optional[str] = None,
    source: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Optional[LLMChatProvider]:
    """
    Selects the best LLMChatProvider *instance* for the given context.
    Falls back to offline provider instance if needed.
    """
    provider_service = get_provider_service()
    all_provider_models = provider_service.get_all_providers()
    llm_chat_provider_models = [p for p in all_provider_models if p.provider_type == ProviderType.LLM_CHAT]

    if not llm_chat_provider_models:
        logger.warning("No LLM chat provider models registered in ProviderService.")
        return offline_fallback_provider_instance # Fallback if no models at all

    # ProviderSelector expects a list of dicts (ProviderModel.dict())
    provider_model_dicts = [p.dict() for p in llm_chat_provider_models]

    selected_model_info_dict = ProviderSelector.select_provider(
        provider_model_dicts, # Pass list of dicts
        ProviderType.LLM_CHAT.value, # Pass the string value of the enum
        archetype=archetype,
        source=source,
        metadata=metadata
    )

    if selected_model_info_dict and selected_model_info_dict.get("id"):
        selected_id = selected_model_info_dict["id"]
        instance = _LLM_PROVIDER_INSTANCES.get(selected_id)
        if instance:
            logger.info(f"Selected LLM provider instance via ProviderSelector: {selected_id}")
            return instance
        else:
            logger.warning(f"ProviderSelector selected model ID '{selected_id}', but no corresponding instance found in _LLM_PROVIDER_INSTANCES. Falling back.")
    else:
        logger.warning("ProviderSelector did not select an LLM provider. Falling back.")
        
    # Fallback to offline if selection fails or no instance for selected
    return offline_fallback_provider_instance
