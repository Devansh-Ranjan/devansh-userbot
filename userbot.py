from telethon import TelegramClient, events
import os, random

# Set your API ID and Hash
api_id = 2048716
api_hash = '459a843d585d65edfdcf60389926b0ca'

# Load session
client = TelegramClient('userbot', api_id, api_hash)

# Default Alive Media
ALIVE_MEDIA = "alive.jpg"

@client.on(events.NewMessage(pattern=r'^\\.alive$'))
async def alive(event):
    await event.reply("**I AM ALIVE!** ✅\n🔥 Custom Userbot Running!", file=ALIVE_MEDIA)

@client.on(events.NewMessage(pattern=r'^\\.setalive$'))
async def set_alive(event):
    global ALIVE_MEDIA
    if event.reply_to and event.reply_to.media:
        ALIVE_MEDIA = await event.reply_to.download_media()
        await event.reply("✅ Alive Media Updated!")
    else:
        await event.reply("❌ Reply to a photo/video/GIF to set alive media!")

@client.on(events.NewMessage(pattern=r'^\\.joke$'))
async def joke(event):
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts!",
        "Parallel lines have so much in common. It’s a shame they’ll never meet."
    ]
    await event.reply(random.choice(jokes))

@client.on(events.NewMessage(pattern=r'^\\.roast$'))
async def roast(event):
    roasts = [
        "You're proof that even evolution can hit the pause button.",
        "You bring everyone so much joy… when you leave the room."
    ]
    await event.reply(random.choice(roasts))

@client.on(events.NewMessage(pattern=r'^\\.quote$'))
async def quote(event):
    quotes = [
        "Believe in yourself!",
        "Success is not final, failure is not fatal: It is the courage to continue that counts."
    ]
    await event.reply(random.choice(quotes))

@client.on(events.NewMessage(pattern=r'^\\.userinfo$'))
async def userinfo(event):
    user = await event.get_sender()
    await event.reply(f"**User Info:**\n👤 Name: {user.first_name}\n🆔 ID: {user.id}")

print("Userbot loaded. Running...")
client.start()
client.run_until_disconnected()
