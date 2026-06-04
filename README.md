# TG2WA — Telegram → WhatsApp

Перенос сообщений и фото из Telegram-канала в группу WhatsApp.

## ETL в два шага

### `src/fetch_channel.py`
Выгружает сообщения и фото из Telegram-канала через Telethon.
- Результат: `data/messages.json` + `data/photos/*.jpg`

### `src/send_to_wa.py`
Отправляет выгруженные сообщения в группу WhatsApp через neonize (WhatsApp Web protocol).
- Авторизация по QR-коду при первом запуске, сессия сохраняется в `neonize.db`
- Фото с подписью, только фото, только текст — все форматы поддержаны

## Запуск

```bash
# 1. Выгрузить из Telegram
uv run python src/fetch_channel.py

# 2. Отправить в WhatsApp
uv run python -u src/send_to_wa.py
```

## .env

```
API_ID=        # my.telegram.org
API_HASH=      # my.telegram.org
GROUP_ID=      # числовой ID канала Telegram

WA_GROUP_NAME=Matvei Live   # название группы WhatsApp
WA_DB=neonize.db            # файл сессии (создаётся автоматически)
WA_DELAY=1.5                # пауза между сообщениями (сек)
```
