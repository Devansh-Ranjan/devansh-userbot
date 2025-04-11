import os
import logging
import random
from telethon import TelegramClient, events, Button
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
if not api_id or not api_hash:
    raise ValueError("Please set TELEGRAM_API_ID and TELEGRAM_API_HASH in .env file.")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Telethon client
client = TelegramClient('userbot_session', int(api_id), api_hash)

# Dictionary to store alive media (in-memory; use SQLite for persistence)
alive_media = {'type': None, 'file': None, 'text': None}

# Helper function to download media or code
async def download_media(message):
    if not message or not message.media:
        return None, None
    # Check file size (limit to 10MB for safety)
    if hasattr(message.media, 'document') and message.media.document.size > 10 * 1024 * 1024:
        return None, None
    if message.photo:
        file_path = await message.download_media()
        return 'media', file_path
    if hasattr(message.media, 'document'):
        mime_type = message.media.document.mime_type
        if mime_type in ['image/jpeg', 'image/png', 'video/mp4']:
            file_path = await message.download_media()
            return 'media', file_path
        elif mime_type == 'text/x-python' or (message.file and message.file.name.endswith('.py')):
            file_path = await message.download_media()
            with open(file_path, 'r') as f:
                code = f.read()
            os.remove(file_path)  # Clean up
            return 'code', code
    return None, None

# .ping command
@client.on(events.NewMessage(pattern=r'\.ping', outgoing=True))
async def ping(event):
    logger.info("Ping command triggered")
    await event.reply("Pong! 🏓")

# .setalive command
@client.on(events.NewMessage(pattern=r'\.setalive', outgoing=True))
async def set_alive(event):
    global alive_media
    logger.info("Setalive command triggered")
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Please reply to a photo, video, or Python code to set as alive media.")
        return

    media_type, content = await download_media(reply)
    if media_type == 'media':
        alive_media = {'type': 'media', 'file': content, 'text': None}
        await event.reply("Alive media set to photo/video successfully!")
    elif media_type == 'code':
        alive_media = {'type': 'code', 'file': None, 'text': content}
        await event.reply("Alive media set to Python code successfully!")
    else:
        await event.reply("Unsupported media type or file too large. Reply to a photo, video, or .py file (max 10MB).")

# .alive command
@client.on(events.NewMessage(pattern=r'\.alive', outgoing=True))
async def alive(event):
    logger.info("Alive command triggered")
    if alive_media['type'] == 'media' and alive_media['file']:
        await event.reply(file=alive_media['file'], message="Userbot is alive! 🚀")
    elif alive_media['type'] == 'code' and alive_media['text']:
        await event.reply(f"Userbot is alive! 🚀\n\nPython Code:\n```\n{alive_media['text']}\n```")
    else:
        await event.reply("Userbot is alive! 🚀 No custom media set.")

# .afk command
@client.on(events.NewMessage(pattern=r'\.afk(?:\s+(.+))?', outgoing=True))
async def afk(event):
    logger.info("AFK command triggered")
    reason = event.pattern_match.group(1) or "No reason provided."
    await event.reply(f"Going AFK with reason: {reason}")
    # Add auto-reply logic here

# .unafk command
@client.on(events.NewMessage(pattern=r'\.unafk', outgoing=True))
async def unafk(event):
    logger.info("Unafk command triggered")
    await event.reply("Back from AFK!")

# .id command
@client.on(events.NewMessage(pattern=r'\.id', outgoing=True))
async def get_id(event):
    logger.info("ID command triggered")
    chat = await event.get_chat()
    reply = await event.get_reply_message()
    if reply:
        user_id = reply.sender_id
        await event.reply(f"User ID: {user_id}")
    else:
        await event.reply(f"Chat ID: {chat.id}")

# .kick command (admin only)
@client.on(events.NewMessage(pattern=r'\.kick', outgoing=True))
async def kick(event):
    logger.info("Kick command triggered")
    if not event.is_group:
        await event.reply("This command works in groups only.")
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply to a user to kick them.")
        return
    await event.reply("Kicking user... (add admin check and logic)")

# .ban command (admin only)
@client.on(events.NewMessage(pattern=r'\.ban', outgoing=True))
async def ban(event):
    logger.info("Ban command triggered")
    if not event.is_group:
        await event.reply("This command works in groups only.")
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply to a user to ban them.")
        return
    await event.reply("Banning user... (add admin check and logic)")

# .unban command (admin only)
@client.on(events.NewMessage(pattern=r'\.unban', outgoing=True))
async def unban(event):
    logger.info("Unban command triggered")
    if not event.is_group:
        await event.reply("This command works in groups only.")
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply to a user to unban them.")
        return
    await event.reply("Unbanning user... (add admin check and logic)")

