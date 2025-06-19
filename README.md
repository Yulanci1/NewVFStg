# VFS France Slot Checker Telegram Bot

Этот бот проверяет наличие слотов на сайте VFS Global для подачи на визу Франции в городах России. Если слот найден, бот отправляет уведомление в Telegram.

## Установка через Render

1. Создай новый репозиторий на GitHub и загрузи содержимое.
2. Перейди на [Render](https://render.com).
3. Создай новый "Web Service" (или Background Worker).
4. Подключи репозиторий.
5. Укажи:
   - **Environment**: Python 3
   - **Start Command**: `python main.py`
   - **Type**: Background Worker
6. Добавь переменные окружения:
   - `TELEGRAM_TOKEN`
   - `CHAT_ID` (ID Telegram-чата или пользователя)

## Использование

- `/check` — ручная проверка.
- Автоматическая проверка каждые 3 минуты.
