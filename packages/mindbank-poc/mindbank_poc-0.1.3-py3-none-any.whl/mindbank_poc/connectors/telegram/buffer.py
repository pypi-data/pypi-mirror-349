"""Simple async buffer for batching entries before sending to the Ingest API."""
from __future__ import annotations

import asyncio
import time
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

import aiohttp

from .constants import (
    BULK_API_SIZE, 
    BUFFER_FLUSH_TIMEOUT, 
    AGGREGATE_GAP_SECONDS,
    MAX_BUFFER_CHARS,
    AUTO_FLUSH_INTERVAL
)  # relative import inside the package

__all__ = ["EntryBuffer"]


class EntryBuffer:
    """Collect entries and send them in bulk.

    Parameters
    ----------
    api_url: str
        Base URL to the API *without* the ``/ingest/entries`` suffix – the class
        will append it automatically.
    bulk_size: int
        How many entries to accumulate before the buffer is flushed.
    flush_timeout: float
        Max time (seconds) to keep entries before they are flushed.
    access_token: str | None
        Optional bearer token passed as *Authorization* header.
    gap_seconds: float
        Максимальный временной интервал (в секундах) между сообщениями для
        агрегирования в один пакет. Если разрыв между сообщениями превышает
        это значение, буфер будет сброшен.
    max_buffer_chars: int
        Максимальный размер буфера в символах. При превышении буфер будет отправлен.
    auto_flush_interval: float
        Интервал (в секундах) для периодической проверки и автоматической отправки буфера.
    """

    def __init__(
        self,
        api_url: str,
        bulk_size: int = BULK_API_SIZE,
        flush_timeout: float = BUFFER_FLUSH_TIMEOUT,
        access_token: Optional[str] = None,
        gap_seconds: float = AGGREGATE_GAP_SECONDS,
        max_buffer_chars: int = MAX_BUFFER_CHARS,
        auto_flush_interval: float = AUTO_FLUSH_INTERVAL,
    ) -> None:
        self._url: str = self._make_url(api_url)
        self._bulk_size = bulk_size
        self._flush_timeout = flush_timeout
        self._access_token = access_token
        self._gap_seconds = gap_seconds
        self._max_buffer_chars = max_buffer_chars
        self._auto_flush_interval = auto_flush_interval

        # Состояние буфера
        self._buffer: List[Dict[str, Any]] = []
        self._buffer_text_size: int = 0  # Текущий размер буфера в символах
        self._lock = asyncio.Lock()
        self._last_flush = time.monotonic()
        self._last_msg_ts: Optional[datetime] = None
        
        # Клиентская сессия
        self._session: Optional[aiohttp.ClientSession] = None
        
        # Управление задачей автоматической отправки
        self._auto_flush_task: Optional[asyncio.Task] = None
        self._running = False

    # ---------------------------------------------------------------------
    # Public helpers
    # ---------------------------------------------------------------------

    async def start(self) -> None:
        """Запускает задачу автоматической отправки буфера."""
        if self._running:
            return
            
        self._running = True
        self._auto_flush_task = asyncio.create_task(self._auto_flush_loop())

    async def add(self, rows: List[Dict[str, Any]]) -> None:
        """
        Добавляет записи в буфер и отправляет их при необходимости.
        
        Буфер отправляется в следующих случаях:
        1. Количество записей достигло лимита
        2. Размер текста превысил лимит
        3. Временной разрыв между сообщениями превышает лимит
        4. Истекло время с момента последней отправки
        """
        if not rows:
            return
            
        # Автоматически запускаем буфер при первом добавлении сообщений
        if not self._running:
            await self.start()
            
        async with self._lock:
            # Вычисляем размер новых записей и получаем timestamp
            new_text_size, current_msg_ts = self._analyze_entries(rows)
            
            # Проверяем временной интервал между сообщениями
            need_flush = self._check_time_gap(current_msg_ts)
            
            # Обновляем timestamp текущего сообщения
            if current_msg_ts:
                self._last_msg_ts = current_msg_ts
            
            # Проверяем другие условия для сброса буфера
            if not need_flush:
                # Проверка по размеру буфера (количество записей)
                if len(self._buffer) + len(rows) >= self._bulk_size:
                    print(f"[EntryBuffer] Достигнут лимит записей ({self._bulk_size})")
                    need_flush = True
                # Проверка по размеру текста
                elif self._buffer_text_size + new_text_size >= self._max_buffer_chars:
                    print(f"[EntryBuffer] Превышен лимит символов ({self._max_buffer_chars})")
                    need_flush = True
            
            # Если нужно сбросить буфер, делаем это перед добавлением новых записей
            if need_flush and self._buffer:
                await self._flush_locked()
                
            # Добавляем новые записи и обновляем размер буфера
            self._buffer.extend(rows)
            self._buffer_text_size += new_text_size

    async def close(self) -> None:
        """Отправляет оставшиеся данные и закрывает сессию."""
        # Останавливаем задачу автоматической отправки
        if self._running and self._auto_flush_task:
            self._running = False
            self._auto_flush_task.cancel()
            try:
                await self._auto_flush_task
            except asyncio.CancelledError:
                pass
                
        # Отправляем оставшиеся данные
        async with self._lock:
            if self._buffer:
                await self._flush_locked()
                
        # Закрываем HTTP сессию
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    def update_access_token(self, new_token: str) -> None:
        """
        Обновляет токен доступа для буфера.
        
        Args:
            new_token: Новый токен доступа
        """
        self._access_token = new_token
        print(f"Токен доступа в буфере обновлен")

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _analyze_entries(self, entries: List[Dict[str, Any]]) -> Tuple[int, Optional[datetime]]:
        """
        Анализирует новые записи, вычисляя их размер и определяя метку времени.
        
        Возвращает:
            - Размер текста в символах
            - Метку времени самого раннего сообщения или None
        """
        text_size = 0
        earliest_ts = None
        
        for entry in entries:
            # Считаем размер текста
            if entry.get("type") == "text" and "payload" in entry:
                content = entry["payload"].get("content", "")
                if isinstance(content, str):
                    text_size += len(content)
            elif "payload" in entry:
                # Также учитываем текстовые превью
                text_preview = entry["payload"].get("text_preview", "")
                if isinstance(text_preview, str):
                    text_size += len(text_preview)
            
            # Определяем временную метку
            if "metadata" in entry and "date" in entry["metadata"]:
                try:
                    msg_ts = datetime.fromisoformat(entry["metadata"]["date"])
                    if earliest_ts is None or msg_ts < earliest_ts:
                        earliest_ts = msg_ts
                except (ValueError, TypeError):
                    pass
                    
        return text_size, earliest_ts

    def _check_time_gap(self, current_ts: Optional[datetime]) -> bool:
        """
        Проверяет временной интервал между текущим и предыдущим сообщением.
        
        Возвращает:
            True, если интервал превышает лимит и нужно сбросить буфер
            False в противном случае
        """
        if not self._buffer or not self._last_msg_ts or not current_ts:
            return False
            
        time_diff = abs((current_ts - self._last_msg_ts).total_seconds())
        if time_diff > self._gap_seconds:
            print(f"[EntryBuffer] Временной интервал {time_diff:.1f}с превышает лимит {self._gap_seconds}с")
            return True
            
        return False

    async def _auto_flush_loop(self) -> None:
        """
        Фоновая задача, которая периодически проверяет и отправляет буфер.
        """
        try:
            while self._running:
                # Проверяем в 4 раза чаще, чем интервал отправки
                await asyncio.sleep(self._auto_flush_interval / 4)
                
                async with self._lock:
                    # Проверяем наличие данных в буфере
                    if not self._buffer:
                        continue
                        
                    # Проверяем время с момента последней отправки
                    elapsed = time.monotonic() - self._last_flush
                    if elapsed >= self._auto_flush_interval:
                        print(f"[EntryBuffer] Автоматическая отправка после {elapsed:.1f}с бездействия")
                        await self._flush_locked()
        except asyncio.CancelledError:
            print("[EntryBuffer] Задача автоматической отправки остановлена")
        except Exception as e:
            print(f"[EntryBuffer] Ошибка автоматической отправки: {e}")

    async def _flush_locked(self) -> None:
        """Отправляет накопленные записи в API."""
        if not self._buffer:
            return

        # Создаем или переиспользуем HTTP-сессию
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()

        # Формируем заголовки запроса
        headers = {"Authorization": f"Bearer {self._access_token}"} if self._access_token else {}
        
        # Создаем уникальный идентификатор группы
        group_id = f"telegram-batch-{int(time.time())}-{id(self._buffer)}"
        
        # Формируем структуру AggregateInput
        payload = {
            "group_id": group_id,
            "entries": list(self._buffer),
            "metadata": {
                "source": "telegram-connector",
                "batch_size": len(self._buffer),
                "char_count": self._buffer_text_size,
                "aggregated_at": datetime.now(timezone.utc).isoformat()
            }
        }
        
        # Сохраняем копию буфера на случай ошибки
        entries_copy = list(self._buffer)
        text_size_copy = self._buffer_text_size
        
        # Очищаем буфер перед отправкой
        self._buffer.clear()
        self._buffer_text_size = 0

        try:
            # Отправляем запрос
            print(f"[EntryBuffer] Отправка {len(entries_copy)} записей ({text_size_copy} символов)")
            async with self._session.post(self._url, json=payload, headers=headers) as resp:
                if resp.status not in (200, 202):
                    error = await resp.text()
                    print(f"[EntryBuffer] Ошибка отправки ({resp.status}): {error}")
                    # Восстанавливаем буфер в случае ошибки
                    self._buffer.extend(entries_copy)
                    self._buffer_text_size = text_size_copy
        except Exception as exc:
            print(f"[EntryBuffer] Исключение при отправке: {exc}")
            # Восстанавливаем буфер в случае исключения
            self._buffer.extend(entries_copy)
            self._buffer_text_size = text_size_copy
        finally:
            # Обновляем время последней отправки
            self._last_flush = time.monotonic()
            # Сбрасываем метку времени последнего сообщения
            self._last_msg_ts = None

    @staticmethod
    def _make_url(api_url: str) -> str:
        """Return correct aggregate endpoint URL for given *api_url*."""
        base = api_url.rstrip("/")
        if base.endswith("/ingest/aggregate"):
            return base
        if base.endswith("/ingest/entry"):
            return base[:-5] + "aggregate"  # entry -> aggregate
        if base.endswith("/ingest/entries"):
            return base[:-8] + "aggregate"  # entries -> aggregate
        if base.endswith("/ingest"):
            return base + "/aggregate"
        return base + "/ingest/aggregate" 