import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

_raw_gid = os.environ["GROUP_ID"]
CHANNEL: int | str = int(_raw_gid) if _raw_gid.lstrip("-").isdigit() else _raw_gid
DATA_DIR = Path("data")
PHOTOS_DIR = DATA_DIR / "photos"
MESSAGES_FILE = DATA_DIR / "messages.json"


async def fetch(client: TelegramClient) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    PHOTOS_DIR.mkdir(exist_ok=True)

    entity = await client.get_entity(CHANNEL)
    print(f"Канал: {getattr(entity, 'title', CHANNEL)}")

    messages = []
    async for msg in client.iter_messages(entity, reverse=True):
        entry = {
            "id": msg.id,
            "date": msg.date.isoformat(),
            "text": msg.text or "",
            "photo": None,
        }

        if msg.photo:
            filename = PHOTOS_DIR / f"{msg.id}.jpg"
            if not filename.exists():
                await client.download_media(msg, file=filename)
                print(f"  Фото сохранено: {filename.name}")
            entry["photo"] = str(filename)

        messages.append(entry)
        if msg.id % 100 == 0:
            print(f"  Обработано сообщений: {msg.id}")

    MESSAGES_FILE.write_text(json.dumps(messages, ensure_ascii=False, indent=2))
    print(f"\nГотово. Сообщений: {len(messages)}, файл: {MESSAGES_FILE}")


async def main() -> None:
    async with TelegramClient("session_tg2wa", API_ID, API_HASH) as client:
        await fetch(client)


if __name__ == "__main__":
    asyncio.run(main())
