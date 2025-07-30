"""
Роутер для API управления провайдерами обработки данных.
"""

from typing import Dict, Any, List, Optional, Literal, Union
from fastapi import APIRouter, Depends, HTTPException, status, Security, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator

from mindbank_poc.core.common.types import ProviderType
from mindbank_poc.core.models.access_token import AccessTokenType, AccessToken, AccessScope, ScopeType
from mindbank_poc.core.services.auth_service import verify_admin_auth
from mindbank_poc.core.config.settings import settings
from datetime import datetime
# Создаем роутер
router = APIRouter(
    prefix="/api/processing/providers",
    tags=["Processing Providers"],
    responses={404: {"description": "Not found"}},
)

# Модели данных для API
class ProviderConfig(BaseModel):
    """Конфигурация провайдера обработки."""
    config: Dict[str, Any] = Field(..., description="Параметры конфигурации провайдера")

class MetadataCondition(BaseModel):
    """Условие для проверки метаданных."""
    key: str = Field(..., description="Ключ метаданных для проверки")
    operator: Literal["eq", "neq", "contains", "gt", "lt", "gte", "lte", "in"] = Field(
        default="eq", 
        description="Оператор сравнения: eq (равно), neq (не равно), contains (содержит), gt (больше), lt (меньше), gte (больше или равно), lte (меньше или равно), in (в списке)"
    )
    value: Any = Field(..., description="Значение для сравнения")

class ProviderFilter(BaseModel):
    """Фильтр для провайдера обработки."""
    name: Optional[str] = Field(default=None, description="Название фильтра")
    archetypes: Optional[List[str]] = Field(default=None, description="Список поддерживаемых архетипов")
    sources: Optional[List[str]] = Field(default=None, description="Список поддерживаемых источников")
    metadata_conditions: Optional[List[MetadataCondition]] = Field(default=None, description="Условия по метаданным")
    priority: int = Field(default=0, description="Приоритет фильтра (выше значение - выше приоритет)")
    config_override: Optional[Dict[str, Any]] = Field(default=None, description="Переопределение конфигурации для этого фильтра")
    
    @validator('archetypes', 'sources', 'metadata_conditions', pre=True)
    def empty_list_to_none(cls, v):
        if isinstance(v, list) and len(v) == 0:
            return None
        return v

class ProviderInfo(BaseModel):
    """Информация о провайдере обработки."""
    id: str
    name: str
    description: str
    provider_type: str
    supported_archetypes: List[str] = []
    config_schema: Dict[str, Any] = {}
    current_config: Dict[str, Any] = {}
    status: str = "active"
    capabilities: List[str] = []
    filters: List[ProviderFilter] = Field(default_factory=list, description="Фильтры для выбора провайдера")

class ProvidersResponse(BaseModel):
    """Ответ со списком доступных провайдеров."""
    providers: List[ProviderInfo]

class DefaultProviderMapping(BaseModel):
    """Маппинг типа провайдера к конкретному провайдеру."""
    provider_type: str
    provider_id: str

class DefaultProvidersRequest(BaseModel):
    """Запрос на установку провайдеров по умолчанию."""
    defaults: List[DefaultProviderMapping]

class DefaultProvidersResponse(BaseModel):
    """Ответ с текущими провайдерами по умолчанию."""
    defaults: List[DefaultProviderMapping]

