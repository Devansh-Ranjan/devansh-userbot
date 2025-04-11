from telethon import TelegramClient
from keep_alive import keep_alive
from dotenv import load_dotenv
import os

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = "userbot"

client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(pattern="/ping"))
async def ping(event):
    await event.respond("Pong!")

keep_alive()
client.start()
client.run_until_disconnected()
