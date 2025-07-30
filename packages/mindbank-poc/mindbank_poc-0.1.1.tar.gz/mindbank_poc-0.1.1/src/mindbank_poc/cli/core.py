#!/usr/bin/env python
"""CLI команда для запуска API ядра Mindbank"""

import argparse
import sys
import uvicorn

from mindbank_poc.core.config.settings import settings


def main():
    """Точка входа для команды run-core."""
    parser = argparse.ArgumentParser(description="Запуск API ядра Mindbank")
    parser.add_argument("--host", default=settings.api.host, help="Хост для запуска API (по умолчанию из настроек)")
    parser.add_argument("--port", type=int, default=settings.api.port, help="Порт для запуска API (по умолчанию из настроек)")
    parser.add_argument("--reload", action="store_true", default=settings.api.reload, help="Включить автоматическую перезагрузку при изменении кода")
    parser.add_argument("--log-level", default="info", choices=["debug", "info", "warning", "error", "critical"], help="Уровень логирования")
    parser.add_argument("--offline-mode", action="store_true", default=settings.normalizer.offline_mode, help="Запуск в автономном режиме")
    
    args = parser.parse_args()
    
    # Переопределяем настройки
    settings.api.host = args.host
    settings.api.port = args.port
    settings.api.reload = args.reload
    settings.normalizer.offline_mode = args.offline_mode
    
    print(f"Запуск API ядра Mindbank на {args.host}:{args.port}")
    print(f"Offline режим: {'включен' if args.offline_mode else 'выключен'}")
    
    try:
        uvicorn.run(
            "mindbank_poc.api.main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level=args.log_level
        )
    except KeyboardInterrupt:
        print("API ядро остановлено пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 