# Временное хранилище провайдеров для PoC
# В реальной системе это должно быть в базе данных или конфигурационных файлах
MOCK_PROVIDERS = {
    "openai-embedding": {
        "id": "openai-embedding",
        "name": "OpenAI Embeddings",
        "description": "Провайдер эмбеддингов на основе OpenAI API",
        "provider_type": ProviderType.EMBEDDING.value,
        "supported_archetypes": ["document", "note", "meeting_notes", "transcription"],
        "config_schema": {
            "api_key": {"type": "string", "description": "API ключ OpenAI"},
            "model": {"type": "string", "description": "Модель для эмбеддингов", "default": "text-embedding-ada-002"}
        },
        "current_config": {
            "api_key": "",  # сюда можно подставлять актуальный ключ через API
            "model": "text-embedding-ada-002"
        },
        "status": "active",
        "capabilities": ["text_embedding", "semantic_search"]
    },
    "openai-classifier": {
        "id": "openai-classifier",
        "name": "OpenAI Classifier",
        "description": "Классификатор на основе OpenAI API",
        "provider_type": ProviderType.CLASSIFICATION.value,
        "supported_archetypes": ["document", "note", "meeting_notes", "transcription"],
        "config_schema": {
            "api_key": {"type": "string", "description": "API ключ OpenAI"},
            "model": {"type": "string", "description": "Модель для классификации", "default": "gpt-3.5-turbo"}
        },
        "current_config": {
            "api_key": "",  # сюда можно подставлять актуальный ключ через API
            "model": "gpt-3.5-turbo"
        },
        "status": "active",
        "capabilities": ["text_classification", "entity_extraction"]
    },
    "fallback-embedding": {
        "id": "fallback-embedding",
        "name": "Fallback Embeddings",
        "description": "Локальный провайдер эмбеддингов (fallback)",
        "provider_type": ProviderType.EMBEDDING.value,
        "supported_archetypes": ["document", "note", "meeting_notes", "transcription"],
        "config_schema": {},
        "current_config": {},
        "status": "active",
        "capabilities": ["text_embedding"]
    },
    "fallback-classifier": {
        "id": "fallback-classifier",
        "name": "Fallback Classifier",
        "description": "Локальный классификатор (fallback)",
        "provider_type": ProviderType.CLASSIFICATION.value,
        "supported_archetypes": ["document", "note", "meeting_notes", "transcription"],
        "config_schema": {},
        "current_config": {},
        "status": "active",
        "capabilities": ["text_classification"]
    }
}

# Временное хранилище провайдеров по умолчанию для PoC
DEFAULT_PROVIDERS = {
    ProviderType.EMBEDDING.value: "openai-embedding",
    ProviderType.CLASSIFICATION.value: "openai-classifier",
    ProviderType.TRANSCRIPTION.value: "openai-classifier",
    ProviderType.CAPTION.value: "openai-classifier"
}

security = HTTPBearer(auto_error=False)

def get_current_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    x_admin_api_key: str = Header(None, alias="X-Admin-API-Key")
) -> AccessToken:
    admin_api_key = settings.auth.admin_api_key
    now = datetime.now()
    if x_admin_api_key and x_admin_api_key == admin_api_key:
        return AccessToken(
            token_id="admin-api-key",
            token_value=admin_api_key,
            name="Admin API Key",
            token_type=AccessTokenType.MASTER,
            scopes=[AccessScope(scope_type=ScopeType.ALL)],
            is_active=True,
            created_at=now,
            updated_at=now,
            expires_at=None,
            created_by="system"
        )
    if credentials and credentials.credentials == admin_api_key:
        return AccessToken(
            token_id="admin-api-key",
            token_value=admin_api_key,
            name="Admin API Key",
            token_type=AccessTokenType.MASTER,
            scopes=[AccessScope(scope_type=ScopeType.ALL)],
            is_active=True,
            created_at=now,
            updated_at=now,
            expires_at=None,
            created_by="system"
        )
    # Здесь можно добавить обычную логику проверки пользовательских токенов, если потребуется
    # Пока возвращаем 401 если не admin ключ
    raise HTTPException(
        status_code=401,
        detail="Недействительный токен или ключ",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.get("", response_model=ProvidersResponse)
async def get_all_providers(_: bool = Depends(verify_admin_auth)):
    """
    Получение списка всех доступных провайдеров обработки данных.
    """
    providers = list(MOCK_PROVIDERS.values())
    return {"providers": providers}

@router.post("/{provider_id}/config", response_model=ProviderInfo)
async def update_provider_config(
    provider_id: str,
    config_data: ProviderConfig,
    _: bool = Depends(verify_admin_auth)
):
    """
    Обновление конфигурации провайдера обработки данных.
    Требует административный API-ключ.
    """
    if provider_id not in MOCK_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Провайдер с ID {provider_id} не найден"
        )
    MOCK_PROVIDERS[provider_id]["current_config"].update(config_data.config)
    
    return MOCK_PROVIDERS[provider_id]

@router.get("/defaults", response_model=DefaultProvidersResponse)
async def get_default_providers(_: bool = Depends(verify_admin_auth)):
    """
    Получение текущих провайдеров по умолчанию для каждого типа обработки.
    """
    defaults = [
        {"provider_type": provider_type, "provider_id": provider_id}
        for provider_type, provider_id in DEFAULT_PROVIDERS.items()
    ]
    return {"defaults": defaults}

