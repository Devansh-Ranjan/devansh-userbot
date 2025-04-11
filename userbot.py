from telethon import TelegramClient, events, Button
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Telethon client (replace with your API ID, API hash, and session)
api_id = YOUR_API_ID  # Replace with your API ID
api_hash = 'YOUR_API_HASH'  # Replace with your API hash
client = TelegramClient('userbot_session', api_id, api_hash)

# Dictionary to store alive media (in-memory for simplicity; use a database for persistence)
alive_media = {'type': None, 'file': None, 'text': None}

# Helper function to download media or code
async def download_media(message):
    if message.media and hasattr(message.media, 'document'):
        mime_type = message.media.document.mime_type
        if mime_type in ['image/jpeg', 'image/png', 'video/mp4']:
            file_path = await message.download_media()
            return 'media', file_path
        elif mime_type == 'text/x-python' or message.file.name.endswith('.py'):
            file_path = await message.download_media()
            with open(file_path, 'r') as f:
                code = f.read()
            return 'code', code
    elif message.photo:
        file_path = await message.download_media()
        return 'media', file_path
    return None, None

# .ping command
@client.on(events.NewMessage(pattern=r'\.ping'))
async def ping(event):
    await event.reply("Pong! 🏓")

# .setalive command
@client.on(events.NewMessage(pattern=r'\.setalive'))
async def set_alive(event):
    global alive_media
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
        await event.reply("Unsupported media type. Reply to a photo, video, or .py file.")

# .alive command
@client.on(events.NewMessage(pattern=r'\.alive'))
async def alive(event):
    if alive_media['type'] == 'media' and alive_media['file']:
        await event.reply(file=alive_media['file'], message="Userbot is alive! 🚀")
    elif alive_media['type'] == 'code' and alive_media['text']:
        await event.reply(f"Userbot is alive! 🚀\n\nPython Code:\n```\n{alive_media['text']}\n```")
    else:
        await event.reply("Userbot is alive! 🚀 No custom media set.")

# .afk command
@client.on(events.NewMessage(pattern=r'\.afk(?:\s+(.+))?'))
async def afk(event):
    reason = event.pattern_match.group(1) or "No reason provided."
    # Store AFK status (implement storage logic as needed)
    await event.reply(f"Going AFK with reason: {reason}")
    # Add logic to auto-reply to mentions or PMs (not implemented here for brevity)

# .unafk command
@client.on(events.NewMessage(pattern=r'\.unafk'))
async def unafk(event):
    # Clear AFK status (implement storage logic as needed)
    await event.reply("Back from AFK!")

# .id command
@client.on(events.NewMessage(pattern=r'\.id'))
async def get_id(event):
    chat = await event.get_chat()
    reply = await event.get_reply_message()
    if reply:
        user_id = reply.sender_id
        await event.reply(f"User ID: {user_id}")
    else:
        await event.reply(f"Chat ID: {chat.id}")

# .kick command (admin only)
@client.on(events.NewMessage(pattern=r'\.kick'))
async def kick(event):
    if not event.is_group:
        await event.reply("This command works in groups only.")
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply to a user to kick them.")
        return
    # Add admin check and kick logic
    await event.reply("Kicking user... (admin check needed)")

# .ban command (admin only)
@client.on(events.NewMessage(pattern=r'\.ban'))
async def ban(event):
    if not event.is_group:
        await event.reply("This command works in groups only.")
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply to a user to ban them.")
        return
    # Add admin check and ban logic
    await event.reply("Banning user... (admin check needed)")

# .unban command (admin only)
@client.on(events.NewMessage(pattern=r'\.unban'))
async def unban(event):
    if not event.is_group:
        await event.reply("This command works in groups only.")
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply to a user to unban them.")
        return
    # Add admin check and unban logic
    await event.reply("Unbanning user... (admin check needed)")

# .mute command (admin only)
@client.on(events.NewMessage(pattern=r'\.mute'))
async def mute(event):
    if not event.is_group:
        await event.reply("This command works in groups only.")
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply to a user to mute them.")
        return
    # Add admin check and mute logic
    await event.reply("Muting user... (admin check needed)")

# .unmute command (admin only)
@client.on(events.NewMessage(pattern=r'\.unmute'))
async def unmute(event):
    if not event.is_group:
        await event.reply("This command works in groups only.")
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply to a user to unmute them.")
        return
    # Add admin check and unmute logic
    await event.reply("Unmuting user... (admin check needed)")

# .roll command
@client.on(events.NewMessage(pattern=r'\.roll'))
async def roll(event):
    import random
    await event.reply(f"🎲 Rolled: {random.randint(1, 6)}")

# .purge command (admin only)
@client.on(events.NewMessage(pattern=r'\.purge'))
async def purge(event):
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply to a message to start purging from there.")
        return
    # Add admin check and purge logic
    await event.reply("Purging messages... (admin check needed)")

# .setbio command
@client.on(events.NewMessage(pattern=r'\.setbio\s+(.+)'))
async def set_bio(event):
    bio = event.pattern_match.group(1)
    # Update bio using client.update_profile
    await event.reply(f"Bio set to: {bio}")

# .setname command
@client.on(events.NewMessage(pattern=r'\.setname\s+(.+)'))
async def set_name(event):
    name = event.pattern_match.group(1)
    # Update name using client.update_profile
    await event.reply(f"Name set to: {name}")

# .commands command
@client.on(events.NewMessage(pattern=r'\.commands'))
async def commands(event):
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
    data = event.data
    if data in cmd_descriptions:
        await event.answer(cmd_descriptions[data], alert=True)

# Start the client
async def main():
    await client.start()
    logger.info("Userbot is running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
