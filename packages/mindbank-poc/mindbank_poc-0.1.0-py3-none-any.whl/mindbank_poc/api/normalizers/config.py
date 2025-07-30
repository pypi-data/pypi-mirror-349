"""
Конфигурация нормализатора в API.
"""
from pathlib import Path
import os
from typing import Dict, Any, Optional

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.normalizer.models import NormalizerConfig, ProviderConfig
from mindbank_poc.core.config.settings import settings, settings_logger

logger = get_logger(__name__)


def load_config(config_path: Optional[Path] = None) -> NormalizerConfig:
    """
    Загружает конфигурацию нормализатора из настроек.
    
    Конфигурация берется из настроек окружения (.env файл).
    
    Args:
        config_path: Путь к конфигурационному файлу (игнорируется, оставлен для совместимости)
        
    Returns:
        Конфигурация нормализатора
    """    
    # Используем настройки из .env
    logger.info("Using normalizer config from environment variables")
    settings_logger.info(f"[load_config] Initial settings.normalizer.offline_mode: {settings.normalizer.offline_mode} (type: {type(settings.normalizer.offline_mode)})" )
    
    # Принудительная проверка для отладки
    # Проверяем переменную среды напрямую
    env_offline_mode = os.getenv("NORMALIZER_OFFLINE_MODE", "").lower()
    is_offline = env_offline_mode in ("true", "1", "yes", "y", "on") or settings.normalizer.offline_mode is True
    
    if is_offline:
        logger.info("Offline mode is enabled, using fallback providers regardless of provider settings")
        transcript_provider = "fallback"
        caption_provider = "fallback"
        embed_provider = "fallback"
        classifier_provider = "fallback"
    else:
        logger.info(f"Using configured providers: "
                  f"transcript={settings.normalizer.transcript_provider}, "
                  f"caption={settings.normalizer.caption_provider}, "
                  f"embed={settings.normalizer.embed_provider}, "
                  f"classifier={settings.normalizer.classifier_provider}")
        transcript_provider = settings.normalizer.transcript_provider
        caption_provider = settings.normalizer.caption_provider
        embed_provider = settings.normalizer.embed_provider
        classifier_provider = settings.normalizer.classifier_provider
        
    # # Создаем конфигурацию с учетом offline_mode
    # loaded_normalizer_config = NormalizerConfig(
    #     transcript=ProviderConfig(
    #         id=settings.normalizer.transcript_provider,
    #         name=transcript_provider,
    #         enabled=settings.normalizer.enable_transcript,
    #         params={"api_key": settings.normalizer.transcript_api_key} if transcript_provider == "openai" else {}
    #     ),
    #     caption=ProviderConfig(
    #         id=settings.normalizer.caption_provider,
    #         name=caption_provider,
    #         enabled=settings.normalizer.enable_caption,
    #         params={"api_key": settings.normalizer.caption_api_key} if caption_provider == "openai" else {}
    #     ),
    #     embed=ProviderConfig(
    #         id=settings.normalizer.embed_provider,
    #         name=embed_provider,
    #         enabled=settings.normalizer.enable_embed,
    #         params={
    #             "api_key": settings.normalizer.embed_api_key,
    #             "model": settings.normalizer.embedding_model
    #         } if embed_provider == "openai" else {}
    #     ),
    #     classifier=ProviderConfig(
    #         id=settings.normalizer.classifier_provider,
    #         name=classifier_provider,
    #         enabled=settings.normalizer.enable_classifier,
    #         params={"api_key": settings.normalizer.classifier_api_key} if classifier_provider == "openai" else {}
    #     ),
    # )
    
    # settings_logger.info(f"[load_config] Created NormalizerConfig: {loaded_normalizer_config.model_dump_json(indent=2)}")
    # return loaded_normalizer_config 

    # Hardcode for PoC, imitating dynamic configuration
    from mindbank_poc.api.routers.processing_providers import MOCK_PROVIDERS
    return NormalizerConfig(**MOCK_PROVIDERS)