@router.post("/defaults", response_model=DefaultProvidersResponse)
async def set_default_providers(
    request: DefaultProvidersRequest,
    _: bool = Depends(verify_admin_auth)
):
    """
    Установка провайдеров по умолчанию для каждого типа обработки.
    Требует административный API-ключ.
    """
    for mapping in request.defaults:
        if mapping.provider_id not in MOCK_PROVIDERS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Провайдер с ID {mapping.provider_id} не найден"
            )
        provider = MOCK_PROVIDERS[mapping.provider_id]
        if provider["provider_type"] != mapping.provider_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Провайдер {mapping.provider_id} не поддерживает тип обработки {mapping.provider_type}"
            )
    for mapping in request.defaults:
        DEFAULT_PROVIDERS[mapping.provider_type] = mapping.provider_id
    defaults = [
        {"provider_type": provider_type, "provider_id": provider_id}
        for provider_type, provider_id in DEFAULT_PROVIDERS.items()
    ]
    return {"defaults": defaults}

@router.get("/{provider_id}/filters", response_model=List[ProviderFilter])
async def get_provider_filters(
    provider_id: str,
    _: bool = Depends(verify_admin_auth)
):
    """
    Получение списка фильтров для провайдера обработки данных.
    Требует административный API-ключ.
    """
    if provider_id not in MOCK_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Провайдер с ID {provider_id} не найден"
        )
    
    # Проверяем, есть ли поле filters в провайдере
    if "filters" not in MOCK_PROVIDERS[provider_id]:
        MOCK_PROVIDERS[provider_id]["filters"] = []
    
    return MOCK_PROVIDERS[provider_id]["filters"]

@router.post("/{provider_id}/filters", response_model=ProviderInfo)
async def add_provider_filter(
    provider_id: str,
    filter_data: ProviderFilter,
    _: bool = Depends(verify_admin_auth)
):
    """
    Добавление фильтра для провайдера обработки данных.
    Требует административный API-ключ.
    """
    if provider_id not in MOCK_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Провайдер с ID {provider_id} не найден"
        )
    
    # Проверяем, есть ли поле filters в провайдере
    if "filters" not in MOCK_PROVIDERS[provider_id]:
        MOCK_PROVIDERS[provider_id]["filters"] = []
    
    # Добавляем новый фильтр
    MOCK_PROVIDERS[provider_id]["filters"].append(filter_data.dict(exclude_none=True))
    
    return MOCK_PROVIDERS[provider_id]

@router.delete("/{provider_id}/filters/{filter_index}", response_model=ProviderInfo)
async def delete_provider_filter(
    provider_id: str,
    filter_index: int,
    _: bool = Depends(verify_admin_auth)
):
    """
    Удаление фильтра для провайдера обработки данных.
    Требует административный API-ключ.
    """
    if provider_id not in MOCK_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Провайдер с ID {provider_id} не найден"
        )
    
    # Проверяем, есть ли поле filters в провайдере
    if "filters" not in MOCK_PROVIDERS[provider_id] or not MOCK_PROVIDERS[provider_id]["filters"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"У провайдера {provider_id} нет фильтров"
        )
    
    # Проверяем, существует ли фильтр с указанным индексом
    if filter_index < 0 or filter_index >= len(MOCK_PROVIDERS[provider_id]["filters"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Фильтр с индексом {filter_index} не найден"
        )
    
    # Удаляем фильтр
    MOCK_PROVIDERS[provider_id]["filters"].pop(filter_index)
    
    return MOCK_PROVIDERS[provider_id]

@router.get("/{provider_id}/status", response_model=Dict[str, Any])
async def get_provider_status(
    provider_id: str,
    token: AccessToken = Depends(get_current_token)
):
    """
    Получение статуса провайдера обработки данных.
    """
    if provider_id not in MOCK_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Провайдер с ID {provider_id} не найден"
        )
    
    # В реальной системе здесь должна быть логика проверки статуса провайдера
    # Например, проверка доступности API, лимитов и т.д.
    
    return {
        "status": MOCK_PROVIDERS[provider_id]["status"],
        "limits": {
            "daily_requests": 10000,
            "remaining_requests": 9500,
            "reset_at": "2025-05-14T00:00:00Z"
        },
        "performance": {
            "avg_response_time_ms": 250,
            "success_rate": 0.99
        }
    }