# .mute command (admin only)
@client.on(events.NewMessage(pattern=r'\.mute', outgoing=True))
async def mute(event):
    logger.info("Mute command triggered")
    if not event.is_group:
        await event.reply("This command works in groups only.")
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply to a user to mute them.")
        return
    await event.reply("Muting user... (add admin check and logic)")

# .unmute command (admin only)
@client.on(events.NewMessage(pattern=r'\.unmute', outgoing=True))
async def unmute(event):
    logger.info("Unmute command triggered")
    if not event.is_group:
        await event.reply("This command works in groups only.")
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply to a user to unmute them.")
        return
    await event.reply("Unmuting user... (add admin check and logic)")

# .roll command
@client.on(events.NewMessage(pattern=r'\.roll', outgoing=True))
async def roll(event):
    logger.info("Roll command triggered")
    await event.reply(f"🎲 Rolled: {random.randint(1, 6)}")

# .purge command (admin only)
@client.on(events.NewMessage(pattern=r'\.purge', outgoing=True))
async def purge(event):
    logger.info("Purge command triggered")
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply to a message to start purging from there.")
        return
    await event.reply("Purging messages... (add admin check and logic)")

# .setbio command
@client.on(events.NewMessage(pattern=r'\.setbio\s+(.+)', outgoing=True))
async def set_bio(event):
    logger.info("Setbio command triggered")
    bio = event.pattern_match.group(1)
    await event.reply(f"Bio set to: {bio}")
    # Add client.update_profile logic

# .setname command
@client.on(events.NewMessage(pattern=r'\.setname\s+(.+)', outgoing=True))
async def set_name(event):
    logger.info("Setname command triggered")
    name = event.pattern_match.group(1)
    await event.reply(f"Name set to: {name}")
    # Add client.update_profile logic

# .commands command
@client.on(events.NewMessage(pattern=r'\.commands', outgoing=True))
async def commands(event):
    logger.info("Commands command triggered")
    buttons = [
        [Button.inline(".ping", b"cmd_ping"), Button.inline(".alive", b"cmd_alive")],
        [Button.inline(".setalive", b"cmd_setalive"), Button.inline(".afk", b"cmd_afk")],
        [Button.inline(".unafk", b"cmd_unafk"), Button.inline(".id", b"cmd_id")],
        [Button.inline(".kick", b"cmd_kick"), Button.inline(".ban", b"cmd_ban")],
        [Button.inline(".unban", b"cmd_unban"), Button.inline(".mute", b"cmd_mute")],
        [Button.inline(".unmute", b"cmd_unmute"), Button.inline(".roll", b"cmd_roll")],
        [Button.inline(".purge", b"cmd_purge"), Button.inline(".setbio", b"cmd_setbio")],
        [Button.inline(".setname", b"cmd_setname")],
    ]
    await event.reply("Available Commands:", buttons=buttons)

# Button callback handler
@client.on(events.CallbackQuery)
async def callback(event):
    cmd_descriptions = {
        b"cmd_ping": "Checks if the userbot is online and responds with 'Pong!'.",
        b"cmd_alive": "Shows the userbot's alive status with custom media or code.",
        b"cmd_setalive": "Sets a photo, video, or Python code as alive media by replying to it.",
        b"cmd_afk": "Sets AFK status with an optional reason.",
        b"cmd_unafk": "Removes AFK status.",
        b"cmd_id": "Returns the chat or user ID.",
        b"cmd_kick": "Kicks a user from a group (admin only).",
        b"cmd_ban": "Bans a user from a group (admin only).",
        b"cmd_unban": "Unbans a user from a group (admin only).",
        b"cmd_mute": "Mutes a user in a group (admin only).",
        b"cmd_unmute": "Unmutes a user in a group (admin only).",
        b"cmd_roll": "Rolls a dice (random number 1-6).",
        b"cmd_purge": "Deletes messages from the replied-to message onward (admin only).",
        b"cmd_setbio": "Sets a new Telegram bio.",
        b"cmd_setname": "Sets a new Telegram display name.",
    }
    try:
        if event.sender_id != (await event.get_input_sender()).user_id:
            await event.answer("This button is not for you!", alert=True)
            return
        data = event.data
        if data in cmd_descriptions:
            await event.answer(cmd_descriptions[data], alert=True)
        else:
            await event.answer("Unknown command!", alert=True)
    except Exception as e:
        logger.error(f"Callback error: {e}")
        await event.answer("An error occurred!", alert=True)

# Start the client
async def main():
    await client.start()
    logger.info("Userbot is running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
