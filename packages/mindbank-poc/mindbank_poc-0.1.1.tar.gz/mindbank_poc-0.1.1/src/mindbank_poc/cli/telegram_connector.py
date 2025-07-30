#!/usr/bin/env python
"""CLI команда для запуска телеграм-коннектора"""

import asyncio
import argparse
import sys

from mindbank_poc.connectors.telegram.client import TelegramConnectorClient


def main():
    """Точка входа для команды run-tg-connector."""
    parser = argparse.ArgumentParser(description="Запуск телеграм-коннектора Mindbank")
    parser.add_argument("--api-url", default="http://localhost:8000", help="URL API сервера Mindbank")
    parser.add_argument("--integration-key", help="Ключ интеграции для авторизации")
    parser.add_argument("--batch-limit", type=int, default=50, help="Максимальное количество сообщений в одной пачке")
    parser.add_argument("--batch-page", type=int, default=1, help="Номер начальной страницы")
    parser.add_argument("--batch-sleep", type=float, default=1.0, help="Задержка между пачками (секунды)")
    parser.add_argument("--check-sleep", type=float, default=30.0, help="Интервал проверки конфигурации (секунды)")
    parser.add_argument("--collector-id", default="telegram-connector", help="ID коллектора")
    
    args = parser.parse_args()
    
    # Проверим, что API URL корректен
    if not args.api_url.startswith(("http://", "https://")):
        args.api_url = f"http://{args.api_url}"
    
    print(f"Запуск телеграм-коннектора с API: {args.api_url}")
    
    # Запускаем клиент
    client = TelegramConnectorClient(
        api_url=args.api_url,
        batch_limit=args.batch_limit,
        batch_page=args.batch_page,
        batch_sleep=args.batch_sleep,
        check_sleep=args.check_sleep,
        collector_id=args.collector_id,
        integration_key=args.integration_key,
    )
    
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        print("Телеграм-коннектор остановлен пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 