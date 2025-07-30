import os
import secrets
from typing import Optional
import hashlib
import base64
from fastapi import Depends, HTTPException, status, Request, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings

logger = get_logger(__name__)

def verify_admin_auth(x_admin_api_key: str = Header(None, alias="X-Admin-API-Key")):
    """
    Проверяет административный API-ключ из заголовка X-Admin-API-Key через Depends(Header).
    Args:
        x_admin_api_key: значение заголовка X-Admin-API-Key
    Returns:
        True, если ключ валиден, иначе вызывает HTTPException 401
    """
    admin_api_key = settings.auth.admin_api_key
    if not x_admin_api_key or x_admin_api_key != admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing admin API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return True

def generate_admin_password_hash(password: str) -> str:
    """
    Генерирует хеш пароля администратора.
    
    Args:
        password: Пароль в открытом виде
        
    Returns:
        Хеш пароля
    """
    password_bytes = password.encode("utf-8")
    hashed_password = hashlib.sha256(password_bytes).hexdigest()
    return hashed_password 