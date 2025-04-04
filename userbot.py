from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os, random

# Environment Variables
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")

# Start client with session string
client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Default Alive Media
ALIVE_MEDIA = "alive.jpg"

# Alive Command
@client.on(events.NewMessage(pattern=r'^\\.alive$'))
async def alive(event):
    await event.reply("**I AM ALIVE!** ✅\nMade by: Devansh Ranjan", file=ALIVE_MEDIA)

# Set new alive media by replying to photo/video/gif
@client.on(events.NewMessage(pattern=r'^\\.setalive$'))
async def set_alive(event):
    global ALIVE_MEDIA
    if event.reply_to and event.reply_to.media:
        ALIVE_MEDIA = await event.reply_to.download_media()
        await event.reply("✅ Alive media updated!")
    else:
        await event.reply("❌ Please reply to a photo, video or GIF to set it as alive media.")

# Joke Command
@client.on(events.NewMessage(pattern=r'^\\.joke$'))
async def joke(event):
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts!",
        "I only know 25 letters of the alphabet. I don't know y.",
    ]
    await event.reply(random.choice(jokes))

# Roast Command
@client.on(events.NewMessage(pattern=r'^\\.roast$'))
async def roast(event):
    roasts = [
        "You're the reason the gene pool needs a lifeguard.",
        "You're not stupid; you just have bad luck thinking.",
    ]
    await event.reply(random.choice(roasts))

# Quote Command
@client.on(events.NewMessage(pattern=r'^\\.quote$'))
async def quote(event):
    quotes = [
        "Believe in yourself and all that you are.",
        "Do what you can with what you have where you are.",
    ]
    await event.reply(random.choice(quotes))

# User Info
@client.on(events.NewMessage(pattern=r'^\\.userinfo$'))
async def userinfo(event):
    user = await event.get_sender()
    await event.reply(f"**User Info:**\n👤 Name: {user.first_name}\n🆔 ID: {user.id}")

# List All Commands
@client.on(events.NewMessage(pattern=r'^\\.commands$'))
async def commands(event):
    cmds = """
**Available Commands:**
`.alive` - Show alive status  
`.setalive` - Change alive media (reply to image/video/gif)  
`.joke` - Send a joke  
`.roast` - Send a roast  
`.quote` - Inspirational quote  
`.userinfo` - Show user info  
`.commands` - List all commands
"""
    await event.reply(cmds)

# Run bot
print("Userbot loaded. Running...")
client.start()
client.run_until_disconnected()
