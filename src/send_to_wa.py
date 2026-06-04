import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from neonize.aioze.client import NewAClient

load_dotenv()

WA_DB = os.environ.get("WA_DB", "neonize.db")
WA_GROUP_NAME = os.environ.get("WA_GROUP_NAME", "Matvei Live")
DELAY = float(os.environ.get("WA_DELAY", "1.5"))

DATA_DIR = Path("data")
MESSAGES_FILE = DATA_DIR / "messages.json"

client = NewAClient(WA_DB)


async def find_group_jid(client: NewAClient, name: str):
    groups = await client.get_joined_groups()
    for g in groups:
        if g.GroupName.Name == name:
            return g.JID
    names = [g.GroupName.Name for g in groups]
    raise ValueError(f"Группа '{name}' не найдена. Доступные: {names}")


async def send_all(client: NewAClient) -> None:
    messages = json.loads(MESSAGES_FILE.read_text())
    jid = await find_group_jid(client, WA_GROUP_NAME)
    print(f"Группа найдена: {WA_GROUP_NAME} → {jid}")

    sent = 0
    skipped = 0
    for msg in messages:
        text = msg.get("text", "").strip()
        photo = msg.get("photo")

        if not text and not photo:
            skipped += 1
            continue

        if photo and Path(photo).exists():
            await client.send_image(jid, photo, caption=text or None)
        elif text:
            await client.send_message(jid, text)
        else:
            skipped += 1
            continue

        sent += 1
        print(f"  [{sent}] id={msg['id']}", end="\r", flush=True)
        await asyncio.sleep(DELAY)

    print(f"\nГотово. Отправлено: {sent}, пропущено: {skipped}")


async def main() -> None:
    await client.connect()
    print("Ожидание подключения...")
    while not client.connected:
        await asyncio.sleep(0.2)
    print("Подключено к WhatsApp")
    await asyncio.sleep(2)  # даём соединению устояться
    await send_all(client)
    await client.stop()


asyncio.run(main())
